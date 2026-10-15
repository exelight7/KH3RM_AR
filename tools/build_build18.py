r"""BUILD-18 (HUD-VECTOR): BUILD-17 (same translation, same TresFont = font_swap_adapter16, same 3 LV label fields, same
HUD label rectangles) with the battle HUD words Focus / Max / Charge of HudStatus and HudStatusCA drawn from the new
texture HudStatusTxtAR at 2 texels per stage px (tools/hud_hires.py) instead of the magnified 256x128 HudStatusTxt(CA)
cells. The texture ships in this text pak next to the two movies that name it, so no movie of this pak refers to a
texture another pak may lack (the images pak stays optional: IMAGES-MASS11 is unchanged).
Gate: no id corrected since the BUILD-17 commit (HUD-SCALE); no locres row differs from BUILD-17; files = BUILD-17's with
exactly HudStatus/HudStatusCA .uasset/.uexp changed and HudStatusTxtAR .uasset/.uexp added; same overflow rows; same
glyph gaps; no missing Arabic; tools/hud_hires.py verify (tags, shapes, ReferencedAssetNames, texture package) and the
look gates (edge >= 110 % of English and >= MASS11, crisp >= 75 % of English at 1080p and 4K).
-> out/builds/BUILD-18/pakchunk99-arabic_P.pak + verify tables: movie_verify.tsv (3 LV fields, the BUILD-17 HUD patch and
the HUD-VECTOR rows), hud_cells.tsv, hud_look.tsv, hud_gates.tsv, diff_vs_build17.tsv, files_vs_build17.tsv,
overflow_vs_build17.tsv, glyph_gaps.tsv, fonts_license/; sheets in out/builds/HUD-VECTOR/ref/.
Usage (from the project root): python -I tools/build_build18.py   |   --installed (after SWAP_TO_BUILD18.bat)"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build17 as b17
import batch2_glyphs, font_swap_adapter16, hud_hires, shaper

m4, b = b17.m4, b17.b
b.BUILD, b.OUT = 'BUILD-18', 'out/builds/BUILD-18'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
PREV = 'out/builds/BUILD-17'
PREV_COMMIT = '^HUD-SCALE$'   # commit of the round that built BUILD-17 (translation = BUILD-17's)
REF = 'out/builds/HUD-VECTOR/ref'
NEW = {hud_hires.HS + hud_hires.NAME + e for e in ('.uasset', '.uexp')}
HUD = {hud_hires.HS + mv + e for mv in hud_hires.TXT for e in ('.uasset', '.uexp')}
EMPTY = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


def movie_files():
    """BUILD-17's movie files (3 LV fields + the 2 HUD movies, verified as BUILD-17 does) with the HUD movies replaced by
    the hud_hires ones and the new texture added; tables and sheets"""
    out = m4.movie_files()
    path = os.path.join(b.OUT, 'movie_verify.tsv')
    table = [l.rstrip('\n').split('\t') for l in open(path, encoding='utf-8')]
    hud17 = b17.hud_files(table)
    for mv in hud_hires.TXT:
        assert hud17[hud_hires.HS + mv + '.uexp'] == hud_hires.movie17(mv)[1], 'BUILD-17 movie'
    files, rows, log, dec, cells, size = hud_hires.build()
    assert set(files) == HUD | NEW
    table += [[r[0], 'HUD-VECTOR ' + r[1], r[2]] for r in rows]
    out.update(files)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in table)
    hud_hires.write_tsv(os.path.join(b.OUT, 'hud_cells.tsv'), [list(log[0])] + [list(r.values()) for r in log])
    for r in log:
        assert ' READABLE' in r['read'] and int(r['margin']) >= min(2, int(r['pad'])), r
        assert (r['fill'], r['outline']) == (r['fill_1x'], r['outline_1x']), ('colours differ from the 1x recipe', r)
        j = re.search(r'joins (\d+) of (\d+)', r['read'])
        assert not j or j[1] == j[2], ('Plex join broken', r)
    os.makedirs(REF, exist_ok=True)
    look = hud_hires.metrics_table(files, dec)
    gates = hud_hires.gates(look)
    for p in (os.path.join(b.OUT, 'hud_look.tsv'), os.path.join(REF, 'hud_look.tsv')):
        hud_hires.write_tsv(p, look)
    hud_hires.write_tsv(os.path.join(b.OUT, 'hud_gates.tsv'), gates)
    bad = [g for g in gates[1:] if g[2] in ('1080p', '4K') and g[-1] != 'PASS']
    print('look gates:', sum(g[-1] == 'PASS' for g in gates[1:]), 'of', len(gates) - 1, 'PASS', bad)
    assert not bad, bad
    hud_hires.sheets(files, dec, REF)
    hud_hires.hud_sheets(files, dec, REF)
    import cv2
    cv2.imwrite(os.path.join(REF, 'HudStatusTxtAR_atlas.png'), dec[..., [2, 1, 0, 3]])
    return out


_open = open


def _open_original(p, *a, **k):
    """build_build1.main reads each pak file's original from extracted/: the new texture has none (empty, marked below)"""
    if p.replace(os.sep, '/') in {'extracted/assets/' + n for n in NEW}:
        return io.BytesIO(b'')
    return _open(p, *a, **k)


