r"""HUD-VECTOR (BUILD-18): the battle HUD gauge words Focus / Max / Charge of HudStatus and HudStatusCA drawn from a NEW
texture with D texels per stage px, instead of the 256x128 HudStatusTxt(CA) cells that BUILD-17 magnifies x1.20-1.45
(bilinear magnification of too few texels = blur / stair-steps).
How the movies find a texture (evidence, all SwfMovie assets in extracted\assets):
  - DefineExternalImage2 (tag 1009): u32 character id, u16 format (13 = TGA), u16 target width, height, u8-length export
    name, u8-length file name ('HudStatusTxt.tga'); a shape's bitmap fill names the character id.
  - the .uexp property ReferencedAssetNames (ArrayProperty<StrProperty>, after RawData) holds the full object path of
    every image ('/Game/UI/Scaleform/01_hud/hud_status/HudStatusTxt.HudStatusTxt') and of imported movies; the .uasset
    imports no texture. The list is sorted by name, not in tag order (187 movies), and 98 images live in another
    folder than their movie: the engine resolves an image by its name through this list, never by position.
  - a SwfMovie export may grow: tools/tresfont.py rewrites TresFont (RawData count + tag size, uasset SerialSize and
    BulkDataStartOffset) and the larger font has shipped since BUILD-1.
Movie edit (on top of BUILD-17): one DefineExternalImage2 (id NEW_ID, 'HudStatusTxtAR') inserted after the last 1009 tag;
shapes 27 (Focus), 19 (Max) and 22 (Charge) keep bounds and edges, only their fill names NEW_ID with the matrix
20/D twips per texel, the texel grid on whole stage px at the final HUD position (1080p: each screen px = the mean of
a D x D block, an exact box filter for D = 2; 4K: 1:1); the object path inserted into ReferencedAssetNames in sorted
place. The Max badge plate (shape 95) is artwork of HudStatus01 without text and stays as BUILD-17 draws it.
Texture: a Texture2D package copied from HudStatusTxtCA (same name length: no name-map offset moves), names renamed with
their UE4.17 hashes (Strihash_DEPRECATED / StrCrc32, low 16 bits; checked on every name of 01_hud), new package and
lighting Guid, ImportedSize / SizeX / SizeY / mip size / SkipOffset / inline bulk offset / SerialSize /
BulkDataStartOffset rewritten, PF_BC7, 1 mip (as every Scaleform UI texture), inline in the .uexp.
Words: tools/texture_text.repaint on the English cell drawn (nearest) at its BUILD-17 on-screen geometry at D texels per
stage px, row values scaled by F = D x movie scale (box, pad, outline, stroke), same face rules (Focus Plex Regular,
Max / Charge Segoe UI Bold), 'snap' / 'hard' dropped for 'aa:1' (4x supersampled, box-filtered, round outline).
Usage: python -I tools\hud_hires.py              -> self check (name hashes, package and movie round trips)
       python -I tools\hud_hires.py trial <out>  -> D = 2 and 4 rendered, encoded and measured (no pak)"""
import hashlib, math, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
import build_build17 as b17
import hud_scale, hud_sheet, tresfont
import texture_codec as tc

D = 2                                  # texels per stage px (trial: D = 2 beats D = 4 at 1080p, equal at 4K)
NAME, TEMPLATE = 'HudStatusTxtAR', 'HudStatusTxtCA'
HS = b17.SF + '01_hud/hud_status/'
GAME = '/Game/UI/Scaleform/01_hud/hud_status/'
NEW_ID = 168                           # first free character id in both movies (ids 1..167 used)
WORDS = {'Focus': 27, 'Max': 19, 'Charge': 22}               # word -> label shape (= key of b17.LABELS)
TXT = {'HudStatus': 'HudStatusTxt', 'HudStatusCA': 'HudStatusTxtCA'}
ORDER = [('HudStatus', 'Focus'), ('HudStatusCA', 'Focus'), ('HudStatus', 'Max'), ('HudStatus', 'Charge'),
         ('HudStatusCA', 'Charge'), ('HudStatusCA', 'Max')]
sha = lambda b: hashlib.sha256(b).hexdigest()


# ---- UE4.17 name hashes --------------------------------------------------------------------------------------------
def _tables():
    rev, msb = [], []
    for i in range(256):
        c, m = i, i << 24
        for _ in range(8):
            c = c >> 1 ^ 0xEDB88320 if c & 1 else c >> 1
            m = (m << 1 ^ 0x04C11DB7) & 0xFFFFFFFF if m & 0x80000000 else m << 1 & 0xFFFFFFFF
        rev.append(c), msb.append(m)
    return rev, msb


REV, MSB = _tables()


def name_hashes(s):
    """(NonCasePreservingHash, CasePreservingHash) as a cooked name map stores them after the string"""
    a = 0
    for ch in s:
        a = (a >> 8) & 0x00FFFFFF ^ MSB[(a ^ ord(ch.upper())) & 0xFF]          # FCrc::Strihash_DEPRECATED (ANSI)
    c = 0xFFFFFFFF
    for ch in s:
        v = ord(ch)
        for _ in range(4):                                                      # FCrc::StrCrc32: 4 bytes per char
            c = (c >> 8) ^ REV[(c ^ v) & 0xFF]
            v >>= 8
    return a & 0xFFFF, (c ^ 0xFFFFFFFF) & 0xFFFF


