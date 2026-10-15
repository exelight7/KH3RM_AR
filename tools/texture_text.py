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
BATCH-234 (IMAGES-MASS5): rows enlarged by tools\images_enlarge.py (note 'MASS5: size') must be readable themselves;
  only their textures may differ from IMAGES-MASS4, the other boxes of the previous build are only reported.
IMAGES-MASS6 (tools\images_sharpen.py, note 'MASS6:'): effect tokens for small text (style_of): face:b|sb (Segoe UI
  Bold / Semibold), stroke:<px> (any size), track:<px> (letter spacing between unjoined letters), snap (pixel grid:
  stems at the best phase, dots as whole pixels kept off the letters), halo (thin dark/light ring under the text).
  Rows without them render exactly as before. Only textures with 'MASS6:' rows (or REWORDED rows) may differ from
  IMAGES-MASS5; 'MASS6: bar' rows must be readable. repaint_log bg_contrast = edge contrast (bg_contrast()).
FOCUS-FIX (IMAGES-MASS7, note 'MASS7:'): the battle HUD gauge words are bitmap shapes of the HudStatus(CA) movie
  (sttsPc > pcEx > pcFocusGg > pcExMaxAnm > pcExLogo | coTextMax, pcExLogoC > coPcExTxCharge), drawn 1:1 from
  HudStatusTxt(CA) on the 1920x1080 stage. Their box is the whole shape cell (erased whole), pad 1 (the margin check
  takes min(2, pad)); effect 'wide:<f>' stretches the text horizontally where the cell height binds, not the width.
  Only textures with 'MASS7:' rows may differ from IMAGES-MASS6.
HUD-SCALE (IMAGES-MASS8, note 'MASS8:'): BUILD-17 draws the Focus cell x1.45 and the Max cell x1.25 (bilinear
  magnification of the same texels); effect 'sharp:<amount>:<sigma>' = a premultiplied unsharp mask of the finished box
  (measured after BC7 + magnification: edge gradient p90 Focus +6.8 % on the bar, Max +10.0 %; Charge x1.20 lost 2.2 %
  on its bar, so it keeps MASS7). Only textures with 'MASS8:' rows may differ from IMAGES-MASS7.
HUD-PLEX (IMAGES-MASS9, note 'MASS9:'): effect token 'face:plex' = IBM Plex Sans Arabic Regular (the verified OFL file
  in out/fonts_gpt/fonts/, SHA256 asserted as in out/fonts_gpt/SOURCES.md; no Bold/SemiBold there), drawn from the same
  pre-shaped presentation forms with the same BASIC layout as Segoe. Plex rows are measured against a Plex 64 px
  reference and must also pass joins(): every run of joined letters, drawn alone in the row's style at 1x, has as many
  letter bodies (coverage >= 128, dots excluded as in snap) as at 64 px, so no join is broken.
  Only textures with 'MASS9:' rows may differ from IMAGES-MASS8.
HUD-CRISP (IMAGES-MASS10, note 'MASS10:'): effect token 'hard:<k>' = coverage a' = 128 + k (a - 128) clipped (k 99 =
  practically a threshold: only coverage 128..130 keeps a middle value; no grey ramps before BC7) for the text, and an outline drawn solid (no 0.6 px blur); picked
  per gauge word by tools\hud_sheet.py trial on the simulated in-game look (BC7 decode, bilinear x movie scale).
  Only textures with 'MASS10:' rows may differ from IMAGES-MASS9.
HUD-SOFTEN (IMAGES-MASS11, note 'MASS11:'): the stair-steps of hard:99 are softened, recipe (face, stroke, outline, pad, snap)
  unchanged. Tokens: 'hard:<k>' with a small k (3 .. 12) = short grey ramp; 'aa:<k>' = text box-filtered from the 4x
  render (no Lanczos) + steep k, outline from the 4x-upsampled mask grown by a round (disk) kernel and box-filtered back
  (smooth contour); 'ramp:<alpha>[:out]' (with hard:<k>) = the outermost outline pixel at alpha (inside the same footprint,
  or one extra ring ':out'). Picked by tools\hud_sheet.py soften on edge / crisp / jaggedness of the simulated look.
  Only textures with 'MASS11:' rows may differ from IMAGES-MASS10.
