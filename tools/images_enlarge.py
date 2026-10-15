r"""BATCH-234 / BATCH 4: the boxes of the IMAGES-MASS3 textures that are under the readability bar (RELEASE-091 measure,
out\builds\IMAGES-MASS4\repaint_log.tsv) get a larger font size where their box has room.
Readability depends only on the shaped text and the pixel size (tools\texture_text.py legibility()), so for every
unreadable box the sizes from the shipped size + 1 up to the largest size whose ink fits the whole box (inside
max(pad, 2) px, the margin check) are measured; the smallest readable one is written into technical\images_rects.tsv
(size column = that number, note + " | MASS5: size <n> (shipped <m>)"). Rows that cannot pass stay as they are.
Not touched: rotated rows, '=k' layer rows (they follow their row k), blur / echo rows (no text measure). A '~g' group
gets one common size (the smallest that makes every unreadable row of the group readable and fits every row), or none.
-> technical\images_enlarge_plan.tsv (every unreadable box: before / after / why)
Usage: python -I tools\images_enlarge.py [--dry]"""
import csv, os, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shaper
import texture_text as tt
from tsvlib import load_translation

LOG = 'out/builds/IMAGES-MASS4/repaint_log.tsv'
PLAN = 'technical/images_enlarge_plan.tsv'
MARK = 'MASS5: size'


