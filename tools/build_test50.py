r"""TEST50 build: 50 test rows (menus, items, equipment, abilities, plural/acronym/set-letter rows, tutorials,
opening subtitles) + the title-screen rows in Arabic, every other string original English; full shaper; TresFont with
the Segoe UI Arabic set (incl. ، ؟ and the join fix) at the locked F1 scale in every font class the text fields use
($jimakuNE 1, $JimakuJP 2, $sougei 3, $KH2Menu 4). Join extension per class from the measured letterSpacing
(out\builds\TEST50\ref\font_fields.tsv, written by tools\font_census.py).
Writes out\builds\TEST50\{pakroot,unpacked}, pakchunk99-test50_P.pak, pak_verify_sha256.tsv, rows.tsv.
Usage (from the project root): python -I tools/build_test50.py"""
import collections, csv, hashlib, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locres, shaper, tresfont
from tsvlib import load_translation, PREFIX
from build_arabictest1 import SRC, FONT, SEGOE, CODES
from build_arabictest2 import GAP, cap, extend_joins, changed_entries

OUT = 'out/builds/TEST50'
PAK = os.path.join(OUT, 'pakchunk99-test50_P.pak')
REPAK = os.path.abspath('tools/repak-0.2.3/repak.exe')
FONT_IDS = {1: '$jimakuNE', 2: '$JimakuJP', 3: '$sougei', 4: '$KH2Menu'}
# movies that show menus, item/ability descriptions, tutorials/help, subtitles and dialog (font_census groups)
RELEVANT = ('00_system', '01_hud', '04_InitialSetting', '11_title', '13_pause', '14_theater', '15_campmenu',
            '16_game_help', '17_saveload', '19_config', '20_keyitem', '22_mapname', '41_shop', '85_settingmenu',
            '90_rsl', '92_message')
GROUPS = [  # (group, ids) — the 50 test rows
    ('main menu', ['00001', '00002', '00003', '00004', '00005', '00008', '00009', '00022', '00023', '00024', '00025',
                   '00028', '00029', '00034', '00046']),
    ('items', ['00115', '00118', '00119', '12542', '12543', '12545', '12558', '12559']),
    ('equipment', ['12232', '12288', '12334', '12386', '12440', '12492']),
    ('abilities', ['16414', '16662', '16360', '16608', '16353', '16601', '16420', '16668', '16701']),
    ('plural', ['14424']),
    ('acronym', ['00041']),
    ('set letter', ['00225']),
    ('tutorials', ['10321', '10336', '10242']),
    ('subtitles', ['00715', '00716', '00719', '00720', '00721', '00723']),
]
sha = lambda b: hashlib.sha256(b).hexdigest()


def title_ids(rows):
    """the title-screen rows of ARABIC-TEST-2: title menu items + help lines, GAME SETTINGS and the button guides"""
    return [r['id'] for r in rows if r['status'] != 'todo' and shaper.has_letters(r['AR']) and (
        r['namespace'] == 'kh3_menu.title' and r['key'].startswith(('menu_', 'detail_')) or
        r['namespace'] == 'kh3_settings.top' and r['key'] in ('title_0010', 'button_0010', 'button_0020', 'button_0050'))]


