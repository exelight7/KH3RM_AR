r"""HUD-SCALE (BUILD-17): enlarge the battle HUD gauge words of the HudStatus / HudStatusCA movies (Focus, Max with its
badge plate, Charge) without changing any tag length. The placements of these words carry no scale field (adding one
would grow the PlaceObject, its DefineSprite, the movie and the uasset), so the scale is written into the label
shapes themselves: each is a bitmap-filled rectangle (bounds, one smoothed bitmap fill, one move, four straight
edges), re-encoded with every coordinate mapped x' = x0' + s (x - x0) and the fill matrix scaled by s, so the same
texture cell is drawn s times larger (bilinear). A field keeps its bit width unless the new value needs more; the
shape must still fit its old byte length (the spare padding bits of the last byte). Translates of chosen placements
are rewritten in place with the same bit width. Nothing else is touched; verify() re-parses and proves it.
Usage: python -I tools\hud_scale.py   -> self check on the extracted movies (no output files)"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx_fonts import movie
from build_build3 import tag_offsets
from gfx_edittext import cstr


class Bits:
    def __init__(self, d, p):
        self.d, self.b = d, p * 8

    def u(self, n):
        v = 0
        for _ in range(n):
            v = v << 1 | (self.d[self.b >> 3] >> (7 - (self.b & 7))) & 1
            self.b += 1
        return v

    def s(self, n):
        v = self.u(n)
        return v - (1 << n) if n and v >> (n - 1) else v


class Writer:
    def __init__(self):
        self.bits = []

    def u(self, n, v):
        assert 0 <= v < 1 << n, (n, v)
        self.bits += [(v >> (n - 1 - i)) & 1 for i in range(n)]

    def s(self, n, v):
        assert -(1 << (n - 1)) <= v < 1 << (n - 1), (n, v)
        self.u(n, v & ((1 << n) - 1))

    def out(self):
        b = self.bits + [0] * (-len(self.bits) % 8)
        return bytes(int(''.join(map(str, b[i:i + 8])), 2) for i in range(0, len(b), 8))


def need(*vs):
    """signed bit width that holds every value"""
    return max(max(v.bit_length() + 1 if v >= 0 else (~v).bit_length() + 1 for v in vs), 1)


def read_shape(t):
    """DefineShape (2) body of a bitmap rectangle -> dict (twips, raw 16.16 fill scale)"""
    r = Bits(t, 2)
    n = r.u(5)
    sh = dict(id=struct.unpack_from('<H', t)[0], rect_n=n, bounds=[r.s(n) for _ in range(4)])
    p = (r.b + 7) // 8
    assert t[p] == 1 and t[p + 1] in (0x40, 0x41), 'one bitmap fill expected'
    sh['ftype'], sh['bitmap'] = t[p + 1], struct.unpack_from('<H', t, p + 2)[0]
    r = Bits(t, p + 4)
    assert r.u(1)
    sh['fs_n'] = r.u(5)
    sh['fs'] = [r.s(sh['fs_n']), r.s(sh['fs_n'])]
    assert not r.u(1), 'rotation'
    sh['ft_n'] = r.u(5)
    sh['ft'] = [r.s(sh['ft_n']), r.s(sh['ft_n'])]
    p = (r.b + 7) // 8
    assert t[p] == 0, 'line styles'
    r = Bits(t, p + 1)
    sh['nfb'], sh['nlb'] = r.u(4), r.u(4)
    recs = []
    while True:
        if not r.u(1):
            fl = r.u(5)
            if fl == 0:
                break
            assert fl & 1 and not fl & 0x18, fl
            mn = r.u(5)
            rec = dict(kind='style', flags=fl, move_n=mn, move=[r.s(mn), r.s(mn)])
            rec['fills'] = [r.u(sh['nfb']) for k in (2, 4) if fl & k]
            recs.append(rec)
        else:
            assert r.u(1), 'curve'
            nb = r.u(4) + 2
            if r.u(1):
                recs.append(dict(kind='line', nb=nb, d=[r.s(nb), r.s(nb)]))
            else:
                v = r.u(1)
                x = r.s(nb)
                recs.append(dict(kind='line', nb=nb, vert=v, d=[0, x] if v else [x, 0]))
    sh['recs'], sh['nbytes'] = recs, len(t)
    return sh


def write_shape(sh):
    w = Writer()
    w.u(16, 0)  # placeholder for the id, replaced below
    w.u(5, sh['rect_n'])
    for v in sh['bounds']:
        w.s(sh['rect_n'], v)
    head = w.out()
    head = struct.pack('<H', sh['id']) + head[2:]
    w = Writer()
    w.u(1, 1)
    w.u(5, sh['fs_n'])
    w.s(sh['fs_n'], sh['fs'][0]), w.s(sh['fs_n'], sh['fs'][1])
    w.u(1, 0)
    w.u(5, sh['ft_n'])
    w.s(sh['ft_n'], sh['ft'][0]), w.s(sh['ft_n'], sh['ft'][1])
    fill = bytes([1, sh['ftype']]) + struct.pack('<H', sh['bitmap']) + w.out() + b'\0'
    w = Writer()
    w.u(4, sh['nfb']), w.u(4, sh['nlb'])
    for rec in sh['recs']:
        if rec['kind'] == 'style':
            w.u(1, 0), w.u(5, rec['flags']), w.u(5, rec['move_n'])
            w.s(rec['move_n'], rec['move'][0]), w.s(rec['move_n'], rec['move'][1])
            for f in rec['fills']:
                w.u(sh['nfb'], f)
        else:
            w.u(1, 1), w.u(1, 1), w.u(4, rec['nb'] - 2)
            if 'vert' not in rec:
                w.u(1, 1), w.s(rec['nb'], rec['d'][0]), w.s(rec['nb'], rec['d'][1])
            else:
                w.u(1, 0), w.u(1, rec['vert']), w.s(rec['nb'], rec['d'][rec['vert']])
    w.u(6, 0)  # end of shape
    return head + fill + w.out()


def exact(v):
    """twips must stay whole: the scaled cell edges land on the same texel borders"""
    assert abs(v - round(v)) < 1e-6, v
    return round(v)


def scaled(sh, s, x0, y0):
    """the shape scaled by s with its bounds' top-left moved to (x0, y0) twips; bit widths grow only where needed"""
    ox, oy = sh['bounds'][0], sh['bounds'][2]
    X = lambda x: x0 + s * (x - ox)
    Y = lambda y: y0 + s * (y - oy)
    new = dict(sh, bounds=[exact(X(sh['bounds'][0])), exact(X(sh['bounds'][1])), exact(Y(sh['bounds'][2])),
                           exact(Y(sh['bounds'][3]))],
               fs=[exact(v * s) for v in sh['fs']], ft=[exact(X(sh['ft'][0])), exact(Y(sh['ft'][1]))], recs=[])
    new['rect_n'] = max(sh['rect_n'], need(*new['bounds']))
    new['fs_n'] = max(sh['fs_n'], need(*new['fs']))
    new['ft_n'] = max(sh['ft_n'], need(*new['ft']))
    for rec in sh['recs']:
        if rec['kind'] == 'style':
            m = [exact(X(rec['move'][0])), exact(Y(rec['move'][1]))]
            new['recs'].append(dict(rec, move=m, move_n=max(rec['move_n'], need(*m))))
        else:
            d = [exact(v * s) for v in rec['d']]
            new['recs'].append(dict(rec, d=d, nb=max(rec['nb'], need(*d))))
    assert sum(r['d'][0] for r in new['recs'] if r['kind'] == 'line') == 0 == sum(
        r['d'][1] for r in new['recs'] if r['kind'] == 'line'), 'outline not closed'
    return new