Usage: python -I tools\texture_text.py                    -> self check
       python -I tools\texture_text.py mass [asset-substr] -> out\builds\IMAGES-MASS11\ assets, checks, ref sheets, pak
       python -I tools\texture_text.py trial               -> technical\images_rects_trial.tsv rendered and measured
                                                              (out\builds\IMAGES-MASS11\trial\, no pak)
       python -I tools\texture_text.py --installed         -> the pak in ~mods = this build (sha)"""
import csv, functools, hashlib, os, re, subprocess, sys, unicodedata
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
OUT = 'out/builds/IMAGES-MASS11'                        # IMAGES-MASS .. IMAGES-MASS10 stay as built
PREV = 'out/builds/IMAGES-MASS10/checks.tsv'            # textures of the previous build: readability only reported
REWORDED = set()                                         # rows reworded after IMAGES-MASS10 that an image draws (none)
ENLARGED = ('MASS5: size', 'MASS6: bar', 'MASS7:', 'MASS8:', 'MASS9:', 'MASS10:', 'MASS11:')   # rect notes (images_enlarge.py, images_sharpen.py, FOCUS-FIX, HUD-SCALE, HUD-PLEX, HUD-CRISP, HUD-SOFTEN): must be readable
CHANGED = 'MASS11:'                                      # IMAGES-MASS11 rect note: only these textures may differ from MASS10
PAK = os.path.join(OUT, 'pakchunk98-arabic-images_P.pak')
MODS = r'C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods'
REPAK = os.path.abspath('tools/repak-0.2.3/repak.exe')
FONT = r'C:\Windows\Fonts\segoeui.ttf'
PLEX = 'out/fonts_gpt/fonts/IBMPlexSansArabic-Regular.ttf'   # HUD-PLEX: OFL, not tracked (out/ is git-ignored)
PLEX_SHA = '8e0f1046c736bf939d4939ee3ae0116acf61cbcd6592deae7656761627080981'   # out/fonts_gpt/SOURCES.md
FACES = {'b': r'C:\Windows\Fonts\segoeuib.ttf', 'sb': r'C:\Windows\Fonts\seguisb.ttf', 'plex': PLEX}   # Segoe UI Bold / Semibold, Plex
SS = 4                                                   # supersampling
BIG = 24                                                 # px: from here 4x supersampling + 1 px stroke
MARGIN = 2                                               # px between the new text and its box


def sha(b):
    return hashlib.sha256(b).hexdigest()


@functools.lru_cache(None)
def face(name):
    """font file of a face token (blank = Segoe UI); the Plex file must be the verified one"""
    if name == 'plex':
        assert sha(open(PLEX, 'rb').read()) == PLEX_SHA, PLEX
    return FACES.get(name, FONT)


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


JOINS = {c for c in map(chr, range(0xFE70, 0xFEFD)) if unicodedata.decomposition(c).split()[:1] in (['<final>'], ['<medial>'])}


def style_of(effect):
    """IMAGES-MASS6 small-text tokens of an effect cell (blank = the old rendering): face:b|sb (Segoe UI Bold /
    Semibold), stroke:<px> (outline in the fill colour, any size), track:<px> (extra space between unjoined letters),
    snap (pixel grid: stems at the sub-pixel phase with most full pixels, dots as whole pixels, 1 px off the letters)"""
    st = {}
    for e in effect.split('+'):
        k, _, v = e.partition(':')
        if k == 'face':
            st['face'] = v
        elif k in ('stroke', 'track', 'wide', 'hard', 'aa'):
            st[k] = float(v)
        elif k == 'snap':
            st['snap'] = True
    return st


def styled(visual, px, st):
    """1x L mask of the text in style st"""
    k = SS if px >= BIG or st.get('stroke') or st.get('snap') or st.get('track', 0) % 1 or st.get('wide') else 1
    font = ImageFont.truetype(face(st.get('face')), px * k, layout_engine=ImageFont.Layout.BASIC)
    sw = int(round(st.get('stroke', 1 if px >= BIG else 0) * k))
    parts, cur = [], ''                                  # runs of joined letters (visual order: a final or medial
    for i, c in enumerate(visual):                       # form joins the glyph on its right)
        cur += c
        if st.get('track') and i + 1 < len(visual) and c not in JOINS:
            parts.append(cur)
            cur = ''
    parts.append(cur)
    m = Image.new('L', (int(sum(font.getlength(p) for p in parts) + st.get('track', 0) * k * len(parts)) + 16 * k + 2 * sw,
                        3 * px * k + 2 * sw), 0)
    d, x = ImageDraw.Draw(m), 6 * k + sw
    for p in parts:
        d.text((x, px * k), p, font=font, fill=255, stroke_width=sw, stroke_fill=255)
        x += font.getlength(p) + st.get('track', 0) * k
    m = Image.fromarray(np.pad(np.asarray(m.crop(m.getbbox())), 4 * k))
    if st.get('wide'):                                   # FOCUS-FIX: horizontal stretch (a wide display face) where
        m = m.resize((int(round(m.width * st['wide'])), m.height), Image.LANCZOS)   # the height binds, not the width
    if k == 1:
        return m
    if st.get('snap'):
        return snap(np.asarray(m), k)
    return m.resize((m.width // k, m.height // k), Image.BOX if st.get('wide') or st.get('aa') else Image.LANCZOS)   # box: no ringing rows


def snap(H, k):
    """k x mask -> 1x: the letter bodies box-filtered at the phase with the most full pixels; dots (components lower
    than 0.3 of the tallest) drawn as whole-pixel blocks, moved 1 px away from the body when they would touch it"""
    n, lab, stt, _ = cv2.connectedComponentsWithStats((H >= 128).astype(np.uint8), connectivity=8)
    big = max([stt[i, cv2.CC_STAT_HEIGHT] for i in range(1, n)] + [1])
    dots = [i for i in range(1, n) if stt[i, cv2.CC_STAT_HEIGHT] < 0.3 * big and stt[i, cv2.CC_STAT_WIDTH] < 0.45 * big]
    body = H.copy()
    for i in dots:
        body[lab == i] = 0
    h, w = H.shape[0] // k + 1, H.shape[1] // k + 1
    best = None
    for py in range(k):
        for px in range(k):
            b = np.pad(body.astype(np.float32), ((py, k), (px, k)))[:h * k, :w * k].reshape(h, k, w, k).mean((1, 3))
            score = (b >= 192).sum() - 0.5 * ((b > 32) & (b < 192)).sum()
            if best is None or score > best[0]:
                best = (score, b, py, px)
    _, b, py, px = best
    solid, out = b >= 128, b.copy()
    mid = np.nonzero(solid.any(1))[0].mean() if solid.any() else h / 2
    for i in dots:
        x, y, bw, bh = stt[i, :4]
        cw, ch = max(1, int(round(bw / k))), max(1, int(round(bh / k)))
        cx, cy = (x + bw / 2 + px) / k, (y + bh / 2 + py) / k
        X, Y = int(round(cx - cw / 2)), int(round(cy - ch / 2))
        for Yy in (Y, Y - 1 if cy < mid else Y + 1):
            if 0 <= Yy <= h - ch and not solid[max(0, Yy - 1):Yy + ch + 1, max(0, X - 1):X + cw + 1].any():
                Y = Yy
                break
        out[max(0, Y):Y + ch, max(0, X):X + cw] = 255
    return Image.fromarray(np.clip(np.round(out), 0, 255).astype(np.uint8))


def steep(m, k):
    """HUD-CRISP 'hard:<k>': coverage pushed away from the middle, a' = 128 + k (a - 128) clipped (large k = threshold)"""
    return Image.fromarray(np.clip(np.round(128 + k * (np.asarray(m, np.float32) - 128)), 0, 255).astype(np.uint8))


