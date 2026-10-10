r"""Repaint English text inside a texture with Arabic (FINAL-1 part 2, image pilot).

For every row of technical\images_rects.tsv (asset, box x0 y0 x1 y1, Arabic source, fill, align, effect):
  1. ink   = the original text pixels inside the box (differ from the background estimate) -> position and size
  2. fill  = the box is refilled from its surroundings: clear (transparent textures), vlerp/hlerp (per column/row linear
             gradient between the pixels just outside the box), fit (quadratic surface through the box's own non-text
             pixels: gradients without touching neighbouring lines), flat (median of the ring around the box)
  3. style = fill colour (and outline/glow/shadow colours) sampled from the original ink: brightest core = fill,
             darkest opaque edge = outline, half-transparent halo = glow, dark offset copy = shadow
  4. text  = the Arabic of a translation\ row (or an approved glossary term), pre-shaped by tools\shaper.py (presentation
             forms, visual order) and drawn with the Segoe UI outlines (C:\Windows\Fonts\segoeui.ttf, the font of the game
             build) with Pillow's BASIC layout (no second bidi pass), 4x supersampled; centred on / aligned to the old ink
The edited mip 0 goes back through tools\texture_codec.py (only the changed 4x4 blocks are re-encoded).
Usage: python -I tools\texture_text.py preview            -> out\builds\IMAGES-PILOT\preview\*_before.png / *_after.png
       python -I tools\texture_text.py pilot              -> out\builds\IMAGES-PILOT\pakchunk98-arabic-images_P.pak + verify
       python -I tools\texture_text.py --installed        -> the pak in ~mods = this build (sha)"""
import csv, hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import shaper
import texture_codec as tc
from tsvlib import load_translation

RECTS = 'technical/images_rects.tsv'
OUT = 'out/builds/IMAGES-PILOT'
PAK = os.path.join(OUT, 'pakchunk98-arabic-images_P.pak')
MODS = r'C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods'
REPAK = os.path.abspath('tools/repak-0.2.3/repak.exe')
FONT = r'C:\Windows\Fonts\segoeui.ttf'
SS = 4                                                   # supersampling


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
    if mode == 'flat':
        ring = np.concatenate([img[y0 - 1, x0 - 1:x1 + 1], img[y1, x0 - 1:x1 + 1], img[y0:y1, x0 - 1], img[y0:y1, x1]])
        return np.broadcast_to(np.median(ring, 0), (h, w, 4)).copy()
    raise ValueError(mode)


def ink_mask(orig, bg, mode):
    if mode == 'clear':
        return orig[..., 3] > 24
    return np.abs(orig[..., :3] - bg[..., :3]).max(-1) > 48


# ---- style --------------------------------------------------------------------------------------------
def hexc(c):
    return '#' + ''.join(f'{int(round(v)):02x}' for v in c[:3])


def sample(orig, bg, ink, mode):
    """fill / outline / halo colours from the original text pixels"""
    px = orig[ink]
    lum = px[..., :3] @ np.array([0.299, 0.587, 0.114])
    if mode == 'clear':
        core = px[px[:, 3] > 230]
        cl = core[..., :3] @ np.array([0.299, 0.587, 0.114])
        fill = np.median(core[cl >= np.percentile(cl, 70)], 0)
        edge = np.median(core[cl <= np.percentile(cl, 15)], 0)
        soft = orig[(orig[..., 3] > 8) & (orig[..., 3] < 160)]
        halo = np.median(soft, 0) if len(soft) > 30 else None
        return dict(fill=fill, outline=edge, halo=halo)
    d = np.abs(px[..., :3] - bg[ink][..., :3]).max(-1)
    fill = np.median(px[d >= np.percentile(d, 70)], 0)
    dark = px[lum <= np.percentile(lum, 10)]
    return dict(fill=fill, outline=np.median(dark, 0), halo=None)


# ---- text ---------------------------------------------------------------------------------------------
def arabic(src, rows):
    """'row:<id>' -> AR of that translation row; tags removed (none expected in UI labels)"""
    kind, val = src.split(':', 1)
    assert kind == 'row', src
    ar = rows[val]['AR']
    assert ar and not re.search(r'<[^>]+>|\{\d', ar), (val, ar)
    return ar


def ss(px):
    """small text is drawn at 1x so FreeType hinting keeps dots and hamza; large text 4x supersampled"""
    return 1 if px < 24 else SS


