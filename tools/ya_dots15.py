r"""BUILD-15 TASK A (read only on out\fonts_gpt): the ya-dots fix, in a COPY of the prepared TresFont.
Measured cause (owner screenshots, BUILD-14: the two dots under ya missing or faint in subtitles, words "qawiy" / "yaeni" =
the isolated and final ya): Plex draws the dots of U+064A / U+FEF1 / U+FEF2 under the bowl, 102 font units below its
lowest point, so they are the deepest Arabic ink by far ($jimakuNE: 156 units below the glyph origin = 23 px at 38 pt;
the deepest letter body is 113, the game's own deepest glyph 68, Segoe BUILD-13 102). Every other measured property is
sound (same contours, same winding as the body, dot size >= Segoe's). The Subtitle movie bottom-anchors its field
(TextFieldEx.setVerticalAutoSize VAUTOSIZE_BOTTOM), so the ink deepest below the last line is the first to be cut.
Fix: those two Plex dot contours (shape untouched) move by MOVE font units into the bowl (above the bottom stroke,
below the head / connector stroke); every other glyph, every body contour and every advance stay byte-identical.
-> out\builds\BUILD-15\TresFont\TresFont.{uasset,uexp}, out\builds\BUILD-15\ya_debug\ (dots.tsv, *.png)
Usage (from the project root): python -I tools/ya_dots15.py"""
import copy, hashlib, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import font_swap_adapter, shaper, tresfont
from tsvlib import load_translation

PREP = 'out/fonts_gpt/TresFont/TresFont.uasset'
ORIG = 'extracted/assets/KINGDOM HEARTS III/Content/UI/Scaleform/91_font/TresFont.uasset'
OUT = 'out/builds/BUILD-15/TresFont'
DBG = 'out/builds/BUILD-15/ya_debug'
PLEX = 'out/fonts_gpt/fonts/IBMPlexSansArabic-Regular.ttf'
SRC = {1: PLEX, 2: 'C:/Windows/Fonts/segoeui.ttf', 3: PLEX, 4: 'C:/Windows/Fonts/segoeuib.ttf'}
NAME = {1: 'jimakuNE', 2: 'JimakuJP', 3: 'sougei', 4: 'KH2Menu'}
PT = {1: 38, 2: 40, 3: 23, 4: 30}  # size used for the px numbers (Subtitle 38 pt, help/menu 23 pt; 2 and 4 info only)
YA = (0x064A, 0xFEF1, 0xFEF2)  # isolated (two code points) and final ya: the only forms with dots under the bowl
# (dx, up) in font units: dots -440..-342 -> -95..+3, i.e. inside the bowl (its bottom stroke's top edge ~ -149); the
# final form's connector (bottom ~ +25 from x ~ 415) sits above the right dot, so there the pair also moves left
MOVE = {0x064A: (0, 345), 0xFEF1: (0, 345), 0xFEF2: (-54, 350)}
TOL_PX = 1.5  # a dot may reach at most this far below the deepest letter body of its class
# letters with dots (the prompt's list + ya / alef maqsura), every form present among the 189 code points
DOTTED = {0x628, 0x62A, 0x62B, 0x646, 0x62C, 0x62E, 0x634, 0x642, 0x641, 0x638, 0x63A, 0x636, 0x632, 0x630, 0x629,
          0x64A, 0x649}
sha = lambda d: hashlib.sha256(d).hexdigest()


def flat(x, y, edges, steps=12):
    pts = [(x, y)]
    for t, v in edges:
        if t < 2: x += v[0]
        elif t < 4: y += v[0]
        elif t < 8: x, y = x + v[0], y + v[1]
        else:
            cx, cy = x + v[0], y + v[1]
            ex, ey = cx + v[2], cy + v[3]
            pts += [((1-s)**2*x + 2*(1-s)*s*cx + s*s*ex, (1-s)**2*y + 2*(1-s)*s*cy + s*s*ey)
                    for s in (i / steps for i in range(1, steps + 1))]
            x, y = ex, ey
            continue
        pts.append((x, y))
    return pts


def area(ps):
    return sum(a[0]*b[1] - b[0]*a[1] for a, b in zip(ps, ps[1:] + ps[:1])) / 2