def render(visual, size, st=None):
    if st:
        m = styled(visual, size, st)
        k = st.get('hard') or st.get('aa')               # HUD-SOFTEN: aa:<k> = box-filtered 4x render, then mild steep
        m = steep(m, k) if k else m
        return m, m.getbbox()
    m = mask(visual, size)
    m = m.resize((m.width // ss(size), m.height // ss(size)), Image.LANCZOS)
    return m, m.getbbox()


def fit(visual, w, h, st=None):
    """largest pixel size whose ink fits w x h -> (size, L mask at 1x, ink bbox in the mask)"""
    lo, hi = 4, 400
    while lo < hi:
        mid = (lo + hi + 1) // 2
        bb = render(visual, mid, st)[1]                   # measured at 1x (after the downscale)
        if bb[2] - bb[0] <= w and bb[3] - bb[1] <= h:
            lo = mid
        else:
            hi = mid - 1
    return (lo,) + render(visual, lo, st)


DOTS23 = set(map(chr, (0x062A, 0x062B, 0x0629, 0x0642, 0x064A, 0x0634)))   # ta tha ta-marbuta qaf ya shin
READ_CONTRAST = 192


def components(m):
    return cv2.connectedComponents((np.asarray(m) >= 128).astype(np.uint8), connectivity=8)[0] - 1


def ref_mask(visual, font=FONT):
    font = ImageFont.truetype(font, 64, layout_engine=ImageFont.Layout.BASIC)
    l, t, r, b = font.getbbox(visual)
    ref = Image.new('L', (r - l + 16, b - t + 16), 0)
    ImageDraw.Draw(ref).text((8 - l, 8 - t), visual, font=font, fill=255)
    return ref


@functools.lru_cache(None)
def ref_components(visual, font=FONT):
    return components(ref_mask(visual, font))


def pieces(m, conn=8):
    """conn-connected coverage >= 128 components as (x0, y0, x1, y1) in the ink box scaled to 0..1, and a dot flag (as
    snap: lower than 0.3 of the tallest and narrower than 0.45 of it)"""
    a = np.asarray(m) >= 128
    n, _, stt, _ = cv2.connectedComponentsWithStats(a.astype(np.uint8), connectivity=conn)
    if n < 2:
        return []
    ys, xs = np.nonzero(a)
    X, Y, W, H = xs.min(), ys.min(), xs.max() + 1 - xs.min(), ys.max() + 1 - ys.min()
    big = stt[1:, cv2.CC_STAT_HEIGHT].max()
    return [((x - X) / W, (y - Y) / H, (x + w - X) / W, (y + h - Y) / H, h < 0.3 * big and w < 0.45 * big)
            for x, y, w, h, _ in stt[1:]]


def bodies(m, ref=None):
    """letter bodies of a mask: 8-connected components that are not dots; with ref (the pieces of a large rendering
    of the same text) the 1x mask is split 4-connected (a joint touching only at a pixel corner reads as a gap once
    the cell is magnified) and a piece is a dot only where ref has a dot (its centre inside a ref dot box grown by
    0.15), so a small broken-off tail still counts as a body"""
    if ref is None:
        return sum(not p[4] for p in pieces(m))
    dots = [p for p in ref if p[4]]
    inside = lambda c, d: d[0] - .15 <= (c[0] + c[2]) / 2 <= d[2] + .15 and d[1] - .15 <= (c[1] + c[3]) / 2 <= d[3] + .15
    return sum(not any(inside(p, d) for d in dots) for p in pieces(m, 4))


def joins(visual, size, st):
    """HUD-PLEX: (runs of 2+ joined letters, runs with a broken join): each run, drawn alone in style st at 1x, must not
    have more letter bodies than at 64 px in the same face and width (visual order: a final or medial form joins the
    glyph on its right)"""
    runs, cur = [], ''
    for c in visual:
        cur += c
        if c not in JOINS:
            runs.append(cur)
            cur = ''
    runs = [r for r in runs + [cur] if len(r) > 1]
    font = face(st.get('face'))
    def ref(r):
        m = ref_mask(r, font)
        return m.resize((int(round(m.width * st['wide'])), m.height), Image.LANCZOS) if st.get('wide') else m
    return len(runs), sum(bodies(render(r, size, st)[0], pieces(ref(r))) > bodies(ref(r)) for r in runs)


def legibility(ar, visual, size, st=None):
    """(stroke contrast, components, reference components, k, readable) of the text at its real size; Plex rows are
    measured against Plex and need intact joins"""
    a = np.asarray(render(visual, size, st)[0]).astype(int)
    contrast = int(np.percentile(a[a >= 64], 75)) if (a >= 64).any() else 0
    plex = bool(st) and st.get('face') == 'plex'
    n, k = components(a.astype(np.uint8)), sum(c in DOTS23 for c in ar)
    nref = ref_components(visual, face('plex')) if plex else ref_components(visual)
    ok = contrast >= READ_CONTRAST and (size >= BIG or nref - k <= n <= nref) and not (plex and joins(visual, size, st)[1])
    return contrast, n, nref, k, ok


def disk_outline(m, r, k, up=4):
    """HUD-SOFTEN 'aa': text mask grown by r px with a round kernel at 4x (bicubic-upsampled mask, contour at 128), box-filtered
    back to 1x and pushed steep k -> L image"""
    a = np.asarray(m, np.float32)
    big = cv2.resize(a, None, fx=up, fy=up, interpolation=cv2.INTER_CUBIC) >= 128
    d = cv2.dilate(big.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * round(r * up) + 1,) * 2))
    o = cv2.resize(d.astype(np.float32) * 255, (a.shape[1], a.shape[0]), interpolation=cv2.INTER_AREA)
    return steep(Image.fromarray(np.clip(np.round(o), 0, 255).astype(np.uint8)), k)


