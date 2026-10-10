r"""TRANS-1 helper. `dump N` prints the rows of menus_ui page N (300 rows, game order) that still need a human translation
(rows whose EN was already translated get the same AR from the translation memory; empty / letterless rows are marked skip).
`apply N file` reads lines '<5-digit id> <AR>' (or '<id> !skip <reason>') and writes AR + status translated.
Usage: python -I tools\trans_page.py dump|apply N [file]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

sys.stdout.reconfigure(encoding='utf-8')
CAT, PAGE = 'menus_ui', 300
for _a in list(sys.argv):
    if _a.startswith('--cat='):
        CAT = _a[6:]
        sys.argv.remove(_a)


def files():
    d = os.path.join(ROOT, 'translation', CAT)
    return {fn[:-4]: read_tsv(os.path.join(d, fn)) for fn in sorted(os.listdir(d)) if fn.endswith('.tsv')}


def save(F):
    d = os.path.join(ROOT, 'translation', CAT)
    for stem, rows in F.items():
        write_tsv(os.path.join(d, stem + '.tsv'), rows)


def game_order(F):
    out = [(r[0], stem, r) for stem, rows in F.items() for r in rows[1:]]
    out.sort(key=lambda t: t[0])
    return out


def letterless(en):
    return not re.search(r'[A-Za-z]', ARG.sub('', TAG.sub('', en)))


def skip_reason(en):
    v = ARG.sub('', TAG.sub('', en)).strip()
    if not en.strip():
        return 'empty'
    if not v:
        return 'tags/args only'
    if re.fullmatch(r'[\d\s.,:/%\-+×x′″★☆°—]*', v):
        return 'numbers/symbols'
    if letterless(en):
        return 'no Latin letters (native script / symbols)'
    return None


def main():
    cmd, n = sys.argv[1], int(sys.argv[2])
    F = files()
    order = game_order(F)
    page = order[(n - 1) * PAGE:n * PAGE]
    tm = {}  # translation memory: this category first, then every other category (same EN = same AR)
    for _, _, r in order:
        if r[5] and r[6] != 'todo':
            tm.setdefault(r[4], r[5])
    for r in load_translation():
        if r['AR'] and r['status'] != 'todo':
            tm.setdefault(r['EN'], r['AR'])
    if cmd == 'dump':
        seen, skipped, filled, ns = {}, [], 0, None
        for rid, stem, r in page:
            if r[5] and r[6] != 'todo':
                continue
            sr = skip_reason(r[4])
            if sr:
                skipped.append((rid, sr, r[4]))
                continue
            if r[4] in tm:
                filled += 1
                continue
            if r[4] in seen:
                continue
            seen[r[4]] = rid
            if r[1] != ns:
                ns = r[1]
                print(f'# {ns}')
            print(f'{rid} {r[4]}')
        print(f'## page {n}: {len(page)} rows, to translate {len(seen)}, from TM {filled}, skip {len(skipped)}')
        for rid, sr, en in skipped:
            if sr != 'empty':
                print(f'## skip {rid} [{sr}] {en[:50]}')
        print(f'## skip empty: {sum(1 for _, sr, _ in skipped if sr == "empty")} rows')
    elif cmd == 'apply':
        new = {}
        for line in open(sys.argv[3], encoding='utf-8'):
            line = line.rstrip('\n')
            if line.strip():
                new[line[:5]] = line[6:]
        notes = {}
        for k, v in list(new.items()):
            if ' ## ' in v:
                new[k], notes[k] = v.split(' ## ', 1)
        byen, skipen = {}, {}
        for rid, stem, r in page:
            if rid in new and not new[rid].startswith('!skip'):
                byen[r[4]] = new[rid]
            elif rid in new:
                skipen[r[4]] = new[rid]
        for rid, stem, r in page:
            if r[5] and r[6] != 'todo':
                continue
            sr = skip_reason(r[4])
            if r[4] in skipen:
                r[7] = 'skip: ' + skipen[r[4]][6:].strip()
            elif sr:
                r[7] = 'skip: ' + sr
            elif r[4] in tm:
                r[5], r[6] = tm[r[4]], 'translated'
            elif r[4] in byen:
                r[5], r[6] = byen[r[4]], 'translated'
            else:
                print('MISSING', rid, r[4])
        for rid, stem, r in page:
            if rid in notes:
                r[7] = notes[rid]
        missing = set(new) - {rid for rid, _, _ in page}
        assert not missing, missing
        save(F)
        print('applied page', n)


main()
