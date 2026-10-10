"""Scaleform TresFont (UE4 SwfMovie .uasset/.uexp) parser + writer, down to individual glyph edges.

Layers (all verified byte-identical on the 3 KH3 TresFont files):
  .uasset  export SerialSize (= len(uexp) - 4) and BulkDataStartOffset (= len(uasset) + len(uexp) - 4)
  .uexp    tagged properties ... RawData ArrayProperty<ByteProperty> {size = n + 4, count n} | GFX file | None + 4 B + tag
  GFX      'GFX' v21, u32 file length, RECT/fps/frames, SWF tags (short/long header kept as found)
  tag 1005 GFx DefineCompactedFont: u16 id | font data (offsets below are relative to here):
           name UTF-8 NUL, u16 flags, u16 nominalSize(256), s16 ascent, s16 descent, s16 leading,
           u32 numGlyphs, u32 glyphBytes, glyph shapes, numGlyphs x {u16 code (ascending), s16 advance, u32 pos},
           UInt30 numKerning, numKerning x {u16 c1, u16 c2, s16 adj}
  shape    SInt15 bbox[4] (xmin, ymin, xmax, ymax; y down), UInt15 numContours,
           contours {SInt15 moveX, SInt15 moveY, UInt30 (numEdges << 1 | isReference), edges}
  edge     low nibble = type; fields packed LSB-first after it, signed, relative to the pen:
           0 H12 1 H20 (dx) | 2 V12 3 V20 (dy) | 4 L6 5 L10 6 L14 7 L18 (dx, dy) |
           8 C5 9 C7 10 C9 11 C11 12 C13 13 C15 (cdx, cdy, adx, ady: quadratic, control then anchor)
  UInt15 = 1 B (b >> 1) if b & 1 == 0 else 2 B; UInt30 = low 2 bits of the first byte = extra bytes.
Usage:
  python -I tresfont.py roundtrip <out_dir> <TresFont.uasset>...   rebuild unchanged, compare SHA256
  python -I tresfont.py estimate <font.ttf>                         Arabic glyph count / compacted bytes
"""
import hashlib, os, struct, sys

ESZ = {0: 2, 1: 3, 2: 2, 3: 3, 4: 2, 5: 3, 6: 4, 7: 5, 8: 3, 9: 4, 10: 5, 11: 6, 12: 7, 13: 8}
W = {0: [12], 1: [20], 2: [12], 3: [20], 4: [6] * 2, 5: [10] * 2, 6: [14] * 2, 7: [18] * 2,
     8: [5] * 4, 9: [7] * 4, 10: [9] * 4, 11: [11] * 4, 12: [13] * 4, 13: [15] * 4}
ARABIC = [(0x0600, 0x06FF), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF)]


# ---- variable-length ints -------------------------------------------------------------------------
def r_u15(d, p):
    return ((d[p] >> 1) | (d[p + 1] << 7), p + 2) if d[p] & 1 else (d[p] >> 1, p + 1)


def r_s15(d, p):
    v, q = r_u15(d, p)
    bits = 15 if q - p == 2 else 7
    return (v - (1 << bits) if v >> (bits - 1) else v), q


def r_u30(d, p):
    n = d[p] & 3
    return (d[p] >> 2) | (int.from_bytes(d[p + 1:p + 1 + n], 'little') << 6), p + 1 + n


def w_u15(v):
    assert 0 <= v < 1 << 15
    return bytes([v << 1]) if v < 128 else bytes([(v << 1 | 1) & 0xFF, v >> 7])


def w_s15(v):
    assert -(1 << 14) <= v < 1 << 14
    if -64 <= v < 64:
        return bytes([(v << 1) & 0xFF])
    x = v & 0x7FFF
    return bytes([(x << 1 | 1) & 0xFF, x >> 7])


def w_u30(v):
    n = 0 if v < 1 << 6 else 1 if v < 1 << 14 else 2 if v < 1 << 22 else 3
    return ((v << 2) | n).to_bytes(n + 1, 'little')


# ---- glyph shapes ---------------------------------------------------------------------------------
def r_edge(d, p):
    t = d[p] & 15
    v, out = int.from_bytes(d[p:p + ESZ[t]], 'little') >> 4, []
    for w in W[t]:
        x = v & ((1 << w) - 1)
        out.append(x - (1 << w) if x >> (w - 1) else x)
        v >>= w
    return (t, out), p + ESZ[t]