def effect_layers(m, eff, st, fillrgb):
    """[(alpha mask, rgb)] bottom to top; eff like 'shadow:2:3:4', 'outline:1', 'glow:5', 'grad', joined by '+'"""
    out = []
    if 'halo' in eff.split('+'):                         # MASS6: thin contrast halo under everything, dark under
        h = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.5))   # light text, light under dark
        out.append((np.asarray(h, np.float32) / 255 * 0.75, (0, 0, 0) if st['fill'][:3] @ LUM >= 128 else (255, 255, 255)))
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
            hard = [float(x[5:]) for x in eff.split('+') if x.startswith('hard:')]   # HUD-CRISP: solid outline, no blur
            aa = [float(x[3:]) for x in eff.split('+') if x.startswith('aa:')]
            if aa:                                       # HUD-SOFTEN: round outline from the 4x-upsampled mask, box-filtered back
                o = disk_outline(m, a[0], aa[0])         # (any radius: HUD-VECTOR scales it to a fraction)
            else:
                o = m.filter(ImageFilter.MaxFilter(int(2 * a[0] + 1)))
                o = steep(o, hard[0]) if hard else o.filter(ImageFilter.GaussianBlur(0.6))
            o = np.asarray(o, np.float32) / 255
            for x in [x for x in eff.split('+') if x.startswith('ramp:')]:   # HUD-SOFTEN: 1-step alpha ramp on the outer edge
                al, *outer = x[5:].split(':')
                hk = (hard or aa)[0]
                if outer:                                # one extra ring beyond the solid outline
                    o = np.maximum(o, float(al) * np.asarray(steep(m.filter(ImageFilter.MaxFilter(int(2 * a[0] + 3))), hk), np.float32) / 255)
                else:                                    # the outermost pixel of the outline, same footprint
                    core = np.asarray(steep(m.filter(ImageFilter.MaxFilter(int(2 * a[0] - 1))), hk), np.float32) / 255 if a[0] > 1 else \
                        np.asarray(m, np.float32) / 255
                    o = np.maximum(core, float(al) * o)
            out.append((o, st['outline'][:3]))
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
        return dict(size=0, fill='-', outline='-', halo='-', margin='-', text='', read='-', bgc='-')
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
    sty = style_of(r['effect'])
    if rot:                                              # vertical label: fit along the box height, then turn
        size, m, mb = fit(visual, bh - 2 * pad, min(bw - 2 * pad, (ib[2] - ib[0]) * float(r['scale'])), sty)
        m = m.rotate(rot, expand=True)
        mb = m.getbbox()
    elif fixed:                                          # sibling's size (layers of one word, pieces of one phrase),
        size = min(fixed, fit(visual, bw - 2 * pad, bh - 2 * pad, sty)[0])   # never larger than this box allows
        m, mb = render(visual, size, sty)
    else:
        size, m, mb = fit(visual, bw - 2 * pad, min(bh - 2 * pad, (ib[3] - ib[1]) * float(r['scale'])), sty)
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
    for e in [e for e in effs if e.startswith('sharp:')]:     # HUD-SCALE: edge contrast for a magnified cell
        out = unsharp(out, *map(float, e.split(':')[1:]))
    bgc = '-' if blur else bg_contrast(out, place(np.asarray(m, np.float32) / 255, oy, ox, out.shape[:2]))
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
        lambda c, n, nr, k, ok: (c, n, nr, k, 'READABLE' if ok else 'UNREADABLE'))(*legibility(ar, visual, size, sty))
    if sty.get('face') == 'plex':                        # HUD-PLEX: the joins check in the log
        read += ', Plex joins %d of %d runs intact' % (lambda n, bad: (n - bad, n))(*joins(visual, size, sty))
    return dict(size=size, fill='grad' if grad else hexc(st['fill']), outline=hexc(st['outline']),
                halo='-' if st['halo'] is None else hexc(st['halo']), margin=margin, text=ar, read=read, bgc=bgc)


