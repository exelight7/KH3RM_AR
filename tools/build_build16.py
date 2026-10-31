r"""BUILD-16: a copy of tools\build_build15.py with the BUILD-16 TresFont (tools\font_swap_adapter16.py: BUILD-15's font with the
6 ya glyphs restored from BUILD-14 by tools\ya_restore16.py, i.e. the BUILD-14 pair byte for byte). Translation = BUILD-15's.
Gate (no hardcoded ids): no id corrected since the BUILD-15 commit; no locres row differs from BUILD-15 (advances unchanged, so
no wrapping changes); files differing from BUILD-15 = TresFont.uasset + .uexp only; no new overflow row; no new glyph gap; no
missing Arabic.
-> out\builds\BUILD-16\pakchunk99-arabic_P.pak + verify tables, diff_vs_build15.tsv, files_vs_build15.tsv,
overflow_vs_build15.tsv, glyph_gaps.tsv, fonts_license\ (OFL.txt + SOURCES.md, outside the pak).
Usage (from the project root): python -I tools/build_build16.py   |   --installed (after SWAP_TO_BUILD16.bat)"""
import collections, hashlib, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4
import batch2_glyphs, font_swap_adapter16, shaper
from tsvlib import COLS, read_tsv

b = m4.b
b.BUILD, b.OUT = 'BUILD-16', 'out/builds/BUILD-16'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT
b.font_bytes, b.gaps = font_swap_adapter16.font_bytes, font_swap_adapter16.gaps  # the BUILD-16 TresFont
PREV = 'out/builds/BUILD-15'
PREV_COMMIT = '^BUILD-15$'  # commit message of the round that built PREV (translation = PREV's)
RAW = 'translation/raw_logical_ids.tsv'  # id <TAB> note; first line = header
LICENSE = {'OFL.txt': 'out/fonts_gpt/fonts/OFL.txt', 'SOURCES.md': 'out/fonts_gpt/SOURCES.md'}
sha = lambda d: hashlib.sha256(d).hexdigest()
git = lambda *a: subprocess.run(['git', *a], capture_output=True, check=True).stdout


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


def corrected_ids():
    """ids whose AR (or status) differs between the PREV round's commit and the working tree"""
    base = git('log', '-1', '--format=%H', f'--grep={PREV_COMMIT}').decode().strip()
    assert base, PREV_COMMIT
    old = {}
    for p in git('ls-tree', '-r', '--name-only', base, 'translation').decode().split('\n'):
        if p.count('/') == 2 and p.endswith('.tsv'):
            lines = git('show', f'{base}:{p}').decode('utf-8').split('\n')
            assert lines[0].split('\t') == COLS and lines[-1] == '', p
            old.update({r[0]: (r[5], r[6]) for r in (l.split('\t') for l in lines[1:-1])})
    now = {r['id']: (r['AR'], r['status']) for r in m4.load_translation()}
    assert set(old) == set(now), 'translation ids differ from PREV'
    out = {i for i in now if now[i] != old[i]}
    print(f'corrected since {PREV} (commit {base[:7]}): {len(out)} ids')
    return out


def entries(unp):
    out = {}
    for d, _, fs in os.walk(unp):
        for fn in fs:
            if fn.endswith('.locres'):
                for ns, _, es in m4.locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                    out.update({(ns, k): (fn, t) for k, _, _, t, _ in es})
    return out


def files(unp):
    return {os.path.relpath(os.path.join(d, fn), unp).replace(os.sep, '/'): sha(open(os.path.join(d, fn), 'rb').read())
            for d, _, fs in os.walk(unp) for fn in fs}


