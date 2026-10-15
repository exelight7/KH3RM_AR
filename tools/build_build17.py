r"""BUILD-17 (HUD-SCALE): a copy of tools/build_build16.py (same translation, same TresFont = font_swap_adapter16) plus the
two battle HUD movies HudStatus (normal) and HudStatusCA (Caribbean) with the gauge words drawn larger (owner option B):
Focus x1.45, Max with its black badge plate x1.25, Charge x1.20 (tools/hud_scale.py: the scale is written into the label
shapes, same byte length; the Max text placement and the 28 placements of its flash copy get new translates so the flash
still zooms about the enlarged word). The 3 LV label fields of BUILD-4 are built by build_build4.movie_files() as before.
Gate: no id corrected since the BUILD-16 commit; no locres row differs from BUILD-16; files = BUILD-16's (all identical,
TresFont = the BUILD-16 pins) + exactly HudStatus/HudStatusCA .uasset (original bytes) + .uexp (patched); same overflow
rows; same glyph gaps; no missing Arabic; every label rectangle obeys the HUD rules (HUD_RULES) at the final position.
-> out/builds/BUILD-17/pakchunk99-arabic_P.pak + verify tables, movie_verify.tsv (3 LV + 2 HUD movies), diff_vs_build16.tsv,
files_vs_build16.tsv, overflow_vs_build16.tsv, glyph_gaps.tsv, hud_labels.tsv, fonts_license/.
Usage (from the project root): python -I tools/build_build17.py   |   --installed (after SWAP_TO_BUILD17.bat)"""
import collections, hashlib, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4
import batch2_glyphs, font_swap_adapter16, hud_scale, shaper
from tsvlib import COLS, read_tsv

b = m4.b
b.BUILD, b.OUT = 'BUILD-17', 'out/builds/BUILD-17'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT
b.font_bytes, b.gaps = font_swap_adapter16.font_bytes, font_swap_adapter16.gaps  # the BUILD-16 TresFont, unchanged
PREV = 'out/builds/BUILD-16'
PREV_COMMIT = '^BUILD-16$'  # commit message of the round that built PREV (translation = PREV's)
RAW = 'translation/raw_logical_ids.tsv'  # id <TAB> note; first line = header
LICENSE = {'OFL.txt': 'out/fonts_gpt/fonts/OFL.txt', 'SOURCES.md': 'out/fonts_gpt/SOURCES.md'}
SF = m4.SF
# HUD movies: (movie, pak with the only copy, sha256 of the extracted .uasset, .uexp); read-only in extracted\assets
HUD = {'01_hud/hud_status/HudStatus': ('Paks/pakchunk0_s6-WindowsNoEditor.pak',
                                       'ad111ddca202279433a758c14ad8e1ba11f4e0f55cdbcf8120528208a12e1432',
                                       '4cd3e6e2fb08d3d183236ba0be09429528e784d0a329c22165eed2274ec0bb56'),
       '01_hud/hud_status/HudStatusCA': ('Paks/pakchunk0_s7-WindowsNoEditor.pak',
                                         '50f9847b44310a11b5074e7bb571dc88716dcda41e5f1d9eab02529f1a0fc7f5',
                                         '0c6798a43a245f8d1f03b80038a9a69ed666d3d9434e81b62e515b74e973db95')}
