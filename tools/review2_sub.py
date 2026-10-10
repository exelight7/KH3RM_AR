r"""REVIEW-2 helper: substring fixes. Usage: python -I tools\review2_sub.py N file ; file lines 'id<TAB>old_fragment<TAB>new_fragment<TAB>reason'
-> review\corrections\review2_pNN.tsv (full old_AR / new_AR from the current text)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
import review2_page as rp
n, path = int(sys.argv[1]), sys.argv[2]
cur = {r['id']: r['AR'] for _, r in rp.page(load_translation(), n)}
out = ['id\told_AR\tnew_AR\treason']
for ln in open(path, encoding='utf-8'):
    ln = ln.rstrip('\n')
    if ln.strip():
        i, a, b, why = (ln.split('\t') + [''])[:4]
        assert a in cur[i], (i, a)
        out.append(f'{i}\t{cur[i]}\t{cur[i].replace(a, b, 1)}\t{why}')
open(os.path.join(rp.ROOT, 'review', 'corrections', f'review2_p{n:02d}.tsv'), 'w', encoding='utf-8', newline='').write('\n'.join(out) + '\n')
print(len(out) - 1, 'fixes')