_TTF = {}


def ttf_areas(path, cp):
    f = _TTF[path] = _TTF.get(path) or TTFont(path)
    gs = f.getGlyphSet()
    rec = DecomposingRecordingPen(gs)
    gs[f.getBestCmap()[cp]].draw(rec)
    out = []
    for op, args in rec.value:
        if op == 'moveTo': out.append([args[0]])
        elif op in ('lineTo', 'qCurveTo'): out[-1].extend(args)
    return [area(ps) for ps in out]


def marks(shape):
    """indices of the dot / mark contours: everything except the largest contour and holes (opposite winding)"""
    a = [area(flat(*c)) for c in shape[1]]
    big = max(range(len(a)), key=lambda i: abs(a[i]))
    return [i for i in range(len(a)) if i != big and a[i] * a[big] > 0 and abs(a[i]) < 0.2 * abs(a[big])]


def bbox(ps):
    xs, ys = [p[0] for p in ps], [p[1] for p in ps]
    return min(xs), min(ys), max(xs), max(ys)


def mindist(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1)).min())


def lifted(shape, k, cp):
    """the same shape with its mark contours moved by MOVE[cp] font units (rounded to compacted units, y down)"""
    dx, dy = (round(v * k) for v in MOVE[cp])
    m = marks(shape)
    cs = [(x + dx, y - dy, e) if i in m else (x, y, e) for i, (x, y, e) in enumerate(shape[1])]
    pts = [p for c in cs for p in flat(*c, steps=1)]
    xs, ys = [round(p[0]) for p in pts], [round(p[1]) for p in pts]
    return [min(xs), min(ys), max(xs), max(ys)], cs


def fix(fonts, k):
    """move the ya dots in the Plex classes ($jimakuNE 1, $sougei 3); returns {(class, cp): (old, new)}"""
    done = {}
    for fid in (1, 3):
        f = fonts[fid]
        for c, adv, s in f['glyphs']:
            if c in YA:
                old = f['shapes'][s]
                f['shapes'][s] = new = lifted(old, k[fid], c)
                done[(fid, c)] = (old, new)
    return done


def glyphs(f):
    return {c: (a, f['shapes'][s]) for c, a, s in f['glyphs']}


def render(gl, text, pt, guides=(), ss=6, pad=10):
    """own rasterizer of the compacted quadratics (non-zero winding, 6x supersampled); text = logical Arabic"""
    vis, scale = shaper.shape(text), pt / 256
    width = pad * 2 + math.ceil(sum(gl[ord(ch)][0] for ch in vis) * scale)
    top, bottom = 290 * scale, 200 * scale
    height = math.ceil(top + bottom + pad * 2)
    base = pad + top
    acc = np.zeros((height * ss, width * ss), np.int16)
    pen = pad
    for ch in vis:
        adv, shape = gl[ord(ch)]
        for x, y, e in shape[1]:
            ps = flat(x, y, e)
            a = area(ps)
            if len(ps) < 3 or not a:
                continue
            layer = Image.new('1', (width * ss, height * ss))
            ImageDraw.Draw(layer).polygon([((pen + px * scale) * ss, (base + py * scale) * ss) for px, py in ps], fill=1)
            acc += (1 if a > 0 else -1) * np.asarray(layer, np.int16)
        pen += adv * scale
    ink = Image.fromarray(np.uint8(acc != 0) * 255).resize((width, height), Image.Resampling.BOX)
    img = Image.new('RGB', (width, height), '#10151f')
    d = ImageDraw.Draw(img)
    for y, col in guides:
        d.line([(0, base + y * scale), (width, base + y * scale)], fill=col)
    img.paste('#f4f6fa', (0, 0), ink)
    return img