def mark_new():
    """pak_verify_sha256.tsv: the original column of the new texture says so instead of the empty-file hash"""
    path = os.path.join(b.OUT, 'pak_verify_sha256.tsv')
    rows = [l.rstrip('\n').split('\t') for l in open(path, encoding='utf-8')]
    for r in rows:
        if r[0] in NEW:
            assert r[1] == EMPTY and r[-1] == 'PASS'
            r[1] = '(new file)'
    assert sum(r[1] == '(new file)' for r in rows) == len(NEW)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in rows)


def diff_prev():
    """BUILD-18 vs BUILD-17: no corrected id, no locres entry differs, every BUILD-17 file byte-identical except the two
    HUD movies (uasset + uexp), new files = exactly the HudStatusTxtAR texture"""
    rows = m4.load_translation()
    b17.PREV, b17.PREV_COMMIT = PREV, PREV_COMMIT     # used by b17.corrected_ids
    corr = b17.corrected_ids()
    ids = {(r['namespace'], r['key']): r['id'] for r in rows}
    old, new = b17.entries(os.path.join(PREV, 'unpacked')), b17.entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build17.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-17\tBUILD-18\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    print(f'locres entries: {len(new)} in both; differ from BUILD-17: {len(diff)}; corrected ids {len(corr)}')
    assert not corr and not diff, 'BUILD-18 must not touch any translation row'
    fo, fn = b17.files(os.path.join(PREV, 'unpacked')), b17.files(os.path.join(b.OUT, 'unpacked'))
    assert set(fn) == set(fo) | NEW and not set(fo) & NEW, sorted(set(fo) ^ set(fn))
    changed = sorted(p for p in fo if fo[p] != fn[p])
    with open(os.path.join(b.OUT, 'files_vs_build17.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('path_in_pak\tsha256_BUILD-17\tsha256_BUILD-18\tchange\n')
        f.writelines(f'{p}\t{fo.get(p, "-")}\t{fn[p]}\t{"added" if p not in fo else "changed" if fo[p] != fn[p] else "same"}\n'
                     for p in sorted(fn))
    print(f'files: BUILD-17 {len(fo)}, BUILD-18 {len(fn)}; added {sorted(NEW)}; changed {changed}')
    assert set(changed) == HUD, 'exactly the two HUD movies may change'
    for name in (m4.b.FONT + '.uasset', m4.b.FONT + '.uexp'):
        assert fn[name] == font_swap_adapter16.PINNED16[name.split('/')[-1]], name


def overflow_prev():
    def ids(d):
        rows = open(os.path.join(d, 'overflow.tsv'), encoding='utf-8').read().splitlines()[1:]
        return {r.split('\t')[0] for r in rows if r}
    old, new = ids(PREV), ids(b.OUT)
    with open(os.path.join(b.OUT, 'overflow_vs_build17.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tchange\n')
        f.writelines(f'{i}\tnew\n' for i in sorted(new - old))
        f.writelines(f'{i}\tgone\n' for i in sorted(old - new))
        f.writelines(f'{i}\tkept\n' for i in sorted(old & new))
    print(f'overflow: BUILD-17 {len(old)}, BUILD-18 {len(new)}, new {sorted(new - old)}, gone {sorted(old - new)}')
    assert new == old, 'overflow rows changed'


def glyph_gaps():
    tr = [r for r in m4.load_translation() if r['status'] != 'todo' and r['AR'] and r['id'] not in b17.raw_ids()]

    def gaps_of(build):
        built, cls = batch2_glyphs.built_text(build), batch2_glyphs.classes(build)
        return {(fid, r['id'], c) for r in tr for c in batch2_glyphs.visible_chars(built[(r['namespace'], r['key'])])
                for fid, have in cls.items() if c not in have}
    old, new = gaps_of(PREV), gaps_of(b.OUT)
    ar = sorted(g for g in new if shaper.is_arabic(g[2]))
    with open(os.path.join(b.OUT, 'glyph_gaps.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('class\tid\tcp\tin_BUILD-17\n')
        f.writelines(f'{b.FONT_IDS[fid]}\t{i}\tU+{ord(c):04X}\t{(fid, i, c) in old}\n' for fid, i, c in sorted(new))
    print(f'glyph gaps (class/row/char): BUILD-17 {len(old)}, BUILD-18 {len(new)}, new {len(new - old)}, '
          f'gone {len(old - new)}, Arabic {len(ar)}')
    assert not ar and new == old, 'glyph gaps changed'


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1:] == ['--installed']:
        b.installed()
    else:
        os.makedirs(b.OUT, exist_ok=True)
        b.EXTRA = movie_files()
        b.open = _open_original
        try:
            b.main()
        finally:
            del b.open
        mark_new()
        for fn, t in b17.entries(os.path.join(b.OUT, 'unpacked')).values():
            assert '<p align' not in t.lower(), fn
        print('no <p align> in any built locres')
        m4.overflow()
        diff_prev()
        overflow_prev()
        glyph_gaps()
        b17.license_files()
