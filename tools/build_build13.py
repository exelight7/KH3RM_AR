r"""BUILD-13: a copy of tools\build_build12.py (pipeline unchanged) run on the current translation\ TSVs = BUILD-12 + the 22 REVIEW6-Q2Q3 fixes
(already in translation\ when this round began) + the 22 build13_round corrections (review\corrections\applied\build13_round.tsv, GPT R2).
diff_vs_build12.tsv / overflow_vs_build12.tsv are report only; the diff must be exactly those 44 ids and no new overflow row.
-> out\builds\BUILD-13\pakchunk99-arabic_P.pak + verify tables.
Usage (from the project root): python -I tools/build_build13.py   |   --installed (after SWAP_TO_BUILD13.bat)"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4
from tsvlib import read_tsv

b = m4.b
b.BUILD, b.OUT = 'BUILD-13', 'out/builds/BUILD-13'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT
PREV = 'out/builds/BUILD-12'
RAW = 'translation/raw_logical_ids.tsv'  # id <TAB> note; first line = header
FIXES = ['review/corrections/applied/build13_round.tsv']
REVIEW6 = '04426 04599 08010 09464 09488 09518 09676 09718 09785 09969 11415 11416 11417 11418 11419 11420 11421 11422 11423 11424 11425 11426'.split()


def raw_ids():
    return {r[0] for r in read_tsv(RAW)[1:]}


_shape_rows = b.shape_rows


def shape_rows(rows, meter, profs):
    """BUILD-10 shaping, then the raw-logical ids overwritten with their unshaped AR (and dropped from the wrap report)"""
    shaped, wrapped, rt = _shape_rows(rows, meter, profs)
    raw, by_id = raw_ids(), {r['id']: r for r in rows}
    assert raw <= set(by_id), sorted(raw - set(by_id))
    for i in raw:
        assert by_id[i]['status'] != 'todo' and by_id[i]['AR'], i
        shaped[i] = b.locres.unesc(by_id[i]['AR'])
    wrapped[:] = [w for w in wrapped if w[0] not in raw]
    return shaped, wrapped, rt


b.shape_rows = shape_rows


def entries(unp):
    out = {}
    for d, _, fs in os.walk(unp):
        for fn in fs:
            if fn.endswith('.locres'):
                for ns, _, es in m4.locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                    out.update({(ns, k): (fn, t) for k, _, _, t, _ in es})
    return out


def diff_prev():
    """report only: every (namespace, key) whose text differs from BUILD-12 -> diff_vs_build12.tsv (id, locres, old, new)"""
    ids = {(r['namespace'], r['key']): r['id'] for r in m4.load_translation()}
    old, new = entries(os.path.join(PREV, 'unpacked')), entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build12.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-12\tBUILD-13\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    print(f'differ from BUILD-12: {len(diff)} entries {dict(collections.Counter(r[1] for r in diff))}: {[r[0] for r in diff]}')
    want = {r[0] for fn in FIXES for r in read_tsv(fn)[1:]} | set(REVIEW6)
    got = {r[0] for r in diff}
    print(f'expected ids {len(want)}; differ but not expected: {sorted(got - want)}; expected but same: {sorted(want - got)}')
    assert got == want, 'BUILD-13 must differ from BUILD-12 in exactly the REVIEW6 + build13_round ids'


def overflow_prev():
    """report only: overflow ids new / gone compared with BUILD-12 -> overflow_vs_build12.tsv"""
    def ids(d):
        rows = open(os.path.join(d, 'overflow.tsv'), encoding='utf-8').read().splitlines()[1:]
        return {r.split('\t')[0] for r in rows if r}
    old, new = ids(PREV), ids(b.OUT)
    with open(os.path.join(b.OUT, 'overflow_vs_build12.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tchange\n')
        f.writelines(f'{i}\tnew\n' for i in sorted(new - old))
        f.writelines(f'{i}\tgone\n' for i in sorted(old - new))
    print(f'overflow: BUILD-12 {len(old)}, BUILD-13 {len(new)}, new {sorted(new - old)}, gone {sorted(old - new)}')
    assert not new - old, 'new overflow rows'


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
