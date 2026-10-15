r"""BUILD-13: review\gpt\R2\proposals.tsv (read only) -> review\corrections\build13_round.tsv (id, old_AR, new_AR, reason), only the ids
approved for this round. Goes through make_batch_corrections.make(): old_AR copied from the current row, new_AR must pass validate.check()
(no ERR, no new flag, tags/args/<br> identical) and contain no U+061F / U+FFFD. A proposal whose old_AR differs from the current AR is skipped
and reported (not written). Usage: python -I tools\make_build13_round.py"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_batch_corrections import make
from tsvlib import load_translation, read_tsv

PROPOSALS = 'review/gpt/R2/proposals.tsv'
DIRECT = '01263 01427 03884 02003 02021 02461 02552 02913 02938 03679 04039 12893 13534 14837 15516'.split()
GLOSSARY = '13217 13397 16172 16321 13474 14822 14158 14550'.split()   # kept only when translation\glossary.tsv agrees (checked by hand, see SKIP)
SKIP = {'14550': 'Sonic Diver: glossary Sonic=approved, but its own example id 10615 is the identical string "Sonic Diver" and keeps the old AR; '
                 'changing only 14550 would split two identical rows'}

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    by = {r['id']: r for r in load_translation()}
    prop = {p[0]: p for p in read_tsv(PROPOSALS)[1:]}
    want = [i for i in DIRECT + GLOSSARY if i not in SKIP]
    draft, skipped = [['id', 'new_AR', 'reason']], dict(SKIP)
    for i in want:
        p = prop[i]
        if p[1] != by[i]['AR']:
            skipped[i] = 'old_AR does not match the current AR'
        elif chr(0x61f) in p[2] or chr(0xfffd) in p[2]:
            skipped[i] = 'new_AR has U+061F or U+FFFD'
        else:
            draft.append([i, p[2], 'GPT R2: ' + p[3]])
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, 'draft.tsv')
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines('\t'.join(r) + '\n' for r in draft)
        make(path, 'build13_round')
    print('applied', sorted(r[0] for r in draft[1:]))
    print('skipped', skipped)
