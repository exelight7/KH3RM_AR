r"""BATCH-234: draft TSV (id, new_AR, reason) or (id, find, replace, reason: new_AR = the current AR with that fragment, which
must occur exactly once, replaced) -> review\corrections\<name>.tsv (id, old_AR, new_AR, reason) with old_AR copied
exactly from the current translation row. Refuses (writes nothing) unless every new_AR passes tools\validate.py check()
with no ERR flag and no flag the current AR does not already have, differs from the current AR, and the id is translated.
Usage: python -I tools\make_batch_corrections.py <draft.tsv> <name>   (e.g. review\proposed\batch3_draft.tsv batch3_review)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate as v
from tsvlib import load_translation, read_tsv


def make(draft, name):
    rows = load_translation()
    by = {r['id']: r for r in rows}
    gloss = v.build_gloss(v.load_glossary(), v.corpus_lowercase_words(rows))
    out, errs = [['id', 'old_AR', 'new_AR', 'reason']], []
    for d in read_tsv(draft)[1:]:
        i, reason = d[0], d[-1]
        r = by.get(i)
        if not r or r['status'] == 'todo':
            errs.append(f'{i}: unknown or todo')
            continue
        if len(d) == 4:                                   # id, find, replace, reason: the fragment must occur once
            if r['AR'].count(d[1]) != 1:
                errs.append(f'{i}: fragment found {r["AR"].count(d[1])} times')
                continue
            new = r['AR'].replace(d[1], d[2])
        else:
            new = d[1]
        old_f, new_f = set(v.check(r['EN'], r['AR'], r['status'], gloss)), set(v.check(r['EN'], new, r['status'], gloss))
        if new == r['AR'] or '�' in new or new_f & v.ERR or not new_f <= old_f:
            errs.append(f'{i}: same={new == r["AR"]} flags old {sorted(old_f)} new {sorted(new_f)}')
        out.append([i, r['AR'], new, reason])
    if errs:
        raise SystemExit('REFUSED:\n' + '\n'.join(errs))
    path = os.path.join('review', 'corrections', name + '.tsv')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in out)
    print(f'{path}: {len(out) - 1} corrections, validate check() clean')


if __name__ == '__main__':
    make(*sys.argv[1:])
