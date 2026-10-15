r"""IMAGES-MASS6: the boxes of IMAGES-MASS5 under the readability bar (out\builds\IMAGES-MASS5\repaint_log.tsv,
UNREADABLE; tools\texture_text.py legibility()) and the battle HUD gauge words (HudStatusTxt, HudStatusTxtCA: the
owner's FOCUS screenshot, thin next to the heavy English) get the first rendering, in this order, that passes:
  (a) a larger size (old face) up to the box limit
  (b) a heavier weight: Segoe UI Bold / Semibold, a 1 / 0.5 px stroke in the text colour, + 0.5-1 px letter spacing
  (c) the same with 'snap' (stems at the best pixel phase, dots as whole pixels 1 px off the letters)
  (d) 'halo' (thin dark / light ring under the text) where it raises the edge contrast (bg_contrast) by >= 20
Pass = the bar (contrast >= 192 and continuity) or, when no candidate reaches it, a measurable gain: fewer component
errors with contrast not lower, or contrast + 16 with errors not higher. Sizes: fit rows from the largest that fits
the box (margin) down to 2 px under the shipped one, fixed-size rows (phrase pieces) keep their size; no candidate may
cover artwork the shipped text does not cover (images_enlarge.covered). Not touched: rotated, '=k' layer rows (they get
the style of their row k), blur / echo rows.
-> technical\images_rects.tsv (effect + tokens, size, note ' | MASS6: bar|improved ...'),
   technical\images_sharpen_plan.tsv (every box: before / after / method / why)
Usage: python -I tools\images_sharpen.py [--dry]"""
import csv, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shaper
import texture_text as tt
import texture_codec as tc
from images_enlarge import load, room, covered
from tsvlib import load_translation

LOG = 'out/builds/IMAGES-MASS5/repaint_log.tsv'
PLAN = 'technical/images_sharpen_plan.tsv'
MARK = 'MASS6:'
HUD = ('HudStatusTxt.uasset', 'HudStatusTxtCA.uasset')
B = [dict(face='b'), dict(face='sb'), dict(stroke=1.0), dict(stroke=0.5), dict(face='b', track=1.0),
     dict(face='sb', track=1.0), dict(stroke=0.5, track=0.5)]
TRY = [('a', {})] + [('b', s) for s in B] + [('c', dict(s, snap=True)) for s in [{}] + B]


def tokens(st):
    return '+'.join(f'{k}:{st[k]:g}' if k in ('stroke', 'track') else f'face:{st[k]}' if k == 'face' else k
                    for k in ('face', 'stroke', 'track', 'snap') if k in st)


def err(n, nr, k, size):
    return 0 if size >= tt.BIG else max(nr - k - n, n - nr, 0)


