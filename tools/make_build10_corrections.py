r"""BUILD-10: generate review\corrections\build10_round.tsv from review\gpt\Q3\proposals.tsv (approved ids only).
Group B ids also need the glossary word (GATE) in new_AR; 10521 is skipped when 10502 is. Skips are printed.
Usage: python -I tools/make_build10_corrections.py"""
import difflib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
import validate

sys.stdout.reconfigure(encoding='utf-8')
DIRECT = '08565 08607 08713 08734 09171 09233 09816 09966 10042 10082 10197 10294'.split()
# glossary: Constellation = كوكبة (row 10663), Crystal = بلورة (row 10656), Special+ = مخطط خاص+ (row 10650)
GATE = {'10502': 'كوكب', '10521': 'كوكب', '10517': 'خاص+', '11568': 'بلور', '12476': 'بلور', '12489': 'بلور'}
rows = {r['id']: r for r in load_translation()}
gloss = validate.build_gloss(load_glossary())
P = {r[0]: r for r in read_tsv(os.path.join(ROOT, 'review', 'gpt', 'Q3', 'proposals.tsv'))[1:] if len(r) >= 4}
out, skip = [], {}
for i in DIRECT + list(GATE) + ['11557']:  # 11557 Magma: no glossary gate
    if i not in P: skip[i] = 'not in proposals'; continue
    _, old, new, why = P[i][:4]
    r = rows[i]
    bad = []
    if r['AR'] != old: bad.append('old_AR != current AR')
    f = validate.check(r['EN'], new, 'translated', gloss)
    f = [x for x in f if x not in validate.check(r['EN'], r['AR'], 'translated', gloss)]  # only NEW flags
    if f: bad.append('flags ' + ','.join(map(str, f)))
    if '؟' in new or '�' in new: bad.append('U+061F/U+FFFD')
    if i in GATE and GATE[i] not in new: bad.append('glossary word missing')
    if i == '10521' and '10502' in skip: bad.append('10502 skipped')
    if bad: skip[i] = '; '.join(bad); continue
    out.append((i, old, new, why))
    sm = difflib.SequenceMatcher(None, old, new)
    d = [(old[a:b], new[c:e]) for t, a, b, c, e in sm.get_opcodes() if t != 'equal']
    print(i, 'OK', len(old), len(new), d[:6])
for i, s in skip.items(): print('SKIP', i, s)
with open(os.path.join(ROOT, 'review', 'corrections', 'build10_round.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('id\told_AR\tnew_AR\treason\n')
    f.writelines('\t'.join(o) + '\n' for o in out)
print(len(out), 'written')
