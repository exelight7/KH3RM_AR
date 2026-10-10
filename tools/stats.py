r"""Write state\STATS.md. translated = status in translated/reviewed/verified; reviewed = reviewed/verified;
verified-by-screenshot = ids with a PASS line in state\SCREENSHOT_LOG.tsv (or status verified);
installed = ids in state\INSTALLED.tsv (written after an install) whose AR is still the installed one."""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

LOG = os.path.join(ROOT, 'state', 'SCREENSHOT_LOG.tsv')
rows = load_translation()
shot = set()
if os.path.exists(LOG):
    for r in read_tsv(LOG)[1:]:
        if r[4].strip().upper().startswith('PASS'):
            shot.update(x.strip() for x in r[2].split(',') if x.strip())
INST = os.path.join(ROOT, 'state', 'INSTALLED.tsv')
inst = {r[0]: r[1] for r in read_tsv(INST)[1:]} if os.path.exists(INST) else {}
ar_hash = lambda ar: hashlib.sha1(ar.encode('utf-8')).hexdigest()[:10]  # same as toolsuild_build1.py
pct = lambda a, b: f'{100 * a / b:.1f}%' if b else '-'
L = ['# STATS', '', '| category | rows | translated | installed | reviewed | verified-by-screenshot |', '|---|---|---|---|---|---|']
for cat in CATEGORIES + ['TOTAL']:
    rs = rows if cat == 'TOTAL' else [r for r in rows if r['category'] == cat]
    n = len(rs)
    t = sum(r['status'] != 'todo' for r in rs)
    v = sum(r['status'] in ('reviewed', 'verified') for r in rs)
    s = sum(r['status'] == 'verified' or r['id'] in shot for r in rs)
    i = sum(inst.get(r['id']) == ar_hash(r['AR']) for r in rs)
    L.append(f'| {cat} | {n} | {t} ({pct(t, n)}) | {i} ({pct(i, n)}) | {v} ({pct(v, n)}) | {s} ({pct(s, n)}) |')
open(os.path.join(ROOT, 'state', 'STATS.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('\n'.join(L[2:]))
