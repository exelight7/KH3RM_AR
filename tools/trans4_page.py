r"""TRANS-4 helper: story dialogue and cutscene subtitles page by page in the order of review\script\ (script_NNN.md,
300 rows; categories dialogue + subtitles_cutscenes only, Re Mind rows are category remind and are left out).
`dump N`  prints the todo rows of script page N (id, scene, speaker, EN) that need a human translation; rows whose EN
          was already translated in dialogue/subtitles get the same AR (translation memory); blank rows are skipped;
          then the approved glossary terms found on the page.
`apply N file` reads lines '<id> <AR>' (optional ' ## <unsure note>') and writes AR + status translated
          (note 'TRANS-4' or 'TRANS-4 unsure: ...'); TM rows of the page are filled the same way.
Usage: python -I tools\trans4_page.py dump|apply N [file]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
import make_script
from validate import build_gloss, corpus_lowercase_words

CATS = ('dialogue', 'subtitles_cutscenes')
PAGE = make_script.PAGE


def page_rows(rows, n):
    """(scene, row) of script page n (same order as review\\script\\script_NNN.md)"""
    flat = [(sc, r) for _, sc, rs in make_script.story(rows) for r in rs]
    return flat[(n - 1) * PAGE:n * PAGE]


def tm(rows):
    return {r['EN']: r['AR'] for r in rows if r['category'] in CATS + ('remind',) and r['AR'] and r['status'] != 'todo'}


def todo(r):
    return bool(r['category'] in CATS and r['status'] == 'todo' and not r['AR'] and r['EN'].strip())


def dump(n):
    rows = load_translation()
    mem, seen, filled = tm(rows), set(), 0
    page = page_rows(rows, n)
    last = None
    for sc, r in page:
        if not todo(r):
            continue
        if r['EN'] in mem:
            filled += 1
            continue
        if sc != last:
            print(f'# {sc}')
            last = sc
        print(f"{r['id']} [{make_script.speaker(r)}]{' (dup)' if r['EN'] in seen else ''} {r['EN']}")
        seen.add(r['EN'])
    gloss = build_gloss(load_glossary(), corpus_lowercase_words(rows))
    text = '\n'.join(norm_en(r['EN']) for _, r in page if todo(r))
    hits = sorted({d['en'] + '=' + d['ar'] for d in load_glossary() if d['status'] == 'approved' and d['type'] != 'menu'
                   and term_re(d['en'], 0).search(text)})
    print(f'## page {n}: {len(page)} rows, todo {sum(todo(r) for _, r in page)}, from TM {filled}; '
          f'not ours (remind/other): {sum(r["category"] not in CATS for _, r in page)}')
    print('## glossary: ' + ' | '.join(hits))


def apply(n, path):
    new, notes = {}, {}
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.strip() and not line.startswith('#'):
            rid, ar = line[:5], line[6:]
            if ' ## ' in ar:
                ar, notes[rid] = ar.split(' ## ', 1)
            new[rid] = ar.strip()
    rows = load_translation()
    mem = tm(rows)
    page = {r['id']: r for _, r in page_rows(rows, n)}
    assert set(new) <= set(page), set(new) - set(page)
    byen = {page[i]['EN']: a for i, a in new.items()}
    done = {}
    for i, r in page.items():
        if not todo(r):
            continue
        ar = new.get(i) or byen.get(r['EN']) or mem.get(r['EN'])
        if not ar:
            print('MISSING', i, r['EN'])
            continue
        done[i] = (ar, 'TRANS-4' + (' unsure: ' + notes[i] if i in notes else ''))
    base = os.path.join(ROOT, 'translation')
    for cat in CATS:
        for fn in sorted(os.listdir(os.path.join(base, cat))):
            p = os.path.join(base, cat, fn)
            t = read_tsv(p)
            hit = False
            for r in t[1:]:
                if r[0] in done:
                    r[5], r[6], r[7] = done[r[0]][0], 'translated', done[r[0]][1]
                    hit = True
            if hit:
                write_tsv(p, t)
    print(f'applied page {n}: {len(done)} rows')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1] == 'dump':
        dump(int(sys.argv[2]))
    else:
        apply(int(sys.argv[2]), sys.argv[3])
