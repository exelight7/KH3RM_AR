r"""Apply review\corrections\*.tsv (header: id old_AR new_AR reason) to translation\<cat>\<file>.tsv.
Refuses (changes nothing) if any old_AR differs from the current AR, an id is unknown, or an id repeats.
Applied files move to review\corrections\applied\; review\corrections\LOG.md is appended.
A correction sets AR; status todo -> translated, any other status is kept.
Cloud review (CLOUD-PREP): files in review\corrections\cloud\*.tsv use the same header; a row with new_AR == old_AR just marks
the row as checked. Every row of a cloud file ends status reviewed (verified is kept; a todo row with empty AR is untouched)
with note "cloud review pass 2" added. Applied cloud files move to review/corrections/applied/cloud/."""
import datetime, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

HEADER = ['id', 'old_AR', 'new_AR', 'reason']
CLOUD_NOTE = 'cloud review pass 2'


def apply(root=ROOT):
    cdir = os.path.join(root, 'review', 'corrections')
    files = sorted(f for f in os.listdir(cdir) if f.endswith('.tsv')) if os.path.isdir(cdir) else []
    cloud = os.path.join(cdir, 'cloud')
    if os.path.isdir(cloud):
        files += ['cloud/' + f for f in sorted(os.listdir(cloud)) if f.endswith('.tsv')]
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
    ar_i, st_i, nt_i = COLS.index('AR'), COLS.index('status'), COLS.index('note')
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
                # parallel cloud branches may touch the same id: identical results or a check mark (new == old) plus one
                # real change are merged (the real change wins); two different real changes stay an error
                i = next(k for k, (_, p) in enumerate(plan) if p[0] == r[0])
                p = plan[i][1]
                if p[2] == r[2] or r[2] == r[1]:
                    continue
                if p[2] == p[1]:
                    plan[i] = (fn, r)
                else:
                    errs.append(f'{fn}: id {r[0]} corrected twice')
            else:
                seen.add(r[0])
                plan.append((fn, r))
    if errs:
        raise SystemExit('apply_corrections REFUSED:\n' + '\n'.join(errs))
    for fn, r in plan:
        row = where[r[0]]
        row[ar_i] = r[2]
        if fn.startswith('cloud/'):
            if row[ar_i] and row[st_i] != 'verified':
                row[st_i] = 'reviewed'
            if row[ar_i] and CLOUD_NOTE not in row[nt_i]:
                row[nt_i] = f'{row[nt_i]}; {CLOUD_NOTE}' if row[nt_i] else CLOUD_NOTE
        elif row[st_i] == 'todo':
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
            dst = os.path.join(cdir, 'applied', fn)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(os.path.join(cdir, fn), dst)
    return len(plan)


if __name__ == '__main__':
    print(f'apply_corrections: {apply()} applied')
