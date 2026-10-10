r"""ARABIC-TEST-2 build: title screen in Arabic (translation\ rows with status != todo, shaped) for kh3_menu + kh3_settings,
TresFont with Segoe UI Regular Arabic in $sougei (id 3) and $KH2Menu (id 4). Initial/medial forms get their left
join stroke extended by GAP so joins stay closed under the menu field's letterSpacing 2 (and overlap at 0).
Two paks, identical text, differing only in Arabic glyph scale: F1 = ARABIC-TEST-1 scale, F2 = x1.15 (baseline kept).
Writes out/builds/ARABIC-TEST-2/{F1,F2}/{pakroot,unpacked}, pakchunk99-arabictest2{F1,F2}_P.pak, pak_verify_sha256.tsv.
Usage (from the project root): python -I tools/build_arabictest2.py"""
import csv, hashlib, io, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locres, shaper, tresfont
from merge_translation import merge
from build_arabictest1 import SRC, FONT, SEGOE, CODES

OUT = 'out/builds/ARABIC-TEST-2'
REPAK = os.path.abspath('tools/repak-0.2.3/repak.exe')
LOC = 'KINGDOM HEARTS III/Content/Localization/Game/en/'
FILES = ['kh3_menu', 'kh3_settings']
GAP = math.ceil(2 * 256 / 30)  # Title menu field: $sougei 30 pt, letterSpacing 2 px = 17.07 compacted units -> 18
TIP = [('lineTo', ((0, -14),)), ('qCurveTo', ((-35, -14), (-70, 38), (-70, 70))),
       ('qCurveTo', ((-70, 102), (-35, 153), (0, 153)))]  # Segoe UI left join tip (first op lineTo or moveTo), stroke y -14..153 (font units)
JOINING = {ord(f[k]) for f in shaper.FORMS.values() for k in ('initial', 'medial') if k in f}
FONT_IDS = (3, 4)  # $sougei, $KH2Menu
VARIANTS = {'F1': 1.0, 'F2': 1.15}
sha = lambda b: hashlib.sha256(b).hexdigest()


def extend_joins(k, gap=GAP):
    """edit hook for ttf_glyphs: insert a straight stroke of `gap` compacted units before the join tip."""
    s = round(gap / k)
    shift = lambda pts: tuple((x - s, y) for x, y in pts)

    def edit(cp, ops):
        if cp not in JOINING:
            return ops
        at = [i for i in range(len(ops) - 2) if ops[i][1] == TIP[0][1] and ops[i + 1:i + 3] == TIP[1:]]
        assert len(at) == 1 and ops[at[0]][0] in ('lineTo', 'moveTo'), f'join tip not found once in U+{cp:04X}'
        i = at[0]
        return ops[:i + 1] + [('lineTo', ((-s, -14),)), ('qCurveTo', shift(TIP[1][1])),
                          ('qCurveTo', shift(TIP[2][1])), ('lineTo', ((0, 153),))] + ops[i + 3:]
    return edit


def cap(font):
    """(baseline y, cap height) of the font's 'H' in compacted units (y down)."""
    adv, si = next((a, s) for c, a, s in font['glyphs'] if c == ord('H'))
    bb = font['shapes'][si][0]
    return bb[3], bb[3] - bb[1]


def font_bytes(scale):
    a, m, fonts = tresfont.load(os.path.join('extracted/assets', FONT + '.uasset'))
    ref = cap(next(f for f in fonts.values() if f['id'] == 3))[1]
    for f in fonts.values():
        if f['id'] in FONT_IDS:
            base, h = cap(f)
            k = 256 / 2048 * scale * h / ref  # same Arabic-to-cap-height ratio as $sougei
            tresfont.add_glyphs(f, tresfont.ttf_glyphs(SEGOE, CODES, k, base, extend_joins(k)))
            print(f'  font id {f["id"]}: baseline {base}, cap height {h}, k {k:.5f}, join +{GAP} units')
    return tresfont.save(a, m, fonts)


def locres_bytes():
    rows = list(csv.DictReader(io.StringIO(merge(True).decode('utf-8'), newline=''), delimiter='\t', quoting=csv.QUOTE_NONE))
    out = {}
    for stem in FILES:
        rs = [dict(r, text=shaper.shape(r['text'])) for r in rows if r['file'] == LOC + stem + '.locres']
        out[LOC + stem + '.locres'] = locres.tsv_import(rs, open(os.path.join(SRC, LOC + stem + '.locres'), 'rb').read())
    return out


