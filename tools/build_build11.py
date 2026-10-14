r"""BUILD-11 (BUGFIX-1): the BUILD-10 pipeline unchanged (tools\build_build4.py via the same wrapper) plus ONE hook: the ids listed in
translation\raw_logical_ids.tsv (strings drawn by Windows itself, e.g. the native quit message box, which does its own bidi and
joining) are emitted as RAW logical-order Arabic = the AR text as typed: base letters, no presentation forms, no reversal, no wrap.
Every other row is shaped exactly as in BUILD-10. diff_vs_build10.tsv / overflow_vs_build10.tsv are report only.
-> out\builds\BUILD-11\pakchunk99-arabic_P.pak + verify tables.
Usage (from the project root): python -I tools/build_build11.py   |   --installed (after SWAP_TO_BUILD11.bat)"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4
from tsvlib import read_tsv

b = m4.b
b.BUILD, b.OUT = 'BUILD-11', 'out/builds/BUILD-11'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT
PREV = 'out/builds/BUILD-10'
RAW = 'translation/raw_logical_ids.tsv'  # id <TAB> note; first line = header


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
    """report only: every (namespace, key) whose text differs from BUILD-10 -> diff_vs_build10.tsv (id, locres, old, new)"""
    ids = {(r['namespace'], r['key']): r['id'] for r in m4.load_translation()}
    old, new = entries(os.path.join(PREV, 'unpacked')), entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build10.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-10\tBUILD-11\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    print(f'differ from BUILD-10: {len(diff)} entries {dict(collections.Counter(r[1] for r in diff))}: {[r[0] for r in diff]}')
    print(f'raw-logical ids {sorted(raw_ids())}; differ-but-not-raw: {sorted({r[0] for r in diff} - raw_ids())}')


def overflow_prev():
    """report only: overflow ids new / gone compared with BUILD-10 -> overflow_vs_build10.tsv"""
    def ids(d):
        rows = open(os.path.join(d, 'overflow.tsv'), encoding='utf-8').read().splitlines()[1:]
        return {r.split('\t')[0] for r in rows if r}
    old, new = ids(PREV), ids(b.OUT)
    with open(os.path.join(b.OUT, 'overflow_vs_build10.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tchange\n')
        f.writelines(f'{i}\tnew\n' for i in sorted(new - old))
        f.writelines(f'{i}\tgone\n' for i in sorted(old - new))
    print(f'overflow: BUILD-10 {len(old)}, BUILD-11 {len(new)}, new {sorted(new - old)}, gone {sorted(old - new)}')


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
