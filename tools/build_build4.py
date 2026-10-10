r"""BUILD-4: the first full build with every translated row (all categories: story dialogue, subtitles, Re Mind,
GPT corrections, new glossary forms) = tools\build_build1.py with the BUILD-4 field table and three patched movies:
- line breaking for cutscene subtitles and field/battle voice (92_message/Subtitle #1), gummi block descriptions
  (EditGumi #385) and, for the namespaces with multi-line EN but no known field, the widest EN line of that namespace
  (rows written by `--fields` into technical\FIELD_WIDTHS.tsv); lines are counted per <pb> page;
- LV label fields widened to the LEFT (only that field's RECT changes; uasset shipped unchanged): CampMenu #335 (as
  BUILD-3, base = the _0_P patch pak), SaveLoad #43 (save card) and HudGumi #255 (gummi battle-level guide); SaveLoad
  and HudGumi have no _0_P copy, base = pakchunk0_s7-WindowsNoEditor.pak; read-only copies in extracted\assets;
- no <p align> anywhere (asserted).
-> out\builds\BUILD-4\pakchunk99-arabic_P.pak + the BUILD-1 verify tables, movie_verify.tsv, overflow.tsv.
Usage (from the project root): python -I tools/build_build4.py [--fields]   |   --installed (after SWAP_TO_BUILD4.bat)"""
import collections, csv, os, re, struct, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build1 as b, locres, shaper
from build_build3 import tag_offsets, fields as edit_fields
from build_test50 import REPAK, sha
from font_census import GAME
from gfx_fonts import movie
from pak_index import load_key
from tsvlib import load_translation

b.BUILD, b.OUT = 'BUILD-4', 'out/builds/BUILD-4'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
SF = 'KINGDOM HEARTS III/Content/UI/Scaleform/'
AR_LV = 770  # مستوى in $sougei font units (row 13858/15936/10888)
# (movie, pak with the newest copy, field, xMin twips now, xMin twips new, why)
PATCHES = [
    ('15_campmenu/CampMenu', 'Paks/pakchunk0_s7-WindowsNoEditor_0_P.pak', 335, 1922, 1739,
     'party LV label, right-aligned 16 pt: 139.1 - (770 x 16/256 + 4) = 86.975 px -> 86.95 (BUILD-3)'),
    ('17_saveload/SaveLoad', 'Paks/pakchunk0_s7-WindowsNoEditor.pak', 43, -40, -382,
     'save card LV label, LEFT-aligned 15 pt (text starts at xMin + 2): label 770 x 15/256 = 45.12 px must end 4 px '
     'before the level number (txNumLv #42 ink at 298 in the card) -> start 248.88 -> xMin 248.88 - 266 - 2 = '
     '-19.12 px -> -19.1 (twip ceil keeps the 4 px gap)'),
    ('71_gummiship/HudGumi', 'Paks/pakchunk0_s7-WindowsNoEditor.pak', 255, -40, -103,
     'gummi battle-level LV label, right-aligned 13 pt: 38 - (770 x 13/256 + 4) = -5.10 px -> -5.15 (twip floor)'),
]
# FIELD_WIDTHS rows added by --fields (evidence starts with 'BUILD-4'); measured with tools\gfx_edittext.py
SUBTITLE = ('92_message/Subtitle', '1', '$jimakuNE', '1', '38', '-519.15', '604.85', '-2', '153', '2', '')
FIXED = [
    ('kh3_event_', '^', *SUBTITLE,
     'BUILD-4: cutscene subtitles = Subtitle #1 ($jimakuNE 38 pt, centred, html multiline WORDWRAP: the engine wraps '
     'by itself, in visual order for Arabic, so every line is pre-broken); the $JimakuJP twins #2-#7 (40 pt, left) '
     'are the ja culture fields (7,168 units: EN lines up to 7,555 would not fit them); EN is pre-broken to #1 '
     '(widest page line p99 7,122 of 7,545 units, max 2 lines per <pb> page, placeholder "textField2lines."); '
     'box 151 px = 4 lines of 35.9 px (ascent 204 + descent 38 at 38 pt); max_lines 2 = the EN design, rows over it '
     'are listed, never reflowed; one-line twin #9 has the same width'),
    ('kh3_fieldvoice_', '^', *SUBTITLE,
     'BUILD-4: field/battle voice and townsfolk lines: same Subtitle #1 (UNVERIFIED in-game; no other $jimakuNE '
     'field fits): EN widths match it (p99 6,988 / town 6,507 of 7,545 units, max 2 lines per page)'),
    ('kh3_gumiship.item', '^detail_', '71_gummiship/EditGumi', '385', '$sougei', '3', '20', '-2', '468', '-2', '114',
     '', '', 'BUILD-4: gummi block descriptions: EditGumi #385 (placeholder "the description of the selected gummi '
     'block goes here", multiline wordwrap, 5 lines); EN lines up to 19,631 units are wrapped there by the engine'),
]
HELP = ('kh3_system.ability', 'kh3_menu.debugcood', 'kh3_camp.customize')  # FULL-1 help fields: reflow to 2 lines