def diff_prev():
    """every (namespace, key) whose text differs from BUILD-15 -> diff_vs_build15.tsv; it must be exactly the corrected
    ids plus the rows whose shaped output differs between the BUILD-15 advances and the BUILD-16 ones (and BUILD-15's own
    advances must reproduce BUILD-15 byte for byte in every other row, so nothing else can be hiding in the diff)"""
    rows = m4.load_translation()
    corr = corrected_ids()
    ids = {(r['namespace'], r['key']): r['id'] for r in rows}
    old, new = entries(os.path.join(PREV, 'unpacked')), entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    profs = b.profiles()
    s_old = b.shape_rows(rows, b.meters(b.font_path(os.path.join(PREV, 'unpacked'))), profs)[0]
    s_new = b.shape_rows(rows, b.meters(b.font_path(os.path.join(b.OUT, 'unpacked'))), profs)[0]
    assert set(s_old) == set(s_new)
    by_key = {(r['namespace'], r['key']): r for r in rows}
    bad = [k for k, (_, t) in old.items() if k in by_key and by_key[k]['id'] in s_old and by_key[k]['id'] not in corr
           and t != b.locres.esc(s_old[by_key[k]['id']])]
    print(f'BUILD-15 reproduced from its own font advances: {len(s_old) - len(corr) - len(bad)} of '
          f'{len(s_old) - len(corr)} uncorrected shaped rows; differ: {bad[:10]}')
    assert not bad, 'current translation + BUILD-15 font does not reproduce BUILD-15'
    wrap = {i for i in s_new if s_new[i] != s_old[i]}
    want = corr | wrap
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build15.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-15\tBUILD-16\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    got = {r[0] for r in diff}
    print(f'differ from BUILD-15: {len(diff)} entries {dict(collections.Counter(r[1] for r in diff))}')
    print(f'corrected ids {len(corr)}, wrapping changed by the new font {len(wrap)}; differ but not expected: '
          f'{sorted(got - want)}; expected but same: {sorted(want - got)}')
    assert not corr and not diff, 'BUILD-16 must not touch any translation row'
    assert got == want, 'BUILD-16 must differ from BUILD-15 in exactly the corrected ids + rows whose wrapping changed'
    # files: TresFont + exactly the locres holding a changed row; movies and every other file unchanged
    fo, fn = files(os.path.join(PREV, 'unpacked')), files(os.path.join(b.OUT, 'unpacked'))
    assert set(fo) == set(fn), sorted(set(fo) ^ set(fn))
    changed = sorted(p for p in fn if fo[p] != fn[p])
    font = {m4.b.FONT + '.uasset', m4.b.FONT + '.uexp'}
    loc = {p for p in fn if p.endswith('.locres') and p.split('/')[-1] in {r[1] for r in diff}}
    with open(os.path.join(b.OUT, 'files_vs_build15.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('path_in_pak\tsha256_BUILD-15\tsha256_BUILD-16\tchange\n')
        f.writelines(f'{p}\t{fo[p]}\t{fn[p]}\t{"changed" if fo[p] != fn[p] else "same"}\n' for p in sorted(fn))
    print(f'files: {len(fn)} in both; changed {len(changed)}: {changed}')
    assert set(changed) == font | loc, sorted(set(changed) ^ (font | loc))
    for name in font:
        assert fn[name] == font_swap_adapter16.PINNED16[name.split('/')[-1]], name


def overflow_prev():
    """overflow ids new / gone compared with BUILD-15 -> overflow_vs_build15.tsv; a new overflow row stops the round"""
    def ids(d):
        rows = open(os.path.join(d, 'overflow.tsv'), encoding='utf-8').read().splitlines()[1:]
        return {r.split('\t')[0] for r in rows if r}
    old, new = ids(PREV), ids(b.OUT)
    with open(os.path.join(b.OUT, 'overflow_vs_build15.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tchange\n')
        f.writelines(f'{i}\tnew\n' for i in sorted(new - old))
        f.writelines(f'{i}\tgone\n' for i in sorted(old - new))
        f.writelines(f'{i}\tkept\n' for i in sorted(old & new))
    print(f'overflow: BUILD-15 {len(old)}, BUILD-16 {len(new)}, new {sorted(new - old)}, gone {sorted(old - new)}, '
          f'kept {sorted(old & new)}')
    assert not new - old, 'new overflow rows'


def glyph_gaps():
    """batch2 glyph lookup of the shipped text in all four classes, BUILD-15 vs BUILD-16 -> glyph_gaps.tsv:
    no Arabic gap in any class, and the non-Arabic gaps are exactly BUILD-15's (none new, none gone)"""
    tr = [r for r in m4.load_translation() if r['status'] != 'todo' and r['AR'] and r['id'] not in raw_ids()]

    def gaps_of(build):
        built, cls = batch2_glyphs.built_text(build), batch2_glyphs.classes(build)
        return {(fid, r['id'], c) for r in tr for c in batch2_glyphs.visible_chars(built[(r['namespace'], r['key'])])
                for fid, have in cls.items() if c not in have}
    old, new = gaps_of(PREV), gaps_of(b.OUT)
    ar = sorted(g for g in new if shaper.is_arabic(g[2]))
    with open(os.path.join(b.OUT, 'glyph_gaps.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('class\tid\tcp\tin_BUILD-15\n')
        f.writelines(f'{b.FONT_IDS[fid]}\t{i}\tU+{ord(c):04X}\t{(fid, i, c) in old}\n' for fid, i, c in sorted(new))
    print(f'glyph gaps (class/row/char): BUILD-15 {len(old)}, BUILD-16 {len(new)}, new {len(new - old)}, '
          f'gone {len(old - new)}, Arabic {len(ar)}; per class {dict(collections.Counter(b.FONT_IDS[g[0]] for g in new))}')
    assert not ar and new == old, 'glyph gaps changed'


def license_files():
    d = os.path.join(b.OUT, 'fonts_license')
    os.makedirs(d, exist_ok=True)
    for name, src in LICENSE.items():
        shutil.copyfile(src, os.path.join(d, name))
        print(f'{d}/{name}: sha256 {sha(open(src, "rb").read())}')


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
        glyph_gaps()
        license_files()