def w_edge(t, f):
    v, sh = t, 4
    for w, x in zip(W[t], f):
        assert -(1 << (w - 1)) <= x < 1 << (w - 1)
        v |= (x & ((1 << w) - 1)) << sh
        sh += w
    return v.to_bytes(ESZ[t], 'little')


def fits(w, *xs):
    return all(-(1 << (w - 1)) <= x < 1 << (w - 1) for x in xs)


def new_edge(f):
    """Smallest encoding for a new edge: f = (dx, dy) line or (cdx, cdy, adx, ady) curve -> (type, fields)."""
    if len(f) == 4:
        return next(t for t in range(8, 14) if fits(W[t][0], *f)), list(f)
    dx, dy = f
    if dy == 0:
        return (0 if fits(12, dx) else 1), [dx]
    if dx == 0:
        return (2 if fits(12, dy) else 3), [dy]
    return next(t for t in (4, 5, 6, 7) if fits(W[t][0], dx, dy)), [dx, dy]


def r_shape(d, p):
    bbox = []
    for _ in range(4):
        v, p = r_s15(d, p)
        bbox.append(v)
    nc, p = r_u15(d, p)
    contours = []
    for _ in range(nc):
        x, p = r_s15(d, p)
        y, p = r_s15(d, p)
        ne, p = r_u30(d, p)
        assert not ne & 1, 'shared contour reference (not seen in KH3 fonts)'
        edges = []
        for _ in range(ne >> 1):
            e, p = r_edge(d, p)
            edges.append(e)
        contours.append((x, y, edges))
    return (bbox, contours), p


def w_shape(shape):
    bbox, contours = shape
    out = [w_s15(v) for v in bbox] + [w_u15(len(contours))]
    for x, y, edges in contours:
        out += [w_s15(x), w_s15(y), w_u30(len(edges) << 1)]
        out += [w_edge(t, f) for t, f in edges]
    return b''.join(out)


# ---- DefineCompactedFont --------------------------------------------------------------------------
def r_font(t):
    fid = struct.unpack_from('<H', t)[0]
    z = t.index(b'\0', 2)
    name = t[2:z]
    flags, nominal, asc, desc, lead, n, gbytes = struct.unpack_from('<HHhhhII', t, z + 1)
    g0 = z + 1 + 18
    base = 2  # glyph pos is relative to the font data (after the u16 id)
    info = [struct.unpack_from('<HhI', t, g0 + gbytes + 8 * i) for i in range(n)]
    shapes, index, p = [], {}, g0
    while p < g0 + gbytes:  # shapes in stored order; info rows may share one
        index[p - base] = len(shapes)
        s, p = r_shape(t, p)
        shapes.append(s)
    assert p == g0 + gbytes
    glyphs = [(c, adv, index[pos]) for c, adv, pos in info]
    p = g0 + gbytes + 8 * n
    nk, p = r_u30(t, p)
    kern = [struct.unpack_from('<HHh', t, p + 6 * i) for i in range(nk)]
    assert p + 6 * nk == len(t), 'trailing bytes in compacted font'
    return dict(id=fid, name=name, flags=flags, nominal=nominal, ascent=asc, descent=desc, leading=lead,
                shapes=shapes, glyphs=glyphs, kerning=kern)


def w_font(f):
    head = struct.pack('<H', f['id']) + f['name'] + b'\0'
    base = len(head) + 18 - 2
    blobs, pos, p = [], [], base
    for s in f['shapes']:
        b = w_shape(s)
        pos.append(p)
        blobs.append(b)
        p += len(b)
    codes = [c for c, _, _ in f['glyphs']]
    assert codes == sorted(set(codes)), 'code table must be ascending and unique'
    out = [head, struct.pack('<HHhhhII', f['flags'], f['nominal'], f['ascent'], f['descent'], f['leading'],
                             len(f['glyphs']), p - base)] + blobs
    out += [struct.pack('<HhI', c, adv, pos[i]) for c, adv, i in f['glyphs']]
    out += [w_u30(len(f['kerning']))] + [struct.pack('<HHh', *k) for k in f['kerning']]
    return b''.join(out)


