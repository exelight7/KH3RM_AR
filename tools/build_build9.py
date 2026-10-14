r"""BUILD-9: the BUILD-8 pipeline unchanged (tools\build_build4.py via the same wrapper) run on the current translation\ TSVs
(BUILD-8 + REVIEW5-Q1 + 13 corrections: DECIDE-19 B x5, GPT Q2 x8). diff_vs_build8.tsv / overflow_vs_build8.tsv are report only.
-> out\builds\BUILD-9\pakchunk99-arabic_P.pak + verify tables.
Usage (from the project root): python -I tools/build_build9.py   |   --installed (after SWAP_TO_BUILD9.bat)"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4

b = m4.b
b.BUILD, b.OUT = 'BUILD-9', 'out/builds/BUILD-9'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT
PREV = 'out/builds/BUILD-8'


def entries(unp):
    out = {}
    for d, _, fs in os.walk(unp):
        for fn in fs:
            if fn.endswith('.locres'):
                for ns, _, es in m4.locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                    out.update({(ns, k): (fn, t) for k, _, _, t, _ in es})
    return out


def diff_prev():
    """report only: every (namespace, key) whose text differs from BUILD-8 -> diff_vs_build8.tsv (id, locres, old, new)"""
    ids = {(r['namespace'], r['key']): r['id'] for r in m4.load_translation()}
    old, new = entries(os.path.join(PREV, 'unpacked')), entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build8.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-8\tBUILD-9\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    print(f'differ from BUILD-8: {len(diff)} entries {dict(collections.Counter(r[1] for r in diff))}: {[r[0] for r in diff][:20]}...')


def overflow_prev():
    """report only: overflow ids new / gone compared with BUILD-8 -> overflow_vs_build8.tsv"""
    def ids(d):
        rows = open(os.path.join(d, 'overflow.tsv'), encoding='utf-8').read().splitlines()[1:]
        return {r.split('\t')[0] for r in rows if r}
    old, new = ids(PREV), ids(b.OUT)
    with open(os.path.join(b.OUT, 'overflow_vs_build8.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tchange\n')
        f.writelines(f'{i}\tnew\n' for i in sorted(new - old))
        f.writelines(f'{i}\tgone\n' for i in sorted(old - new))
    print(f'overflow: BUILD-8 {len(old)}, BUILD-9 {len(new)}, new {sorted(new - old)}, gone {sorted(old - new)}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1:] == ['--installed']:
        b.installed()
    else:
        os.makedirs(b.OUT, exist_ok=True)
        b.EXTRA = m4.movie_files()
        b.main()
        for fn, t in entries(os.path.join(b.OUT, 'unpacked')).values():
            assert '<p align' not in t.lower(), fn
        print('no <p align> in any built locres')
        m4.overflow()
        diff_prev()
        overflow_prev()