def gaps():
    """join extension per font class: letterSpacing (px) / size (pt) * 256 units, max over the relevant fields,
    never below the F1 value GAP (verified in-game at letterSpacing 0 and 2)"""
    need = collections.defaultdict(int)
    path = os.path.join(OUT, 'ref', 'font_fields.tsv')
    assert os.path.exists(path), 'run tools/font_census.py first'
    for r in csv.DictReader(open(path, encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        ls = float(r['letterSpacing'].split(',')[-1])
        if r['movie'].startswith(RELEVANT) and ls > 0:
            need[r['font']] = max(need[r['font']], math.ceil(ls * 256 / float(r['size_pt'])))
    return {i: (max(GAP, need[a]), need[a]) for i, a in FONT_IDS.items()}


def font_bytes(g):
    """Arabic set added to fonts 1-4 at the F1 scale (k = 1/8 for $sougei, same Arabic-to-cap-height ratio elsewhere)"""
    a, m, fonts = tresfont.load(os.path.join('extracted/assets', FONT + '.uasset'))
    ref = cap(next(f for f in fonts.values() if f['id'] == 3))[1]
    info = {}
    for f in fonts.values():
        if f['id'] in FONT_IDS:
            base, h = cap(f)
            k = 256 / 2048 * h / ref
            tresfont.add_glyphs(f, tresfont.ttf_glyphs(SEGOE, CODES, k, base, extend_joins(k, g[f['id']][0])))
            info[f['id']] = (base, h, k)
    return tresfont.save(a, m, fonts), info


def check_font(root):
    """only fonts 1-4 change, only by the added codes; every other tag and every existing glyph is unchanged"""
    o = tresfont.load(os.path.join('extracted/assets', FONT + '.uasset'))
    n = tresfont.load(os.path.join(root, FONT + '.uasset'))
    tags = lambda m: [(c, d) for c, _, d in m['tags'] if c != 1005]
    assert tags(o[1]) == tags(n[1]), 'non-font tags changed'
    out = {}
    for i, f in o[2].items():
        g = n[2][i]
        old = {c: (a, f['shapes'][s]) for c, a, s in f['glyphs']}
        new = {c: (a, g['shapes'][s]) for c, a, s in g['glyphs']}
        assert all(new[c] == old[c] for c in old), f'existing glyph changed in font {f["id"]}'
        added = set(new) - set(old)
        assert added == (set(CODES) & set(new) if f['id'] in FONT_IDS else set()), f['id']
        out[f['id']] = (len(old), len(new), {c for c, _, _ in g['glyphs']})
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rows = load_translation()
    by_id = {r['id']: r for r in rows}
    test = [i for _, ids in GROUPS for i in ids]
    assert len(test) == len(set(test)) == 50, len(test)
    title = title_ids(rows)
    chosen = set(test) | set(title)
    for i in chosen:
        assert by_id[i]['status'] != 'todo' and by_id[i]['AR'], i
    files = sorted({PREFIX + by_id[i]['stem'] + '.locres' for i in chosen})

    # text: AR (shaped) for the chosen rows, EN for everything else in the touched files
    report, loc, shaped = [], {}, {}
    for rel in files:
        out = []
        for r in rows:
            if PREFIX + r['stem'] + '.locres' != rel:
                continue
            text = r['EN']
            if r['id'] in chosen:
                logical = locres.unesc(r['AR'])
                v = shaper.shape(logical)
                u = shaper.unshape(v)
                rt = 'exact' if u == logical else 'same-visual' if shaper.shape(u) == v else 'FAIL'
                assert rt != 'FAIL', r['id']
                shaped[r['id']] = (v, rt)
                text = locres.esc(v)
            out.append(dict(namespace=r['namespace'], key=r['key'], source_hash=r['source_hash'], text=text))
        loc[rel] = locres.tsv_import(out, open(os.path.join(SRC, rel), 'rb').read())

    g = gaps()
    (ua, ue), info = font_bytes(g)
    files_out = dict(loc, **{FONT + '.uasset': ua, FONT + '.uexp': ue})
    root = os.path.join(OUT, 'pakroot')
    for rel, data in files_out.items():
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        open(os.path.join(root, rel), 'wb').write(data)
    subprocess.run([REPAK, 'pack', '--version', 'V4', '--compression', 'Zlib', '--mount-point', '../../../', root, PAK],
                   check=True, capture_output=True)
    listed = subprocess.run([REPAK, 'list', PAK], check=True, capture_output=True, text=True).stdout.splitlines()
    hl = dict(l.split(' ', 1)[::-1] for l in subprocess.run([REPAK, 'hash-list', PAK], check=True, capture_output=True,
                                                             text=True).stdout.splitlines() if l.strip())
    unp = os.path.join(OUT, 'unpacked')
    subprocess.run([REPAK, 'unpack', '-q', '-f', '-o', unp, PAK], check=True, capture_output=True)
    assert sorted(listed) == sorted(files_out), (listed, list(files_out))
    report.append(['path_in_pak', 'sha256_original', 'sha256_input', 'sha256_repak_hash_list', 'sha256_unpacked', 'result'])
    for rel, data in files_out.items():
        orig = open(os.path.join('extracted/locres' if rel.endswith('.locres') else 'extracted/assets', rel), 'rb').read()
        got = open(os.path.join(unp, rel), 'rb').read()
        ok = sha(data) == hl.get(rel) == sha(got)
        report.append([rel, sha(orig), sha(data), hl.get(rel, ''), sha(got), 'PASS' if ok else 'FAIL'])
        assert ok, rel
    with open(os.path.join(OUT, 'pak_verify_sha256.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join('\t'.join(r) for r in report) + '\n')

    # re-parse: exactly the chosen rows changed; fonts: only the new codes; every shaped code point is in the font
    want = collections.Counter(PREFIX + by_id[i]['stem'] + '.locres' for i in chosen
                               if locres.esc(shaped[i][0]) != by_id[i]['EN'])
    for rel in loc:
        ch = changed_entries(open(os.path.join(SRC, rel), 'rb').read(), open(os.path.join(unp, rel), 'rb').read())
        assert len(ch) == want[rel], (rel, len(ch), want[rel])
        print(f'  {rel.split("/")[-1]}: {len(ch)} entries changed')
    fonts = check_font(unp)
    tag = shaper.TOKEN
    for i, (v, _) in shaped.items():
        cps = {ord(c) for c in tag.sub('', v)}
        fid = 1 if by_id[i]['stem'].startswith('kh3_event') else 3  # subtitles: $jimakuNE; menus/help: $sougei
        missing = cps - fonts[fid][2]
        assert not missing, (i, [hex(c) for c in missing])
    for fid, (old, new, _) in sorted(fonts.items()):
        if fid in FONT_IDS:
            base, h, k = info[fid]
            print(f'  font {fid} {FONT_IDS[fid]}: {old} -> {new} glyphs, baseline {base}, cap {h}, k {k:.5f}, '
                  f'join +{g[fid][0]} (measured need {g[fid][1]})')
    with open(os.path.join(OUT, 'rows.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('group\tid\tfile\tnamespace\tkey\tEN\tAR\tround_trip\n')
        for grp, ids in GROUPS + [('title screen', title)]:
            for i in ids:
                r = by_id[i]
                f.write('\t'.join([grp, i, r['stem'], r['namespace'], r['key'], r['EN'], r['AR'], shaped[i][1]]) + '\n')
    rt = collections.Counter(x for _, x in shaped.values())
    print(f'rows: {len(test)} test + {len(title)} title = {len(chosen)}; round trip {dict(rt)}')
    print(f'{PAK}: {os.path.getsize(PAK)} B sha256 {sha(open(PAK, "rb").read())}')


if __name__ == '__main__':
    main()
