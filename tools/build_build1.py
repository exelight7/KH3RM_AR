r"""BUILD-1 build: every translated row of every category (status != todo, AR not empty) shaped into the en .locres,
every other row original English; lines wider than their text field are broken first (shaper.wrap) with the glyph
advances of the rebuilt TresFont and the field widths in technical\FIELD_WIDTHS.tsv (namespace prefix -> movie
field; keys = regex of the body/description keys shown in it); all other rows stay unbroken. TresFont = the TEST50
font (Arabic set at the locked F1 scale in $jimakuNE, $JimakuJP, $sougei, $KH2Menu).
Writes out\builds\BUILD-1\{pakroot,unpacked}, pakchunk99-arabic_P.pak, pak_verify_sha256.tsv, changed_per_locres.tsv,
wrapped.tsv (every row the wrap changed or that still overflows its field).
Usage (from the project root): python -I tools/build_build1.py   |   --installed (after SWAP_TO_BUILD1.bat: writes
state\INSTALLED.tsv)"""
import collections, csv, hashlib, math, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locres, shaper, tresfont
from tsvlib import load_translation, PREFIX
from build_arabictest1 import SRC, FONT
from build_arabictest2 import changed_entries
from build_test50 import REPAK, FONT_IDS, gaps, font_bytes, check_font, sha

BUILD = 'BUILD-1'  # tools/build_build2.py sets BUILD/OUT/PAK for the next full build
OUT = 'out/builds/BUILD-1'
PAK = os.path.join(OUT, 'pakchunk99-arabic_P.pak')
WIDTHS = 'technical/FIELD_WIDTHS.tsv'
MODS = r'C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods'
EXTRA = {}  # tools/build_build3.py: more pak files (path in pak -> bytes; original in extracted/assets), e.g. a patched movie
ALIGN_RIGHT = set()  # tools/build_build3.py: row ids whose built text is wrapped in <p align="right">..</p> (alignment test)
MARGIN = 0.97  # ponytail: safety margin on the measured field width (icon/{n} widths are estimates); tune in-game
GUTTER = 4  # Flash text fields keep 2 px on each side


def profiles():
    """-> [(prefix, font id, capacity in font units, lines that fit, row)] longest prefix first; row['keys'] = key regex"""
    out = []
    with open(WIDTHS, encoding='utf-8') as f:
        table = list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))
    for r in table:
        size = float(r['size_pt'])
        cap = (float(r['x1']) - float(r['x0']) - GUTTER) * 256 / size * MARGIN
        fit = float(r['max_lines']) if r.get('max_lines') else (float(r['y1']) - float(r['y0']) - GUTTER) / size
        out.append((r['prefix'], int(r['font_id']), cap, fit, r))
    return sorted(out, key=lambda p: -len(p[0]))


def profile(ns, key, profs):
    """the field profile of one row: longest namespace prefix whose key regex matches (BUILD-4: a shorter prefix is
    tried when the longest one's keys do not match); None if no field shows that key"""
    return next((p for p in profs if ns.startswith(p[0]) and re.match(p[4]['keys'], key)), None)


def meters(font_path):
    """font id -> shaper.meter over that font's glyph advances (font units, 256 = 1 em)"""
    fonts = tresfont.load(font_path)[2].values()
    return {f['id']: shaper.meter({c: a for c, a, _ in f['glyphs']}) for f in fonts if f['id'] in FONT_IDS}


def split(text):
    """logical lines of a row (a whole-row conv pair removed first)"""
    m = shaper.CONV.fullmatch(text)
    return shaper.BREAK.split(m[2] if m else text)[::2]


PB = re.compile(r'<pb(?:\([^)]*\))?>')


def page_lines(text):
    """BUILD-4: lines of the fullest page; <pb> starts a new page (a new subtitle or popup screen), <br> a new line"""
    return max(len(split(p)) for p in PB.split(text))


def font_path(root):
    return os.path.join(root, FONT + '.uasset')