# ---- GFX file -------------------------------------------------------------------------------------
def r_gfx(g):
    assert g[:3] == b'GFX', 'only uncompressed GFX handled'
    assert struct.unpack_from('<I', g, 4)[0] == len(g)
    nbits = g[8] >> 3
    hp = 8 + (5 + 4 * nbits + 7) // 8 + 4
    tags, p = [], hp
    while p < len(g):
        h = struct.unpack_from('<H', g, p)[0]
        code, ln, long = h >> 6, h & 0x3F, False
        p += 2
        if ln == 0x3F:
            ln, long = struct.unpack_from('<I', g, p)[0], True
            p += 4
        tags.append([code, long, g[p:p + ln]])
        p += ln
    assert p == len(g)
    return dict(head=g[:hp], tags=tags)


def w_gfx(m):
    out = [m['head']]
    for code, long, data in m['tags']:
        if long or len(data) >= 0x3F:
            out.append(struct.pack('<HI', code << 6 | 0x3F, len(data)))
        else:
            out.append(struct.pack('<H', code << 6 | len(data)))
        out.append(data)
    g = bytearray(b''.join(out))
    struct.pack_into('<I', g, 4, len(g))
    return bytes(g)


# ---- UE4 SwfMovie asset -----------------------------------------------------------------------------
def r_asset(uasset, uexp):
    at = uexp.find(b'GFX')
    n = struct.unpack_from('<i', uexp, at - 4)[0]
    assert n == struct.unpack_from('<I', uexp, at + 4)[0], 'RawData count != GFX length'
    assert struct.unpack_from('<i', uexp, at - 21)[0] == n + 4, 'RawData tag size'
    ss = uasset.find(struct.pack('<q', len(uexp) - 4))
    bulk = uasset.find(struct.pack('<q', len(uasset) + len(uexp) - 4))
    assert ss > 0 and bulk > 0 and uasset.count(struct.pack('<q', len(uexp) - 4)) == 1
    return dict(uasset=uasset, pre=uexp[:at], gfx=uexp[at:at + n], post=uexp[at + n:], ss_at=ss, bulk_at=bulk)


def w_asset(a, gfx):
    pre = bytearray(a['pre'])
    struct.pack_into('<i', pre, len(pre) - 4, len(gfx))
    struct.pack_into('<i', pre, len(pre) - 21, len(gfx) + 4)
    uexp = bytes(pre) + gfx + a['post']
    ua = bytearray(a['uasset'])
    struct.pack_into('<q', ua, a['ss_at'], len(uexp) - 4)
    struct.pack_into('<q', ua, a['bulk_at'], len(ua) + len(uexp) - 4)
    return bytes(ua), uexp


def load(uasset_path):
    a = r_asset(open(uasset_path, 'rb').read(), open(uasset_path[:-7] + '.uexp', 'rb').read())
    m = r_gfx(a['gfx'])
    fonts = {i: r_font(t[2]) for i, t in enumerate(m['tags']) if t[0] == 1005}
    return a, m, fonts


def save(a, m, fonts):
    for i, f in fonts.items():
        m['tags'][i][2] = w_font(f)
    return w_asset(a, w_gfx(m))


# ---- CLI --------------------------------------------------------------------------------------------
def roundtrip(out_dir, paths):
    sha = lambda b: hashlib.sha256(b).hexdigest()
    bad = 0
    for up in paths:
        a, m, fonts = load(up)
        ua, ue = save(a, m, fonts)
        rel = up.replace(os.sep, '/').split('/Content/')[-1][:-7]
        for ext, new in (('.uasset', ua), ('.uexp', ue)):
            orig = open(up[:-7] + ext, 'rb').read()
            dst = os.path.join(out_dir, rel + ext)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(new)
            ok = new == orig
            bad += not ok
            print(f'{rel}{ext}\t{len(orig)}\t{sha(orig)}\t{sha(new)}\t{"PASS" if ok else "FAIL"}')
        for f in fonts.values():
            edges = [e for s in f['shapes'] for c in s[1] for e in c[2]]
            canon = sum(new_edge(fl if t >= 4 else (fl[0], 0) if t < 2 else (0, fl[0]))[0] == t for t, fl in edges)
            print(f'  font id={f["id"]} glyphs={len(f["glyphs"])} shapes={len(f["shapes"])} '
                  f'edges={len(edges)} canonical_edge_types={canon / len(edges):.4%}')
    return bad