def fields():
    """rewrite technical\\FIELD_WIDTHS.tsv: 'reflow' column (yes for the FULL-1 help fields), the FIXED rows and one
    EN-widest row per namespace that still has rows with <br>/<pb> in EN but no field (x0..x1 = that widest line in
    $sougei font units at size 256, y = its EN maximum of lines per page)"""
    with open(b.WIDTHS, encoding='utf-8') as f:
        table = [r for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
                 if not r['evidence'].startswith('BUILD-4')]
    cols = list(table[0].keys())
    if 'reflow' not in cols:
        cols.insert(cols.index('max_lines') + 1, 'reflow')
    for r in table:
        r['reflow'] = 'yes' if r['prefix'] in HELP else ''
    for x in FIXED:
        table.append(dict(zip(cols, x)))
    open(b.WIDTHS, 'w', encoding='utf-8', newline='\n').write(tsv(cols, table))  # profiles() reads the file
    profs = b.profiles()
    meter = b.meters(b.font_path('out/builds/BUILD-3/unpacked'))[3]  # same TresFont as BUILD-4 (font_bytes unchanged)
    per = collections.defaultdict(list)
    for r in load_translation():
        if ('<br>' in r['EN'] or '<pb' in r['EN']) and not b.profile(r['namespace'], r['key'], profs):
            per[r['namespace']].append(r)
    for ns, rs in sorted(per.items()):
        # wrap points the writers chose: a line ended by <br> in mid-sentence (a last line, a sentence end or a line
        # before an empty one ends a paragraph, which the engine may have wrapped)
        ended = [(l, nxt) for r in rs for p in b.PB.split(locres.unesc(r['EN']))
                 for l, nxt in zip(b.split(p), b.split(p)[1:]) if shaper.TOKEN.sub('', l).strip()]
        mid = [l for l, nxt in ended if nxt.strip() and not re.search(r'[.!?:)\]]\W*$', shaper.TOKEN.sub('', l))]
        # ponytail: no mid-sentence break -> the widest EN line of the key family (literal EN-widest rule); an
        # engine-wrapped EN paragraph then leaves Arabic unbroken there, as in BUILD-3 (listed in the report)
        family = re.compile('^(' + '|'.join(sorted({re.sub(r'\d+', r'\\d+', r['key']) for r in rs})) + ')$')
        kind = 'in mid-sentence' if mid else '(no mid-sentence break: widest EN line of these keys)'
        w = max(meter(l) for l in mid) if mid else max(
            meter(l) for r in load_translation() if r['namespace'] == ns and family.match(r['key'])
            for l in b.split(locres.unesc(r['EN'])))
        keys = '^(' + '|'.join(sorted({re.sub(r'\d+', r'\\d+', r['key']) for r in rs})) + ')$'
        n = max(b.page_lines(locres.unesc(r['EN'])) for r in rs)
        table.append(dict(zip(cols, (ns, keys, '(EN widest)', '-', '$sougei', '3', '256', '-2', f'{w + 2:.0f}', '-2',
                                     str(n * 256 + 2), '', '',
                                     f'BUILD-4 EN-widest: no field found; widest EN line ended by <br> {kind} in '
                                     f'the {len(rs)} rows with <br>/<pb> = {w:.0f} $sougei units (safe: EN shows it '
                                     f'unbroken; a paragraph end may be engine-wrapped, so mid-sentence breaks are '
                                     f'preferred), EN max {n} lines per page'))))
    open(b.WIDTHS, 'w', encoding='utf-8', newline='\n').write(tsv(cols, table))
    print(f'{b.WIDTHS}: {len(table)} rows ({len(FIXED)} measured + {len(per)} EN-widest)')


def tsv(cols, table):
    return '\t'.join(cols) + '\n' + ''.join('\t'.join(r[c] for c in cols) + '\n' for r in table)