def cell(sh):
    """texel rectangle drawn by the shape: (u0, u1, v0, v1) from bounds and fill matrix"""
    x0, x1, y0, y1 = sh['bounds']
    return ((x0 - sh['ft'][0]) * 65536 / sh['fs'][0], (x1 - sh['ft'][0]) * 65536 / sh['fs'][0],
            (y0 - sh['ft'][1]) * 65536 / sh['fs'][1], (y1 - sh['ft'][1]) * 65536 / sh['fs'][1])


def matrix(d, q):
    """matrix at byte q of d -> dict(scale, rot, tn, tx, ty, tbit = bit offset of the translate values, end)"""
    r = Bits(d, q)
    m = dict(scale=None, rot=None)
    if r.u(1):
        n = r.u(5)
        m['scale'] = (r.s(n), r.s(n))
    if r.u(1):
        n = r.u(5)
        m['rot'] = (r.s(n), r.s(n))
    m['tn'] = r.u(5)
    m['tbit'] = r.b
    m['tx'], m['ty'] = r.s(m['tn']), r.s(m['tn'])
    m['end'] = (r.b + 7) // 8
    return m


def placements(d):
    """every PlaceObject2/3 with a matrix inside a DefineSprite -> [(sprite, frame, depth, char, name, file offset
    of the matrix, matrix dict)]; plus the shape tags {id: (file offset of the body, length)}"""
    sig, ver, size, at, body = movie(d)
    assert sig == b'GFX', 'compressed movie: offsets would not map'
    base = at + 8
    out, shapes = [], {}
    for code, p, n in tag_offsets(body):
        if code == 2:
            shapes[struct.unpack_from('<H', body, p)[0]] = (base + p, n)
        if code != 39:
            continue
        sid, q, fr = struct.unpack_from('<H', body, p)[0], p + 4, 0
        while q < p + n:
            h = struct.unpack_from('<H', body, q)[0]
            q += 2
            c, ln = h >> 6, h & 0x3F
            if ln == 0x3F:
                ln = struct.unpack_from('<I', body, q)[0]
                q += 4
            if c == 1:
                fr += 1
            elif c in (26, 70):
                f = body[q]
                k = q + (3 if c == 26 else 4)
                if c == 70 and body[q + 1] & 0x08:
                    k = cstr(body, k)[1]
                ch = None
                if f & 0x02:
                    ch = struct.unpack_from('<H', body, k)[0]
                    k += 2
                if f & 0x04:
                    m = matrix(d, base + k)
                    k2 = m['end'] - base
                    name = ''
                    if f & 0x20:  # name after the colour transform / ratio
                        kk = k2
                        if f & 0x08:
                            rr = Bits(body, kk)
                            ha, hm, nn = rr.u(1), rr.u(1), rr.u(4)
                            for _ in range((4 if hm else 0) + (4 if ha else 0)):
                                rr.s(nn)
                            kk = (rr.b + 7) // 8
                        if f & 0x10:
                            kk += 2
                        name = cstr(body, kk)[0]
                    depth = struct.unpack_from('<H', body, q + (1 if c == 26 else 2))[0]
                    out.append((sid, fr, depth, ch, name, base + k, m))
            elif c == 0:
                break
            q += ln
    return out, shapes