def shape_rows(rows, meter, profs):
    """every translated row (status != todo, AR not empty) -> {id: visual text}, the wrap report rows, round-trip counts"""
    shaped, wrapped, rt = {}, [], collections.Counter()
    for r in rows:
        if r['status'] == 'todo' or not r['AR']:
            continue
        logical = locres.unesc(r['AR'])
        p = profile(r['namespace'], r['key'], profs)
        text = logical
        if p and shaper.has_letters(logical):
            prefix, fid, cap, fit, prow = p
            if prow.get('reflow') and page_lines(logical) > fit:  # FULL-1: fewer visible lines than the row has
                text = shaper.reflow(logical)
            text = shaper.wrap(text, cap, meter[fid])
            lines = split(text)
            widest = max(meter[fid](l) for l in lines)
            over = [l for l in lines if meter[fid](l) > cap]
            need = page_lines(text)
            if text != logical or over or need > fit:
                wrapped.append([r['id'], r['namespace'], r['key'], f'{prow["movie"]}#{prow["field"]}', str(round(cap)),
                                str(page_lines(logical)), str(need), str(math.floor(fit)),
                                str(round(widest)), 'OVERWIDE' if over else 'OVERHEIGHT' if need > fit else 'ok'])
        v = shaper.shape(text)
        u = shaper.unshape(v)
        kind = 'exact' if u == text else 'same-visual' if shaper.shape(u) == v else 'FAIL'
        assert kind != 'FAIL', r['id']
        rt[kind] += 1
        shaped[r['id']] = f'<p align="right">{v}</p>' if r['id'] in ALIGN_RIGHT else v
    return shaped, wrapped, rt


def installed():
    """after the install: the pak in ~mods must be this build; state/INSTALLED.tsv = the rows whose text in it is the
    shaping of their current AR (stats.py counts them as installed; an AR edited later no longer counts)"""
    mods = os.path.join(MODS, os.path.basename(PAK))
    assert sha(open(mods, 'rb').read()) == sha(open(PAK, 'rb').read()), 'the pak in ~mods is not this build'
    rows = load_translation()
    shaped = shape_rows(rows, meters(font_path(os.path.join(OUT, 'unpacked'))), profiles())[0]
    have = {}
    for rel in {PREFIX + r['stem'] + '.locres' for r in rows if r['id'] in shaped}:
        for ns, _, es in locres.read(open(os.path.join(OUT, 'unpacked', rel), 'rb').read())['namespaces']:
            have.update({(ns, k): t for k, _, _, t, _ in es})
    ok = [r for r in rows if r['id'] in shaped and have.get((r['namespace'], r['key'])) == shaped[r['id']]]
    with open('state/INSTALLED.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tar_sha1\tbuild\n')
        f.writelines(f"{r['id']}\t{ar_hash(r['AR'])}\t{BUILD}\n" for r in ok)
    print(f'state/INSTALLED.tsv: {len(ok)} of {len(shaped)} shaped rows found in the installed pak')