def patch(d, field, old, new):
    """the movie with one edit field's xMin set to new twips (same RECT bit width: file size unchanged)"""
    sig, ver, size, at, body = movie(d)
    assert sig == b'GFX', 'compressed movie: offsets would not map'
    p = next(p for c, p, n in tag_offsets(body) if c == 37 and struct.unpack_from('<H', body, p)[0] == field)
    q = at + 8 + p + 2  # RECT in the file
    nb = d[q] >> 3
    nbytes = (5 + 4 * nb + 7) // 8
    bits = int.from_bytes(d[q:q + nbytes], 'big')
    shift = nbytes * 8 - 5 - nb
    mask = (1 << nb) - 1
    assert (bits >> shift) & mask == old & mask and -(1 << (nb - 1)) <= new < 1 << (nb - 1)
    bits = bits & ~(mask << shift) | (new & mask) << shift
    return d[:q] + bits.to_bytes(nbytes, 'big') + d[q + nbytes:]


def verify(name, field, old, new):
    """re-parse: only that field's bounds differ -> table rows"""
    assert len(old) == len(new)
    diff = [i for i in range(len(old)) if old[i] != new[i]]
    fo, fn = edit_fields(old), edit_fields(new)
    changed = [i for i in fo if fo[i] != fn[i]]
    assert changed == [field] and {k for k in fo[field] if fo[field][k] != fn[field][k]} == {'bounds'}
    assert fn[field]['bounds'][1:] == fo[field]['bounds'][1:]
    so, sn = movie(old), movie(new)
    assert [(c, n) for c, p, n in tag_offsets(so[4])] == [(c, n) for c, p, n in tag_offsets(sn[4])]
    return [[name, 'size', f'{len(old)} = {len(new)} B'],
            [name, 'bytes differing', f'{len(diff)} (file offsets {diff[0]}..{diff[-1]}, inside the #{field} RECT)'],
            [name, 'edit fields', f'{len(fo)}; changed: {changed} (bounds only)'],
            [name, f'#{field} bounds px', f'{fo[field]["bounds"]} -> {fn[field]["bounds"]}'],
            [name, 'tags', f'{sum(1 for _ in tag_offsets(sn[4]))} top-level tags, same codes and lengths'],
            [name, 'sha256 base', sha(old)], [name, 'sha256 patched', sha(new)]]


def movie_files():
    """patched movies (uexp) + their unchanged uasset; base copies extracted read-only into extracted\\assets"""
    out, table = {}, [['movie', 'check', 'result']]
    for mv, pak, field, old, new, why in PATCHES:
        rel = SF + mv
        if not all(os.path.exists(os.path.join('extracted/assets', rel + e)) for e in ('.uasset', '.uexp')):
            subprocess.run([REPAK, '-a', '0x' + load_key().hex(), 'unpack', '-q', '-f', '-o', 'extracted/assets',
                            os.path.join(GAME, pak.replace('/', os.sep)), '-i', rel + '.uasset', '-i', rel + '.uexp'],
                           check=True, capture_output=True)
        ua, ue = (open(os.path.join('extracted/assets', rel + e), 'rb').read() for e in ('.uasset', '.uexp'))
        new_ue = patch(ue, field, old, new)
        table += verify(mv.split('/')[-1], field, ue, new_ue) + [[mv.split('/')[-1], 'base pak', pak], [mv.split('/')[-1], 'why', why]]
        out.update({rel + '.uasset': ua, rel + '.uexp': new_ue})
    with open(os.path.join(b.OUT, 'movie_verify.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in table)
    return out


def overflow():
    """rows whose Arabic needs more lines per page than the field shows (wrapped.tsv OVERHEIGHT/OVERWIDE) ->
    overflow.tsv with EN and AR (the report lists them; nothing is shortened)"""
    rows = {r['id']: r for r in load_translation()}
    with open(os.path.join(b.OUT, 'wrapped.tsv'), encoding='utf-8') as f:
        w = [r for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE) if r['check'] != 'ok']
    with open(os.path.join(b.OUT, 'overflow.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tfield\tcheck\tlines_needed\tlines_fit\tEN\tAR\n')
        f.writelines(f"{r['id']}\t{r['field']}\t{r['check']}\t{r['lines_after']}\t{r['lines_fit']}\t"
                     f"{rows[r['id']]['EN']}\t{rows[r['id']]['AR']}\n" for r in w)
    print('overflow:', dict(collections.Counter((r['field'], r['check']) for r in w)))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1:] == ['--installed']:
        b.installed()
    elif sys.argv[1:] == ['--fields']:
        fields()
    else:
        os.makedirs(b.OUT, exist_ok=True)
        b.EXTRA = movie_files()
        b.main()
        unp = os.path.join(b.OUT, 'unpacked')
        for d, _, fs in os.walk(unp):
            for fn in fs:
                if fn.endswith('.locres'):
                    for ns, _, es in locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                        assert not any('<p align' in t.lower() for _, _, _, t, _ in es), (fn, ns)
        print('no <p align> in any built locres')
        overflow()