def set_translate(d, q, tx, ty):
    """d with the matrix at byte q given translate tx, ty twips (same bit width: length unchanged)"""
    m = matrix(d, q)
    n = m['tn']
    assert need(tx, ty) <= n, f'translate {tx},{ty} needs {need(tx, ty)} bits, the matrix has {n}'
    b = bytearray(d)
    for i, v in enumerate((tx, ty)):
        v &= (1 << n) - 1
        for j in range(n):
            pos = m['tbit'] + i * n + j
            bit = (v >> (n - 1 - j)) & 1
            b[pos >> 3] = b[pos >> 3] & ~(0x80 >> (pos & 7)) | (bit << (7 - (pos & 7)))
    return bytes(b)


def patch(d, shapes, moves):
    """shapes {id: (s, x0, y0)}, moves {(sprite, depth): f(scale k) -> (tx, ty) twips} -> (patched d, plan rows)"""
    pls, tags = placements(d)
    out = bytearray(d)
    plan = []
    for sid, (s, x0, y0) in shapes.items():
        q, n = tags[sid]
        old = read_shape(d[q:q + n])
        new = scaled(old, s, x0, y0)
        enc = write_shape(new)
        assert len(enc) == n, f'shape {sid}: {len(enc)} bytes, tag has {n} (spare bits exhausted)'
        assert read_shape(enc) == dict(new, nbytes=n)
        out[q:q + n] = enc
        plan.append(('shape', sid, q, n, old, new))
    d2 = bytes(out)
    for sid, fr, depth, ch, name, q, m in pls:
        if (sid, depth) in moves:
            k = m['scale'][0] / 65536 if m['scale'] else 1.0
            tx, ty = moves[(sid, depth)](k)
            d2 = set_translate(d2, q, tx, ty)
            plan.append(('move', (sid, fr, depth, name), q, m['end'] - q, (m['tx'], m['ty']), (tx, ty)))
    return d2, plan