def name_entries(ua):
    """[(string, offset of the entry, stored hashes)] of a package's name map"""
    p = 0x1c + 4 + struct.unpack_from('<i', ua, 0x1c)[0]
    _, count, off = struct.unpack_from('<Iii', ua, p)
    out = []
    for _ in range(count):
        n = struct.unpack_from('<i', ua, off)[0]
        out.append((ua[off + 4:off + 3 + n].decode('ascii'), off, struct.unpack_from('<HH', ua, off + 4 + n)))
        off += 8 + n
    return out


# ---- texture package -----------------------------------------------------------------------------------------------
GUID_AT = 0x5d    # FPackageFileSummary.Guid (FolderName 'None' + 14 i32 before it; asserted in package())


def prop_values(ue, names):
    """{property name: offset of its value in the .uexp} (tagged properties as texture_codec.read walks them)"""
    out, p = {}, 0
    fn = lambda p: names[struct.unpack_from('<i', ue, p)[0]]
    while fn(p) != 'None':
        typ, size, q = fn(p + 8), struct.unpack_from('<i', ue, p + 16)[0], p + 24
        q += {'StructProperty': 24, 'BoolProperty': 1, 'ByteProperty': 8, 'EnumProperty': 8, 'ArrayProperty': 8}.get(typ, 0)
        q += 1 + 16 * ue[q]
        out[fn(p)] = q
        p = q + size
    return out


def package(ua, ue, name, w, h, payload):
    """Texture2D package (uasset, uexp) = the template (ua, ue: PF_BC7, 1 inline mip) renamed to name (same length as
    the template's), mip 0 = payload (w x h BC7). With the template's own name, size and payload: the template bytes."""
    t = tc.read(ua, ue)
    pl, = t['platforms']
    m, = pl['mips']
    assert pl['pf'] == 'PF_BC7' and m['where'] == 'uexp' and pl['slices'] == 1 and len(payload) == w * h
    stem = next(n for n in t['names'] if n.startswith(GAME)).split('/')[-1]
    assert len(stem) == len(name), 'same name length keeps every offset of the name map'
    same = stem == name
    a = bytearray(ua)
    assert struct.unpack_from('<i', a, 0x1c)[0] == 5 and a[0x20:0x25] == b'None\0'
    hit = 0
    for s, off, _ in name_entries(ua):
        if s in (stem, GAME + stem):
            new = s.replace(stem, name)
            a[off + 4:off + 4 + len(new)] = new.encode('ascii')
            struct.pack_into('<HH', a, off + 5 + len(new), *name_hashes(new))
            hit += 1
    assert hit == 2, 'package path and object name'
    if not same:                                         # a new asset gets its own ids (deterministic)
        a[GUID_AT:GUID_AT + 16] = hashlib.md5(('package ' + GAME + name).encode()).digest()
    # .uexp: ImportedSize, LightingGuid, then the platform block rebuilt
    e = bytearray(ue)
    at = prop_values(ue, t['names'])
    q = at['ImportedSize']
    assert ue[q:q + 8] == struct.pack('<ii', pl['sx'], pl['sy'])
    e[q:q + 8] = struct.pack('<ii', w, h)
    if not same:
        q = at['LightingGuid']
        e[q:q + 16] = hashlib.md5(('lighting ' + GAME + name).encode()).digest()
    p0 = m['at'] - 67                                    # FName PF, SkipOffset, SizeX/Y, slices, FString PF, first, n, mip head
    base = len(ua)
    assert t['names'][struct.unpack_from('<i', ue, p0)[0]] == 'PF_BC7' and ue[p0 + 28:p0 + 35] == b'PF_BC7\0'
    end = struct.unpack_from('<i', ue, p0 + 8)[0] - base  # SkipOffset (package-absolute) = end of the platform block
    assert end == m['at'] + m['size'] + 8
    blk = bytearray(ue[p0:m['at']]) + payload + struct.pack('<2i', w, h)
    struct.pack_into('<i', blk, 8, base + p0 + len(blk))  # SkipOffset
    struct.pack_into('<2i', blk, 12, w, h)               # SizeX, SizeY
    mh = 43                                              # mip head inside blk: bCooked, flags, count, sizeOnDisk, offset
    assert struct.unpack_from('<iIiiq', blk, mh) == (1, m['flags'], m['size'], m['size'], base + m['at'])
    struct.pack_into('<iIiiq', blk, mh, 1, m['flags'], len(payload), len(payload), base + p0 + 67)
    ue2 = bytes(e[:p0]) + bytes(blk) + bytes(e[end:])
    ss = ua.find(struct.pack('<q', len(ue) - 4))
    bulk = ua.find(struct.pack('<q', len(ua) + len(ue) - 4))
    assert ss > 0 and bulk > 0 and ua.count(struct.pack('<q', len(ue) - 4)) == 1
    struct.pack_into('<q', a, ss, len(ue2) - 4)
    struct.pack_into('<q', a, bulk, len(a) + len(ue2) - 4)
    return bytes(a), ue2


def template():
    rd = lambda e: open(os.path.join('extracted/assets', HS + TEMPLATE + e), 'rb').read()
    return rd('.uasset'), rd('.uexp')


# ---- geometry and cells --------------------------------------------------------------------------------------------
def geometry(d):
    """word -> dict(shape, origin (x, y) twips of the shape at the final HUD position, shape dict, rect stage px)"""
    pls, tags = hud_scale.placements(d)
    first = {}
    for sid, fr, depth, ch, name, q, m in pls:
        first.setdefault((sid, depth), m)
    out = {}
    for wd, shp in WORDS.items():
        path, s2 = b17.LABELS[wd]
        assert s2 == shp
        x, y = b17.ROOT
        for key in path:
            m = first[key]
            assert m['scale'] is None and m['rot'] is None, key
            x, y = x + m['tx'], y + m['ty']
        q, n = tags[shp]
        sh = hud_scale.read_shape(d[q:q + n])
        b = sh['bounds']
        out[wd] = dict(shape=shp, ox=x, oy=y, sh=sh, rect=((x + b[0]) / 20, (x + b[1]) / 20, (y + b[2]) / 20, (y + b[3]) / 20))
    return out