def ar_hash(ar):
    return hashlib.sha1(ar.encode('utf-8')).hexdigest()[:10]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    root = os.path.join(OUT, 'pakroot')
    g = gaps()
    (ua, ue), info = font_bytes(g)
    files_out = {FONT + '.uasset': ua, FONT + '.uexp': ue, **EXTRA}
    for rel, data in files_out.items():
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        open(os.path.join(root, rel), 'wb').write(data)
    meter, profs = meters(font_path(root)), profiles()
    rows = load_translation()
    shaped, wrapped, rt = shape_rows(rows, meter, profs)
    files = sorted({PREFIX + r['stem'] + '.locres' for r in rows if r['id'] in shaped})

    loc = {}
    for rel in files:
        out = [dict(namespace=r['namespace'], key=r['key'], source_hash=r['source_hash'],
                    text=locres.esc(shaped[r['id']]) if r['id'] in shaped else r['EN'])
               for r in rows if PREFIX + r['stem'] + '.locres' == rel]
        loc[rel] = locres.tsv_import(out, open(os.path.join(SRC, rel), 'rb').read())
    files_out.update(loc)
    for rel, data in loc.items():
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        open(os.path.join(root, rel), 'wb').write(data)

    subprocess.run([REPAK, 'pack', '--version', 'V4', '--compression', 'Zlib', '--mount-point', '../../../', root, PAK],
                   check=True, capture_output=True)
    listed = subprocess.run([REPAK, 'list', PAK], check=True, capture_output=True, text=True).stdout.splitlines()
    hl = dict(l.split(' ', 1)[::-1] for l in subprocess.run([REPAK, 'hash-list', PAK], check=True, capture_output=True,
                                                             text=True).stdout.splitlines() if l.strip())
    unp = os.path.join(OUT, 'unpacked')
    subprocess.run([REPAK, 'unpack', '-q', '-f', '-o', unp, PAK], check=True, capture_output=True)
    assert sorted(listed) == sorted(files_out), (sorted(set(listed) ^ set(files_out)))
    report = [['path_in_pak', 'sha256_original', 'sha256_input', 'sha256_repak_hash_list', 'sha256_unpacked', 'result']]
    for rel, data in sorted(files_out.items()):
        orig = open(os.path.join('extracted/locres' if rel.endswith('.locres') else 'extracted/assets', rel), 'rb').read()
        got = open(os.path.join(unp, rel), 'rb').read()
        ok = sha(data) == hl.get(rel) == sha(got)
        report.append([rel, sha(orig), sha(data), hl.get(rel, ''), sha(got), 'PASS' if ok else 'FAIL'])
        assert ok, rel
    with open(os.path.join(OUT, 'pak_verify_sha256.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join('\t'.join(r) for r in report) + '\n')

    # re-parse: exactly the rows whose text differs from EN changed, per locres
    by_id = {r['id']: r for r in rows}
    want = collections.Counter(PREFIX + by_id[i]['stem'] + '.locres' for i, v in shaped.items()
                               if locres.esc(v) != by_id[i]['EN'])
    entries = collections.Counter(PREFIX + r['stem'] + '.locres' for r in rows)
    per = [['locres', 'entries', 'changed']]
    for rel in sorted(loc):
        ch = changed_entries(open(os.path.join(SRC, rel), 'rb').read(), open(os.path.join(unp, rel), 'rb').read())
        assert len(ch) == want[rel], (rel, len(ch), want[rel])
        per.append([rel.split('/')[-1], str(entries[rel]), str(len(ch))])
    per.append(['TOTAL', str(sum(entries[r] for r in loc)), str(sum(want.values()))])
    with open(os.path.join(OUT, 'changed_per_locres.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join('\t'.join(r) for r in per) + '\n')

    # fonts: only the new codes; every Arabic code point of the output is in all 4 classes; other new characters
    # (not in the row's EN) must be in $sougei
    fonts = check_font(unp)
    missing = collections.Counter()
    for i, v in shaped.items():
        chars = set(shaper.TOKEN.sub('', v))
        for c in chars:
            if shaper.is_arabic(c):
                assert all(ord(c) in fonts[fid][2] for fid in FONT_IDS), (i, hex(ord(c)))
            elif c not in by_id[i]['EN'] and ord(c) not in fonts[3][2]:
                missing[c] += 1
    with open(os.path.join(OUT, 'wrapped.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tnamespace\tkey\tfield\tcapacity_units\tlines_before\tlines_after\tlines_fit\twidest_units\tcheck\n')
        f.writelines('\t'.join(w) + '\n' for w in wrapped)
    for fid, (old, new, _) in sorted(fonts.items()):
        if fid in FONT_IDS:
            base, h, k = info[fid]
            print(f'  font {fid} {FONT_IDS[fid]}: {old} -> {new} glyphs, k {k:.5f}, join +{g[fid][0]}')
    checks = collections.Counter(w[-1] for w in wrapped)
    print(f'rows shaped: {len(shaped)}; round trip {dict(rt)}; wrap changed {sum(1 for w in wrapped if w[5] != w[6])} '
          f'rows; checks {dict(checks)}; characters missing in $sougei: {dict(missing)}')
    for r in per[1:]:
        print('  ' + '\t'.join(r))
    print(f'{PAK}: {os.path.getsize(PAK)} B sha256 {sha(open(PAK, "rb").read())}')


if __name__ == '__main__':
    installed() if sys.argv[1:] == ['--installed'] else main()
