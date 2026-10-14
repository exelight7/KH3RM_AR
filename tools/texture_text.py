r"""Repaint English text inside a texture with Arabic (FINAL-1 pilot, IMAGES-MASS).

For every row of technical\images_rects.tsv (asset, box x0 y0 x1 y1, Arabic source, fill, align, effect, scale, pad,
rotate, size (blank = fit; =k = same size as row k of the asset; ~g = smallest fit of the rows of group g), erase (blank = the box: the old text's area,
refilled; the Arabic may use the whole box, pixels between the two boxes stay unless the new text covers them), note):
  1. ink   = the original text pixels inside the box (differ from the background estimate) -> position and size
  2. fill  = the box is refilled from its surroundings: clear (transparent textures), vlerp/hlerp (per column/row linear
             gradient between the pixels just outside the box), fit (quadratic surface through the box's own non-text
             pixels: gradients without touching neighbouring lines), flat (median of the ring around the box),
             inpaint (text on a painted plate: only the ink pixels are inpainted from the plate around them),
             heal (screenshot labels: only the thin light strokes found by a top-hat, and their shadow rim, are inpainted;
             heal:dark for dark text, :ctx = also the rows above/below as context),
             holes (a plate with cut-out text: the holes inside each row of the plate get the plate colour)
  3. style = fill colour (and outline/glow/shadow colours) sampled from the original ink: brightest core = fill,
             darkest opaque edge = outline, half-transparent halo = glow, dark offset copy = shadow; effect 'grad' =
             the fill follows the original's vertical colour gradient (row by row); 'knockout' = the text is cut out
             of an opaque plate (alpha holes, as the English on the bx/ts banners)
  4. text  = the Arabic of a translation\ row or of translation\images_strings.tsv (never typed), pre-shaped by
             tools\shaper.py (presentation forms, visual order) and drawn with the Segoe UI outlines
             (C:\Windows\Fonts\segoeui.ttf, the font of the game build) with Pillow's BASIC layout (no second bidi
             pass); text >= 24 px gets a 1 px stroke in the fill colour (weight of the English display faces) and is
             4x supersampled, smaller text is drawn at 1x so FreeType hinting keeps dots and hamza
Sources: row:<id> | img:<id> (images_strings.tsv) | tpl:<id>:<arg>...[#line] (template row, tags dropped, {n} = rows or =digits) | <src>@<i>/<n> = word group i of n of that Arabic (logical order;
         for a phrase split over separate sprite pieces) | blank (empty the box: a piece whose word moved elsewhere).
The edited mip 0 goes back through tools\texture_codec.py (only the changed 4x4 blocks are re-encoded).
Effect extras (OPUS-090): fillc:/linec:/haloc:<hex> set a colour instead of sampling it; blur:<r> = a blurred glow copy.
RELEASE-091 extras: fill 'rowmed' = each row of the box gets its own median (a horizontal bar with specks);
  effect 'plate:<r>:<b>' = the halo colour becomes an opaque plate: the text grown by r px (1 px soft edge) plus the
  bottom b rows of the erased area (alpha profile of the old plate there), so the plate runs on into the bar below;
  'feather:<sides>:<px>' = the new box fades into the old pixels over px at the given sides (l t r b);
  fill 'echo:<dx>:<dy>:<d>:<s>:<gain>' (source blank) = a blurred flash copy of the texture's own artwork at offset
  dx dy (glow = gain * blur(dilate(alpha, d), s), core = blur(alpha, 1)): the copy is changed by the difference of
  the model between the old and the repainted artwork, so pixels whose model did not change stay as they were.
Readability (RELEASE-091): every drawn box is measured at its real size with this renderer: stroke contrast = 75th
  percentile of the coverage of the ink pixels (coverage >= 64), continuity = 8-connected components of the
  coverage >= 128 mask against a 64 px reference rendering (ref - k .. ref, k = letters with 2 or 3 dots that may
  merge into one blob; below 24 px only). Readable = contrast >= 192 and continuity. Textures that are new against
  IMAGES-MASS3 must be readable in every box; the MASS3 textures are byte-identical and only reported.
Usage: python -I tools\texture_text.py                    -> self check
       python -I tools\texture_text.py mass [asset-substr] -> out\builds\IMAGES-MASS4\ assets, checks, ref sheets, pak
       python -I tools\texture_text.py trial               -> technical\images_rects_trial.tsv rendered and measured
                                                              (out\builds\IMAGES-MASS4\trial\, no pak)
       python -I tools\texture_text.py --installed         -> the pak in ~mods = this build (sha)"""
import csv, hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
import shaper
import texture_codec as tc
from tsvlib import load_translation