def sheet(path, before, after, k, lines):
    """before / after sheet: per class rows of samples, guide lines = glyph origin, class descent, deepest body"""
    label = ImageFont.truetype(SRC[2], 16)
    rows = []
    for fid, pt, text, env in lines:
        g = [(0, '#3a6ea5'), (before[fid]['descent'], '#7a7a7a'), (env, '#b5651d')]
        rows.append((f'${NAME[fid]} {pt} pt', render(glyphs(before[fid]), text, pt, g), render(glyphs(after[fid]), text, pt, g)))
    w = 40 + max(a.width for _, a, _ in rows) + max(b.width for _, _, b in rows) + 40
    h = 40 + sum(max(a.height, b.height) + 28 for _, a, b in rows)
    img = Image.new('RGB', (w, h), '#0b0f16')
    d = ImageDraw.Draw(img)
    d.text((10, 8), 'left: BUILD-14 (out/fonts_gpt)   right: BUILD-15 (ya dots lifted)   lines: blue origin, grey descent, '
           'orange deepest letter body', font=label, fill='#cfd8e3')
    y, colb = 40, 20 + max(a.width for _, a, _ in rows) + 20
    for name, a, b in rows:
        d.text((10, y), name, font=label, fill='#9eb4d1')
        img.paste(a, (10, y + 20))
        img.paste(b, (colb, y + 20))
        y += max(a.height, b.height) + 28
    img.save(path)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(DBG, exist_ok=True)
    for n in ('TresFont.uasset', 'TresFont.uexp'):
        assert sha(open(PREP[:-7] + n[8:], 'rb').read()) == font_swap_adapter.PINNED[n], n
    k = {font_swap_adapter.IDS[c['class']]: c['K'] for c in font_swap_adapter.analysis()['classes']}
    a, m, tags = tresfont.load(PREP)
    before = {f['id']: copy.deepcopy(f) for f in tags.values()}
    fonts = {f['id']: f for f in tags.values()}
    changed = fix(fonts, k)
    ua, ue = tresfont.save(a, m, tags)
    for n, data in (('TresFont.uasset', ua), ('TresFont.uexp', ue)):
        open(os.path.join(OUT, n), 'wb').write(data)
        print(f'{OUT}/{n}: {len(data)} B sha256 {sha(data)}')
    # ---- verify the saved copy, re-parsed
    _, m2, t2 = tresfont.load(os.path.join(OUT, 'TresFont.uasset'))
    after = {f['id']: f for f in t2.values()}
    _, m0, t0 = tresfont.load(ORIG)
    orig = {f['id']: f for f in t0.values()}
    assert [t for t in m2['tags'] if t[0] != 1005] == [t for t in m0['tags'] if t[0] != 1005], 'non-font tags'
    for fid, f in after.items():
        o, b, n = glyphs(orig[fid]), glyphs(before[fid]), glyphs(f)
        assert all(n[c] == v for c, v in o.items()), f'{fid}: original game glyph changed'
        assert len(set(n) - set(o)) == 189 and set(n) == set(b), fid
        assert all(f[x] == orig[fid][x] for x in ('id', 'name', 'flags', 'nominal', 'ascent', 'descent', 'leading', 'kerning'))
        for c in b:
            if (fid, c) in changed:
                assert n[c][0] == b[c][0], 'advance'
                mk = marks(b[c][1])
                assert [cc for i, cc in enumerate(n[c][1][1]) if i not in mk] == \
                       [cc for i, cc in enumerate(b[c][1][1]) if i not in mk], 'body contour changed'
            else:
                assert n[c] == b[c], f'{fid} U+{c:04X} changed'
    print(f'original glyphs unchanged in all 4 classes, 189 Arabic code points per class, changed only '
          f'{sorted((NAME[f], f"U+{c:04X}") for f, c in changed)} (dot contours only, advances and bodies identical)')
    # ---- dot check, every dotted form of every class: source TTF vs BUILD-14 vs BUILD-15
    rows, fail, envs = [], [], {}
    for fid in (1, 2, 3, 4):
        ar = sorted(set(glyphs(after[fid])) - set(glyphs(orig[fid])))
        px = PT[fid] / 256
        for state, fs in (('BUILD-14', before), ('BUILD-15', after)):
            g = glyphs(fs[fid])
            env = envs[fid] = max(bbox(flat(*g[c][1][1][i]))[3] for c in ar for i in range(len(g[c][1][1]))
                                  if i not in marks(g[c][1]))  # deepest letter body (bodies identical in both)
            for c in ar:
                if not set(map(ord, shaper.BASE.get(chr(c), chr(c)))) & DOTTED:
                    continue
                shape = g[c][1]
                src = ttf_areas(SRC[fid], c)
                cs = [flat(*cc) for cc in shape[1]]
                wind = len(src) == len(cs) and all((s < 0) == (area(p) > 0) for s, p in zip(src, cs))
                mk = marks(shape)
                body = [p for i, ps in enumerate(cs) if i not in mk for p in ps]
                for i in mk:
                    bx = bbox(cs[i])
                    others = [p for j, ps in enumerate(cs) if j in mk and j != i for p in ps]
                    gap_b, gap_d = mindist(cs[i], body), (mindist(cs[i], others) if others else float('nan'))
                    deep = bx[3] - env
                    ok = wind and deep <= TOL_PX / px
                    rows.append((state, NAME[fid], f'U+{c:04X}', len(src), len(cs), 'same' if wind else 'DIFF', i,
                                 f'{bx[0]:.0f},{bx[1]:.0f},{bx[2]:.0f},{bx[3]:.0f}', f'{bx[3] * px:.1f}',
                                 f'{(bx[2] - bx[0]) * px:.1f}x{(bx[3] - bx[1]) * px:.1f}', f'{gap_b * px:.2f}',
                                 f'{gap_d * px:.2f}', f'{env:.0f}', f'{deep * px:+.1f}', 'PASS' if ok else 'FAIL'))
                    if state == 'BUILD-15' and not ok:
                        fail.append(rows[-1])
    with open(os.path.join(DBG, 'dots.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('font\tclass\tcp\tttf_contours\tgfx_contours\twinding_vs_ttf\tmark_contour\tbbox_units\t'
                'bottom_px_below_origin\tsize_px\tgap_to_body_px\tgap_to_other_mark_px\tdeepest_body_units\t'
                'below_deepest_body_px\tcheck\n')
        f.writelines('\t'.join(map(str, r)) + '\n' for r in rows)
    for st in ('BUILD-14', 'BUILD-15'):
        rs = [r for r in rows if r[0] == st]
        print(f'dot check {st}: {len(rs)} mark contours in {len({(r[1], r[2]) for r in rs})} dotted forms, '
              f'FAIL {sum(r[-1] == "FAIL" for r in rs)}: {sorted({(r[1], r[2]) for r in rs if r[-1] == "FAIL"})}')
    assert not fail, fail[:5]
    # a moved dot must stay at least as far from the body as the tightest unmoved Plex dot of its class
    for fid in (1, 3):
        gaps = lambda moved: [float(r[10]) for r in rows if r[0] == 'BUILD-15' and r[1] == NAME[fid]
                              and (int(r[2][2:], 16) in YA) == moved]
        print(f'${NAME[fid]} at {PT[fid]} pt: moved ya dots >= {min(gaps(True)):.2f} px from the body; '
              f'tightest unmoved Plex dot {min(gaps(False)):.2f} px')
        fail += [NAME[fid]] if min(gaps(True)) < min(gaps(False)) else []
    # ---- renders: ya isolated / final / initial / medial ("qawiy", "yaeni", "yawm bayt fi qawiy") + two subtitle rows
    tr = {r['id']: r for r in load_translation()}
    line = lambda i: tr[i]['AR'].split('<br>')
    samples = ['\u0642\u0648\u064a', '\u064a\u0639\u0646\u064a', '\u064a\u0648\u0645 \u0628\u064a\u062a \u0641\u064a \u0642\u0648\u064a']
    lines = [(1, 38, t, envs[1]) for t in samples + line('00811')[:1] + line('00846')[:1]]
    lines += [(3, 23, t, envs[3]) for t in samples] + [(3, 26, t, envs[3]) for t in samples[2:]] + [(1, 21, samples[2], envs[1])]
    sheet(os.path.join(DBG, 'before_after.png'), before, after, k, lines)
    zoom = [(fid, 150, '\u064a \u0641\u064a \u0642\u0648\u064a \u0628\u064a\u062a', envs[fid]) for fid in (1, 3)]
    sheet(os.path.join(DBG, 'zoom_ya.png'), before, after, k, zoom)
    print(f'renders: {DBG}/before_after.png, {DBG}/zoom_ya.png; table {DBG}/dots.tsv')
    assert not fail, f'moved dots closer to the body than any Plex dot: {fail}'


if __name__ == '__main__':
    main()