def ttf_glyphs(ttf, codes, k=None, dy=0, edit=None):
    """TrueType outlines -> {code: (advance, shape)} in compacted units: scale k (default 256/unitsPerEm),
    y flipped and shifted by dy (font units after scaling, y down).
    edit(code, ops) -> ops may change the decomposed outline (fontTools RecordingPen ops, font units) first."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.basePen import BasePen
    from fontTools.pens.recordingPen import DecomposingRecordingPen
    font = TTFont(ttf)
    k = k or 256 / font['head'].unitsPerEm
    cmap, gs, hmtx = font.getBestCmap(), font.getGlyphSet(), font['hmtx']

    class Pen(BasePen):
        def __init__(self):
            super().__init__(gs)
            self.contours, self.pt, self.all = [], None, []

        def q(self, p):
            return round(p[0] * k), round(-p[1] * k + dy)

        def _moveTo(self, p):
            self.pt = self.q(p)
            self.contours.append((*self.pt, []))
            self.all.append(self.pt)

        def _lineTo(self, p):
            x, y = self.q(p)
            if (x, y) != self.pt:
                self.contours[-1][2].append(new_edge((x - self.pt[0], y - self.pt[1])))
                self.all.append((x, y))
            self.pt = (x, y)

        def _qCurveToOne(self, c, p):
            cx, cy = self.q(c)
            x, y = self.q(p)
            self.contours[-1][2].append(new_edge((cx - self.pt[0], cy - self.pt[1], x - cx, y - cy)))
            self.all += [(cx, cy), (x, y)]
            self.pt = (x, y)

        def _curveToOne(self, *a):
            raise ValueError('cubic outlines not expected in a TrueType font')

    out = {}
    for cp in codes:
        if cp not in cmap:
            continue
        rec, pen = DecomposingRecordingPen(gs), Pen()
        gs[cmap[cp]].draw(rec)
        for op, args in (edit(cp, rec.value) if edit else rec.value):
            getattr(pen, op)(*args)
        if pen.all:
            xs, ys = [x for x, _ in pen.all], [y for _, y in pen.all]
            bbox = [min(xs), min(ys), max(xs), max(ys)]
        else:
            bbox = [16383, 16383, -16383, -16383]  # empty glyph, as in the KH3 fonts
        out[cp] = (round(hmtx[cmap[cp]][0] * k), (bbox, pen.contours))
    return out


def add_glyphs(font, new):
    """Append {code: (advance, shape)} to a parsed compacted font; existing codes are an error."""
    have = {c for c, _, _ in font['glyphs']}
    assert not have & set(new), sorted(have & set(new))
    for c, (adv, shape) in new.items():
        font['glyphs'].append((c, adv, len(font['shapes'])))
        font['shapes'].append(shape)
    font['glyphs'].sort()


def estimate(ttf):
    """Encode the Arabic glyphs of <ttf> as compacted shapes (nominal 256, y down); nothing is written."""
    total = 0
    for lo, hi in ARABIC + [(0x30, 0x39)]:
        g = ttf_glyphs(ttf, range(lo, hi + 1))
        b = sum(len(w_shape(s)) + 8 for _, s in g.values())  # + info row
        print(f'U+{lo:04X}-{hi:04X}	glyphs={len(g)}	bytes={b}')
        total += b
    print(f'total_bytes={total} (shape data + 8 B info row each)')


def self_check():
    for v in (0, 63, 64, 127, 128, 16383):
        assert r_u15(w_u15(v), 0)[0] == v
    for v in (-16384, -65, -64, -1, 0, 63, 64, 16383):
        assert r_s15(w_s15(v), 0)[0] == v
    for v in (0, 63, 64, 1 << 14, 1 << 22, (1 << 30) - 1):
        assert r_u30(w_u30(v), 0)[0] == v
    for f in ((5, 0), (0, -300), (3, 4), (-200, 1000), (1, 2, 3, 4), (-500, 900, 7, 7)):
        t, fl = new_edge(f)
        assert r_edge(w_edge(t, fl), 0)[0] == (t, fl)


if __name__ == '__main__':
    self_check()
    if sys.argv[1] == 'roundtrip':
        sys.exit(1 if roundtrip(sys.argv[2], sys.argv[3:]) else 0)
    if sys.argv[1] == 'estimate':
        estimate(sys.argv[2])