def verify(old, new, shapes, moves):
    """re-parse: same size and tags; bytes differ only inside the planned shapes and matrices; every other placement
    and shape decodes the same; each scaled shape still draws exactly its old texture cell -> (rows, plan)"""
    assert len(old) == len(new), 'size changed'
    so, sn = movie(old), movie(new)
    assert so[:4] == sn[:4]
    assert [(c, p, n) for c, p, n in tag_offsets(so[4])] == [(c, p, n) for c, p, n in tag_offsets(sn[4])], 'tags'
    _, plan = patch(old, shapes, moves)
    allowed = set()
    for kind, _, q, n, *_ in plan:
        allowed.update(range(q, q + n))
    diff = [i for i in range(len(old)) if old[i] != new[i]]
    assert set(diff) <= allowed, f'bytes outside the plan: {sorted(set(diff) - allowed)[:10]}'
    po, to = placements(old)
    pn, tn = placements(new)
    assert to == tn and len(po) == len(pn)
    moved = 0
    for a, b in zip(po, pn):
        assert a[:6] == b[:6]
        ma, mb = dict(a[6]), dict(b[6])
        if (a[0], a[2]) in moves:
            k = ma['scale'][0] / 65536 if ma['scale'] else 1.0
            assert (mb['tx'], mb['ty']) == moves[(a[0], a[2])](k)
            moved += (ma['tx'], ma['ty']) != (mb['tx'], mb['ty'])
            for m in (ma, mb):
                m.pop('tx'), m.pop('ty')
        assert ma == mb, (a[:5], ma, mb)
    for sid, (q, n) in to.items():
        a, b = old[q:q + n], new[q:q + n]
        if sid not in shapes:
            assert a == b, sid
            continue
        sa, sb = read_shape(a), read_shape(b)
        assert cell(sa) == cell(sb), (sid, cell(sa), cell(sb))
        s, x0, y0 = shapes[sid]
        assert sb['bounds'][0] == x0 and sb['bounds'][2] == y0
        assert sb['bounds'][1] - sb['bounds'][0] == round(s * (sa['bounds'][1] - sa['bounds'][0]))
        assert sb['bounds'][3] - sb['bounds'][2] == round(s * (sa['bounds'][3] - sa['bounds'][2]))
    return diff, plan, moved


if __name__ == '__main__':
    import build_build17 as b17
    for mv in b17.HUD:
        d = open(os.path.join('extracted/assets', b17.SF + mv + '.uexp'), 'rb').read()
        new, plan = patch(d, b17.HUD_SHAPES, b17.HUD_MOVES)
        diff, plan, moved = verify(d, new, b17.HUD_SHAPES, b17.HUD_MOVES)
        assert patch(new, {}, {})[0] == new
        print(f'{mv}: {len(diff)} bytes differ, {len(plan)} planned edits, {moved} placements moved: PASS')