# label shape id -> (scale, new bounds xMin, yMin in twips of the shape). Stage px at 1920x1080, final HUD position:
# sprite pcFocusGg origin (1680, 872) = root sttsPc (1602, 872) + pcEx (78, 0); the words sit on the top of the yellow
# Focus bar, HP ring below (top y 906), party portraits above (bottom y 869), screen edge 120 px right of the final x
# during the slide-in (root x 1722 -> 1602). Rules (HUD_RULES): right <= 1800, top >= its old top, bottom <= 905, both
# bottom corners on the bar. Room by geometry: Focus 1.50, Max+plate 1.45, Charge 1.20 (step 0.05; tools/hud_scale.py
# notes). The same byte length caps Focus at 1.45 (bounds/move fields are 11-bit: |x| <= 51.15 px from its origin, and
# the copy inside the Max badge has a 6-bit translate, so the origin cannot move) and Max at 1.25 (shape 19 has 2 spare
# bits: its 60 px edges need 12 bits, 1.30 would need 11-bit vertical edges too).
HUD_SHAPES = {
    27: (1.45, -992, -200),  # FOCUS (pcExLogo, also inside pcExMaxAnm): 59x20 -> 85.55x29, x 1714.40..1799.95, y 875..904
    19: (1.25, -200, -250),  # MAX (coTextMax + flash coTextMaxEff): 48x20 -> 60x25, x 1734..1794, y 875.25..900.25
    95: (1.25, -688, -220),  # MAX badge plate (pcExMaxAnm d3): 55x22 -> 68.75x27.5, x 1729.60..1798.35, y 874..901.5
    22: (1.20, -261, 0),     # CHARGE (coPcExTxCharge): 71x21 -> 85.2x25.2, x 1714.80..1800, y 875..900.2
}
# Max group = text + plate scaled 1.25 about (1764, 874) (top centre of the plate); the flash zoom point (pcExMaxAnm
# origin 1765, 885) maps to (1765.25, 887.75). Text placement t = (-21, +2.75) px (was -26, 0: the shape re-centred to
# fit its 9/11-bit fields); flash frame of scale k: t_k = 0.25 (1 - k) - 21 k, 2.75 px (k = 1 at frames 0 and 76).
MAX_T = lambda k: (round(20 * (0.25 * (1 - k) - 21 * k)), 55)
HUD_MOVES = {(97, 5): MAX_T, (97, 7): MAX_T}
ROOT = (1602 * 20, 872 * 20)  # sttsPc on the root timeline at its final frame (twips)
# label -> (path of (sprite, depth) placements below sttsPc, shape)
LABELS = {'Focus': ([(167, 3), (105, 1), (104, 50), (31, 1)], 27),
          'Focus in Max badge': ([(167, 3), (105, 1), (104, 54), (97, 1), (31, 1)], 27),
          'Max': ([(167, 3), (105, 1), (104, 54), (97, 5), (21, 1)], 19),
          'Max flash (k=1)': ([(167, 3), (105, 1), (104, 54), (97, 7), (21, 1)], 19),
          'Max badge plate': ([(167, 3), (105, 1), (104, 54), (97, 3), (96, 1)], 95),
          'Charge': ([(167, 3), (105, 1), (104, 52), (94, 1), (26, 1)], 22)}
HUD_RULES = dict(right=1800 * 20, bottom=905 * 20)
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


def label_rects(d):
    """label -> (x0, x1, y0, y1) stage twips at the final HUD position, from the movie's own frame-0 placements"""
    pls, tags = hud_scale.placements(d)
    first = {}
    for sid, fr, depth, ch, name, q, m in pls:
        first.setdefault((sid, depth), m)
    out = {}
    for label, (path, shp) in LABELS.items():
        x, y = ROOT
        for key in path:
            m = first[key]
            assert m['scale'] is None and m['rot'] is None, key
            x, y = x + m['tx'], y + m['ty']
        q, n = tags[shp]
        x0, x1, y0, y1 = hud_scale.read_shape(d[q:q + n])['bounds']
        out[label] = (x + x0, x + x1, y + y0, y + y1)
    return out


