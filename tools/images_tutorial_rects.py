r"""Tutorial pictures (IMAGES-MASS): technical\images_work\tutorial_spec.tsv -> technical\images_rects.tsv rows for every
platform copy of each HelpItem id (rows of those assets are replaced; a copy whose pixels differ in a box is skipped).
spec: id <TAB> box [/ erase box] <TAB> English (by eye) <TAB> align [<TAB> fill <TAB> effect <TAB> source <TAB> scale
      <TAB> rotate <TAB> size]; a single box = the tight old text (erase), outer box = 4 px / 2 px around it; ~box = approximate,
      tightened to the strokes inside it;
      no source = the translation row whose EN equals the English (menu namespaces first; variants printed)
Usage: python -I tools\images_tutorial_rects.py technical\images_work\tutorial_spec.tsv [ids...]"""
import sys, os, collections, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import texture_codec as tc, texture_text as tt
from tsvlib import load_translation
INV = [l.split('	')[0] for l in open('technical/IMAGES_INVENTORY.tsv', encoding='utf-8')][1:]


def copies(i):
    return [a for a in INV if a.endswith('/' + i + '.uasset') and '/HelpItem/' in a]


def main_copy(i):
    c = copies(i)
    return ([a for a in c if '/windows/' in a] or c)[0]


PREF = ['kh3_menu', 'kh3_camp', 'kh3_system', 'kh3_tutorial', 'kh3_gamehelp', 'kh3_settings', 'kh3_item', 'kh3_minigame', 'kh3_level', 'kh3_gumiship', 'kh3_mobile', 'kh3_map']
idx = collections.defaultdict(list)
for r in load_translation():
    idx[' '.join(r['EN'].split()).lower()].append(r)
strings = tt.load_strings()
sidx = {' '.join(r['EN'].split()).lower(): r for r in strings.values()}
def find(en):
    k = ' '.join(en.split()).lower()
    if k in sidx: return 'img:' + sidx[k]['id'], sidx[k]['AR']
    c = [r for r in idx.get(k, []) if r['AR']]
    if not c: return None, None
    rank = lambda r: next((i for i, p in enumerate(PREF) if r['namespace'].startswith(p)), 99)
    c.sort(key=lambda r: (rank(r), r['id']))
    ars = collections.Counter(r['AR'] for r in c)
    return 'row:' + c[0]['id'], c[0]['AR'] + ('' if len(ars) == 1 else f'   [variants: {dict(ars)}]')
def tight(asset, b, fill):
    """bounding box of the text strokes (top-hat, or black-hat for dark text) inside the approximate box b"""
    x0, y0, x1, y1 = b
    reg = tc.rgba0(tc.load('extracted/assets/' + asset)).astype(np.float32)[y0:y1, x0:x1]
    ys, xs = np.nonzero(tt.heal_ink(reg, fill))
    assert len(xs), (asset, b)
    return [x0 + xs.min() + 1, y0 + ys.min() + 1, x0 + xs.max(), y0 + ys.max()]   # heal_ink grows by 1 px


spec = [l.rstrip('\n').split('\t') for l in open(sys.argv[1], encoding='utf-8') if l.strip() and not l.startswith('#')]
only = set(sys.argv[2:])
rows, miss, warn = [], [], []
done = set()
for s in spec:
    i, box, en, align = s[:4]
    if only and i not in only: continue
    fill = s[4] if len(s) > 4 and s[4] else 'heal'
    eff = s[5] if len(s) > 5 and s[5] else 'outline:1'
    src = s[6] if len(s) > 6 and s[6] else None
    scale = s[7] if len(s) > 7 and s[7] else '1.7'
    rot = s[8] if len(s) > 8 and s[8] else '0'
    size = s[9] if len(s) > 9 else ''
    if not src:
        src, ar = find(en)
        if not src: miss.append((i, en)); continue
        print(i, en, '->', src, ar)
    done.add(i)
    if box.startswith('~'):                              # ~ approximate box: tighten to the text strokes inside it
        e = tight(main_copy(i), list(map(int, box[1:].split())), fill)   # (fixed size: 40 px room to the right)
        box = f'{e[0] - 4} {e[1] - 3} {min(768, e[2] + (40 if size else 4))} {e[3] + 3} / {e[0] - 1} {e[1] - 1} {e[2] + 1} {e[3] + 1}'
    box, erase = (box.split('/') + [''])[:2]
    box, erase = box.strip(), erase.strip()
    if not erase:                                        # tight text box given: outer box = 4 px / 2 px around it
        e = list(map(int, box.split()))
        erase, box = box, ' '.join(map(str, [max(0, e[0] - 4), max(0, e[1] - 2), min(768, e[2] + 4), min(432, e[3] + 2)]))
    if size.isdigit():                                   # a fixed size needs room: outer box >= size + 4 px tall
        o = list(map(int, box.split()))
        g = int(size) + 4 - (o[3] - o[1])
        if g > 0:
            o[1], o[3] = max(0, o[1] - g // 2), min(432, o[3] + g - g // 2)
            box = ' '.join(map(str, o))
    b = list(map(int, (erase or box).split()))
    m = tc.rgba0(tc.load('extracted/assets/' + main_copy(i))).astype(int)
    for a in copies(i):
        o = tc.rgba0(tc.load('extracted/assets/' + a)).astype(int)
        d = (np.abs(o[b[1]:b[3], b[0]:b[2]] - m[b[1]:b[3], b[0]:b[2]]).max(-1) > 40).mean()
        if d > 0.12:                                     # BC7 noise between copies is below this
            warn.append((a.split('/')[-2], i, en, round(d, 3))); continue
        rows.append([a, box, src, fill, align, eff, scale, '2', rot, size, erase, en])
print('MISSING', miss); print('COPY DIFFERS (box skipped)', warn)
assets = {r[0] for r in rows}
with open(tt.RECTS, encoding='utf-8') as f:
    keep = [l for l in f.read().splitlines() if l.split('\t')[0] not in assets]
with open(tt.RECTS, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(keep + ['\t'.join(r) for r in rows]) + '\n')
print(len(rows), 'rows for', len(assets), 'assets')
