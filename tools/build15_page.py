r"""BUILD-15 TASK B helper (read only): the 16,415 translated rows in id order, pages of 300 (1-55; 56 = the image strings).
`dump N` prints one line per row: id, protected mark (*), key, EN, AR; `range N` prints the first and last id;
`check <file.tsv>` = the gate for a correction file: every id on page N's range, none protected, old_AR = current AR,
validate.check() gives no ERR and no new flag.  Protected = ids named in review\DECISIONS_ANSWERED.md /
BATCH3_DECISIONS.md, the Codex corrections, the corrections applied in BUILD-9..13 (build9/10/13 rounds, REVIEW5,
REVIEW6), Tangled rows and Sonic Diver 10615 / 14550.
Usage: python -I tools\build15_page.py dump|range N   |   check N review\corrections\build15_NN.tsv"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import ROOT, load_translation, load_images_strings, read_tsv
import validate

SIZE = 300
APPLIED = ['CODEX-REVIEW4-*.tsv', 'build9_round.tsv', 'build10_round.tsv', 'build13_round.tsv', 'review5_*.tsv',
           'review6_*.tsv', 'batch3_review.tsv']


def rows():
    return sorted((r for r in load_translation() if r['status'] != 'todo' and r['AR']), key=lambda r: r['id'])


def protected():
    ids = {'10615', '14550'}
    for f in ('DECISIONS_ANSWERED.md', 'BATCH3_DECISIONS.md'):
        ids |= set(re.findall(r'\b\d{5}\b', open(os.path.join(ROOT, 'review', f), encoding='utf-8').read()))
    for pat in APPLIED:
        for p in glob.glob(os.path.join(ROOT, 'review', 'corrections', 'applied', pat)):
            ids |= {r[0] for r in read_tsv(p)[1:]}
    return ids | {r['id'] for r in rows() if 'tangled' in r['EN'].lower()}


def page(n):
    rs = rows()
    return rs[(n - 1) * SIZE:n * SIZE]


def dump(n):
    prot = protected()
    if n == 56:
        for r in load_images_strings():
            print('\t'.join(str(r.get(k, '')) for k in r))
        return
    by_en = {}
    for r in rows():
        by_en.setdefault(r['EN'], []).append(r)
    for r in page(n):
        # same EN (>= 20 chars) elsewhere with another AR: name the first such id
        other = next((o['id'] for o in by_en[r['EN']] if o['AR'] != r['AR']), '') if len(r['EN']) >= 20 else ''
        print(f"{r['id']}{'*' if r['id'] in prot else ''} {r['key']} | {r['EN']} || {r['AR']}"
              + (f'  [SAME-EN differs: {other}]' if other else ''))


def check(n, path):
    pg, prot = {r['id']: r for r in page(n)}, protected()
    gloss = validate.build_gloss(validate.load_glossary(), validate.corpus_lowercase_words(load_translation()))
    fx = read_tsv(path)
    assert fx[0] == ['id', 'old_AR', 'new_AR', 'reason'], fx[0]
    for i, old, new, why in fx[1:]:
        assert i in pg, f'{i} not on page {n}'
        assert i not in prot, f'{i} is protected'
        assert pg[i]['AR'] == old, f'{i}: old_AR differs from the current AR'
        before = validate.check(pg[i]['EN'], old, pg[i]['status'], gloss)
        after = validate.check(pg[i]['EN'], new, pg[i]['status'], gloss)
        assert not validate.ERR & set(after), (i, after)
        assert set(after) <= set(before), (i, 'new flag', after)
        assert chr(0xFFFD) not in new and chr(0x61F) not in new, i
        assert why.strip(), i
    print(f'{path}: {len(fx) - 1} fixes, gate PASS')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    cmd, n = sys.argv[1], int(sys.argv[2])
    if cmd == 'dump':
        dump(n)
    elif cmd == 'range':
        p = page(n)
        print(n, p[0]['id'], p[-1]['id'], len(p))
    else:
        check(n, sys.argv[3])