def changed_entries(old, new):
    flat = lambda d: {(ns, k): (h, t) for ns, _, es in locres.read(d)['namespaces'] for k, _, h, t, _ in es}
    a, b = flat(old), flat(new)
    assert a.keys() == b.keys() and all(a[x][0] == b[x][0] for x in a), 'keys/hashes changed'
    return {x for x in a if a[x] != b[x]}


def check_font(root):
    """only fonts 3/4 change, only by the added codes; every other tag and glyph is unchanged."""
    o = tresfont.load(os.path.join('extracted/assets', FONT + '.uasset'))
    n = tresfont.load(os.path.join(root, FONT + '.uasset'))
    tags = lambda m: [(c, d) for c, _, d in m['tags'] if c != 1005]
    assert tags(o[1]) == tags(n[1]), 'non-font tags changed'
    for i, f in o[2].items():
        g = n[2][i]
        old = {c: (a, f['shapes'][s]) for c, a, s in f['glyphs']}
        new = {c: (a, g['shapes'][s]) for c, a, s in g['glyphs']}
        assert all(new[c] == old[c] for c in old), f'existing glyph changed in font {f["id"]}'
        added = set(new) - set(old)
        assert added == (set(CODES) & set(new) if f['id'] in FONT_IDS else set()), f['id']
    return {f['id']: len(n[2][i]['glyphs']) for i, f in o[2].items()}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    loc = locres_bytes()
    report = [['variant', 'path_in_pak', 'sha256_original', 'sha256_input', 'sha256_repak_hash_list', 'sha256_unpacked', 'result']]
    for name, scale in VARIANTS.items():
        print(name, 'scale', scale)
        ua, ue = font_bytes(scale)
        files = dict(loc, **{FONT + '.uasset': ua, FONT + '.uexp': ue})
        root = os.path.join(OUT, name, 'pakroot')
        for rel, data in files.items():
            os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
            open(os.path.join(root, rel), 'wb').write(data)
        pak = os.path.join(OUT, f'pakchunk99-arabictest2{name}_P.pak')
        subprocess.run([REPAK, 'pack', '--version', 'V4', '--compression', 'Zlib', '--mount-point', '../../../', root, pak],
                       check=True, capture_output=True)
        listed = subprocess.run([REPAK, 'list', pak], check=True, capture_output=True, text=True).stdout.splitlines()
        hl = dict(l.split(' ', 1)[::-1] for l in subprocess.run([REPAK, 'hash-list', pak], check=True, capture_output=True,
                                                                 text=True).stdout.splitlines() if l.strip())
        unp = os.path.join(OUT, name, 'unpacked')
        subprocess.run([REPAK, 'unpack', '-q', '-f', '-o', unp, pak], check=True, capture_output=True)
        assert sorted(listed) == sorted(files), (listed, list(files))
        for rel, data in files.items():
            orig = open(os.path.join('extracted/locres' if rel.endswith('.locres') else 'extracted/assets', rel), 'rb').read()
            got = open(os.path.join(unp, rel), 'rb').read()
            ok = sha(data) == hl.get(rel) == sha(got)
            report.append([name, rel, sha(orig), sha(data), hl.get(rel, ''), sha(got), 'PASS' if ok else 'FAIL'])
            assert ok, rel
        for rel in loc:
            ch = changed_entries(open(os.path.join(SRC, rel), 'rb').read(), loc[rel])
            print(f'  {rel.split("/")[-1]}: {len(ch)} entries changed')
        print('  glyphs per font id:', check_font(unp))
        print(f'  {pak}: {os.path.getsize(pak)} B sha256 {sha(open(pak, "rb").read())}')
    with open(os.path.join(OUT, 'pak_verify_sha256.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join('\t'.join(r) for r in report) + '\n')
    f1, f2 = (os.path.join(OUT, v, 'pakroot') for v in VARIANTS)
    same = [rel for rel in loc if open(os.path.join(f1, rel), 'rb').read() == open(os.path.join(f2, rel), 'rb').read()]
    print('F1 vs F2: locres identical', len(same), '/', len(loc), '; TresFont differs',
          open(os.path.join(f1, FONT + '.uexp'), 'rb').read() != open(os.path.join(f2, FONT + '.uexp'), 'rb').read())


if __name__ == '__main__':
    main()