RECTS = 'technical/images_rects.tsv'
STRINGS = 'translation/images_strings.tsv'
TRIAL = 'technical/images_rects_trial.tsv'
OUT = 'out/builds/IMAGES-MASS4'                         # IMAGES-MASS .. IMAGES-MASS3 stay as built
PREV = 'out/builds/IMAGES-MASS3/checks.tsv'             # textures of the previous build: readability only reported
REWORDED = {'10694'}                                     # rows reworded after IMAGES-MASS3 (DECIDE-19 B, BUILD-9)
PAK = os.path.join(OUT, 'pakchunk98-arabic-images_P.pak')
MODS = r'C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods'
REPAK = os.path.abspath('tools/repak-0.2.3/repak.exe')
FONT = r'C:\Windows\Fonts\segoeui.ttf'
SS = 4                                                   # supersampling
BIG = 24                                                 # px: from here 4x supersampling + 1 px stroke
MARGIN = 2                                               # px between the new text and its box


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---- background ---------------------------------------------------------------------------------------
def fill_bg(img, box, mode):
    """img float32 (h, w, 4); returns the refilled box (y1-y0, x1-x0, 4)"""
    x0, y0, x1, y1 = box
    h, w = y1 - y0, x1 - x0
    if mode == 'clear':
        return np.zeros((h, w, 4), np.float32)
    if mode == 'vlerp':
        a, b = img[y0 - 1, x0:x1], img[y1, x0:x1]
        t = ((np.arange(h) + 1) / (h + 1))[:, None, None]
        return a[None] * (1 - t) + b[None] * t
    if mode == 'hlerp':
        a, b = img[y0:y1, x0 - 1], img[y0:y1, x1]
        t = ((np.arange(w) + 1) / (w + 1))[None, :, None]
        return a[:, None] * (1 - t) + b[:, None] * t
    if mode == 'fit':                                     # quadratic surface through the non-text pixels of the box
        reg = img[y0:y1, x0:x1]
        ring = np.concatenate([reg[0], reg[-1], reg[:, 0], reg[:, -1]])
        ink = np.abs(reg[..., :3] - np.median(ring, 0)[:3]).max(-1) > 40
        ink = np.asarray(Image.fromarray(ink.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0
        yy, xx = np.mgrid[0:h, 0:w]
        xx, yy = xx / max(w - 1, 1), yy / max(h - 1, 1)
        A = np.stack([np.ones_like(xx), xx, yy, xx * xx, yy * yy, xx * yy], -1)
        coef = np.linalg.lstsq(A[~ink], reg[~ink], rcond=None)[0]
        return (A.reshape(-1, 6) @ coef).reshape(h, w, 4).astype(np.float32)
    if mode == 'rowmed':
        return np.broadcast_to(np.median(img[y0:y1, x0:x1], 1)[:, None], (h, w, 4)).copy()
    if mode == 'flat':
        ring = np.concatenate([img[y0 - 1, x0 - 1:x1 + 1], img[y1, x0 - 1:x1 + 1], img[y0:y1, x0 - 1], img[y0:y1, x1]])
        return np.broadcast_to(np.median(ring, 0), (h, w, 4)).copy()
    if mode.startswith('inpaint'):                        # plate: the ink (far from the plate colour) is inpainted
        reg = img[y0:y1, x0:x1]
        ink = plate_ink(reg, mode)
        k = ink.astype(np.uint8) * 255
        u8 = np.clip(np.round(reg), 0, 255).astype(np.uint8)
        rgb = cv2.inpaint(np.ascontiguousarray(u8[..., :3]), k, 4, cv2.INPAINT_TELEA)
        al = cv2.inpaint(np.ascontiguousarray(u8[..., 3]), k, 4, cv2.INPAINT_TELEA)
        return np.dstack([rgb, al]).astype(np.float32)
    if mode == 'holes':                                   # plate with cut-out text: each row is made opaque between
        reg = img[y0:y1, x0:x1].copy()                    # its first and last opaque pixel, in the plate colour
        op = reg[..., 3] > 128
        col = np.median(reg[reg[..., 3] > 250], 0)
        for y in range(h):
            xs = np.nonzero(op[y])[0]
            if len(xs):
                reg[y, xs[0]:xs[-1] + 1] = col
        return reg
    if mode.startswith('heal'):                           # screenshot label: only the thin strokes are healed,
        p, v = 4, 4 if ':ctx' in mode else 0              # 4 px of the picture left and right as context (':ctx' =
        X0, Y0, X1, Y1 = max(0, x0 - p), max(0, y0 - v), min(img.shape[1], x1 + p), min(img.shape[0], y1 + v)  # all round)
        reg = img[Y0:Y1, X0:X1]
        k = np.zeros(reg.shape[:2], np.uint8)
        k[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = heal_ink(img[y0:y1, x0:x1], mode) * 255
        u8 = np.clip(np.round(reg), 0, 255).astype(np.uint8)
        rgb = cv2.inpaint(np.ascontiguousarray(u8[..., :3]), k, 3, cv2.INPAINT_TELEA)
        return np.dstack([rgb, u8[..., 3]]).astype(np.float32)[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0]
    raise ValueError(mode)


def heal_ink(reg, mode='heal'):
    """strokes of light text (top-hat; 'heal:dark' = dark text, black-hat) and their shadow rim, grown by 1 px"""
    g = cv2.cvtColor(np.clip(np.round(reg[..., :3]), 0, 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    ker = np.ones((9, 9), np.uint8)
    th = cv2.morphologyEx(g, cv2.MORPH_BLACKHAT if ':dark' in mode else cv2.MORPH_TOPHAT, ker)
    bh = cv2.morphologyEx(g, cv2.MORPH_TOPHAT if ':dark' in mode else cv2.MORPH_BLACKHAT, ker)
    core = th > 30
    rim = (bh > 20) & (cv2.dilate(core.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0)   # the drop shadow
    return cv2.dilate((core | rim).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0

def plate_ink(reg, mode='inpaint'):
    """text pixels on a plate: colour far from the plate (median of the box border; 'inpaint:<t>' = threshold t,
    default 90), grown by 2 px for the anti-aliased edge"""
    ring = np.concatenate([reg[0], reg[-1], reg[:, 0], reg[:, -1]])
    ink = np.abs(reg[..., :3] - np.median(ring, 0)[:3]).max(-1) > int((mode.split(':') + ['90'])[1])
    return np.asarray(Image.fromarray(ink.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0


def ink_mask(orig, bg, mode):
    if mode == 'clear':                                   # thresholds relative to the box's peak alpha (faint text)
        return orig[..., 3] > 24 * orig[..., 3].max() / 255
    if mode.startswith('heal'):
        return heal_ink(orig, mode) & (np.abs(orig[..., :3] - bg[..., :3]).max(-1) > 24)
    if mode == 'holes':
        return orig[..., 3] < 128
    if mode.startswith('inpaint'):
        return plate_ink(orig, mode) & (np.abs(orig[..., :3] - bg[..., :3]).max(-1) > 24)
    return np.abs(orig[..., :3] - bg[..., :3]).max(-1) > 48


# ---- style --------------------------------------------------------------------------------------------
def hexc(c):
    return '#' + ''.join(f'{int(round(v)):02x}' for v in c[:3])


LUM = np.array([0.299, 0.587, 0.114])


def sample(orig, bg, ink, mode):
    """fill / outline / halo colours from the original text pixels"""
    px = orig[ink]
    lum = px[..., :3] @ LUM
    if mode == 'clear':
        amax = orig[..., 3].max()
        core = px[px[:, 3] > 230 * amax / 255]
        cl = core[..., :3] @ LUM
        fill = np.median(core[cl >= np.percentile(cl, 70)], 0)
        edge = np.median(core[cl <= np.percentile(cl, 15)], 0)
        soft = orig[(orig[..., 3] > 8 * amax / 255) & (orig[..., 3] < 160 * amax / 255)]
        halo = np.median(soft, 0) if len(soft) > 30 else None
        return dict(fill=fill, outline=edge, halo=halo)
    if mode.startswith('heal') and ':dark' not in mode:   # light strokes: the brightest third is the fill
        return dict(fill=np.median(px[lum >= np.percentile(lum, 70)], 0),
                    outline=np.median(px[lum <= np.percentile(lum, 10)], 0), halo=None)
    d = np.abs(px[..., :3] - bg[ink][..., :3]).max(-1)
    fill = np.median(px[d >= np.percentile(d, 70)], 0)
    dark = px[lum <= np.percentile(lum, 10)]
    return dict(fill=fill, outline=np.median(dark, 0), halo=None)


def row_gradient(orig, ink, ib):
    """fill colour per row of the old ink (median of the brighter opaque half of each row), gaps interpolated"""
    cols = []
    for y in range(ib[1], ib[3]):
        p = orig[y][ink[y] & (orig[y, :, 3] > 200 * orig[..., 3].max() / 255)]
        if len(p) >= 3:
            l = p[:, :3] @ LUM
            cols.append(np.median(p[l >= np.median(l)][:, :3], 0))
        else:
            cols.append(None)
    ok = [i for i, c in enumerate(cols) if c is not None]
    g = np.array([np.array([np.interp(i, ok, [cols[j][ch] for j in ok]) for ch in range(3)]) for i in range(len(cols))])
    return g


# ---- text ---------------------------------------------------------------------------------------------
def load_strings():
    if not os.path.exists(STRINGS):
        return {}
    with open(STRINGS, encoding='utf-8') as f:
        return {r['id']: r for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)}


def arabic(src, rows, strings):
    """'row:<id>' / 'img:<id>' [@i/n] -> Arabic; tags not allowed in image labels"""
    src, part = (src.split('@') + [''])[:2]
    kind, val = src.split(':', 1)
    if kind == 'tpl':                                    # tpl:<row>:<arg>...[#k] = a template row, {n} = arg rows
        val, line = (val.split('#') + [''])[:2]           # (=<digits> = the number shown), #k = its k-th <br> line
        t, *args = val.split(':')
        ar = rows[t]['AR'] or rows[t]['EN']               # rows like '{0} / {1}' keep their (letter-free) EN
        assert rows[t]['AR'] or not re.search('[A-Za-z]', re.sub(r'<[^<>]*>|\{\d\}', '', ar)), t
        if line:
            ar = ar.split('<br>')[int(line)]
        ar = re.sub(r'<[^<>]*>', '', ar)
        for n, v in enumerate(args):
            assert not v.startswith('=') or v[1:].isdigit(), v
            ar = ar.replace('{%d}' % n, v[1:] if v.startswith('=') else rows[v]['AR'])
        ar = ar.strip()
    else:
        ar = {'row': rows, 'img': strings}[kind][val]['AR']
    assert ar and not re.search(r'<[^>]+>|\{\d', ar), (val, ar)
    if part:
        i, n = map(int, part.split('/'))
        w = ar.split(' ')
        k = -(-len(w) // n)
        ar = ' '.join(w[i * k:(i + 1) * k])
        assert ar, (src, part)
    return ar


def ss(px):
    return 1 if px < BIG else SS


def mask(visual, px, stroke=True):
    k = ss(px)
    sw = k if px >= BIG and stroke else 0                # 1 px stroke (at 1x) for large text
    font = ImageFont.truetype(FONT, px * k, layout_engine=ImageFont.Layout.BASIC)
    l, t, r, b = font.getbbox(visual, stroke_width=sw)
    m = Image.new('L', (r - l + 8 * k, b - t + 8 * k), 0)
    ImageDraw.Draw(m).text((4 * k - l, 4 * k - t), visual, font=font, fill=255, stroke_width=sw, stroke_fill=255)
    return m


def render(visual, size):
    m = mask(visual, size)
    m = m.resize((m.width // ss(size), m.height // ss(size)), Image.LANCZOS)
    return m, m.getbbox()


def fit(visual, w, h):
    """largest pixel size whose ink fits w x h -> (size, L mask at 1x, ink bbox in the mask)"""
    lo, hi = 4, 400
    while lo < hi:
        mid = (lo + hi + 1) // 2
        bb = render(visual, mid)[1]                       # measured at 1x (after the downscale)
        if bb[2] - bb[0] <= w and bb[3] - bb[1] <= h:
            lo = mid
        else:
            hi = mid - 1
    return (lo,) + render(visual, lo)


DOTS23 = set(map(chr, (0x062A, 0x062B, 0x0629, 0x0642, 0x064A, 0x0634)))   # ta tha ta-marbuta qaf ya shin
READ_CONTRAST = 192


def components(m):
    return cv2.connectedComponents((np.asarray(m) >= 128).astype(np.uint8), connectivity=8)[0] - 1


def legibility(ar, visual, size):
    """(stroke contrast, components, reference components, k, readable) of the text at its real size"""
    a = np.asarray(render(visual, size)[0]).astype(int)
    contrast = int(np.percentile(a[a >= 64], 75)) if (a >= 64).any() else 0
    font = ImageFont.truetype(FONT, 64, layout_engine=ImageFont.Layout.BASIC)
    l, t, r, b = font.getbbox(visual)
    ref = Image.new('L', (r - l + 16, b - t + 16), 0)
    ImageDraw.Draw(ref).text((8 - l, 8 - t), visual, font=font, fill=255)
    n, nref, k = components(a.astype(np.uint8)), components(ref), sum(c in DOTS23 for c in ar)
    ok = contrast >= READ_CONTRAST and (size >= BIG or nref - k <= n <= nref)
    return contrast, n, nref, k, ok


def effect_layers(m, eff, st, fillrgb):
    """[(alpha mask, rgb)] bottom to top; eff like 'shadow:2:3:4', 'outline:1', 'glow:5', 'grad', joined by '+'"""
    out = []
    for e in [x for x in eff.split('+') if x.split(':')[0] in ('glow', 'shadow', 'outline')]:   # other tokens: see repaint
        k, *a = e.split(':')
        a = [float(v) for v in a]
        if k == 'glow' and st['halo'] is not None:
            g = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(a[0]))
            out.append((np.asarray(g, np.float32) / 255 * min(1, st['halo'][3] / 255 * 2.2), st['halo'][:3]))
        elif k == 'shadow':
            dx, dy, blur = a
            s = Image.new('L', m.size, 0)
            s.paste(m, (int(dx), int(dy)))
            s = s.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(blur))
            col, k_a = (st['halo'][:3], min(1, st['halo'][3] / 255 * 2)) if st['halo'] is not None else (st['outline'][:3], 0.85)
            out.append((np.asarray(s, np.float32) / 255 * k_a, col))
        elif k == 'outline':
            o = m.filter(ImageFilter.MaxFilter(int(2 * a[0] + 1))).filter(ImageFilter.GaussianBlur(0.6))
            out.append((np.asarray(o, np.float32) / 255, st['outline'][:3]))
    out.append((np.asarray(m, np.float32) / 255, fillrgb))
    return out


def over(dst, alpha, rgb):
    """straight-alpha 'over' of a colour (solid or per pixel) with coverage alpha onto dst (h, w, 4) float 0..255"""
    a0 = dst[..., 3:] / 255
    a1 = alpha[..., None]
    ao = a1 + a0 * (1 - a1)
    c = (np.asarray(rgb, np.float32) * a1 + dst[..., :3] * a0 * (1 - a1)) / np.maximum(ao, 1e-6)
    dst[..., :3] = np.where(ao > 0, c, dst[..., :3])
    dst[..., 3:] = ao * 255


def place(layer, oy, ox, shape):
    a = np.zeros(shape, np.float32)
    sy0, sx0 = max(0, -oy), max(0, -ox)
    dy0, dx0 = max(0, oy), max(0, ox)
    hh = min(layer.shape[0] - sy0, shape[0] - dy0)
    ww = min(layer.shape[1] - sx0, shape[1] - dx0)
    a[dy0:dy0 + hh, dx0:dx0 + ww] = layer[sy0:sy0 + hh, sx0:sx0 + ww]
    return a


def repaint(img, r, ar):
    x0, y0, x1, y1 = map(int, r['box'].split())
    bw, bh = x1 - x0, y1 - y0
    e0, f0, e1, f1 = map(int, (r.get('erase') or r['box']).split())   # erase box (old text) inside the box
    assert x0 <= e0 < e1 <= x1 and y0 <= f0 < f1 <= y1, r['box']
    box0 = img[y0:y1, x0:x1].copy()
    eorig = img[f0:f1, e0:e1].copy()
    ebg = fill_bg(img, (e0, f0, e1, f1), r['fill'])
    ink = ink_mask(eorig, ebg, r['fill']) if ar is not None else None
    img[f0:f1, e0:e1] = ebg
    if ar is None:                                       # blank: the piece's word moved to another box
        return dict(size=0, fill='-', outline='-', halo='-', margin='-', text='', read='-')
    st = sample(eorig, ebg, ink, r['fill'])
    orig, bg = np.zeros((bh, bw, 4), np.float32), img[y0:y1, x0:x1].copy()   # bg = the box with the old text erased
    orig[f0 - y0:f1 - y0, e0 - x0:e1 - x0] = eorig
    ink = np.pad(ink, ((f0 - y0, y1 - f1), (e0 - x0, x1 - e1)))
    ys, xs = np.nonzero(ink)
    ib = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)          # old ink, box coordinates
    visual = shaper.shape(ar)
    pad = int(r.get('pad') or 2)
    rot = int(r.get('rotate') or 0)
    fixed = int(r.get('size') or 0)
    if rot:                                              # vertical label: fit along the box height, then turn
        size, m, mb = fit(visual, bh - 2 * pad, min(bw - 2 * pad, (ib[2] - ib[0]) * float(r['scale'])))
        m = m.rotate(rot, expand=True)
        mb = m.getbbox()
    elif fixed:                                          # sibling's size (layers of one word, pieces of one phrase),
        size = min(fixed, fit(visual, bw - 2 * pad, bh - 2 * pad)[0])   # never larger than this box allows
        m, mb = render(visual, size)
    else:
        size, m, mb = fit(visual, bw - 2 * pad, min(bh - 2 * pad, (ib[3] - ib[1]) * float(r['scale'])))
    # place: vertical centre on the old ink; horizontal by align
    cy = (ib[1] + ib[3]) / 2
    if r['align'] == 'center':
        ox = (ib[0] + ib[2]) / 2 - (mb[0] + mb[2]) / 2
    elif r['align'] == 'left':
        ox = ib[0] - mb[0]
    else:
        ox = ib[2] - mb[2]
    oy = cy - (mb[1] + mb[3]) / 2
    ox = int(round(min(max(ox, pad - mb[0]), bw - pad - mb[2])))
    oy = int(round(min(max(oy, pad - mb[1]), bh - pad - mb[3])))
    for e in r['effect'].split('+'):                     # 'fillc:rrggbb' / 'linec:rrggbb' / 'haloc:rrggbbaa' override a sampled colour
        if e[:6] in ('fillc:', 'linec:', 'haloc:'):
            st[{'f': 'fill', 'l': 'outline', 'h': 'halo'}[e[0]]] = np.array([int(e[6 + 2 * i:8 + 2 * i], 16) for i in range(len(e[6:]) // 2)] + [255], np.float32)[:4]
    blur = [float(e[5:]) for e in r['effect'].split('+') if e.startswith('blur:')]
    wide = max([float(e[5:]) for e in r['effect'].split('+') if e.startswith('glow:')] + blur + [0])
    if wide > 4:                                         # wide glow / blur: room around the mask so it fades out, not cut off
        b = int(3 * wide)                                # (round 1 used glow <= 4: its output is unchanged)
        m = ImageOps.expand(m, b)
        mb, ox, oy = (mb[0] + b, mb[1] + b, mb[2] + b, mb[3] + b), ox - b, oy - b
    if blur:                                             # glow copy of a word: the text itself is a soft blurred blob
        m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(blur[0]))
    fillrgb = st['fill'][:3]
    grad = 'grad' in r['effect'].split('+')
    if grad:
        g = row_gradient(orig, ink, ib)
        t = np.clip((np.arange(bh) - (oy + mb[1])) / max(mb[3] - mb[1] - 1, 1), 0, 1)
        fillrgb = np.stack([np.interp(t * (len(g) - 1), np.arange(len(g)), g[:, ch]) for ch in range(3)], -1)
        fillrgb = np.broadcast_to(fillrgb[:, None, :], (bh, bw, 3))
    out = bg.copy()
    effs = r['effect'].split('+')
    fa = st['fill'][3] / 255 if r['fill'] == 'clear' and st['fill'][3] < 230 else 1   # faint (half-transparent) text
    if 'knockout' in effs:                               # text cut out of an opaque plate (alpha holes)
        out[..., 3] *= 1 - place(np.asarray(m, np.float32) / 255, oy, ox, out.shape[:2])
    else:
        for e in [e for e in effs if e.startswith('plate:')]:   # opaque plate: the text grown by pr px + bottom rows
            pr, pb = map(int, e.split(':')[1:])
            tm = place(np.asarray(m, np.float32) / 255, oy, ox, out.shape[:2]) > 0.5
            grown = cv2.dilate(tm.astype(np.uint8), np.ones((2 * pr + 1, 2 * pr + 1), np.uint8)).astype(np.float32)
            grown = cv2.GaussianBlur(grown, (3, 3), 0.7)
            band, fb = np.zeros_like(grown), f1 - y0              # the bottom pb rows of the erased area
            band[fb - pb:fb] = orig[fb - pb:fb, :, 3] / 255 * np.minimum(1, (np.arange(pb) + 1) / 3)[:, None]
            over(out, np.maximum(grown, band) * st['halo'][3] / 255, st['halo'][:3])
        for alpha, rgb in effect_layers(m, r['effect'], st, fillrgb):
            over(out, place(alpha * fa, oy, ox, out.shape[:2]), rgb)
    for e in [e for e in effs if e.startswith('feather:')]:     # fade into the old pixels at the given sides
        sides, px = e.split(':')[1], int(e.split(':')[2])
        yy, xx = np.mgrid[0:bh, 0:bw]
        w = np.ones((bh, bw), np.float32)
        for s, d in (('l', xx), ('r', bw - 1 - xx), ('t', yy), ('b', bh - 1 - yy)):
            if s in sides:
                w = np.minimum(w, (d + 1) / (px + 1))
        out = blend(box0, out, w)
    img[y0:y1, x0:x1] = out
    margin = min(ox + mb[0], oy + mb[1], bw - (ox + mb[2]), bh - (oy + mb[3]))
    read = '-' if blur else 'contrast %d, components %d of %d (k %d), %s' % (
        lambda c, n, nr, k, ok: (c, n, nr, k, 'READABLE' if ok else 'UNREADABLE'))(*legibility(ar, visual, size))
    return dict(size=size, fill='grad' if grad else hexc(st['fill']), outline=hexc(st['outline']),
                halo='-' if st['halo'] is None else hexc(st['halo']), margin=margin, text=ar, read=read)


def blend(a, b, w):
    """premultiplied mix of two straight-alpha RGBA arrays: w = 1 -> b, w = 0 -> a"""
    w = w[..., None]
    pa, pb = a[..., :3] * a[..., 3:] / 255, b[..., :3] * b[..., 3:] / 255
    al = a[..., 3:] * (1 - w) + b[..., 3:] * w
    rgb = (pa * (1 - w) + pb * w) * 255 / np.maximum(al, 1e-6)
    mix = np.concatenate([np.where(al > 0, rgb, 0), al], -1)
    return np.where(w == 0, a, np.where(w == 1, b, mix)).astype(np.float32)   # untouched pixels stay exact


def echo(img, before, r):
    """flash copy (box) of the artwork at offset dx dy, two layers: a glow in the box's pink (model
    gain * blur(dilate(art, d), s)) under an opaque core in its orange (model clip((blur(art, 1) - 0.7) / 0.5 + 0.5));
    each pixel moves from its old value to the model of the repainted artwork (img) in proportion to how much the
    model changed against the old artwork (before): weight = 8 x the larger layer difference, capped at 1"""
    x0, y0, x1, y1 = map(int, r['box'].split())
    dx, dy, d, s, gain = (float(v) for v in r['fill'].split(':')[1:])
    shift = np.float32([[1, 0, dx], [0, 1, dy]])
    def model(rgba):
        art = rgba[..., 3].astype(np.float32) / 255
        art[y0:y1, x0:x1] = 0                                          # the artwork, not the flash itself
        glow = gain * cv2.GaussianBlur(cv2.dilate(art, np.ones((int(d), int(d)), np.uint8)), (0, 0), s)
        core = np.clip((cv2.GaussianBlur(art, (0, 0), 1) - 0.7) / 0.5 + 0.5, 0, 1)
        return [cv2.warpAffine(v, shift, art.shape[::-1])[y0:y1, x0:x1] for v in (glow, core)]
    (g0, c0), (g1, c1) = model(before), model(img)
    box = img[y0:y1, x0:x1]
    a = box[..., 3] / 255
    pink = np.median(box[(a > 0.1) & (a < 0.8)][:, :3], 0)
    orange = np.median(box[(a > 0.97) & (box[..., 1] > 190)][:, :3], 0)
    glow, core = np.clip(g1, 0, 1), c1
    al = core + glow * (1 - core)
    rgb = (orange * core[..., None] + pink * (glow * (1 - core))[..., None]) / np.maximum(al, 1e-6)[..., None]
    new = np.concatenate([rgb, al[..., None] * 255], -1).astype(np.float32)
    img[y0:y1, x0:x1] = blend(box, new, np.clip(np.maximum(np.abs(g1 - g0), np.abs(c1 - c0)) * 8, 0, 1))
    return dict(size=0, fill='echo', outline='-', halo='-', margin='-', text='', read='-')


def rows_by_asset(rects=RECTS):
    with open(rects, encoding='utf-8') as f:
        rs = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
    by = {}
    for r in rs:
        by.setdefault(r['asset'], []).append(r)
    return by


def sheet(before, after, path):
    """contact sheet: before | after over a dark backdrop (private, out/builds/IMAGES-MASS3/ref)"""
    ims = []
    for a in (before, after):
        im = Image.fromarray(a, 'RGBA')
        ims.append(Image.alpha_composite(Image.new('RGBA', im.size, (36, 52, 84, 255)), im))
    w, h = ims[0].size
    k = max(1, min(2, 900 // max(w, h)))
    c = Image.new('RGB', (2 * w * k + 6, h * k), (255, 255, 255))
    for i, im in enumerate(ims):
        c.paste(im.convert('RGB').resize((w * k, h * k), Image.NEAREST), (i * (w * k + 6), 0))
    c.save(path)


def edit_all(only='', rects=RECTS, out=OUT):
    tr = {r['id']: r for r in load_translation()}
    strings = load_strings()
    files, log, checks = {}, [], []
    os.makedirs(os.path.join(out, 'ref'), exist_ok=True)
    prev = set()
    if os.path.exists(PREV):
        with open(PREV, encoding='utf-8') as f:
            prev = {l.split('\t')[0] for l in f.read().splitlines()[1:]}
    for asset, rs in rows_by_asset(rects).items():
        if only and only not in asset:
            continue
        t = tc.load(os.path.join('extracted/assets', asset))
        img = tc.rgba0(t).astype(np.float32)
        before = tc.rgba0(t)
        inside = np.zeros(img.shape[:2], bool)
        sizes = {}
        groups = {}                                      # size '~g': the rows of group g share the smallest fitting size
        for i, r in enumerate(rs):
            if (r.get('size') or '').startswith('~'):
                probe = dict(r, size='')
                info = repaint(img.copy(), probe, arabic(r['source'], tr, strings))
                groups[r['size']] = min(groups.get(r['size'], 999), info['size'])
        rs = [dict(r, size=str(groups[r['size']])) if r['size'] in groups else r for r in rs]
        linked = lambda i: (rs[i].get('size') or '').startswith('=')
        last = lambda i: (rs[i]['fill'].startswith('echo:'), linked(i))   # flash copies after their artwork
        for i in sorted(range(len(rs)), key=last):       # '=k' = the size of row k of this asset (layers of one word)
            r = dict(rs[i])
            if linked(i):
                r['size'] = sizes[int(r['size'][1:])]
            x0, y0, x1, y1 = map(int, r['box'].split())
            inside[y0:y1, x0:x1] = True
            if r['fill'].startswith('echo:'):
                info = echo(img, before, r)
            else:
                info = repaint(img, r, None if r['source'] == 'blank' else arabic(r['source'], tr, strings))
            sizes[i] = info['size']
            log.append([asset.split('/')[-1], r['box'], r['source'], str(info['size']), info['fill'], info['outline'],
                        info['halo'], str(info['margin']), info['read'], r.get('note', '')])
        new = np.clip(np.round(img), 0, 255).astype(np.uint8)
        name = asset.split('/')[-1][:-7]
        tag = asset.split('/')[-3] if asset.split('/')[-3] in ('hud_dance', 'hud_specialship') else             asset.split('/')[-2] if asset.split('/')[-2] in ('ps4', 'windows', 'xboxone') else ''
        ua, ue, ub = tc.write(t, tc.mip_chain(t, new))
        t2 = tc.read(ua, ue, ub)
        got = tc.rgba0(t2)
        pl, pl2 = t['platforms'][0], t2['platforms'][0]
        m0 = pl['mips'][0]
        old_b, new_b = tc.mip_bytes(t, m0), tc.mip_bytes(t2, pl2['mips'][0])
        bs = tc.BLOCK.get(pl['pf'], 16 * tc.RAW.get(pl['pf'], 4))
        blocks = sum(1 for i in range(0, len(old_b), bs) if old_b[i:i + bs] != new_b[i:i + bs]) if pl['pf'] in tc.BLOCK else \
            int((before != got).any(-1).reshape(m0['h'] // 4, 4, m0['w'] // 4, 4).any((1, 3)).sum())
        edit_out = int((new != before).any(-1)[~inside].sum())            # edit outside the boxes (must be 0)
        enc = (got != before).any(-1) & ~inside                           # after encoding: only 4x4 neighbours
        near = cv2.dilate(inside.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
        far = int((enc & ~near).sum())
        same = tc.info(t2) == tc.info(t) and len(ue) == len(t['ue']) and len(ub) == len(t['ub'])
        mine = [l for l in log if l[0] == asset.split('/')[-1]]
        margins = [int(l[7]) for l in mine if l[7] not in ('-',)]
        low = sum('UNREADABLE' in l[8] for l in mine)
        readable = ('PASS' if not low else 'FAIL') if asset not in prev else \
            'MASS3 (reported only' + (f': {low} box(es) under the bar)' if low else ')')
        checks.append([asset, f"{pl['pf']} {pl['sx']}x{pl['sy']} mips {len(pl['mips'])}", 'PASS' if same else 'FAIL',
                       str(blocks), str(edit_out), str(int(enc.sum())), str(far), str(min(margins) if margins else '-'),
                       readable, 'PASS' if same and edit_out == 0 and far == 0 and (not margins or min(margins) >= MARGIN)
                       and readable != 'FAIL' else 'FAIL'])
        sheet(before, got, os.path.join(out, 'ref', (tag + '_' if tag else '') + name + '.png'))
        stem = asset[:-7]
        files[stem + '.uasset'], files[stem + '.uexp'] = ua, ue
        if ub:
            files[stem + '.ubulk'] = ub
    return files, log, checks


def write_tsv(path, head, rows):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(head) + '\n')
        f.writelines('\t'.join(map(str, r)) + '\n' for r in rows)


def mass(only='', rects=RECTS, out=OUT):
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(out, exist_ok=True)
    files, log, checks = edit_all(only, rects, out)
    write_tsv(os.path.join(out, 'repaint_log.tsv'), ['texture', 'box', 'source', 'font_px', 'fill', 'outline', 'halo',
              'margin_px', 'readability', 'note'], log)
    write_tsv(os.path.join(out, 'checks.tsv'), ['asset', 'format', 'reparse_same_size', 'changed_blocks_mip0',
              'edit_px_outside_boxes', 'encoded_px_outside_boxes', 'encoded_px_beyond_3px', 'min_margin_px',
              'readability', 'result'], checks)
    bad = [c[0] for c in checks if c[-1] != 'PASS']
    print(f'{len(checks)} textures, {len(log)} boxes, {len(bad)} FAIL', *bad, sep='\n  ')
    if only or out != OUT:
        return
    old = os.path.join(os.path.dirname(PREV), 'assets')            # the previous build's files stay byte-identical,
    same = [rel for rel in files if os.path.exists(os.path.join(old, rel))]   # except textures drawing a row that
    diff = [rel for rel in same if open(os.path.join(old, rel), 'rb').read() != files[rel]]   # was reworded since
    by = rows_by_asset()
    allowed = {a[:-7] for a, rs in by.items() if any(re.search(r'\b(%s)\b' % '|'.join(REWORDED), r['source']) for r in rs)}
    assert all(rel.rsplit('.', 1)[0] in allowed for rel in diff), f'changed against {old}: {diff}'
    print(f'{len(same) - len(diff)} files byte-identical to {old}; {len(diff)} changed by reworded rows '
          f'{sorted(REWORDED)}: {diff}; {len(files) - len(same)} new')
    root = os.path.join(OUT, 'assets')
    for rel, data in files.items():
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        open(os.path.join(root, rel), 'wb').write(data)
    stale = [os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs
             if os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/') not in files]
    assert not stale, f'unexpected files in {root}: {stale}'
    if os.path.exists(PAK):
        os.remove(PAK)
    subprocess.run([REPAK, 'pack', '--version', 'V4', '--compression', 'Zlib', '--mount-point', '../../../', root, PAK],
                   check=True, capture_output=True)
    listed = subprocess.run([REPAK, 'list', PAK], check=True, capture_output=True, text=True).stdout.splitlines()
    hl = dict(l.split(' ', 1)[::-1] for l in subprocess.run([REPAK, 'hash-list', PAK], check=True, capture_output=True,
                                                             text=True).stdout.splitlines() if l.strip())
    unp = os.path.join(OUT, 'unpacked')
    subprocess.run([REPAK, 'unpack', '-q', '-f', '-o', unp, PAK], check=True, capture_output=True)
    assert sorted(listed) == sorted(files), set(listed) ^ set(files)
    rep = []
    for rel, data in sorted(files.items()):
        orig = open(os.path.join('extracted/assets', rel), 'rb').read()
        got = open(os.path.join(unp, rel), 'rb').read()
        rp = '-'
        if rel.endswith('.uexp'):
            a0 = tc.read(open(os.path.join('extracted/assets', rel[:-5] + '.uasset'), 'rb').read(), orig)
            a1 = tc.read(open(os.path.join(unp, rel[:-5] + '.uasset'), 'rb').read(), got)
            same = tc.info(a0) == tc.info(a1) and len(orig) == len(got)
            ch = sum(1 for i in range(0, len(orig), 16) if orig[i:i + 16] != got[i:i + 16])
            rp = f"{'PASS' if same else 'FAIL'} ({tc.info(a1)['format']} {tc.info(a1)['w']}x{tc.info(a1)['h']}, {ch} of {len(orig) // 16} 16-byte units changed)"
            assert same
        ok = sha(data) == hl.get(rel) == sha(got)
        rep.append([rel, sha(orig), sha(data), hl.get(rel, ''), sha(got), rp, 'PASS' if ok else 'FAIL'])
        assert ok, rel
    write_tsv(os.path.join(OUT, 'pak_verify_sha256.tsv'), ['path_in_pak', 'sha256_original', 'sha256_input',
              'sha256_repak_hash_list', 'sha256_unpacked', 'reparse', 'result'], rep)
    print(f'{len(files)} files list / hash-list / unpack PASS')
    print(f'{PAK}: {os.path.getsize(PAK)} B sha256 {sha(open(PAK, "rb").read())}')


def self_check():
    """synthetic: vlerp keeps a gradient, the shaped text is drawn right-to-left, @i/n splits a phrase, big text
    gets the stroke (wider ink than without)"""
    img = np.zeros((40, 60, 4), np.float32)
    img[..., 0] = np.arange(40)[:, None] * 5
    img[..., 3] = 255
    f = fill_bg(img, (10, 10, 50, 30), 'vlerp')
    assert np.allclose(f[:, :, 0], img[10:30, 10:50, 0], atol=0.01)
    vis = shaper.shape(chr(0x0628) + chr(0x0627))           # ba + alef: visual order puts alef (final) left of ba
    m = np.asarray(mask(vis, 40))
    assert vis[0] != chr(0x0628) and m.any()
    rows = {'1': {'AR': 'aa bb cc'}, '2': {'AR': 'x {0}<br>y <c>{1}</c>'}}
    assert arabic('row:1@0/2', rows, {}) == 'aa bb' and arabic('row:1@1/2', rows, {}) == 'cc'
    assert arabic('tpl:2:=7:1#0', rows, {}) == 'x 7' and arabic('tpl:2:=7:1#1', rows, {}) == 'y aa bb cc'
    wd = lambda st: (lambda b: b[2] - b[0])(mask(vis, 30, st).getbbox())
    assert wd(True) >= wd(False) + 2 * SS - 1, (wd(True), wd(False))
    word = chr(0x0645) + chr(0x0633) + chr(0x062A) + chr(0x0648) + chr(0x0649)   # 5-letter word, ta has 2 dots
    assert legibility(word, shaper.shape(word), 16)[-1] and not legibility(word, shaper.shape(word), 6)[-1]
    bar = img.copy(); bar[20, 30] = 0
    assert np.allclose(fill_bg(bar, (10, 18, 50, 22), 'rowmed')[2], img[20, 10:50])          # one speck gone
    a, b = np.zeros((2, 2, 4), np.float32), np.full((2, 2, 4), 200, np.float32)
    w = np.array([[0, 1], [0.5, 0.5]], np.float32)
    m = blend(a, b, w)
    assert (m[0, 0] == a[0, 0]).all() and (m[0, 1] == b[0, 1]).all() and m[1, 0, 3] == 100 and m[1, 0, 0] == 200
    print('texture_text self check: PASS')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        self_check()
    elif a[0] == 'mass':
        mass(a[1] if len(a) > 1 else '')
    elif a[0] == 'trial':
        mass(a[1] if len(a) > 1 else '', TRIAL, os.path.join(OUT, 'trial'))
    elif a[0] == '--installed':
        got = sha(open(os.path.join(MODS, os.path.basename(PAK)), 'rb').read())
        assert got == sha(open(PAK, 'rb').read()), 'the pak in ~mods is not this build'
        print('installed images pak = build', got)
