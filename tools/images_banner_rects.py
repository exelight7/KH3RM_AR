r"""Area banners (IMAGES-MASS): technical\images_rects.tsv rows for the 25 mapName_* textures of the repaint plan.
Lines: alpha row bands of the English; an Arabic of 2+ words is set on 2 lines (the two halves of the English block,
same size), one word on one line over all bands. White plates with cut-out text (bx01-03, ts01-02): the top band is
plain text, the plate keeps its shape and the Arabic is cut out of it (effect knockout). Monstropolis (mi02-04): only
the stencil letters (components >= 40 px tall), the paint splatter stays. mi01 = world logo (kept); tt01 = pilot rows.
Usage: python -I tools\images_banner_rects.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
import texture_codec as tc, texture_text as tt
from tsvlib import load_translation

INV = [l.rstrip('\n').split('\t') for l in open('technical/IMAGES_INVENTORY.tsv', encoding='utf-8')][1:]
PLATE = ('bx01', 'bx02', 'bx03', 'ts01', 'ts02')


def bands(al):
    on = al.sum(1) > 3
    out, i = [], 0
    while i < len(on):
        j = i
        while j < len(on) and on[j]:
            j += 1
        if j - i > 8:
            out.append((i, j))
        i = max(j, i + 1)
    return out


def bbox(m, y0=0, y1=None):
    ys, xs = np.nonzero(m[y0:y1])
    return [int(xs.min()), int(y0 + ys.min()), int(xs.max() + 1), int(y0 + ys.max() + 1)]


def grow(b, g, W=720, H=400):
    return [max(0, b[0] - g), max(0, b[1] - g), min(W, b[2] + g), min(H, b[3] + g)]


def row(a, box, src, eff, scale, size='', erase='', note='', fill='clear'):
    pad = '10' if eff == 'knockout' else '2'             # cut-out text stays clear of the slanted plate edges
    return [a, ' '.join(map(str, box)), src, fill, 'center', eff, f'{scale:.2f}', pad, '0', str(size),
            ' '.join(map(str, erase)) if erase else '', note]


def main():
    tr = {r['id']: r for r in load_translation()}
    out = []
    for r in INV:
        if r[1] != 'title' or 'row ' not in r[9] or r[0].endswith('mapName_tt01.uasset'):
            continue
        a, key = r[0], r[0].split('_')[-1][:-7]
        rid = re.search(r'row (\d+)', r[9]).group(1)
        words = tr[rid]['AR'].split()
        img = tc.rgba0(tc.load('extracted/assets/' + a))
        al = img[..., 3] > 40
        if key.startswith('mi'):                          # stencil letters only
            n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(al.astype(np.uint8), np.ones((5, 5), np.uint8)))
            keep = np.isin(lab, [k for k in range(1, n) if st[k, 3] >= 40])
            al = al & keep
        bs = [b for b in bands(al) if not key.startswith('mi') or b[1] - b[0] >= 40]
        if key.startswith('mi'):
            al[:bs[0][0]] = al[bs[-1][1]:] = False
        eff, note = 'shadow:3:3:2', r[8]
        if key in PLATE:
            top, plate = bs[0], bs[-1]
            pb = bbox(img[..., 3] > 128, plate[0], plate[1])
            inside = (img[..., 3] < 128) & (np.cumsum(img[..., 3] > 128, 1) > 0) & \
                     (np.cumsum((img[..., 3] > 128)[:, ::-1], 1)[:, ::-1] > 0)
            inside[:plate[0]] = inside[plate[1]:] = False
            hb = grow(bbox(inside), 2)
            hb = [max(hb[0], pb[0]), max(hb[1], pb[1]), min(hb[2], pb[2]), min(hb[3], pb[3])]
            tb = grow(bbox(al, top[0], top[1]), 6)
            h = top[1] - top[0]
            if len(words) == 1:
                out.append(row(a, tb, 'blank', 'none', 1, note=note + ' (top word: the Arabic is one word, set on the plate)'))
                out.append(row(a, pb, f'row:{rid}', 'knockout', 1.0, erase=hb, fill='holes', note=note + ' (plate)'))
            else:
                out.append(row(a, tb, f'row:{rid}@0/2', eff, 1.5, note=note + ' (top line)'))
                out.append(row(a, pb, f'row:{rid}@1/2', 'knockout', 1.0, erase=hb, fill='holes', note=note + ' (plate)'))
            continue
        full = grow(bbox(al), 6)
        if len(words) == 1 or len(bs) == 1:
            sc = 1.1 * max(b1 - b0 for b0, b1 in bs) / (full[3] - full[1] - 12)
            out.append(row(a, full, f'row:{rid}', eff, min(0.9, sc), note=note))
        else:
            mid = (full[1] + full[3]) // 2                # two equal lines over the English block
            tb, bb = [full[0], full[1], full[2], mid], [full[0], mid, full[2], full[3]]
            n0 = len(out)
            out.append(row(a, tb, f'row:{rid}@0/2', eff, 1.0, size='~1', note=note + ' (line 1)'))
            out.append(row(a, bb, f'row:{rid}@1/2', eff, 1.0, size='~1', note=note + ' (line 2)'))
    assets = {o[0] for o in out}
    with open(tt.RECTS, encoding='utf-8') as f:
        keep = [l for l in f.read().splitlines() if l.split('\t')[0] not in assets]
    with open(tt.RECTS, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(keep + ['\t'.join(o) for o in out]) + '\n')
    print(len(out), 'rows for', len(assets), 'banners')


if __name__ == '__main__':
    main()