def load(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def room(visual, r, st=None):
    x0, y0, x1, y1 = map(int, r['box'].split())
    p = max(int(r.get('pad') or 2), tt.MARGIN)
    return tt.fit(visual, x1 - x0 - 2 * p, y1 - y0 - 2 * p, st)[0]


def first_readable(ar, visual, lo, hi, ok=lambda s: True):
    return next((s for s in range(lo, hi + 1) if tt.legibility(ar, visual, s)[-1] and ok(s)), None)


_tex = {}


def covered(r, visual, size, st=None, grow=1):
    """artwork pixels outside the erase box (icons, frames beside the old text: colour far from the box's fitted
    background, or any opaque pixel on a clear texture) under the text's ink bbox (+1 px) at this size, placed as
    repaint() does. A wide text is clamped at the box edge and pushed over such icons, so a larger size may only cover
    artwork the shipped size already covers (HelpItem60610 Everlink: the box reaches over the X icon)"""
    if r['asset'] not in _tex:
        _tex[r['asset']] = tt.tc.rgba0(tt.tc.load(os.path.join('extracted/assets', r['asset']))).astype(np.float32)
    img = _tex[r['asset']]
    x0, y0, x1, y1 = map(int, r['box'].split())
    e0, f0, e1, f1 = map(int, (r.get('erase') or r['box']).split())
    ink = tt.ink_mask(img[f0:f1, e0:e1], tt.fill_bg(img.copy(), (e0, f0, e1, f1), r['fill']), r['fill'])
    ys, xs = np.nonzero(ink)
    ib = (xs.min() + e0 - x0, ys.min() + f0 - y0, xs.max() + 1 + e0 - x0, ys.max() + 1 + f0 - y0) if len(xs) else \
        (e0 - x0, f0 - y0, e1 - x0, f1 - y0)
    mode = 'clear' if r['fill'] == 'clear' else 'fit'
    art = tt.ink_mask(img[y0:y1, x0:x1], tt.fill_bg(img.copy(), (x0, y0, x1, y1), mode), mode)
    art[f0 - y0:f1 - y0, e0 - x0:e1 - x0] = False
    mb = tt.render(visual, size, st)[1]
    pad, bw, bh = int(r.get('pad') or 2), x1 - x0, y1 - y0
    ox = (ib[0] + ib[2]) / 2 - (mb[0] + mb[2]) / 2 if r['align'] == 'center' else ib[0] - mb[0] if r['align'] == 'left' else ib[2] - mb[2]
    oy = (ib[1] + ib[3]) / 2 - (mb[1] + mb[3]) / 2
    ox = int(round(min(max(ox, pad - mb[0]), bw - pad - mb[2])))
    oy = int(round(min(max(oy, pad - mb[1]), bh - pad - mb[3])))
    hit = np.zeros_like(art)
    hit[max(0, oy + mb[1] - grow):oy + mb[3] + grow, max(0, ox + mb[0] - grow):ox + mb[2] + grow] = True
    return hit & art


def main(dry=False):
    sys.stdout.reconfigure(encoding='utf-8')
    tr = {r['id']: r for r in load_translation()}
    strings = tt.load_strings()
    prev = {l.split('\t')[0] for l in open(tt.PREV.replace('MASS4', 'MASS3'), encoding='utf-8').read().splitlines()[1:]}
    rects = load(tt.RECTS)
    cols = list(rects[0].keys())
    log = {}
    for l in load(LOG):                                   # (texture, box, source) -> shipped size + readability
        log.setdefault((l['texture'], l['box'], l['source']), []).append(l)
    seen = {}
    plan, groups = [], {}
    for i, r in enumerate(rects):
        key = (r['asset'].split('/')[-1], r['box'], r['source'])
        n = seen[key] = seen.get(key, -1) + 1
        l = log[key][n]
        if r['asset'] not in prev or 'UNREADABLE' not in l['read' if 'read' in l else 'readability']:
            continue
        ar = tt.arabic(r['source'], tr, strings)
        vis, cur = shaper.shape(ar), int(l['font_px'])
        why = ('rotated' if (r.get('rotate') or '0') != '0' else 'layer row (=k)' if r['size'].startswith('=') else
               'blur / echo' if 'blur:' in r['effect'] or r['fill'].startswith('echo:') else '')
        item = dict(i=i, r=r, ar=ar, vis=vis, cur=cur, read=l['readability'], new=None, why=why)
        plan.append(item)
        if why:
            continue
        if r['size'].startswith('~'):
            groups.setdefault(r['size'], []).append(item)
            continue
        top = room(vis, r)
        base = covered(r, vis, cur) if top > cur else None
        side = lambda s: not (covered(r, vis, s) & ~base).any()
        s = first_readable(ar, vis, cur + 1, top, side) if top > cur else None
        wide = first_readable(ar, vis, cur + 1, top) if top > cur and not s else None
        item['new'], item['why'] = s, (f'readable at {s} px (box allows {top})' if s else
                                       f'readable at {wide} px only by covering artwork beside the old text' if wide else
                                       f'box allows {top} px, not readable up to it' if top > cur else
                                       f'no room (box allows {top} px)')
    for g, items in groups.items():                      # one size for every row of the group
        members = [x for x in rects if x['asset'] == items[0]['r']['asset'] and x['size'] == g]
        top = min(room(shaper.shape(tt.arabic(m['source'], tr, strings)), m) for m in members)
        cur = items[0]['cur']
        s = next((s for s in range(cur + 1, top + 1) if all(tt.legibility(x['ar'], x['vis'], s)[-1] for x in items)), None)
        for x in items:
            x['new'], x['why'] = s, (f'group {g}: all readable at {s} px (group allows {top})' if s else
                                     f'group {g}: allows {top} px, not all readable')
        if s:                                            # the readable members of the group move with it
            for m in members:
                if m not in [x['r'] for x in items]:
                    plan.append(dict(i=rects.index(m), r=m, ar='', vis='', cur=cur, read='READABLE (group member)',
                                     new=s, why=f'group {g} member, follows the group size'))
    done = [p for p in plan if p['new']]
    with open(PLAN, 'w', encoding='utf-8', newline='\n') as f:
        f.write('texture\tbox\tsource\tshipped_px\treadability_mass4\tnew_px\twhy\n')
        f.writelines(f"{p['r']['asset'].split('/')[-1]}\t{p['r']['box']}\t{p['r']['source']}\t{p['cur']}\t{p['read']}\t"
                     f"{p['new'] or '-'}\t{p['why']}\n" for p in plan)
    n_unread = sum(1 for p in plan if 'group member' not in p['read'])
    print(f'unreadable MASS3 boxes {n_unread}; enlarged {sum(1 for p in done if "group member" not in p["read"])} '
          f'(+{len(done) - sum(1 for p in done if "group member" not in p["read"])} group members); '
          f'remain {n_unread - sum(1 for p in done if "group member" not in p["read"])}; textures touched '
          f'{len({p["r"]["asset"] for p in done})}')
    if dry:
        return
    for p in done:
        r = rects[p['i']]
        if MARK in r['note']:
            continue
        r['note'] = f"{r['note']} | {MARK} {p['new']} (shipped {p['cur']}, was '{r['size']}')".strip(' |')
        r['size'] = str(p['new'])
    with open(tt.RECTS, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(cols) + '\n')
        f.writelines('\t'.join(r[c] for c in cols) + '\n' for r in rects)
    print(f'{tt.RECTS}: {len(done)} size cells changed')


if __name__ == '__main__':
    main(sys.argv[1:] == ['--dry'])
