r"""Apply review\corrections\*.tsv (header: id old_AR new_AR reason) to translation\<cat>\<file>.tsv.
Refuses (changes nothing) if any old_AR differs from the current AR, an id is unknown, or an id repeats.
Applied files move to review\corrections\applied\; review\corrections\LOG.md is appended.
A correction sets AR; status todo -> translated, any other status is kept."""
import datetime, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

HEADER = ['id', 'old_AR', 'new_AR', 'reason']


def apply(root=ROOT):
    cdir = os.path.join(root, 'review', 'corrections')
    files = sorted(f for f in os.listdir(cdir) if f.endswith('.tsv')) if os.path.isdir(cdir) else []
    tables, where = {}, {}
    base = os.path.join(root, 'translation')
    for cat in os.listdir(base):
        d = os.path.join(base, cat)
        if os.path.isdir(d):
            for fn in os.listdir(d):
                if fn.endswith('.tsv'):
                    p = os.path.join(d, fn)
                    tables[p] = read_tsv(p)
                    for r in tables[p][1:]:
                        where[r[0]] = r
    ar_i, st_i = COLS.index('AR'), COLS.index('status')
    plan, errs, seen = [], [], set()
    for fn in files:
        rows = read_tsv(os.path.join(cdir, fn))
        if rows[0] != HEADER:
            errs.append(f'{fn}: bad header {rows[0]}')
            continue
        for r in rows[1:]:
            if len(r) != 4:
                errs.append(f'{fn}: bad row {r[:2]}')
            elif r[0] not in where:
                errs.append(f'{fn}: unknown id {r[0]}')
            elif where[r[0]][ar_i] != r[1]:
                errs.append(f'{fn}: id {r[0]} old_AR does not match current AR')
            elif r[0] in seen:
                errs.append(f'{fn}: id {r[0]} corrected twice')
            else:
                seen.add(r[0])
                plan.append((fn, r))
    if errs:
        raise SystemExit('apply_corrections REFUSED:\n' + '\n'.join(errs))
    for fn, r in plan:
        row = where[r[0]]
        row[ar_i] = r[2]
        if row[st_i] == 'todo':
            row[st_i] = 'translated'
    if plan:
        for p, t in tables.items():
            write_tsv(p, t)
        log = os.path.join(cdir, 'LOG.md')
        new = not os.path.exists(log)
        with open(log, 'a', encoding='utf-8', newline='\n') as f:
            if new:
                f.write('# Corrections log\n')
            f.write(f'\n## {datetime.date.today()} — {len(plan)} applied\n\n')
            for fn, r in plan:
                f.write(f'- {r[0]} ({fn}): {r[3] or "-"}\n')
    if files:
        os.makedirs(os.path.join(cdir, 'applied'), exist_ok=True)
        for fn in files:
            shutil.move(os.path.join(cdir, fn), os.path.join(cdir, 'applied', fn))
    return len(plan)


if __name__ == '__main__':
    print(f'apply_corrections: {apply()} applied')