def layout(geo, d=D):
    """(movie, word) -> cell dict(P = stage px of the cell's texel 0, at = texel of the cell in the texture, size, box =
    the shape rectangle in cell texels rounded inward); shelf-packed in ORDER, 4-texel aligned, >= 4 empty texels
    between cells; texture width 256 d, height the next power of two -> (cells, (W, H))"""
    W, x, y, row = 256 * d, 0, 0, 0
    cells = {}
    for mv, wd in ORDER:
        x0, x1, y0, y1 = geo[mv][wd]['rect']
        P = (math.floor(x0), math.floor(y0))
        size = (math.ceil((x1 - P[0]) * d), math.ceil((y1 - P[1]) * d))
        if x + size[0] > W:
            x, y, row = 0, y + row, 0
        box = (math.ceil((x0 - P[0]) * d), math.ceil((y0 - P[1]) * d), math.floor((x1 - P[0]) * d), math.floor((y1 - P[1]) * d))
        cells[(mv, wd)] = dict(P=P, at=(x, y), size=size, box=box)
        x += -(-(size[0] + 4) // 4) * 4
        row = max(row, -(-(size[1] + 4) // 4) * 4)
    H = 1 << (y + row - 1).bit_length()
    return cells, (W, H)


def fill_of(g, c, d=D):
    """fill matrix (fs, ft) twips of shape g drawing cell c: 20/d twips per texel, the cell's texel 0 at stage P"""
    k = 20 // d
    assert k * d == 20
    return [k * 65536] * 2, [20 * c['P'][0] - g['ox'] - k * c['at'][0], 20 * c['P'][1] - g['oy'] - k * c['at'][1]]


# ---- words ---------------------------------------------------------------------------------------------------------
def hires_effect(eff, F):
    """the row's effect at F x the size: outline / stroke scaled, snap and hard (1x pixel-grid tricks) dropped, aa:1"""
    out = []
    for e in eff.split('+'):
        k, _, v = e.partition(':')
        if k in ('outline', 'stroke'):
            out.append(f'{k}:{float(v) * F:.4g}')
        elif k not in ('snap', 'hard', 'aa'):
            out.append(e)
    if not any(e.startswith('stroke:') for e in out):   # below 24 px the 1x text had no stroke; keep none
        out.append('stroke:0')
    return '+'.join(out + ['aa:1'])


def render_cell(tt, row, ar, eng, g, c, d=D):
    """the Arabic word of an images_rects row in cell c: the English cell drawn nearest at its on-screen geometry (d texels
    per stage px), repainted with the scaled row -> (RGBA float canvas, repaint info, hi-res row)"""
    u0, v0, u1, v1 = map(int, row['box'].split())
    src = np.zeros_like(eng, np.float32)
    src[v0:v1, u0:u1] = eng[v0:v1, u0:u1]
    sh = g['sh']
    s = sh['fs'][0] / 65536 / 20                         # BUILD-17 movie scale of the cell (texel -> stage px)
    assert sh['fs'][0] == sh['fs'][1]
    ax, bx = d * s, d * ((g['ox'] + sh['ft'][0]) / 20 - c['P'][0])   # old texel u -> stage px -> cell texel
    ay, by = d * s, d * ((g['oy'] + sh['ft'][1]) / 20 - c['P'][1])
    M = np.float32([[ax, 0, ax * 0.5 + bx - 0.5], [0, ay, ay * 0.5 + by - 0.5]])
    w, h = c['size']
    canvas = cv2.warpAffine(src, M, (w, h), flags=cv2.INTER_NEAREST, borderValue=0)
    F = d * s
    bx0, by0, bx1, by1 = c['box']
    r = dict(row, box=f'{bx0} {by0} {bx1} {by1}', erase='', size='', pad=str(round(int(row['pad']) * F)),
             effect=hires_effect(row['effect'], F))
    info = tt.repaint(canvas, r, ar)
    keep = np.zeros(canvas.shape[:2], bool)
    keep[by0:by1, bx0:bx1] = True
    canvas[~keep] = 0                                    # nothing outside the shape rectangle (English slivers)
    return canvas, info, r


def atlas(d=D, log=None):
    """the new texture (H, W, 4) uint8 + cells + per-cell repaint log rows"""
    import texture_text as tt
    tr = {r['id']: r for r in tt.load_translation()}
    strings = tt.load_strings()
    by = tt.rows_by_asset()
    geo = {mv: geometry(movie17(mv)[1]) for mv in TXT}
    cells, (W, H) = layout(geo, d)
    img = np.zeros((H, W, 4), np.float32)
    rows = []
    for (mv, wd), c in cells.items():
        asset = HS + TXT[mv] + '.uasset'
        eng = tc.rgba0(tc.load(os.path.join('extracted/assets', asset))).astype(np.float32)
        u0, v0 = hud_scale.cell(geo[mv][wd]['sh'])[0::2]
        row = next(r for r in by[asset] if tuple(map(int, r['box'].split()))[:2] == (int(u0), int(v0)))
        ar = tt.arabic(row['source'], tr, strings)
        canvas, info, r = render_cell(tt, row, ar, eng, geo[mv][wd], c, d)
        one = eng.copy()                                 # the same row at 1x (the MASS11 recipe) for the colour check
        info1 = tt.repaint(one, row, ar)
        x, y = c['at']
        img[y:y + c['size'][1], x:x + c['size'][0]] = canvas
        rows.append(dict(movie=mv, word=wd, texture=TXT[mv], effect=r['effect'], pad=r['pad'], box=r['box'],
                         at=f'{x} {y}', size='%dx%d' % c['size'], P='%d %d' % c['P'],
                         font_px=str(info['size']), font_px_1x_equiv=f'{info["size"] / (d * geo[mv][wd]["sh"]["fs"][0] / 65536 / 20):.2f}',
                         font_px_mass11=str(info1['size']), fill=info['fill'], fill_1x=info1['fill'],
                         outline=info['outline'], outline_1x=info1['outline'], margin=str(info['margin']),
                         read=info['read']))
    return np.clip(np.round(img), 0, 255).astype(np.uint8), cells, (W, H), rows


# ---- movies --------------------------------------------------------------------------------------------------------
def movie17(mv):
    """(uasset, BUILD-17 uexp) of a HUD movie: the pinned original uasset and the hud_scale patch of the original uexp"""
    rel = HS + mv
    ua, ue = (open(os.path.join('extracted/assets', rel + e), 'rb').read() for e in ('.uasset', '.uexp'))
    h_ua, h_ue = b17.HUD['01_hud/hud_status/' + mv][1:]
    assert sha(ua) == h_ua and sha(ue) == h_ue, mv
    return ua, hud_scale.patch(ue, b17.HUD_SHAPES, b17.HUD_MOVES)[0]


def image_tag(cid, w, h, name):
    return struct.pack('<IHHH', cid, 13, w, h) + bytes([len(name)]) + name.encode() + bytes([len(name) + 4]) + (name + '.tga').encode()


def refs(post, ua):
    """ReferencedAssetNames of a SwfMovie .uexp tail (right after RawData): (list, end offset of the value)"""
    nm = tc.names(ua)
    fn = lambda p: nm[struct.unpack_from('<i', post, p)[0]]
    assert (fn(0), fn(8), fn(24), post[32]) == ('ReferencedAssetNames', 'ArrayProperty', 'StrProperty', 0)
    n, p, out = struct.unpack_from('<i', post, 33)[0], 37, []
    for _ in range(n):
        ln = struct.unpack_from('<i', post, p)[0]
        out.append(post[p + 4:p + 3 + ln].decode('ascii'))
        p += 4 + ln
    assert p == 33 + struct.unpack_from('<i', post, 16)[0], 'property size'
    return out, p


def with_ref(post, ua, path):
    """post with path inserted into ReferencedAssetNames at its sorted place (the list is sorted by name)"""
    old, end = refs(post, ua)
    assert old == sorted(old, key=str.lower) == sorted(old) and path not in old
    new = sorted(old + [path], key=str.lower)
    assert new == sorted(new)
    val = struct.pack('<i', len(new)) + b''.join(struct.pack('<i', len(s) + 1) + s.encode('ascii') + b'\0' for s in new)
    out = bytearray(post[:33]) + val + post[end:]
    struct.pack_into('<i', out, 16, len(val))
    return bytes(out)


def patch(ua, ue, cells, mv, tex_size, d=D):
    """BUILD-17 movie -> BUILD-18 movie (uasset, uexp): image tag + 3 shape fills + ReferencedAssetNames"""
    a = tresfont.r_asset(ua, ue)
    m = tresfont.r_gfx(a['gfx'])
    last = max(i for i, t in enumerate(m['tags']) if t[0] == 1009)
    ids = {struct.unpack_from('<H', t[2])[0] for t in m['tags'] if t[0] in (2, 22, 32, 83, 39, 37, 46, 84, 10, 48, 75, 1005)}
    assert NEW_ID not in ids and NEW_ID not in {struct.unpack_from('<I', t[2])[0] for t in m['tags'] if t[0] == 1009}
    m['tags'].insert(last + 1, [1009, False, image_tag(NEW_ID, *tex_size, NAME)])
    geo = geometry(ue)
    for wd, shp in WORDS.items():
        i = next(i for i, t in enumerate(m['tags']) if t[0] == 2 and struct.unpack_from('<H', t[2])[0] == shp)
        sh = hud_scale.read_shape(m['tags'][i][2])
        fs, ft = fill_of(geo[wd], cells[(mv, wd)], d)
        new = dict(sh, bitmap=NEW_ID, fs=fs, ft=ft, fs_n=max(sh['fs_n'], hud_scale.need(*fs)),
                   ft_n=max(sh['ft_n'], hud_scale.need(*ft)))
        enc = hud_scale.write_shape(new)
        assert hud_scale.read_shape(enc) == dict(new, nbytes=len(enc))
        m['tags'][i][2] = enc
    a['post'] = with_ref(a['post'], ua, f'{GAME}{NAME}.{NAME}')
    return tresfont.w_asset(a, tresfont.w_gfx(m))


def verify_movie(ua0, ue0, ua1, ue1, cells, mv, tex_size, d=D):
    """BUILD-17 (0) against BUILD-18 (1): -> table rows; asserts every rule"""
    a0, a1 = tresfont.r_asset(ua0, ue0), tresfont.r_asset(ua1, ue1)
    t0, t1 = tresfont.r_gfx(a0['gfx'])['tags'], tresfont.r_gfx(a1['gfx'])['tags']
    i = next(k for k in range(len(t1)) if k >= len(t0) or t0[k] != t1[k] and t1[k][0] == 1009)
    assert t1[i] == [1009, False, image_tag(NEW_ID, *tex_size, NAME)] and len(t1) == len(t0) + 1
    rest = t1[:i] + t1[i + 1:]
    changed = []
    geo0, geo1 = geometry(ue0), geometry(ue1)
    for x, y in zip(t0, rest):
        assert x[0] == y[0], 'tag order'
        if x == y:
            continue
        sid = struct.unpack_from('<H', x[2])[0]
        assert x[0] == 2 and sid in WORDS.values(), ('unplanned tag change', x[0], sid)
        s0, s1 = hud_scale.read_shape(x[2]), hud_scale.read_shape(y[2])
        wd = next(k for k, v in WORDS.items() if v == sid)
        fs, ft = fill_of(geo0[wd], cells[(mv, wd)], d)
        assert s0['bitmap'] == 2 and s1['bitmap'] == NEW_ID and s1['fs'] == fs and s1['ft'] == ft
        assert s0['bounds'] == s1['bounds'] and s0['recs'] == s1['recs'] and s0['ftype'] == s1['ftype'], sid
        assert geo1[wd]['rect'] == geo0[wd]['rect'] and (geo1[wd]['ox'], geo1[wd]['oy']) == (geo0[wd]['ox'], geo0[wd]['oy'])
        # the shape rectangle maps into its own cell, inside the rendered box, texel grid on whole stage px
        u0, u1, v0, v1 = hud_scale.cell(s1)
        c = cells[(mv, wd)]
        bx = (u0 - c['at'][0], u1 - c['at'][0], v0 - c['at'][1], v1 - c['at'][1])
        assert -1e-9 <= bx[0] and bx[1] <= c['size'][0] and -1e-9 <= bx[2] and bx[3] <= c['size'][1], (wd, bx)
        org = (geo1[wd]['ox'] + s1['ft'][0] + 20 // d * c['at'][0], geo1[wd]['oy'] + s1['ft'][1] + 20 // d * c['at'][1])
        assert org == (20 * c['P'][0], 20 * c['P'][1]), (wd, org, c['P'])   # cell texel 0 on a whole stage px
        changed.append((sid, wd, len(x[2]), len(y[2]), s0, s1, bx))
    assert sorted(c[0] for c in changed) == sorted(WORDS.values())
    # placements decode the same (their file offsets shift by the inserted tag only)
    p0, sh0 = hud_scale.placements(ue0)
    p1, sh1 = hud_scale.placements(ue1)
    key = lambda x: x[:5] + (tuple((k, v) for k, v in x[6].items() if k not in ('tbit', 'end')),)
    assert [key(x) for x in p0] == [key(x) for x in p1] and set(sh0) == set(sh1)
    # .uexp outside the movie: RawData count and size only; tail: ReferencedAssetNames + the new path only
    pre0, pre1 = bytearray(a0['pre']), bytearray(a1['pre'])
    diff = [k for k in range(len(pre0)) if pre0[k] != pre1[k]]
    assert len(pre0) == len(pre1) and set(diff) <= set(range(len(pre0) - 21, len(pre0) - 17)) | set(range(len(pre0) - 4, len(pre0)))
    r0, e0 = refs(a0['post'], ua0)
    r1, e1 = refs(a1['post'], ua1)
    assert sorted(r1, key=str.lower) == r1 and set(r1) - set(r0) == {f'{GAME}{NAME}.{NAME}'} and len(r1) == len(r0) + 1
    assert a0['post'][e0:] == a1['post'][e1:] and a0['post'][:16] == a1['post'][:16] and a0['post'][20:33] == a1['post'][20:33]
    du = [k for k in range(len(ua0)) if ua0[k] != ua1[k]]
    assert len(ua0) == len(ua1) and set(du) <= set(range(a0['ss_at'], a0['ss_at'] + 8)) | set(range(a0['bulk_at'], a0['bulk_at'] + 8))
    assert struct.unpack_from('<q', ua1, a1['ss_at'])[0] == len(ue1) - 4
    rows = [[mv, 'uexp size', f'{len(ue0)} -> {len(ue1)} B (+{len(ue1) - len(ue0)})'],
            [mv, 'uasset', f'{len(du)} bytes differ: export SerialSize {len(ue0) - 4} -> {len(ue1) - 4}, BulkDataStartOffset'],
            [mv, 'tags', f'{len(t0)} -> {len(t1)}: tag {i} inserted = DefineExternalImage2 id {NEW_ID} {tex_size[0]}x{tex_size[1]} '
                         f'{NAME}.tga; {len(changed)} shapes changed (bitmap + fill matrix), all other tags byte-identical'],
            [mv, 'ReferencedAssetNames', f'{len(r0)} -> {len(r1)}: + {GAME}{NAME}.{NAME} (sorted place {r1.index(GAME + NAME + "." + NAME)})']]
    for sid, wd, n0, n1, s0, s1, bx in changed:
        rows.append([mv, f'shape #{sid} {wd}', f'{n0} -> {n1} B; bitmap 2 -> {NEW_ID}; fill twips/texel {s0["fs"][0] / 65536:g} -> '
                     f'{s1["fs"][0] / 65536:g}, translate {s0["ft"]} -> {s1["ft"]}; bounds and edges unchanged; draws texels '
                     f'{hud_scale.cell(s1)} = cell {cells[(mv, wd)]["at"]} + {tuple(round(v, 2) for v in bx)}'])
    rows += [[mv, 'sha256 BUILD-17 uexp', sha(ue0)], [mv, 'sha256 BUILD-18 uexp', sha(ue1)],
             [mv, 'sha256 BUILD-18 uasset', sha(ua1)]]
    return rows


def verify_texture(ua, ue, rgba, tex_size):
    t = tc.read(ua, ue)
    pl, = t['platforms']
    m, = pl['mips']
    assert (pl['pf'], pl['sx'], pl['sy'], m['w'], m['h'], m['where'], pl['first']) == ('PF_BC7', *tex_size, *tex_size, 'uexp', 0)
    nm = {s: hs for s, _, hs in name_entries(ua)}
    assert GAME + NAME in nm and NAME in nm and not any(TEMPLATE in s for s in nm)
    assert all(hs == name_hashes(s) for s, hs in nm.items()), 'name hash'
    exp = struct.unpack_from('<i', ua, 0x3d)[0]          # ExportOffset -> ObjectName FName index at +16
    assert t['names'][struct.unpack_from('<i', ua, exp + 16)[0]] == NAME
    assert tc.mip_bytes(t, m) == encode(rgba)
    ta, te = template()
    du = sum(x != y for x, y in zip(ua, ta))
    return [['texture', 'path', f'{HS}{NAME}.uasset/.uexp (object {GAME}{NAME}.{NAME})'],
            ['texture', 'format', f'{pl["pf"]} {pl["sx"]}x{pl["sy"]}, mips {len(pl["mips"])}, inline in .uexp, slices {pl["slices"]}'],
            ['texture', 'sizes', f'uasset {len(ua)} B (template {len(ta)}), uexp {len(ue)} B (template {len(te)})'],
            ['texture', 'parse', 'texture_codec.read PASS (SerialSize, SkipOffset, inline offset); mip 0 = the BC7 of the atlas'],
            ['texture', 'names', f'{len(nm)} names, hashes recomputed and checked; export ObjectName = {NAME}; '
                                 f'{du} uasset bytes differ from the {TEMPLATE} template (2 names + hashes, Guid, sizes)'],
            ['texture', 'sha256 uasset', sha(ua)], ['texture', 'sha256 uexp', sha(ue)]]


def encode(img):
    """BC7 with linear channel weights and bc7enc uber level 4: worst visible (premultiplied) block error 8.2 instead of
    11.8 with texture_codec's perceptual default; mean ~1 level either way"""
    import etcpak
    p = etcpak.BC7CompressBlockParams()
    p.init_linear_weights()
    p.m_uber_level = 4
    h, w = img.shape[:2]
    assert h % 4 == 0 and w % 4 == 0
    return etcpak.compress_bc7(np.ascontiguousarray(img).tobytes(), w, h, p)


def build(d=D):
    """-> files {path in pak: bytes}, verify rows, repaint log rows, BC7-decoded atlas, cells, size"""
    img, cells, size, log = atlas(d)
    payload = encode(img)
    dec = tc.decode('PF_BC7', payload, *size)            # what the GPU samples
    for r, ((mv, wd), c) in zip(log, cells.items()):
        x, y = c['at']
        r['bc7_rms_mean'], r['bc7_rms_max'] = (f'{v:.2f}' for v in hud_sheet.bc7_error(img, dec, (x, y, x + c['size'][0], y + c['size'][1])))
    tu, te = package(*template(), NAME, *size, payload)
    files = {HS + NAME + '.uasset': tu, HS + NAME + '.uexp': te}
    rows = verify_texture(tu, te, img, size)
    for mv in TXT:
        ua0, ue0 = movie17(mv)
        ua1, ue1 = patch(ua0, ue0, cells, mv, size, d)
        rows += verify_movie(ua0, ue0, ua1, ue1, cells, mv, size, d)
        files.update({HS + mv + '.uasset': ua1, HS + mv + '.uexp': ue1})
    return files, rows, log, dec, cells, size


# ---- simulation ----------------------------------------------------------------------------------------------------
def look(d, tex, word, zoom=1):
    """straight RGBA float 0..1 of one label shape as the GPU draws it: movie geometry at the final HUD position, bilinear
    from tex[bitmap id] (mip 0, no mips), output px = stage px x zoom (1 = 1920x1080, 2 = 3840x2160), 1 stage px of
    empty border, alpha x the rectangle's pixel coverage (as hud_sheet.magnify)"""
    g = geometry(d)[word]
    sh = g['sh']
    x0, x1, y0, y1 = g['rect']
    X0, Y0 = math.floor(x0) - 1, math.floor(y0) - 1
    w, h = math.ceil((x1 + 1 - X0) * zoom), math.ceil((y1 + 1 - Y0) * zoom)
    ax, ay = (zoom * sh['fs'][k] / 65536 / 20 for k in (0, 1))
    bx, by = zoom * ((g['ox'] + sh['ft'][0]) / 20 - X0), zoom * ((g['oy'] + sh['ft'][1]) / 20 - Y0)
    M = np.float32([[ax, 0, ax * 0.5 + bx - 0.5], [0, ay, ay * 0.5 + by - 0.5]])
    out = cv2.warpAffine(tex[sh['bitmap']].astype(np.float32) / 255, M, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
    cov = lambda n, lo, hi: np.clip(np.minimum(np.arange(n) + 1, hi) - np.maximum(np.arange(n), lo), 0, 1)
    out[..., 3] *= np.outer(cov(h, zoom * (y0 - Y0), zoom * (y1 - Y0)), cov(w, zoom * (x0 - X0), zoom * (x1 - X0)))
    return out


def measure(m):
    """(edge, crisp, contrast, jag, steps), mean of the bar and dark backdrops"""
    (eb, cb, kb), (ed, cd, kd) = hud_sheet.metrics(m, 'bar'), hud_sheet.metrics(m, 'dark')
    (jb, sb), (jd, sd) = hud_sheet.jaggedness(m, 'bar'), hud_sheet.jaggedness(m, 'dark')
    return (eb + ed) / 2, (kb + kd) / 2, (cb + cd) / 2, (jb + jd) / 2, (sb + sd) / 2


def sources(files, img):
    """label -> [(column, movie uexp, textures by bitmap id)] English | MASS11 | HUD-VECTOR"""
    out = {}
    for mv, txt in TXT.items():
        ue17 = movie17(mv)[1]
        ld = lambda root: tc.rgba0(tc.load(os.path.join(root, HS + txt + '.uasset')))
        out[mv] = [('English (BUILD-17)', ue17, {2: ld('extracted/assets')}),
                   ('MASS11 (BUILD-17)', ue17, {2: ld('out/builds/IMAGES-MASS11/assets')}),
                   ('HUD-VECTOR (BUILD-18)', files[HS + mv + '.uexp'], {NEW_ID: img})]
    return out


DISPLAYS = ((1, '1080p'), (4 / 3, '1440p'), (2, '4K'))   # output px per stage px


def blur(m, s):
    """premultiplied Gaussian blur of a straight RGBA look"""
    a = m[..., 3:]
    pm = cv2.GaussianBlur(np.concatenate([m[..., :3] * a, a], -1), (0, 0), s)
    out = pm.copy()
    out[..., :3] = np.where(pm[..., 3:] > 1e-6, pm[..., :3] / np.maximum(pm[..., 3:], 1e-6), 0)
    return out


def matched_jag(m, edge):
    """jag of look m blurred until its edge equals edge (jag rises with sharpness: a sharper word has more contour detail;
    at equal sharpness it compares the stair-steps alone) -> (jag, sigma)"""
    e = lambda x: (hud_sheet.metrics(x, 'bar')[0] + hud_sheet.metrics(x, 'dark')[0]) / 2
    lo, hi = 0.0, 3.0
    for _ in range(16):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if e(blur(m, mid)) > edge else (lo, mid)
    return measure(blur(m, lo))[3], lo


def metrics_table(files, img):
    head = ['movie', 'word', 'display', 'source', 'edge', 'crisp_pct', 'contrast', 'jag', 'steps', 'edge_vs_english_pct',
            'crisp_vs_english_pct', 'edge_vs_mass11_pct', 'jag_vs_mass11_pct', 'jag_at_mass11_edge', 'matched_jag_vs_mass11_pct']
    rows = []
    for mv, cols in sources(files, img).items():
        for wd in WORDS:
            for zoom, disp in DISPLAYS:
                base = ref = None
                for label, ue, tex in cols:
                    m = look(ue, tex, wd, zoom)
                    e, c, k, j, s = measure(m)
                    base = base or dict(e=e, c=c)
                    if label.startswith('MASS11'):
                        ref = dict(e=e, j=j)
                    mj = matched_jag(m, ref['e'])[0] if label.startswith('HUD') else None
                    rows.append([mv, wd, disp, label, f'{e:.1f}', f'{c:.0f}', f'{k:.1f}', f'{j:.1f}', f'{s:.1f}',
                                 f'{100 * e / base["e"]:.0f}', f'{100 * c / base["c"]:.0f}',
                                 *((f'{100 * e / ref["e"]:.0f}', f'{100 * j / ref["j"]:.0f}') if ref else ('-', '-')),
                                 f'{mj:.1f}' if mj else '-', f'{100 * mj / ref["j"]:.0f}' if mj else '-'])
    return [head] + rows


def gates(table):
    """per movie, word and display: HUD-VECTOR edge >= 110 % of English and >= MASS11, crisp >= 75 % of English (the
    HUD-CRISP / HUD-SOFTEN look gates); the build requires PASS at 1080p and 4K -> rows"""
    h = table[0]
    out = [['movie', 'word', 'display', 'edge_vs_english_pct', 'edge_vs_mass11_pct', 'crisp_vs_english_pct', 'result']]
    for r in (dict(zip(h, r)) for r in table[1:] if r[3].startswith('HUD')):
        ok = (int(r['edge_vs_english_pct']) >= 110 and int(r['edge_vs_mass11_pct']) >= 100 and int(r['crisp_vs_english_pct']) >= 75)
        out.append([r['movie'], r['word'], r['display'], r['edge_vs_english_pct'], r['edge_vs_mass11_pct'],
                    r['crisp_vs_english_pct'], 'PASS' if ok else 'FAIL'])
    return out


def sheets(files, img, out):
    """LOOK_<movie>_<display>.png: columns English | MASS11 | HUD-VECTOR, rows Focus / Max / Charge, each bar | dark;
    1080p also as a 3x nearest zoom (the same pixels, larger)"""
    for mv, cols in sources(files, img).items():
        for zoom, disp in ((1, '1080p'), (2, '4K')):
            rows = []
            for wd in WORDS:
                parts = []
                for label, ue, tex in cols:
                    m = look(ue, tex, wd, zoom)
                    c = [hud_sheet.composite(m, b) for b in ('bar', 'dark')]
                    parts.append(np.hstack([c[0], np.full((c[0].shape[0], 3, 3), 255.0), c[1]]))
                hh = max(p.shape[0] for p in parts)
                parts = [np.pad(p, ((0, hh - p.shape[0]), (0, 10), (0, 0)), constant_values=255) for p in parts]
                rows.append(np.pad(np.hstack(parts), ((0, 6), (0, 0), (0, 0)), constant_values=255))
            ww = max(r.shape[1] for r in rows)
            sheet = np.clip(np.vstack([np.pad(r, ((0, 0), (0, ww - r.shape[1]), (0, 0)), constant_values=255) for r in rows]), 0, 255).astype(np.uint8)
            for z in ((1, 3) if zoom == 1 else (1,)):
                im = cv2.resize(sheet, (sheet.shape[1] * z, sheet.shape[0] * z), interpolation=cv2.INTER_NEAREST)[..., ::-1]
                head = np.full((30, max(im.shape[1], 640), 3), 255, np.uint8)
                for i, line in enumerate((f'SIMULATION (not a game screenshot) {mv} at {disp}' + (f', zoomed {z}x nearest' if z > 1 else '')
                                          + ': BC7 decode, bilinear from the texture, no mips',
                                          'columns: ' + ' | '.join(c[0] for c in cols) + ' (each: yellow bar | dark); rows: Focus / Max / Charge')):
                    cv2.putText(head, line, (4, 12 + 14 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (0, 0, 0), 1, cv2.LINE_AA)
                im = np.pad(im, ((0, 0), (0, head.shape[1] - im.shape[1]), (0, 0)), constant_values=255)
                name = f'LOOK_{mv}_{disp}' + (f'_zoom{z}x' if z > 1 else '')
                cv2.imwrite(os.path.join(out, name + '.png'), np.vstack([head, im]))


def hud_sheets(files, img, out):
    """the whole HUD simulation (hud_sheet.render): left BUILD-17 + IMAGES-MASS11 | right BUILD-18 (+ MASS11 for the other
    cells of HudStatusTxt), one row per gauge-word state -> HUD_<movie>_1x.png / _2x.png (2x = nearest)"""
    load = lambda f: tc.rgba0(tc.load(f)).astype(np.float32) / 255
    base = {1: load('extracted/assets/' + HS + 'HudThunder.uasset'), 3: load('extracted/assets/' + HS + 'HudStatus01.uasset'),
            4: load('extracted/assets/' + HS + 'CrossEff01.uasset')}
    for mv, txt in TXT.items():
        if mv.endswith('CA'):
            base[3] = load('extracted/assets/' + HS + 'HudStatus01CA.uasset')
        t17 = {**base, 2: load('out/builds/IMAGES-MASS11/assets/' + HS + txt + '.uasset')}
        t18 = {**t17, NEW_ID: img.astype(np.float32) / 255}
        rs = []
        for state, hide in hud_sheet.STATES.items():
            a, b = hud_sheet.render(movie17(mv)[1], t17, hide), hud_sheet.render(files[HS + mv + '.uexp'], t18, hide)
            rs.append(np.hstack([a, np.ones((a.shape[0], 4, 3)), b]))
        sheet = (np.clip(np.vstack([np.vstack([r, np.ones((4, r.shape[1], 3))]) for r in rs]), 0, 1) * 255).astype(np.uint8)
        for z in (1, 2):
            im = cv2.resize(sheet, (sheet.shape[1] * z, sheet.shape[0] * z), interpolation=cv2.INTER_NEAREST)[..., ::-1].copy()
            head = np.full((34 * z, im.shape[1], 3), 255, np.uint8)
            for i, line in enumerate((f'SIMULATION, not a game screenshot: {mv} at {z}x of 1920x1080',
                                      'left BUILD-17 + IMAGES-MASS11 | right BUILD-18 (HUD-VECTOR); rows Focus / Max / Charge')):
                cv2.putText(head, line, (4, (14 + 15 * i) * z), cv2.FONT_HERSHEY_SIMPLEX, 0.36 * z, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.imwrite(os.path.join(out, f'HUD_{mv}_{z}x.png'), np.vstack([head, im]))


def write_tsv(path, rows):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(map(str, r)) + '\n' for r in rows)


def trial(out):
    """D = 2 and D = 4 side by side on the simulator -> <out>/trial_D.tsv"""
    os.makedirs(out, exist_ok=True)
    rows = []
    for d in (2, 4):
        files, vrows, log, img, cells, size = build(d)
        t = metrics_table(files, img)
        rows += [['D'] + t[0]] if not rows else []
        rows += [[str(d)] + r for r in t[1:] if r[3].startswith('HUD') or d == 2]
        print(f'D={d}: texture {size}, cells {len(cells)}', flush=True)
    write_tsv(os.path.join(out, 'trial_D.tsv'), rows)
    for r in rows:
        print('\t'.join(r))


def self_check():
    names = bad = 0
    root = os.path.join('extracted/assets', b17.SF, '01_hud')
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.uasset'):
                for s, _, hs in name_entries(open(os.path.join(dp, f), 'rb').read()):
                    names += 1
                    bad += hs != name_hashes(s)
    assert names > 10000 and not bad, (names, bad)
    ua, ue = template()
    t = tc.read(ua, ue)
    m = t['platforms'][0]['mips'][0]
    assert package(ua, ue, TEMPLATE, m['w'], m['h'], tc.mip_bytes(t, m)) == (ua, ue), 'package round trip'
    for mv in TXT:                                       # the movie writer reproduces BUILD-17 byte for byte
        ua, ue = movie17(mv)
        a = tresfont.r_asset(ua, ue)
        assert tresfont.w_asset(a, tresfont.w_gfx(tresfont.r_gfx(a['gfx']))) == (ua, ue), mv
        old, end = refs(a['post'], ua)
        assert old == sorted(old, key=str.lower) == sorted(old)
    print(f'hud_hires self check: {names} name hashes, package round trip, movie round trip: PASS')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1:2] == ['trial']:
        trial(sys.argv[2])
    else:
        self_check()
