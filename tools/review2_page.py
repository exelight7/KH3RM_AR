r"""REVIEW-2 helper: page N (300 rows) in story order = review\script order (dialogue, subtitles, Re Mind in story) then the
remaining Re Mind rows. `dump N` prints id / EN / AR of the translated rows (repeats of the same EN+AR on the page skipped);
`mark N` sets every translated row of the page to reviewed + note. Usage: python -I tools\review2_page.py dump|mark|count N"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
import make_script

NOTE = 'reviewed_by Claude Sonnet 5.5 pass, REVIEW-2'


def flat(rows):
    f = [(sc, r) for _, sc, rs in make_script.story(rows) for r in rs]
    seen = {r['id'] for _, r in f}
    f += [(r['stem'], r) for r in rows if r['category'] == 'remind' and r['id'] not in seen]
    return [(sc, r) for sc, r in f if r['status'] in ('translated', 'reviewed') and r['AR'].strip()]


def page(rows, n):
    return flat(rows)[(n - 1) * 300:n * 300]


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    cmd, n = sys.argv[1], (int(sys.argv[2]) if len(sys.argv) > 2 else 0)
    rows = load_translation()
    if cmd == 'count':
        print(len(flat(rows)), -(-len(flat(rows)) // 300), 'pages')
    elif cmd == 'dump':
        last, seen = None, set()
        for sc, r in page(rows, n):
            if sc != last:
                print('#', sc)
                last = sc
            k = (r['EN'], r['AR'])
            if k in seen:
                continue
            seen.add(k)
            print(f"{r['id']}\t{r['EN']}\n\t{r['AR']}")
    elif cmd == 'flags':  # validator flags (VALIDATION.md) of this page's rows
        ids = {r['id']: r for _, r in page(rows, n)}
        for ln in open(os.path.join(ROOT, 'review', 'VALIDATION.md'), encoding='utf-8'):
            c = [x.strip() for x in ln.split('|')]
            if len(c) > 3 and c[1] in ids and ('GLOSS' in c[3] or 'TYPO' in c[3] or 'ERR' in c[3] or 'DSPACE' in c[3]):
                print(c[1], c[3], ids[c[1]]['EN'], '=>', ids[c[1]]['AR'])
    elif cmd == 'fix':  # fix N file: lines 'id<TAB>new_AR<TAB>reason' -> review\corrections\review2_pNN.tsv (old_AR filled)
        cur = {r['id']: r['AR'] for _, r in page(rows, n)}
        out = ['id\told_AR\tnew_AR\treason']
        for ln in open(sys.argv[3], encoding='utf-8'):
            ln = ln.rstrip('\n')
            if ln.strip():
                i, new, why = (ln.split('\t') + [''])[:3]
                assert i in cur, i
                out.append(f'{i}\t{cur[i]}\t{new.replace(chr(0x61f), "?")}\t{why}')
        open(os.path.join(ROOT, 'review', 'corrections', f'review2_p{n:02d}.tsv'), 'w', encoding='utf-8', newline='').write('\n'.join(out) + '\n')
        print(len(out) - 1, 'fixes')
    elif cmd == 'mark':
        ids = {r['id'] for _, r in page(rows, n)}
        base = os.path.join(ROOT, 'translation')
        k = 0
        for cat in sorted(os.listdir(base)):
            d = os.path.join(base, cat)
            if not os.path.isdir(d):
                continue
            for fn in sorted(os.listdir(d)):
                p = os.path.join(d, fn)
                t = read_tsv(p)
                hit = False
                for r in t[1:]:
                    if r[0] in ids and r[6] == 'translated':
                        r[6], r[7] = 'reviewed', NOTE
                        hit = True
                        k += 1
                if hit:
                    write_tsv(p, t)
        print('marked', k)