def mask(visual, px):
    k = ss(px)
    font = ImageFont.truetype(FONT, px * k, layout_engine=ImageFont.Layout.BASIC)
    l, t, r, b = font.getbbox(visual)
    m = Image.new('L', (r - l + 8 * k, b - t + 8 * k), 0)
    ImageDraw.Draw(m).text((4 * k - l, 4 * k - t), visual, font=font, fill=255)
    return m


def fit(visual, w, h):
    """largest pixel size whose ink fits w x h -> (size, L mask at 1x, ink bbox in the mask)"""
    lo, hi = 4, 400
    while lo < hi:
        mid = (lo + hi + 1) // 2
        bb = mask(visual, mid).getbbox()
        if (bb[2] - bb[0]) / ss(mid) <= w and (bb[3] - bb[1]) / ss(mid) <= h:
            lo = mid
        else:
            hi = mid - 1
    m = mask(visual, lo)
    m = m.resize((m.width // ss(lo), m.height // ss(lo)), Image.LANCZOS)
    return lo, m, m.getbbox()


def effect_layers(m, eff, st):
    """[(alpha mask, rgb)] bottom to top; eff like 'shadow:2:3:4', 'outline:1', 'glow:5', joined by '+'"""
    out = []
    for e in [x for x in eff.split('+') if x and x != 'none']:
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
    out.append((np.asarray(m, np.float32) / 255, st['fill'][:3]))
    return out


def over(dst, alpha, rgb):
    """straight-alpha 'over' of a solid colour with coverage alpha onto dst (h, w, 4) float 0..255"""
    a0 = dst[..., 3:] / 255
    a1 = alpha[..., None]
    ao = a1 + a0 * (1 - a1)
    c = (np.asarray(rgb, np.float32) * a1 + dst[..., :3] * a0 * (1 - a1)) / np.maximum(ao, 1e-6)
    dst[..., :3] = np.where(ao > 0, c, dst[..., :3])
    dst[..., 3:] = ao * 255


def repaint(img, r, ar):
    x0, y0, x1, y1 = map(int, r['box'].split())
    orig = img[y0:y1, x0:x1].copy()
    bg = fill_bg(img, (x0, y0, x1, y1), r['fill'])
    ink = ink_mask(orig, bg, r['fill'])
    ys, xs = np.nonzero(ink)
    ib = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)          # old ink, box coordinates
    st = sample(orig, bg, ink, r['fill'])
    visual = shaper.shape(ar)
    pad = int(r.get('pad') or 2)
    rot = int(r.get('rotate') or 0)
    if rot:                                              # vertical label: fit along the box height, then turn
        size, m, mb = fit(visual, (y1 - y0) - 2 * pad, min((x1 - x0) - 2 * pad, (ib[2] - ib[0]) * float(r['scale'])))
        m = m.rotate(rot, expand=True)
        mb = m.getbbox()
    else:
        size, m, mb = fit(visual, (x1 - x0) - 2 * pad, min((y1 - y0) - 2 * pad, (ib[3] - ib[1]) * float(r['scale'])))
    layers = effect_layers(m, r['effect'], st)
    # place: vertical centre on the old ink; horizontal by align
    cy = (ib[1] + ib[3]) / 2
    if r['align'] == 'center':
        ox = (ib[0] + ib[2]) / 2 - (mb[0] + mb[2]) / 2
    elif r['align'] == 'left':
        ox = ib[0] - mb[0]
    else:
        ox = ib[2] - mb[2]
    oy = cy - (mb[1] + mb[3]) / 2
    ox = int(round(min(max(ox, pad - mb[0]), (x1 - x0) - pad - mb[2])))
    oy = int(round(min(max(oy, pad - mb[1]), (y1 - y0) - pad - mb[3])))
    out = bg.copy()
    for alpha, rgb in layers:
        a = np.zeros(out.shape[:2], np.float32)
        sy0, sx0 = max(0, -oy), max(0, -ox)
        dy0, dx0 = max(0, oy), max(0, ox)
        hh = min(alpha.shape[0] - sy0, out.shape[0] - dy0)
        ww = min(alpha.shape[1] - sx0, out.shape[1] - dx0)
        a[dy0:dy0 + hh, dx0:dx0 + ww] = alpha[sy0:sy0 + hh, sx0:sx0 + ww]
        over(out, a, rgb)
    img[y0:y1, x0:x1] = out
    return dict(size=size, fill=hexc(st['fill']), outline=hexc(st['outline']),
                halo='-' if st['halo'] is None else hexc(st['halo']), ink=ib, text=ar)


def rows_by_asset():
    with open(RECTS, encoding='utf-8') as f:
        rs = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
    by = {}
    for r in rs:
        by.setdefault(r['asset'], []).append(r)
    return by


def edit_all(save_previews=True):
    tr = {r['id']: r for r in load_translation()}
    out, log = {}, []
    os.makedirs(os.path.join(OUT, 'preview'), exist_ok=True)
    for asset, rs in rows_by_asset().items():
        t = tc.load(os.path.join('extracted/assets', asset))
        img = tc.rgba0(t).astype(np.float32)
        before = img.copy()
        for r in rs:
            info = repaint(img, r, arabic(r['source'], tr))
            log.append([asset.split('/')[-1], r['box'], r['source'], str(info['size']), info['fill'], info['outline'], info['halo']])
        new = np.clip(np.round(img), 0, 255).astype(np.uint8)
        name = asset.split('/')[-1][:-7]
        if save_previews:
            for tag, a in (('before', before.astype(np.uint8)), ('after', new)):
                im = Image.fromarray(a, 'RGBA')
                bgc = Image.new('RGBA', im.size, (36, 52, 84, 255))
                Image.alpha_composite(bgc, im).save(os.path.join(OUT, 'preview', f'{name}_{tag}.png'))
        ua, ue, ub = tc.write(t, tc.mip_chain(t, new))
        stem = asset[:-7]
        out[stem + '.uasset'], out[stem + '.uexp'] = ua, ue
        if ub:
            out[stem + '.ubulk'] = ub
    return out, log


def pilot():
    sys.stdout.reconfigure(encoding='utf-8')
    files, log = edit_all()
    root = os.path.join(OUT, 'pakroot')
    for rel, data in files.items():
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        open(os.path.join(root, rel), 'wb').write(data)
    stale = [os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs
             if os.path.relpath(os.path.join(d, f), root).replace(os.sep, '/') not in files]
    assert not stale, f'unexpected files in {root}: {stale}'
    subprocess.run([REPAK, 'pack', '--version', 'V4', '--compression', 'Zlib', '--mount-point', '../../../', root, PAK],
                   check=True, capture_output=True)
    listed = subprocess.run([REPAK, 'list', PAK], check=True, capture_output=True, text=True).stdout.splitlines()
    hl = dict(l.split(' ', 1)[::-1] for l in subprocess.run([REPAK, 'hash-list', PAK], check=True, capture_output=True,
                                                             text=True).stdout.splitlines() if l.strip())
    unp = os.path.join(OUT, 'unpacked')
    subprocess.run([REPAK, 'unpack', '-q', '-f', '-o', unp, PAK], check=True, capture_output=True)
    assert sorted(listed) == sorted(files), set(listed) ^ set(files)
    rep = [['path_in_pak', 'sha256_original', 'sha256_input', 'sha256_repak_hash_list', 'sha256_unpacked', 'reparse', 'result']]
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
    with open(os.path.join(OUT, 'pak_verify_sha256.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in rep)
    with open(os.path.join(OUT, 'repaint_log.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('texture\tbox\tsource\tfont_px\tfill\toutline\thalo\n')
        f.writelines('\t'.join(r) + '\n' for r in log)
    print(f'{len(files)} files PASS; {len(log)} text boxes repainted')
    print(f'{PAK}: {os.path.getsize(PAK)} B sha256 {sha(open(PAK, "rb").read())}')


def self_check():
    """synthetic: vlerp keeps a gradient, the shaped text is drawn right-to-left (first logical letter on the right)"""
    img = np.zeros((40, 60, 4), np.float32)
    img[..., 0] = np.arange(40)[:, None] * 5
    img[..., 3] = 255
    f = fill_bg(img, (10, 10, 50, 30), 'vlerp')
    assert np.allclose(f[:, :, 0], img[10:30, 10:50, 0], atol=0.01)
    vis = shaper.shape(chr(0x0628) + chr(0x0627))           # ba + alef: visual order puts alef (final) left of ba
    m = np.asarray(mask(vis, 40))
    assert vis[0] != chr(0x0628) and m.any()
    print('texture_text self check: PASS')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        self_check()
    elif a[0] == 'preview':
        print(edit_all()[1])
    elif a[0] == 'pilot':
        pilot()
    elif a[0] == '--installed':
        got = sha(open(os.path.join(MODS, os.path.basename(PAK)), 'rb').read())
        assert got == sha(open(PAK, 'rb').read()), 'the pak in ~mods is not this build'
        print('installed pilot pak = build', got)
