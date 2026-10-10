r"""BUILD-6: the BUILD-5 pipeline unchanged (tools\build_build4.py via the same wrapper as build_build5.py: same movie
patches, TresFont, line breaking, no <p align>) run on the current translation\ TSVs (REVIEW-3 + the FINAL-1 05051 fix).
Only the build name/output dir differ; diff_vs_build5.tsv (report only) lists the locres entries that differ from BUILD-5.
-> out\builds\BUILD-6\pakchunk99-arabic_P.pak + verify tables, diff_vs_build5.tsv.
Usage (from the project root): python -I tools/build_build6.py   |   --installed (after SWAP_TO_BUILD6.bat)"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4

b = m4.b
b.BUILD, b.OUT = 'BUILD-6', 'out/builds/BUILD-6'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT
PREV = 'out/builds/BUILD-5/unpacked'


def entries(unp):
    out = {}
    for d, _, fs in os.walk(unp):
        for fn in fs:
            if fn.endswith('.locres'):
                for ns, _, es in m4.locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                    out.update({(ns, k): (fn, t) for k, _, _, t, _ in es})
    return out


def diff_prev():
    """report only: every (namespace, key) whose text differs from BUILD-5 -> diff_vs_build5.tsv (id, locres, old, new)"""
    ids = {(r['namespace'], r['key']): r['id'] for r in m4.load_translation()}
    old, new = entries(PREV), entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build5.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-5\tBUILD-6\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    print(f'differ from BUILD-5: {len(diff)} entries {dict(collections.Counter(r[1] for r in diff))}: {[r[0] for r in diff]}')


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
