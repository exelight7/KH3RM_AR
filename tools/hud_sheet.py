r"""HUD-SCALE contact sheet: a SIMULATION of the battle HUD (not a game screenshot), drawn from the movie's own
bitmap-fill shapes and textures on the 1920x1080 stage at the final HUD position (frame-0 display lists; colour
transforms, masks and ActionScript visibility ignored; one gauge-word state per row: Focus | Max + plate | Charge).
before = BUILD-16 movie + IMAGES-MASS7 texture, after = BUILD-17 movie + IMAGES-MASS8 texture.
-> out/builds/BUILD-17/ref/HUD_<movie>_1x.png and _2x.png (2x = nearest of the 1x render)
HUD-PLEX: with an output dir, both sides use the BUILD-17 movie (texture against texture, e.g. IMAGES-MASS8 | -MASS9).
HUD-SOFTEN: 'soften' = the edge variants (hard:<k>, aa, ramp) of each gauge word's recipe, measured as 'trial' plus a
jaggedness metric (jag, steps) -> <out>/soften.tsv; 'crisp' and 'soften' also print jag / steps.
HUD-CRISP: 'crisp' = the in-game look of each gauge word (BC7 decode, bilinear x movie scale, on the bar / dark) and its
metrics for English and each build -> <out>/look.tsv + LOOK_<texture>_1x/2x.png; 'trial' = every candidate effect of
every gauge word rendered, encoded and measured the same way -> <out>/trial.tsv.
Usage: python -I tools\hud_sheet.py [before images dir after images dir [out dir]] (default IMAGES-MASS7 IMAGES-MASS8)
       python -I tools\hud_sheet.py crisp <out dir> <build dir>...
       python -I tools\hud_sheet.py trial <out dir> [word...]
       python -I tools\hud_sheet.py soften <out dir> [word...]"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
import texture_codec as tc
from build_build3 import tag_offsets
from gfx_fonts import movie
from gfx_layout import Bits
from gfx_edittext import cstr
import build_build17 as b17
import hud_scale

HS = 'KINGDOM HEARTS III/Content/UI/Scaleform/01_hud/hud_status/'
CROP = (1640, 770, 1920, 1050)  # stage px x0, y0, x1, y1
STATES = {'Focus': ('LogoC', 'MaxAnm', 'MaxEff'), 'Max': ('pcExLogo/', 'LogoC', 'MaxEff', 'MaxAnm/pcExLogo'),
          'Charge': ('pcExLogo/', 'MaxAnm', 'MaxEff')}   # path parts hidden in each row
HIDE = ('Eff', 'GgR', 'GgC', 'DodaiAnm/', 'stateIcon', 'LogoC1', 'Logo1', 'pcMpGgC')


def fmatrix(r):
    a = d = 1.0
    b = c = 0.0
    if r.u(1):
        n = r.u(5)
        a, d = r.s(n) / 65536, r.s(n) / 65536
    if r.u(1):
        n = r.u(5)
        b, c = r.s(n) / 65536, r.s(n) / 65536
    n = r.u(5)
    return np.array([[a, c, r.s(n) / 20], [b, d, r.s(n) / 20], [0, 0, 1]])


def shape(code, t):
    """-> (bitmap id, fill matrix texel -> shape px, outline segments in shape px) for a one-bitmap-fill shape"""
    r = Bits(t, 2)
    n = r.u(5)
    [r.s(n) for _ in range(4)]
    p = (r.b + 7) // 8
    if code == 83:
        r = Bits(t, p)
        n = r.u(5)
        [r.s(n) for _ in range(4)]
        p = (r.b + 7) // 8 + 1
    fills = []

    def styles(p):
        n = t[p]
        p += 1
        if n == 0xFF:
            n, p = struct.unpack_from('<H', t, p)[0], p + 2
        for _ in range(n):
            ft = t[p]
            p += 1
            if ft == 0:
                p += 4 if code in (32, 83) else 3
                fills.append(None)
            elif ft in (0x10, 0x12, 0x13):
                r = Bits(t, p)
                fmatrix(r)
                p = (r.b + 7) // 8
                p += 1 + (t[p] & 15) * (5 if code in (32, 83) else 4) + (2 if ft == 0x13 else 0)
                fills.append(None)
            else:
                bid = struct.unpack_from('<H', t, p)[0]
                r = Bits(t, p + 2)
                m = fmatrix(r)
                m[:2, :2] /= 20
                fills.append((bid, m))
                p = (r.b + 7) // 8
        n = t[p]
        p += 1
        if n == 0xFF:
            n, p = struct.unpack_from('<H', t, p)[0], p + 2
        assert code != 83 or n == 0
        return p + n * (2 + (4 if code == 32 else 3))
    p = styles(p)
    r = Bits(t, p)
    fb, lb = r.u(4), r.u(4)
    x = y = 0
    f0 = f1 = 0
    segs = []
    while True:
        if not r.u(1):
            fl = r.u(5)
            if fl == 0:
                break
            if fl & 1:
                m = r.u(5)
                x, y = r.s(m), r.s(m)
            if fl & 2:
                f0 = r.u(fb)
            if fl & 4:
                f1 = r.u(fb)
            if fl & 8:
                r.u(lb)
            if fl & 16:
                p = styles((r.b + 7) // 8)
                r = Bits(t, p)
                fb, lb = r.u(4), r.u(4)
        elif r.u(1):
            nb = r.u(4) + 2
            if r.u(1):
                dx, dy = r.s(nb), r.s(nb)
            elif r.u(1):
                dx, dy = 0, r.s(nb)
            else:
                dx, dy = r.s(nb), 0
            segs.append(((x, y), (x + dx, y + dy), f0, f1))
            x, y = x + dx, y + dy
        else:
            nb = r.u(4) + 2
            cx, cy, ax, ay = (r.s(nb) for _ in range(4))
            s0, c, e = (x, y), (x + cx, y + cy), (x + cx + ax, y + cy + ay)
            prev = s0
            for i in range(1, 9):
                u = i / 8
                q = tuple((1 - u) ** 2 * s0[k] + 2 * (1 - u) * u * c[k] + u * u * e[k] for k in (0, 1))
                segs.append((prev, q, f0, f1))
                prev = q
            x, y = e
    bm = [f for f in fills if f]
    return (bm[0] if len(bm) == 1 and len(fills) == 1 else None), [((a[0] / 20, a[1] / 20), (b[0] / 20, b[1] / 20), f0, f1) for a, b, f0, f1 in segs]


def parse(d):
    """-> shapes {id: (fill, segs)}, sprites {id: [placement events]}, root placements"""
    body = movie(d)[4]
    shapes, sprites, root = {}, {}, []

    def place(code, t, fr):
        f = t[0]
        depth = struct.unpack_from('<H', t, 1 if code == 26 else 2)[0]
        p = 3 if code == 26 else 4
        if code == 70 and t[1] & 0x08:
            p = cstr(t, p)[1]
        ch = None
        if f & 2:
            ch, p = struct.unpack_from('<H', t, p)[0], p + 2
        m = None
        if f & 4:
            r = Bits(t, p)
            m = fmatrix(r)
        return dict(fr=fr, depth=depth, char=ch, m=m, move=bool(f & 1))
    fr = 0
    for code, p, n in tag_offsets(body):
        t = body[p:p + n]
        if code in (2, 22, 32, 83):
            try:
                shapes[struct.unpack_from('<H', t)[0]] = shape(code, t)
            except (AssertionError, IndexError):
                pass
        elif code == 39:
            ev, f2, q = [], 0, 4
            while q < len(t):
                h = struct.unpack_from('<H', t, q)[0]
                q += 2
                c, ln = h >> 6, h & 0x3F
                if ln == 0x3F:
                    ln, q = struct.unpack_from('<I', t, q)[0], q + 4
                if c == 1:
                    f2 += 1
                elif c in (26, 70):
                    ev.append(place(c, t[q:q + ln], f2))
                elif c == 0:
                    break
                q += ln
            sprites[struct.unpack_from('<H', t)[0]] = ev
        elif code in (26, 70):
            root.append(place(code, t, fr))
        elif code == 1:
            fr += 1
    return shapes, sprites, root


def names(d):
    """instance names by (sprite, depth) from hud_scale.placements (frame-0 placements with a matrix)"""
    return {(sid, depth): name for sid, fr, depth, ch, name, q, m in hud_scale.placements(d)[0] if name}


def leaves(d, frames={167: 8}):
    shapes, sprites, root = parse(d)
    nm = names(d)
    out = []

    def walk(sid, M, path):
        dl = {}
        for o in sprites[sid]:
            if o['fr'] > frames.get(sid, 0):
                continue
            if o['char'] is not None and not o['move']:
                dl[o['depth']] = [o['char'], o['m'] if o['m'] is not None else np.eye(3)]
            elif o['depth'] in dl and o['m'] is not None:
                dl[o['depth']][1] = o['m']
        for depth, (ch, m) in sorted(dl.items()):
            p = path + '/' + (nm.get((sid, depth)) or f'd{depth}#{ch}')
            if ch in sprites:
                walk(ch, M @ m, p)
            elif ch in shapes and shapes[ch][0]:
                out.append((p, M @ m, shapes[ch]))
    for r in root:
        if r['fr'] == 0 and r['char'] in sprites:
            walk(r['char'], r['m'], {49: 'sttsNpc', 54: 'sttsSnpc', 167: 'sttsPc'}[r['char']])
    return out


def coverage(segs, M, h, w, ss=4):
    acc = np.zeros((h * ss, w * ss + 1), np.int32)
    ys = (np.arange(h * ss) + 0.5) / ss
    for a, b, f0, f1 in segs:
        if f0 == f1:
            continue
        x0, y0 = (M @ [a[0], a[1], 1])[:2]
        x1, y1 = (M @ [b[0], b[1], 1])[:2]
        if y0 == y1:
            continue
        sel = np.where((ys >= min(y0, y1)) & (ys < max(y0, y1)))[0]
        xc = x0 + (ys[sel] - y0) * (x1 - x0) / (y1 - y0)
        np.add.at(acc, (sel, np.clip(np.ceil(xc * ss - 0.5), 0, w * ss).astype(int)), 1)
    return (np.cumsum(acc, axis=1)[:, :w * ss] % 2).astype(np.float32).reshape(h, ss, w, ss).mean((1, 3))


def render(d, tex, hide):
    x0, y0, x1, y1 = CROP
    h, w = y1 - y0, x1 - x0
    c = np.zeros((h, w, 3), np.float32)
    c[:] = (0.28, 0.33, 0.30)  # neutral backdrop (our own colour, no game pixels)
    T = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]])
    for p, M, ((bid, F), segs) in leaves(d):
        if any(k in p for k in HIDE + hide) or bid not in tex:
            continue
        img = cv2.warpAffine(tex[bid], (T @ M @ F)[:2], (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
        a = img[..., 3:4] * coverage(segs, T @ M, h, w)[..., None]
        c = c * (1 - a) + img[..., :3] * a
    return c


# ---- HUD-CRISP: the in-game look of one gauge word -------------------------------------------------------------
# cell box in HudStatusTxt(CA), movie scale and the sub-pixel stage offset of the cell's top-left corner (BUILD-17
# HUD_SHAPES: Focus x 1714.40, Max y 875.25, Charge x 1714.80); Air is not drawn by the HUD movies (1:1)
CELLS = {'Focus': ((0, 0, 59, 20), 1.45, (0.40, 0)), 'Max': ((0, 24, 48, 44), 1.25, (0, 0.25)),
         'Charge': ((0, 106, 71, 127), 1.20, (0.80, 0)), 'Air': ((99, 24, 140, 46), 1.0, (0, 0))}
BACKS = {'bar': (255, 220, 0), 'dark': (16, 16, 16)}   # yellow Focus bar (sampled from HudStatus01), Max plate / dark
LUM = np.array([0.299, 0.587, 0.114], np.float32)


def magnify(tex, word):
    """texture mip 0 (h, w, 4) uint8 as the game shows it -> straight RGBA float 0..1 in stage px: the shape rectangle
    of the cell drawn at the movie scale, bilinear from the whole texture (neighbour texels included, as the GPU
    samples), alpha times the rectangle's pixel coverage; 1 px of empty stage around"""
    (x0, y0, x1, y1), s, (fx, fy) = CELLS[word]
    a, b = 1 + fx, 1 + fy                                  # rectangle corner in output px
    w, h = int(np.ceil(a + s * (x1 - x0))) + 1, int(np.ceil(b + s * (y1 - y0))) + 1
    M = np.float32([[s, 0, s * (0.5 - x0) + a - 0.5], [0, s, s * (0.5 - y0) + b - 0.5]])
    out = cv2.warpAffine(tex.astype(np.float32) / 255, M, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
    cov = lambda n, lo, hi: np.clip(np.minimum(np.arange(n) + 1, hi) - np.maximum(np.arange(n), lo), 0, 1)
    out[..., 3] *= np.outer(cov(h, b, b + s * (y1 - y0)), cov(w, a, a + s * (x1 - x0)))
    return out


def composite(m, back):
    return m[..., :3] * 255 * m[..., 3:] + np.float32(BACKS[back]) * (1 - m[..., 3:])


def metrics(m, back):
    """magnified word on a backdrop -> (edge = p90 luminance gradient (forward differences, 0..360), stroke contrast =
    p95 - p5 luminance, crisp = share of the inked pixels that are full strength: luminance distance to the backdrop
    d >= 0.6 D against 0.15 D <= d < 0.6 D (grey ramps), D = p99 of d), all over the word area = alpha > 0.1 grown 2 px"""
    L = composite(m, back) @ LUM
    R = cv2.dilate((m[..., 3] > 0.1).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    g = np.hypot(np.diff(L, axis=1)[:-1], np.diff(L, axis=0)[:, :-1])
    d = np.abs(L[R] - np.float32(BACKS[back]) @ LUM)
    D = np.percentile(d, 99)
    solid, ramp = (d >= 0.6 * D).sum(), ((d >= 0.15 * D) & (d < 0.6 * D)).sum()
    return float(np.percentile(g[R[:-1, :-1]], 90)), float(np.percentile(L[R], 95) - np.percentile(L[R], 5)), \
        float(100 * solid / max(solid + ramp, 1))


def jaggedness(m, back, up=16, chord=0.5, sigma=2.0):
    """stair-step noise of the word contour on the magnified look (HUD-SOFTEN). Field = luminance distance to the backdrop
    over D (as in metrics), bicubic-upsampled 16x, iso-contour at 0.5 (silhouette on the bar = outer outline edge, on dark =
    the fill edge). jag = excess turning of the contour: sum |d heading| of the contour resampled every 0.5 px minus the same
    sum after a Gaussian smoothing of the heading over sigma = 2 px, in degrees per 100 px of contour (a smooth curve or
    corner has little excess, a staircase a lot). steps = number of 1-px stair-step corners of the stage-pixel silhouette
    (both neighbouring polygon edges <= 1 px) per 100 px of its perimeter. -> (jag, steps)"""
    L = composite(m, back) @ LUM
    R = cv2.dilate((m[..., 3] > 0.1).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    d = np.abs(L - np.float32(BACKS[back]) @ LUM)
    f = np.clip(d / np.percentile(d[R], 99), 0, 1).astype(np.float32)
    f = np.pad(f, 2)
    big = cv2.resize(f, None, fx=up, fy=up, interpolation=cv2.INTER_CUBIC)
    exc = tot = 0.0
    for c in cv2.findContours((big >= 0.5).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]:
        pt = c[:, 0, :].astype(np.float64) / up
        seg = np.hypot(*np.diff(np.vstack([pt, pt[:1]]), axis=0).T)
        s_ = np.concatenate([[0], np.cumsum(seg)])
        if s_[-1] < 6:                                   # specks and 1-px noise
            continue
        n = int(s_[-1] * up)                             # dense uniform resampling, then a 0.3 px Gaussian on x, y: removes
        t = np.arange(n) * s_[-1] / n                    # the 1/16 px chain-code quantisation (it would swamp the heading)
        xy = np.stack([np.interp(t, s_, np.append(pt[:, k], pt[0, k])) for k in (0, 1)], 1)
        wq = int(0.9 * up)
        kq = np.exp(-0.5 * (np.arange(-wq, wq + 1) / (0.3 * up)) ** 2)
        xy = np.stack([np.convolve(np.concatenate([xy[-wq:, k], xy[:, k], xy[:wq, k]]), kq / kq.sum(), 'valid')[:n] for k in (0, 1)], 1)
        n = int(s_[-1] / chord)
        xy = xy[(np.arange(n) * len(xy) / n).astype(int)]
        v = np.diff(np.vstack([xy, xy[:1]]), axis=0)
        h = np.unwrap(np.arctan2(v[:, 1], v[:, 0]))
        w = int(3 * sigma / chord)
        kern = np.exp(-0.5 * (np.arange(-w, w + 1) * chord / sigma) ** 2)
        hp = np.concatenate([h[-w:] - 2 * np.pi * round((h[-1] - h[0]) / (2 * np.pi)), h, h[:w] + 2 * np.pi * round((h[-1] - h[0]) / (2 * np.pi))])
        hs = np.convolve(hp, kern / kern.sum(), 'valid')[:len(h)]
        exc += np.abs(np.diff(h)).sum() - np.abs(np.diff(hs)).sum()
        tot += s_[-1]
    steps = per = 0
    for c in cv2.findContours((f >= 0.5).astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]:
        q = c[:, 0, :]
        if len(q) < 4:
            continue
        ln = np.abs(q - np.roll(q, 1, 0)).max(1)         # length of the edge arriving at each vertex
        steps += int(((ln <= 1) & (np.roll(ln, -1) <= 1)).sum())
        per += int(ln.sum())
    return float(np.degrees(exc) * 100 / max(tot, 1)), float(100 * steps / max(per, 1))


def bc7_error(src, dec, box):
    """(mean, max) RMS RGBA error per 4x4 block over the blocks touching box: pre-encode pixels against the BC7 decode"""
    x0, y0, x1, y1 = box
    X0, Y0, X1, Y1 = x0 // 4 * 4, y0 // 4 * 4, -(-x1 // 4) * 4, -(-y1 // 4) * 4
    d = (src[Y0:Y1, X0:X1].astype(np.float32) - dec[Y0:Y1, X0:X1]) ** 2
    e = np.sqrt(d.reshape((Y1 - Y0) // 4, 4, (X1 - X0) // 4, 4, 4).mean((1, 3, 4)))
    return float(e.mean()), float(e.max())


def look_sheet(texs, labels, words, path):
    """columns = textures (English | builds ...), rows = words; each cell: raw cell 1x | magnified on the bar | on dark,
    drawn at 1x and again 2x (nearest) -> path_1x.png, path_2x.png"""
    rows = []
    for wd in words:
        box = CELLS[wd][0]
        cols = []
        for t in texs:
            raw = t[box[1]:box[3], box[0]:box[2]].astype(np.float32) / 255
            raw = raw[..., :3] * 255 * raw[..., 3:] + np.float32(BACKS['dark']) * (1 - raw[..., 3:])
            m = magnify(t, wd)
            parts = [raw] + [composite(m, b) for b in BACKS]
            hh = max(p.shape[0] for p in parts)
            parts = [np.pad(p, ((0, hh - p.shape[0]), (0, 3), (0, 0)), constant_values=255) for p in parts]
            cols.append(np.hstack(parts))
        ww = max(c.shape[1] for c in cols)
        rows.append(np.hstack([np.pad(c, ((0, 4), (0, ww - c.shape[1] + 8), (0, 0)), constant_values=255) for c in cols]))
    ww = max(r.shape[1] for r in rows)
    sheet = np.clip(np.vstack([np.pad(r, ((0, 0), (0, ww - r.shape[1]), (0, 0)), constant_values=255) for r in rows]), 0, 255).astype(np.uint8)
    for z in (1, 2):
        im = cv2.resize(sheet, (sheet.shape[1] * z, sheet.shape[0] * z), interpolation=cv2.INTER_NEAREST)[..., ::-1]
        head = np.full((30, max(im.shape[1], 560), 3), 255, np.uint8)
        for i, line in enumerate((f'SIMULATION at {z}x of 1920x1080: BC7 decode, bilinear x movie scale; per column raw | bar | dark',
                                  'columns: ' + ' | '.join(labels) + '; rows: ' + ' / '.join(words))):
            cv2.putText(head, line, (4, 12 + 14 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (0, 0, 0), 1, cv2.LINE_AA)
        im = np.pad(im, ((0, 0), (0, head.shape[1] - im.shape[1]), (0, 0)), constant_values=255)
        cv2.imwrite(f'{path}_{z}x.png', np.vstack([head, im]))


def crisp(builds):
    """table of the magnified metrics: English and each build, Focus / Max / Charge (and Air) in both textures"""
    rows = [['texture', 'word', 'scale', 'source', 'edge_bar', 'edge_dark', 'contrast_bar', 'contrast_dark',
             'crisp_bar_pct', 'crisp_dark_pct', 'edge_vs_english_pct', 'jag', 'steps']]
    for txt in ('HudStatusTxt', 'HudStatusTxtCA'):
        srcs = [('English', 'extracted/assets')] + [(d.rstrip('/').split('/')[-1], os.path.join(d, 'assets')) for d in builds]
        for wd in CELLS:
            eng = None
            for label, d in srcs:
                t = tc.rgba0(tc.load(os.path.join(d, HS + txt + '.uasset')))
                m = magnify(t, wd)
                (eb, cb, kb), (ed, cd, kd) = metrics(m, 'bar'), metrics(m, 'dark')
                eng = eng or (eb + ed) / 2
                rows.append([txt, wd, str(CELLS[wd][1]), label, f'{eb:.1f}', f'{ed:.1f}', f'{cb:.1f}', f'{cd:.1f}',
                             f'{kb:.0f}', f'{kd:.0f}', f'{100 * (eb + ed) / 2 / eng:.0f}', *(f'{v:.1f}' for v in jag_of(t, wd))])
    return rows


def candidates():
    """(effect, pad) per HUD-CRISP family: a heavier stems (face b / sb / plex + stroke), b 2 px outline, c hard edges
    (hard:<k>, solid outline), d unsharp pre-compensation (sharp, soft edges only), e flat fill (no row gradient: the
    hard cell then holds only fill, outline and clear: two colours per 4x4 block plus alpha)"""
    out = []
    for fc in ('b', 'sb', 'plex'):
        for sk in (0, 0.5, 1, 1.5) if fc != 'plex' else (0, 0.5, 1):
            for ol in (1, 2):
                for sn in ('', '+snap'):
                    base = f'outline:{ol}+%s+face:{fc}' + (f'+stroke:{sk}' if sk else '') + sn
                    for sh in ('', '+sharp:0.5:0.8', '+sharp:1:0.6'):
                        out.append(((base % 'grad') + '+halo' + sh, ol))
                    for hk in (2, 4, 99):
                        for g in ('grad', 'flat'):
                            out.append(((base % g).replace('+flat', '') + f'+hard:{hk}', ol))
    return out


def score(e, base):
    """edge (mean of bar and dark) and crisp (mean) against the English cell: 1 + 1 = English"""
    return e[0] / base[0] + e[1] / base[1]


def look_of(dec, wd):
    m = magnify(dec, wd)
    (eb, cb, kb), (ed, cd, kd) = metrics(m, 'bar'), metrics(m, 'dark')
    return (eb + ed) / 2, (kb + kd) / 2, (cb + cd) / 2


def jag_of(dec, wd):
    """(jag, steps) of the magnified word, mean of the bar and the dark backdrop"""
    m = magnify(dec, wd)
    (jb, sb), (jd, sd) = jaggedness(m, 'bar'), jaggedness(m, 'dark')
    return (jb + jd) / 2, (sb + sd) / 2


def softens(eff):
    """HUD-SOFTEN: the edge variants of a recipe ending in +hard:99 (everything else unchanged)"""
    assert eff.endswith('+hard:99'), eff
    b = eff[:-len('+hard:99')]
    out = [b + f'+hard:{k}' for k in (1, 1.25, 1.5, 2, 3, 4, 6, 8, 12)]
    out += [b + f'+aa:{k}' for k in (1.5, 2, 3)]
    out += [b + f'+hard:{k}+ramp:{al}{o}' for k in (99, 6) for al in (0.5,) for o in ('', ':out')]
    out += [b + f'+aa:{k}+ramp:0.5{o}' for k in (2, 3) for o in ('', ':out')]
    return out


def pick(rows, edge_min=110, crisp_min=75):
    """HUD-SOFTEN: per word the candidate (same effect in both textures) that passes every gate in both - readable, joins
    intact, margin, same font px as the previous recipe, edge >= 110 % and crisp >= 75 % of English - with the lowest jag
    (mean over the two textures). -> [(word, effect, {metrics})], all candidates ranked in the .tsv by the caller"""
    by = {}
    for r in rows:
        if r['effect'].startswith(('English', 'MASS')) or r['note'] == 'previous recipe re-rendered':
            continue
        j = r['joins'].split('/')
        ok = (r['readable'] == 'READABLE' and j[0] == j[1] and r['margin_ok'] == 'PASS' and r['text_px_same'] == 'yes'
              and float(r['edge_vs_english_pct']) >= edge_min and float(r['crisp_vs_english_pct']) >= crisp_min)
        by.setdefault((r['word'], r['effect']), []).append((ok, r))
    best = {}
    for (wd, eff), v in by.items():
        if len(v) == 2 and all(o for o, _ in v):
            jag = sum(float(r['jag']) for _, r in v) / 2
            if wd not in best or jag < best[wd][0]:
                best[wd] = (jag, eff, [r for _, r in v])
    return best


def trial(out, txts=('HudStatusTxt', 'HudStatusTxtCA'), only=None, soften=False):
    """every candidate of every gauge word, rendered with tools/texture_text.repaint on the English texture, BC7 encoded
    as the build does (texture_codec.patch), decoded, magnified and measured -> out/trial.tsv, sorted per word"""
    import texture_text as tt, shaper
    tr = {r['id']: r for r in tt.load_translation()}
    strings = tt.load_strings()
    by = tt.rows_by_asset()
    head = ['texture', 'word', 'effect', 'pad', 'font_px', 'readable', 'joins', 'margin_ok', 'edge', 'crisp', 'contrast',
            'edge_vs_english_pct', 'crisp_vs_english_pct', 'score', 'bc7_rms_mean', 'bc7_rms_max', 'note', 'jag', 'steps', 'text_px_same']
    rows = []
    word = {v[0]: k for k, v in CELLS.items()}
    for txt in txts:
        asset = HS + txt + '.uasset'
        t = tc.load(os.path.join('extracted/assets', asset))
        pl = t['platforms'][0]
        m0 = pl['mips'][0]
        raw0 = tc.mip_bytes(t, m0)
        eng = tc.rgba0(t)
        m9 = tc.rgba0(tc.load(os.path.join('out/builds/IMAGES-MASS%d/assets' % (10 if soften else 9), asset)))
        for r in by[asset]:
            wd = word[tuple(map(int, r['box'].split()))]
            if only and wd not in only:
                continue
            base = look_of(eng, wd)
            ar = tt.arabic(r['source'], tr, strings)
            vis = shaper.shape(ar)
            ref9 = look_of(m9, wd)
            jg = jag_of(eng, wd)
            rows.append([txt, wd, 'English cell', '-', '-', '-', '-', '-', f'{base[0]:.1f}', f'{base[1]:.0f}', f'{base[2]:.0f}',
                         '100', '100', '2.000', '-', '-', 'reference', f'{jg[0]:.1f}', f'{jg[1]:.1f}', '-'])
            jg = jag_of(m9, wd)
            rows.append([txt, wd, ('MASS10' if soften else 'MASS9') + ' shipped: ' + r['effect'], r['pad'], '-', '-', '-', '-', f'{ref9[0]:.1f}', f'{ref9[1]:.0f}',
                         f'{ref9[2]:.0f}', f'{100 * ref9[0] / base[0]:.0f}', f'{100 * ref9[1] / base[1]:.0f}',
                         f'{score(ref9, base):.3f}', '-', '-', 'reference', f'{jg[0]:.1f}', f'{jg[1]:.1f}', '-'])
            size0 = None
            for eff, pad in [(r['effect'], int(r['pad']))] + ([(e, 0) for e in softens(r['effect'])] if soften else candidates()):
                pad = int(r['pad']) if soften else pad
                img = eng.astype(np.float32)
                info = tt.repaint(img, dict(r, effect=eff, pad=str(pad)), ar)
                new = np.clip(np.round(img), 0, 255).astype(np.uint8)
                dec = tc.decode(pl['pf'], tc.patch(pl['pf'], raw0, m0['w'], m0['h'], new), m0['w'], m0['h'])
                lk = look_of(dec, wd)
                n, bad = tt.joins(vis, info['size'], tt.style_of(eff))
                e = bc7_error(new, dec, CELLS[wd][0])
                jg = jag_of(dec, wd)
                size0 = size0 or info['size']
                rows.append([txt, wd, eff, str(pad), str(info['size']), 'READABLE' if ' READABLE' in info['read'] else 'UNREADABLE',
                             f'{n - bad}/{n}', 'PASS' if info['margin'] >= min(2, pad) else 'FAIL', f'{lk[0]:.1f}', f'{lk[1]:.0f}',
                             f'{lk[2]:.0f}', f'{100 * lk[0] / base[0]:.0f}', f'{100 * lk[1] / base[1]:.0f}', f'{score(lk, base):.3f}',
                             f'{e[0]:.1f}', f'{e[1]:.1f}', ('previous recipe re-rendered' if eff == r['effect'] else ''),
                             f'{jg[0]:.1f}', f'{jg[1]:.1f}', 'yes' if info['size'] == size0 else 'NO'])
            print(txt, wd, len(rows), flush=True)
    if soften:
        best = pick([dict(zip(head, r)) for r in rows])
        with open(os.path.join(out, 'pick.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\t'.join(['word', 'effect', 'jag_mean'] + [f'{k}_{t}' for t in ('Txt', 'CA') for k in ('edge_pct', 'crisp_pct', 'jag', 'steps')]) + '\n')
            for wd, (jag, eff, rr) in best.items():
                f.write('\t'.join([wd, eff, f'{jag:.1f}'] + [r[k] for r in rr for k in ('edge_vs_english_pct', 'crisp_vs_english_pct', 'jag', 'steps')]) + '\n')
                print('PICK', wd, eff, f'{jag:.1f}')
    with open(os.path.join(out, 'soften.tsv' if soften else 'trial.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in [head] + rows)
    return rows


def main():
    if sys.argv[1:2] == ['trial']:                       # HUD-CRISP: python -I tools\hud_sheet.py trial <out dir> [word...]
        os.makedirs(sys.argv[2], exist_ok=True)
        trial(sys.argv[2], only=sys.argv[3:] or None)
        return
    if sys.argv[1:2] == ['soften']:                      # HUD-SOFTEN: python -I tools\hud_sheet.py soften <out dir> [word...]
        os.makedirs(sys.argv[2], exist_ok=True)
        trial(sys.argv[2], only=sys.argv[3:] or None, soften=True)
        return
    if sys.argv[1:2] == ['crisp']:                       # HUD-CRISP: python -I tools\hud_sheet.py crisp <out dir> <build dir>...
        out, builds = sys.argv[2], sys.argv[3:]
        os.makedirs(out, exist_ok=True)
        rows = crisp(builds)
        with open(os.path.join(out, 'look.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.writelines('\t'.join(r) + '\n' for r in rows)
        for txt in ('HudStatusTxt', 'HudStatusTxtCA'):
            texs = [tc.rgba0(tc.load(os.path.join(d, HS + txt + '.uasset'))) for d in ['extracted/assets'] + [os.path.join(b, 'assets') for b in builds]]
            look_sheet(texs, ['English'] + [b.rstrip('/').split('/')[-1] for b in builds], list(CELLS), os.path.join(out, f'LOOK_{txt}'))
        print('\n'.join('\t'.join(r) for r in rows))
        return
    before, after = sys.argv[1:3] if len(sys.argv) > 2 else ('out/builds/IMAGES-MASS7', 'out/builds/IMAGES-MASS8')
    same = len(sys.argv) > 3                     # HUD-PLEX: one movie (BUILD-17) on both sides
    out = sys.argv[3] if same else os.path.join(b17.b.OUT, 'ref')
    os.makedirs(out, exist_ok=True)
    load = lambda f: tc.rgba0(tc.load(f)).astype(np.float32) / 255
    for mv in b17.HUD:
        name = mv.split('/')[-1]
        old = open(os.path.join('extracted/assets', b17.SF + mv + '.uexp'), 'rb').read()
        new = open(os.path.join(b17.b.OUT, 'pakroot', b17.SF + mv + '.uexp'), 'rb').read()
        old = new if same else old
        txt = HS + ('HudStatusTxtCA' if name.endswith('CA') else 'HudStatusTxt') + '.uasset'
        base = {1: load('extracted/assets/' + HS + 'HudThunder.uasset'), 3: load('extracted/assets/' + HS + 'HudStatus01.uasset'),
                4: load('extracted/assets/' + HS + 'CrossEff01.uasset')}
        tb, ta = ({**base, 2: load(os.path.join(d, 'assets', txt))} for d in (before, after))
        rows = []
        for state, hide in STATES.items():
            a, b = render(old, tb, hide), render(new, ta, hide)
            rows.append(np.hstack([a, np.ones((a.shape[0], 4, 3)), b]))
        sheet = (np.clip(np.vstack([np.vstack([r, np.ones((4, r.shape[1], 3))]) for r in rows]), 0, 1) * 255).astype(np.uint8)
        for z in (1, 2):
            im = cv2.resize(sheet, (sheet.shape[1] * z, sheet.shape[0] * z), interpolation=cv2.INTER_NEAREST)[..., ::-1].copy()
            head = np.full((34 * z, im.shape[1], 3), 255, np.uint8)
            for i, line in enumerate((f'SIMULATION, not a game screenshot: {name} at {z}x of 1920x1080',
                                      f'left BUILD-{17 if same else 16} + {before.split("/")[-1]} | right BUILD-17 + {after.split("/")[-1]}; rows Focus / Max / Charge')):
                cv2.putText(head, line, (4, (14 + 15 * i) * z), cv2.FONT_HERSHEY_SIMPLEX, 0.36 * z, (0, 0, 0), 1, cv2.LINE_AA)
            path = os.path.join(out, f'HUD_{name}_{z}x.png')
            cv2.imwrite(path, np.vstack([head, im]))
            print(path)

if __name__ == '__main__':
    main()