def unsharp(rgba, amount, sigma):
    """premultiplied unsharp mask of a straight-alpha float RGBA box (alpha kept; colour where alpha > 0)"""
    a = rgba[..., 3:] / 255
    pm = rgba[..., :3] * a
    sh = np.clip(pm + amount * (pm - cv2.GaussianBlur(pm, (0, 0), sigma)), 0, None)
    out = rgba.copy()
    out[..., :3] = np.where(a > 0, np.clip(sh / np.maximum(a, 1e-3), 0, 255), rgba[..., :3])
    return out


def bg_contrast(out, cov):
    """MASS6 edge contrast: luminance distance (over mid grey) between the text core (coverage >= 0.75) and the ring
    up to 2 px around the ink (coverage < 0.1): the outline / halo / background the text has to stand out from"""
    a = out[..., 3:] / 255
    lum = (out[..., :3] * a + 128 * (1 - a)) @ LUM
    core = cov >= 0.75
    ring = (cv2.dilate((cov >= 0.25).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & (cov < 0.1)
    return int(round(abs(np.median(lum[core]) - np.median(lum[ring])))) if core.any() and ring.any() else 0


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
    return dict(size=0, fill='echo', outline='-', halo='-', margin='-', text='', read='-', bgc='-')


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


FOCUS = 'KINGDOM HEARTS III/Content/UI/Scaleform/01_hud/hud_status/HudStatusTxt.uasset'


def focus_sheet(out=OUT, crop=(0, 0, 144, 128)):
    """battle HUD gauge words (FOCUS, MAX, AIR, CHARGE) of both textures: English | previous build (PREV) | this build, at 1x
    (the real on-screen size at 1920x1080: the movie draws the cells 1:1) and 3x (nearest)"""
    for asset in (FOCUS, FOCUS[:-7] + 'CA.uasset'):
        ims = [tc.rgba0(tc.load(os.path.join(d, asset)))[crop[1]:crop[3], crop[0]:crop[2]]
               for d in ('extracted/assets', os.path.join(os.path.dirname(PREV), 'assets'), os.path.join(out, 'assets'))]
        for z in (1, 3):
            w, h = (crop[2] - crop[0]) * z, (crop[3] - crop[1]) * z
            c = Image.new('RGB', (3 * w + 12, h), (255, 255, 255))
            for i, a in enumerate(ims):
                im = Image.alpha_composite(Image.new('RGBA', (a.shape[1], a.shape[0]), (36, 52, 84, 255)), Image.fromarray(a, 'RGBA'))
                c.paste(im.convert('RGB').resize((w, h), Image.NEAREST), (i * (w + 6), 0))
            c.save(os.path.join(out, 'ref', f'FOCUS_{asset.split("/")[-1][:-7]}_{z}x.png'))


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
        sizes, short = {}, []
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
            if info['margin'] != '-' and info['margin'] < min(MARGIN, int(r.get('pad') or 2)):
                short.append(r['box'])                   # FOCUS-FIX: a pad-1 row (HUD cell) needs 1 px, others 2
            log.append([asset.split('/')[-1], r['box'], r['source'], str(info['size']), info['fill'], info['outline'],
                        info['halo'], str(info['margin']), info['read'], r.get('note', ''), str(info['bgc'])])
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
        grown = [l for l in mine if any(e in l[9] for e in ENLARGED)]     # enlarged / MASS6 / MASS7 boxes must pass themselves
        readable = ('PASS' if not low else 'FAIL') if asset not in prev else \
            'FAIL' if any('UNREADABLE' in l[8] for l in grown) else \
            'previous build (reported only' + (f': {low} box(es) under the bar' if low else '') + \
            (f'; {len(grown)} enlarged box(es) READABLE)' if grown else ')')
        checks.append([asset, f"{pl['pf']} {pl['sx']}x{pl['sy']} mips {len(pl['mips'])}", 'PASS' if same else 'FAIL',
                       str(blocks), str(edit_out), str(int(enc.sum())), str(far), str(min(margins) if margins else '-'),
                       readable, 'PASS' if same and edit_out == 0 and far == 0 and not short
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
              'margin_px', 'readability', 'note', 'bg_contrast'], log)
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
    allowed = {a[:-7] for a, rs in by.items() if any(CHANGED in r['note'] or REWORDED and
                                                     re.search(r'\b(%s)\b' % '|'.join(REWORDED), r['source']) for r in rs)}
    assert all(rel.rsplit('.', 1)[0] in allowed for rel in diff), f'changed against {old}: {diff}'
    print(f'{len(same) - len(diff)} files byte-identical to {old}; {len(diff)} changed on purpose (reworded rows '
          f'{sorted(REWORDED)}, {CHANGED[:-1]} boxes in {len(allowed)} textures); {len(files) - len(same)} new')
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
    focus_sheet()
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
    sw5 = shaper.shape(word)                             # MASS6 styles: bold reaches the bar at 8 px, snap raises
    assert not legibility(word, sw5, 8)[-1] and legibility(word, sw5, 8, {'face': 'b'})[-1]   # contrast, track widens
    assert legibility(word, sw5, 10, {'face': 'b', 'snap': True})[0] > legibility(word, sw5, 10)[0]
    wide = lambda st: (lambda b: (b[2] - b[0], b[3] - b[1]))(render(sw5, 16, st)[1])   # FOCUS-FIX: wide stretches the
    assert wide({'face': 'b', 'wide': 1.25})[0] >= wide({'face': 'b'})[0] * 1.2 and         abs(wide({'face': 'b', 'wide': 1.25})[1] - wide({'face': 'b'})[1]) <= 1 and style_of('wide:1.25') == {'wide': 1.25}   # width only
    wd5 = lambda st: (lambda b: b[2] - b[0])(render(sw5, 10, st)[1])
    assert wd5({'face': 'b', 'track': 1.0}) > wd5({'face': 'b'}) and not style_of('outline:1') and \
        style_of('outline:1+face:b+track:1+snap') == {'face': 'b', 'track': 1.0, 'snap': True}
    bar = img.copy(); bar[20, 30] = 0
    assert np.allclose(fill_bg(bar, (10, 18, 50, 22), 'rowmed')[2], img[20, 10:50])          # one speck gone
    a, b = np.zeros((2, 2, 4), np.float32), np.full((2, 2, 4), 200, np.float32)
    w = np.array([[0, 1], [0.5, 0.5]], np.float32)
    m = blend(a, b, w)
    assert (m[0, 0] == a[0, 0]).all() and (m[0, 1] == b[0, 1]).all() and m[1, 0, 3] == 100 and m[1, 0, 0] == 200
    edge = np.zeros((8, 8, 4), np.float32); edge[..., 3] = 255; edge[:, 4:, :3] = 200   # HUD-SCALE: sharp raises the step
    sh = unsharp(edge, 0.5, 0.8)
    assert sh[0, 4, 0] > 200 and sh[0, 3, 0] == 0 and (sh[..., 3] == 255).all()
    px = {'face': 'plex', 'snap': True}                  # HUD-PLEX: Plex draws other ink than Segoe Bold; the thin Plex
    assert style_of('face:plex+snap') == px and face('plex') == PLEX and \
        render(sw5, 16, px)[1] != render(sw5, 16, {'face': 'b', 'snap': True})[1]   # Regular baseline breaks the
    assert joins(sw5, 16, px) == (1, 1) and joins(sw5, 24, px) == (1, 0) and joins(sw5, 16, {'face': 'b', 'snap': True}) == (1, 0)
    assert bodies(np.pad(np.full((9, 3), 255, np.uint8), 2)) == 1                # meem-seen-ta-waw run at 16 px, not at 24
    two = np.zeros((12, 20), np.uint8); two[:, 2:5] = two[:, 12:15] = 255
    assert bodies(two) == 2 and bodies(np.zeros((5, 5), np.uint8)) == 0
    hm = np.asarray(render(sw5, 16, {'face': 'b', 'hard': 99})[0])   # HUD-CRISP: hard:99 leaves (almost) only 0 / 255
    assert ((hm > 0) & (hm < 255)).mean() < 0.01 and style_of('outline:2+hard:99') == {'hard': 99.0} and \
        np.array_equal(np.asarray(steep(Image.fromarray(np.array([[100, 128, 200]], np.uint8)), 2)), [[72, 128, 255]])
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
