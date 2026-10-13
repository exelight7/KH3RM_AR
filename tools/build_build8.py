r"""BUILD-8: the BUILD-7 pipeline unchanged (tools\build_build4.py via the same wrapper as build_build7.py: same movie
patches, TresFont, line breaking, no <p align>) run on the current translation\ TSVs (CODEX-REVIEW4 corrections, OPUS-090).
Only the build name/output dir differ; diff_vs_build7.tsv (report only) lists the locres entries that differ from BUILD-7,
overflow_vs_build7.tsv (report only) lists overflow rows that are new or gone compared with BUILD-7.
-> out\builds\BUILD-8\pakchunk99-arabic_P.pak + verify tables, diff_vs_build7.tsv.
Usage (from the project root): python -I tools/build_build8.py   |   --installed (after SWAP_TO_BUILD8.bat)"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4

b = m4.b
b.BUILD, b.OUT = 'BUILD-8', 'out/builds/BUILD-8'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT
PREV = 'out/builds/BUILD-7'


def entries(unp):
    out = {}
    for d, _, fs in os.walk(unp):
        for fn in fs:
            if fn.endswith('.locres'):
                for ns, _, es in m4.locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                    out.update({(ns, k): (fn, t) for k, _, _, t, _ in es})
    return out


def diff_prev():
    """report only: every (namespace, key) whose text differs from BUILD-7 -> diff_vs_build7.tsv (id, locres, old, new)"""
    ids = {(r['namespace'], r['key']): r['id'] for r in m4.load_translation()}
    old, new = entries(os.path.join(PREV, 'unpacked')), entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build7.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-7\tBUILD-8\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    print(f'differ from BUILD-7: {len(diff)} entries {dict(collections.Counter(r[1] for r in diff))}: {[r[0] for r in diff][:20]}...')


def overflow_prev():
    """report only: overflow ids new / gone compared with BUILD-7 -> overflow_vs_build7.tsv"""
    def ids(d):
        rows = open(os.path.join(d, 'overflow.tsv'), encoding='utf-8').read().splitlines()[1:]
        return {r.split('\t')[0] for r in rows if r}
    old, new = ids(PREV), ids(b.OUT)
    with open(os.path.join(b.OUT, 'overflow_vs_build7.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tchange\n')
        f.writelines(f'{i}\tnew\n' for i in sorted(new - old))
        f.writelines(f'{i}\tgone\n' for i in sorted(old - new))
    print(f'overflow: BUILD-7 {len(old)}, BUILD-8 {len(new)}, new {sorted(new - old)}, gone {sorted(old - new)}')


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
