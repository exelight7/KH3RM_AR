r"""BUILD-9: generate review\corrections\build9_round.tsv from review\proposed\BUILD9_proposed.tsv (+ 10847 wording from
argv[1], plural form) and the 8 approved ids of review\gpt\Q2\proposals.tsv. Skips (old_AR mismatch, glossary, validate) are printed.
Usage: python -I tools/make_build9_corrections.py <file with the 10847 new_AR>"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
import validate

sys.stdout.reconfigure(encoding='utf-8')
GPT = '04538 04915 06712 07464 07515 07903 07339 08531'.split()
rows = {r['id']: r for r in load_translation()}
gloss = validate.build_gloss(load_glossary())
cand = [r for r in read_tsv(os.path.join(ROOT, 'review', 'proposed', 'BUILD9_proposed.tsv'))[1:] if len(r) >= 4]
plural = open(sys.argv[1], encoding='utf-8').read().strip()
cand = [[r[0], r[1], plural if r[0] == '10847' else r[2], r[3]] for r in cand]
g = {r[0]: r for r in read_tsv(os.path.join(ROOT, 'review', 'gpt', 'Q2', 'proposals.tsv'))[1:] if len(r) >= 4}
cand += [g[i] for i in GPT]
out, skip = [], []
for i, old, new, why in cand:
    r = rows[i]
    f = validate.check(r['EN'], new, 'translated', gloss) if True else []
    bad = []
    if r['AR'] != old: bad.append('old_AR != current AR')
    if f: bad.append('flags ' + ','.join(f))
    if '؟' in new or '�' in new: bad.append('U+061F/U+FFFD')
    (skip if bad else out).append((i, old, new, why) if not bad else (i, bad))
    if not bad: print(i, 'OK', r['EN'][:60].replace('\n', ' '))
for s in skip: print('SKIP', s)
with open(os.path.join(ROOT, 'review', 'corrections', 'build9_round.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('id\told_AR\tnew_AR\treason\n')
    f.writelines('\t'.join(o) + '\n' for o in out)
print(len(out), 'written')