def hud_files(table):
    """the two HUD movies patched (uexp) + their unchanged uasset; rows for movie_verify.tsv and hud_labels.tsv"""
    out, labels = {}, [['movie', 'label', 'old x0..x1 y0..y1 px', 'new x0..x1 y0..y1 px', 'scale', 'rules']]
    px = lambda r: f'{r[0] / 20:.2f}..{r[1] / 20:.2f} {r[2] / 20:.2f}..{r[3] / 20:.2f}'
    ref = None
    for mv, (pak, h_ua, h_ue) in HUD.items():
        rel = SF + mv
        ua, ue = (open(os.path.join('extracted/assets', rel + e), 'rb').read() for e in ('.uasset', '.uexp'))
        assert sha(ua) == h_ua and sha(ue) == h_ue, f'{mv}: extracted copy is not the pinned original'
        new, _ = hud_scale.patch(ue, HUD_SHAPES, HUD_MOVES)
        diff, plan, moved = hud_scale.verify(ue, new, HUD_SHAPES, HUD_MOVES)
        # the CA movie must carry the same shapes and placements (only offsets differ)
        sig = [(k, p[0], p[3], str(p[4])) for k, *p in plan]  # shape id / placement, old and new values
        assert ref is None or sig == ref, f'{mv}: plan differs from HudStatus'
        ref = sig
        old_r, new_r = label_rects(ue), label_rects(new)
        for label in LABELS:
            o, n = old_r[label], new_r[label]
            bad = [k for k, ok in (('right', n[1] <= HUD_RULES['right']), ('top', n[2] >= o[2]),
                                   ('bottom', n[3] <= HUD_RULES['bottom'])) if not ok]
            assert not bad, (mv, label, bad, n)
            labels.append([mv.split('/')[-1], label, px(o), px(n), f'{(n[1] - n[0]) / (o[1] - o[0]):.2f}', 'PASS'])
        name = mv.split('/')[-1]
        shapes = [p for p in plan if p[0] == 'shape']
        table += [[name, 'size', f'{len(ue)} = {len(new)} B'],
                  [name, 'bytes differing', f'{len(diff)} (file offsets {diff[0]}..{diff[-1]}, inside {len(shapes)} '
                                            f'label shapes and {moved} placement matrices only)'],
                  *[[name, f'shape #{p[1]} bounds twips', f'{p[4]["bounds"]} -> {p[5]["bounds"]} (x{HUD_SHAPES[p[1]][0]}, '
                                                         f'{p[3]} B, texel cell {hud_scale.cell(p[4])} unchanged)']
                    for p in shapes],
                  [name, 'placements moved', f'{moved}: sprite 97 depth 5 (coTextMax) and 7 (coTextMaxEff, frames 0, '
                                             f'49-74, 76) translate -> MAX_T(k); scale bytes unchanged'],
                  [name, 'tags', f'{sum(1 for _ in m4.tag_offsets(m4.movie(new)[4]))} top-level tags, same codes, '
                                 f'offsets and lengths'],
                  [name, 'sha256 base', sha(ue)], [name, 'sha256 patched', sha(new)], [name, 'base pak', pak],
                  [name, 'why', 'HUD-SCALE (owner option B): Focus x1.45, Max + plate x1.25, Charge x1.20; '
                                'see hud_labels.tsv']]
        out.update({rel + '.uasset': ua, rel + '.uexp': new})
    with open(os.path.join(b.OUT, 'hud_labels.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in labels)
    return out


def movie_files():
    """BUILD-4's 3 LV fields (movie_verify.tsv written by m4) + the 2 HUD movies appended to the same table"""
    out = m4.movie_files()
    path = os.path.join(b.OUT, 'movie_verify.tsv')
    table = [l.rstrip('\n').split('\t') for l in open(path, encoding='utf-8')]
    out.update(hud_files(table))
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in table)
    return out


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
    """BUILD-17 vs BUILD-16: no corrected id, no locres entry differs (diff_vs_build16.tsv stays empty), every BUILD-16
    file byte-identical (TresFont = the BUILD-16 pins), new files = exactly the two HUD movies (files_vs_build16.tsv)"""
    rows = m4.load_translation()
    corr = corrected_ids()
    ids = {(r['namespace'], r['key']): r['id'] for r in rows}
    old, new = entries(os.path.join(PREV, 'unpacked')), entries(os.path.join(b.OUT, 'unpacked'))
    assert set(old) == set(new), 'entry sets differ'
    diff = sorted((ids.get(k, '?'), new[k][0], old[k][1], new[k][1]) for k in new if old[k][1] != new[k][1])
    with open(os.path.join(b.OUT, 'diff_vs_build16.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tlocres\tBUILD-16\tBUILD-17\n')
        f.writelines('\t'.join(r) + '\n' for r in diff)
    print(f'locres entries: {len(new)} in both; differ from BUILD-16: {len(diff)}; corrected ids {len(corr)}')
    assert not corr and not diff, 'BUILD-17 must not touch any translation row'
    fo, fn = files(os.path.join(PREV, 'unpacked')), files(os.path.join(b.OUT, 'unpacked'))
    hud = {SF + mv + e for mv in HUD for e in ('.uasset', '.uexp')}
    assert set(fn) == set(fo) | hud and not set(fo) & hud, sorted(set(fo) ^ set(fn))
    changed = sorted(p for p in fo if fo[p] != fn[p])
    with open(os.path.join(b.OUT, 'files_vs_build16.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('path_in_pak\tsha256_BUILD-16\tsha256_BUILD-17\tchange\n')
        f.writelines(f'{p}\t{fo.get(p, "-")}\t{fn[p]}\t{"added" if p not in fo else "changed" if fo[p] != fn[p] else "same"}\n'
                     for p in sorted(fn))
    print(f'files: BUILD-16 {len(fo)}, BUILD-17 {len(fn)}; added {sorted(hud)}; changed {changed}')
    assert not changed, 'a BUILD-16 file changed'
    for name in (m4.b.FONT + '.uasset', m4.b.FONT + '.uexp'):
        assert fn[name] == font_swap_adapter16.PINNED16[name.split('/')[-1]], name


def overflow_prev():
    """overflow ids new / gone compared with BUILD-16 -> overflow_vs_build16.tsv; any change stops the round"""
    def ids(d):
        rows = open(os.path.join(d, 'overflow.tsv'), encoding='utf-8').read().splitlines()[1:]
        return {r.split('\t')[0] for r in rows if r}
    old, new = ids(PREV), ids(b.OUT)
    with open(os.path.join(b.OUT, 'overflow_vs_build16.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tchange\n')
        f.writelines(f'{i}\tnew\n' for i in sorted(new - old))
        f.writelines(f'{i}\tgone\n' for i in sorted(old - new))
        f.writelines(f'{i}\tkept\n' for i in sorted(old & new))
    print(f'overflow: BUILD-16 {len(old)}, BUILD-17 {len(new)}, new {sorted(new - old)}, gone {sorted(old - new)}')
    assert new == old, 'overflow rows changed'


def glyph_gaps():
    """batch2 glyph lookup of the shipped text in all four classes, BUILD-16 vs BUILD-17 -> glyph_gaps.tsv:
    no Arabic gap in any class, and the non-Arabic gaps are exactly BUILD-16's (none new, none gone)"""
    tr = [r for r in m4.load_translation() if r['status'] != 'todo' and r['AR'] and r['id'] not in raw_ids()]

    def gaps_of(build):
        built, cls = batch2_glyphs.built_text(build), batch2_glyphs.classes(build)
        return {(fid, r['id'], c) for r in tr for c in batch2_glyphs.visible_chars(built[(r['namespace'], r['key'])])
                for fid, have in cls.items() if c not in have}
    old, new = gaps_of(PREV), gaps_of(b.OUT)
    ar = sorted(g for g in new if shaper.is_arabic(g[2]))
    with open(os.path.join(b.OUT, 'glyph_gaps.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('class\tid\tcp\tin_BUILD-16\n')
        f.writelines(f'{b.FONT_IDS[fid]}\t{i}\tU+{ord(c):04X}\t{(fid, i, c) in old}\n' for fid, i, c in sorted(new))
    print(f'glyph gaps (class/row/char): BUILD-16 {len(old)}, BUILD-17 {len(new)}, new {len(new - old)}, '
          f'gone {len(old - new)}, Arabic {len(ar)}')
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
        b.EXTRA = movie_files()
        b.main()
        for fn, t in entries(os.path.join(b.OUT, 'unpacked')).values():
            assert '<p align' not in t.lower(), fn
        print('no <p align> in any built locres')
        m4.overflow()
        diff_prev()
        overflow_prev()
        glyph_gaps()
        license_files()