def main(dry=False):
    sys.stdout.reconfigure(encoding='utf-8')
    tr = {r['id']: r for r in load_translation()}
    strings = tt.load_strings()
    rects = load(tt.RECTS)
    cols = list(rects[0].keys())
    log, seen, plan = {}, {}, []
    for l in load(LOG):
        log.setdefault((l['texture'], l['box'], l['source']), []).append(l)
    for i, r in enumerate(rects):
        name = r['asset'].split('/')[-1]
        key = (name, r['box'], r['source'])
        n = seen[key] = seen.get(key, -1) + 1
        l = log[key][n]
        if MARK in r['note'] or not ('UNREADABLE' in l['readability'] or name in HUD and l['readability'] != '-'):
            continue
        ar = tt.arabic(r['source'], tr, strings)
        vis, cur = shaper.shape(ar), int(l['font_px'])
        c0, n0, nr, k, ok0 = tt.legibility(ar, vis, cur)
        p = dict(i=i, r=r, ar=ar, vis=vis, cur=cur, before=l['readability'], ok0=ok0, method='-', st=None, new=cur,
                 after='', halo=False, bgc='-', why='')
        plan.append(p)
        skip = ('rotated' if (r.get('rotate') or '0') != '0' else 'layer row (=k): follows its row k' if r['size'].startswith('=')
                else 'group row (~g)' if r['size'].startswith('~') else
                'blur / echo' if 'blur:' in r['effect'] or r['fill'].startswith('echo:') else '')
        if skip:
            p['why'] = skip
            continue
        e0 = err(n0, nr, k, cur)
        better = lambda c, e: (e < e0 and c >= c0) or (e <= e0 and c >= c0 + 16)
        base = covered(r, vis, cur)
        fixed = r['size'].isdigit()
        best, art = None, None                            # best gain (no bar), best candidate stopped by artwork
        for m, st in TRY:
            top = room(vis, r, st or None)
            sizes = [min(cur, top)] if fixed else list(range(top, max(5, cur - 2) - 1, -1))
            if m == 'a':
                sizes = [s for s in sizes if s > cur]
            for s in sizes:
                c, nn, _, _, ok = tt.legibility(ar, vis, s, st or None)
                e = err(nn, nr, k, s)
                if not (ok and (not ok0 or better(c, e))) and not better(c, e):
                    continue
                if (covered(r, vis, s, st or None) & ~base).any():
                    art = art or (m, st, s)
                    continue
                if ok and (not ok0 or better(c, e)):
                    p.update(method=m, st=st, new=s, after=f'contrast {c}, components {nn} of {nr} (k {k}), READABLE',
                             kind='bar' if not ok0 else 'improved')
                    break
                if best is None or (e, -c, -s) < best[0]:
                    best = ((e, -c, -s), m, st, s, f'contrast {c}, components {nn} of {nr} (k {k}), UNREADABLE')
            if p['method'] != '-':
                break
        if p['method'] == '-' and best:
            _, m, st, s, after = best
            p.update(method=m, st=st, new=s, after=after, kind='improved')
        if p['method'] == '-':
            p['why'] = (f'best candidate ({art[0]} {tokens(art[1]) or "plain"} {art[2]} px) covers artwork' if art else
                        'no candidate reaches the bar or improves contrast / continuity')
    # (d) halo: measured on the repainted box (texture as extracted), with the chosen style
    todo = [p for p in plan if not p['why'].startswith(('rotated', 'layer', 'group', 'blur'))]
    for asset in sorted({p['r']['asset'] for p in todo}):
        img = tc.rgba0(tc.load(os.path.join('extracted/assets', asset))).astype(np.float32)
        for p in [p for p in todo if p['r']['asset'] == asset]:
            r = dict(p['r'])
            if p['st']:
                r.update(effect=r['effect'] + '+' + tokens(p['st']), size=str(p['new']))
            b0 = tt.repaint(img.copy(), r, p['ar'])['bgc']
            b1 = tt.repaint(img.copy(), dict(r, effect=r['effect'] + '+halo'), p['ar'])['bgc']
            p['bgc'] = f'{b0} -> {b1}'
            if b1 - b0 >= 20 and not (covered(p['r'], p['vis'], p['new'], p['st'] or None, 2) & ~covered(p['r'], p['vis'], p['cur'])).any():
                p['halo'] = True
                p.setdefault('kind', 'improved')
                if p['method'] == '-':
                    p['why'] = ''
    with open(PLAN, 'w', encoding='utf-8', newline='\n') as f:
        f.write('texture\tbox\tsource\tshipped_px\treadability_mass5\tmethod\ttokens\tnew_px\treadability_mass6\t'
                'bg_contrast_halo\tresult\twhy\n')
        for p in plan:
            meth = p['method'] + ('+d' if p['halo'] else '') if p['method'] != '-' else 'd' if p['halo'] else '-'
            tok = '+'.join(x for x in [tokens(p['st'] or {}), 'halo' * p['halo']] if x)
            res = 'kept (MASS5)' if meth == '-' else p.get('kind', '-')
            f.write(f"{p['r']['asset'].split('/')[-1]}\t{p['r']['box']}\t{p['r']['source']}\t{p['cur']}\t{p['before']}\t"
                    f"{meth}\t{tok or '-'}\t{p['new'] if p['method'] != '-' else '-'}\t{p['after'] or '-'}\t{p['bgc']}\t"
                    f"{res}\t{p['why'] or '-'}\n")
    under = [p for p in plan if not p['ok0']]
    by = lambda ps, m: sum(1 for p in ps if p['method'] == m)
    print(f'under the bar in MASS5: {len(under)}; HUD gauge rows also tried: {len(plan) - len(under)}')
    for kind in ('bar', 'improved'):
        ps = [p for p in under if p.get('kind') == kind and p['method'] != '-']
        print(f"  {kind}: a {by(ps, 'a')}, b {by(ps, 'b')}, c {by(ps, 'c')}")
    print(f"  halo (d) shipped on {sum(p['halo'] for p in plan)} boxes ({sum(p['halo'] and p['method'] == '-' for p in plan)} halo only)")
    print(f"  still under the bar: {sum(1 for p in under if p.get('kind') != 'bar')}")
    if dry:
        return
    for p in plan:
        if p['method'] == '-' and not p['halo']:
            continue
        r = rects[p['i']]
        tok = '+'.join(x for x in [tokens(p['st'] or {}), 'halo' * p['halo']] if x)
        was = f"size '{r['size'] or 'fit'}', effect '{r['effect']}'"
        if tok:
            r['effect'] = r['effect'] + '+' + tok
        if p['method'] != '-':
            r['size'] = str(p['new'])
        meth = p['method'] + ('+d' if p['halo'] else '') if p['method'] != '-' else 'd'
        r['note'] = f"{r['note']} | {MARK} {p.get('kind', 'improved')} ({meth}) {tok} {p['new']} px (shipped {p['cur']}, was {was})".strip(' |')
        if p['st']:                                       # '=k' layers of this row draw the same word: same style
            same = [x for x in rects if x['asset'] == r['asset']]
            for x in same:
                if x['size'] == f'={same.index(r)}' and MARK not in x['note']:
                    x['effect'] = x['effect'] + '+' + tokens(p['st'])
                    x['note'] = f"{x['note']} | {MARK} layer of a MASS6 row, style {tokens(p['st'])}".strip(' |')
    with open(tt.RECTS, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(cols) + '\n')
        f.writelines('\t'.join(r[c] for c in cols) + '\n' for r in rects)
    print(f"{tt.RECTS}: {sum(1 for r in rects if MARK in r['note'])} rows marked {MARK}")


if __name__ == '__main__':
    main(sys.argv[1:] == ['--dry'])
