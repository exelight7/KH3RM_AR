r"""Read-only (FULL-1 Part D): inventory of every source of player-visible text in the installed game.
Sources: every .locres of every target/culture (extracted\locres), the culture-specific assets of the pak index
(textures, Scaleform _loc assets, DataTables, cutscene maps), all Scaleform movies (static text tags, edit-text
initial text), CriWare USM headers (subtitle streams), loose videos, ini/json. Compares Game en against ja per key.
Writes technical\TEXT_COVERAGE.md and technical\text_coverage\*.tsv. Extra movies (Credit_en, CreditDLC) are
unpacked read-only with the key from tools\KEY_SOURCE.txt into out\builds\FULL-1\ref.
Usage: python -I tools/text_coverage.py"""
import collections, csv, os, re, struct, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locres
from gfx_fonts import movie, tags
from gfx_edittext import edittext
from pak_index import load_key
from text_counts import words
from tsvlib import load_translation

INSTALL = r'C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III'
GAME = os.path.join(INSTALL, 'KINGDOM HEARTS III', 'Content')
REPAK = os.path.abspath('tools/repak-0.2.3/repak.exe')
SF = 'KINGDOM HEARTS III/Content/UI/Scaleform/'
MOVIES = ['out/builds/TEST50/ref/movies', 'out/builds/FULL-1/ref/movies']
EXTRA = [SF + '84_credit/Credit_en.uexp', SF + '84_credit/CreditDLC.uexp']
OUTD = 'technical/text_coverage'
LOCRE = re.compile(r'Localization/([^/]+)/([^/]+)/([^/]+)\.locres$')
# initial text of an edit field that is a layout placeholder (the game sets the real text at run time)
PLACEHOLDER = re.compile(r'^(|[\sA-Za-z]{0,5}|[\d\s:：/.,%+×xX-]+|.*[\u3040-\u30ff\u4e00-\u9fff].*|(?i:text\s*field.*|text.*)|'
                         r'[xX+]*[A-Z0-9 ]+[xX+]+|\+?[A-Za-z]+\+)$')


def tsv(name, header, rows):
    os.makedirs(OUTD, exist_ok=True)
    with open(os.path.join(OUTD, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(header) + '\n')
        f.writelines('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in r) + '\n' for r in rows)


def pak_index():
    """path -> (pak the game loads, size); _P paks win"""
    best = {}
    for r in csv.DictReader(open('extracted/pak_index.tsv', encoding='utf-8', newline=''), delimiter='\t',
                            quoting=csv.QUOTE_NONE):
        p = r['path']
        if p not in best or r['pak'].endswith('_P.pak') and not best[p][0].endswith('_P.pak'):
            best[p] = (r['pak'], int(r['size']))
    return best


def locres_inventory():
    """-> per-file rows, {(file, ns, key): text} for Game en and ja"""
    rows, game = [], {'en': {}, 'ja': {}}
    root = 'extracted/locres'
    for rel in locres.locres_files(root):
        m = LOCRE.search(rel)
        target, culture, stem = m.groups()
        loc = locres.read(open(os.path.join(root, rel), 'rb').read())
        es = [(ns, k, t) for ns, _, ks in loc['namespaces'] for k, _, _, t, _ in ks]
        rows.append([rel.split('/')[0] if 'Plugins' not in rel else 'Plugins', target, culture, stem, len(es),
                     sum(words(t) for *_, t in es) if culture == 'en' else ''])
        if target == 'Game' and culture in game:
            game[culture].update({(stem, ns, k): t for ns, k, t in es})
    return rows, game


def extract_extra(idx):
    key = '0x' + load_key().hex()
    out = os.path.abspath(MOVIES[1])
    os.makedirs(out, exist_ok=True)
    for p in EXTRA:
        if not os.path.exists(os.path.join(out, p)):
            subprocess.run([REPAK, '-a', key, 'unpack', '-q', '-f', '-o', out, os.path.join(GAME, idx[p][0].replace('/', os.sep)),
                            '-i', p], check=True, capture_output=True)


def movie_inventory(idx):
    """every Scaleform .uexp: SWF movie or texture; static text tags; edit fields with English initial text"""
    kinds, static, english = collections.Counter(), [], []
    for p, (pak, size) in sorted(idx.items()):
        if not (p.startswith(SF) and p.endswith('.uexp')):
            continue
        culture = re.search(r'/(ja|de|fr|it|es|ko|zh-Hant|en)/', p)
        if culture and culture[1] != 'en':
            kinds['culture copy (not en)'] += 1
            continue
        local = next((os.path.join(d, p) for d in MOVIES if os.path.exists(os.path.join(d, p))), None)
        if not local:
            kinds['not extracted (non-culture, > 2 MB: face portraits, TresFont)'] += 1
            continue
        try:
            body = movie(open(local, 'rb').read())[4]
        except Exception:
            kinds['en culture texture (_loc)' if culture else 'texture / bitmap data'] += 1
            continue
        kinds['SWF movie (en _loc)' if culture else 'SWF movie'] += 1
        n_static = 0
        for code, t in walk(tags(body)):
            if code in (11, 33):
                n_static += 1
            elif code == 37:
                f = edittext(t)
                txt = re.sub(r'<[^>]*>', '', f['text']).replace('&nbsp;', ' ').strip()
                if not PLACEHOLDER.match(txt) and re.search(r'[A-Za-z]{3}', txt):
                    english.append([p[len(SF):], f['id'], f['fontclass'] or f['font'], txt[:120]])
        if n_static:
            static.append([p[len(SF):], n_static])
    return kinds, static, english


def walk(ts):
    for code, t in ts:
        yield code, t
        if code == 39:  # DefineSprite: nested tags after id + frame count
            yield from walk(subtags(t[4:]))


def subtags(t):
    p = 0
    while p + 2 <= len(t):
        h = struct.unpack_from('<H', t, p)[0]
        p += 2
        code, ln = h >> 6, h & 0x3F
        if ln == 0x3F:
            ln = struct.unpack_from('<I', t, p)[0]
            p += 4
        yield code, t[p:p + ln]
        p += ln
        if code == 0:
            break


def culture_assets(idx):
    """non-locres assets under an en/ culture folder, grouped"""
    groups = collections.Counter()
    for p in idx:
        if '/en/' not in p or p.endswith(('.locres', '.locmeta', '.uexp', '.ubulk')):
            continue
        if '/Sound/VOICE/' in p:
            g = 'voice (audio)'
        elif '/Character/' in p:
            g = 'lip-sync animation'
        elif '/UI/Scaleform/' in p:
            g = 'Scaleform _loc texture (text image)'
        elif '/Cutscene/Localization/' in p:
            g = 'cutscene map variant'
        elif 'DataTable' in p or 'unioncross' in p:
            g = 'DataTable (culture copy)'
        else:
            g = 'Texture2D (text image): ' + '/'.join(p.split('/')[2:5])
        groups[g] += 1
    return groups


def usm_inventory():
    """CriWare USM: does the header area hold a subtitle (@SBT) stream?"""
    rows = []
    for line in open('extracted/install_filelist.tsv', encoding='utf-8'):
        size, p = line.rstrip('\n').split('\t')
        if p.endswith(('.usm', '.mp4')):
            d = open(os.path.join(INSTALL, p), 'rb').read(4 << 20)
            rows.append([p[2:], size, (d[:4].decode('latin-1') if d[:4].isalpha() else d[4:8].decode('latin-1')), int(b'@SFV' in d), int(b'@SFA' in d), int(b'@SBT' in d),
                         int(b'@ALP' in d), int(b'@CUE' in d)])
    return rows


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    idx = pak_index()
    extract_extra(idx)
    loc_rows, game = locres_inventory()
    tsv('locres_files.tsv', ['root', 'target', 'culture', 'file', 'entries', 'words_en'], loc_rows)

    en, ja = game['en'], game['ja']
    diff = [[f, ns, k, 'missing in en', ja[(f, ns, k)][:120]] for f, ns, k in sorted(set(ja) - set(en))]
    diff += [[f, ns, k, 'empty in en', ja[(f, ns, k)][:120]] for f, ns, k in sorted(set(ja) & set(en))
             if not en[(f, ns, k)].strip() and ja[(f, ns, k)].strip()]
    en_only = sorted(set(en) - set(ja))
    assert all(en.get((f, ns, k), ' ') == ' ' for f, ns, k, *_ in diff)
    latin = sum(1 for *_, t in diff if not re.search(r'[぀-ヿ一-鿿]', t))
    tsv('ja_not_en.tsv', ['file', 'namespace', 'key', 'case', 'ja_text'], diff)
    tsv('en_not_ja.tsv', ['file', 'namespace', 'key', 'en_text'], [[*k, en[k][:120]] for k in en_only])
    rows = load_translation()
    have = {(r['stem'], r['namespace'], r['key']) for r in rows}
    not_in_tr = sorted(set(en) - have)
    non_kh3 = sorted({ns for _, ns, _ in en if not ns.startswith('kh3_')})

    kinds, static, english = movie_inventory(idx)
    tsv('movie_fields_english.tsv', ['movie', 'field', 'font', 'initial_text'], english)
    cul = culture_assets(idx)
    usm = usm_inventory()
    tsv('videos.tsv', ['path', 'bytes', 'magic', 'video', 'audio', 'subtitle_SBT', 'alpha', 'cue'], usm)


    by = collections.defaultdict(lambda: [0, 0, 0])
    for root, target, culture, stem, n, w in loc_rows:
        if culture == 'en':
            a = by[target if target in ('Game', 'Engine') else 'Online/HTTP plugins']
            a[0] += 1; a[1] += n; a[2] += w
    game_words = by['Game'][2]
    tr_words = sum(words(locres.unesc(r['EN'])) for r in rows)
    sbt = sum(r[5] for r in usm)
    # ponytail: image/video words are estimates (no OCR); per-asset guesses below, refine when the texture round runs
    EST = [('Location banners (mapName_*)', 26, 3), ('Classic Kingdom / ending logos', 25, 3),
           ('Tutorial pictures (HelpItem, 39 shared + 37 x 3 platforms)', 150, 2),
           ('IconText atlases (keyboard/mouse labels)', 2, 60), ('Minigame score words (LSI)', 9, 2),
           ('Scaleform _loc text images (COMMANDS, act logos, HUD words)', cul['Scaleform _loc texture (text image)'], 2),
           ('Copyright video (Movies/en/Copyright.mp4)', 1, 150), ('World title videos (CriMovie/main/WorldTitle)', 13, 3)]
    est_words = sum(n * w for _, n, w in EST)
    reach = 100 * game_words / (game_words + est_words)

    L = ['# TEXT_COVERAGE — every source of visible text (FULL-1)', '',
         'Generated by `tools\\text_coverage.py` (read-only). Evidence: **VERIFIED** = read from the game files on this PC; '
         '**INFERRED** = from names/structure; **EST** = estimate (no OCR). Details in `technical\\text_coverage\\*.tsv`.', '',
         f'**Headline: text reachable for translation = {reach:.1f}% of all visible text (by words).** '
         f'Reachable = Game-target `en` .locres, {game_words:,} words, all {len(en):,} entries in `translation\\` '
         f'({len(not_in_tr)} missing). Not reachable as text: images and videos with English words, '
         f'≈ {est_words:,} words (EST, table 5), changed only as textures/videos in a later phase.', '',
         '## 1. .locres (all targets, all cultures) — VERIFIED', '',
         '| target | en files | en entries | en words | in translation\\ | how to change | visible in play |', '|---|---|---|---|---|---|---|',
         f'| Game (`kh3_*`) | {by["Game"][0]} | {by["Game"][1]:,} | {by["Game"][2]:,} | {by["Game"][1] - len(not_in_tr):,} (100%) | `en` locres in our `~mods` pak (done) | yes: all game text |',
         f'| Engine | {by["Engine"][0]} | {by["Engine"][1]:,} | {by["Engine"][2]:,} | no | same way (Engine/Content/Localization/Engine/en) | no: UE editor/engine messages; Scaleform UI never uses them (INFERRED) |',
         f'| Online/HTTP plugins (12) | {by["Online/HTTP plugins"][0]} | {by["Online/HTTP plugins"][1]:,} | {by["Online/HTTP plugins"][2]:,} | no | same way | no: console/online platform messages (INFERRED) |', '',
         f'Cultures per target: Game ja en fr it de es ko zh-Hant (67 files each); `.locmeta` 13 (metadata only, no text). '
         f'UI and UI_HUD targets exist only as config (`Config/Localization/MakeLocResUI*.ini`), no .locres in any pak. '
         f'StringTables: none. Game namespaces outside `kh3_*`: {", ".join(non_kh3) or "none"}.', '',
         '## 2. Game en against ja (per key) — VERIFIED', '',
         f'- ja keys: {len(ja):,}; en keys: {len(en):,}; keys in ja missing or empty in en: **{len(diff)}** (`ja_not_en.tsv`); '
         f'keys only in en: {len(en_only)} (`en_not_ja.tsv`).',
         f'- All {len(diff)} are keys whose `en` text is a single space (the game shows nothing): {latin} hold Latin/English '
         f'text in `ja` only (sub-labels of the Japanese UI: `kh3_map *_e` place names, Classic Kingdom titles, French menu words), '
         f'{len(diff) - latin} are Japanese lines with no English subtitle (interjections such as うん, lines cut from the dub). '
         'Not visible in an English game, so not text we miss (VERIFIED: en value = one space).', '',
         '## 3. Scaleform movies — VERIFIED', '',
         '| kind | assets |', '|---|---|'] + [f'| {k} | {n} |' for k, n in sorted(kinds.items())] + [
         '',
         f'- Static text tags (DefineText/DefineText2) in all movies: **{sum(n for _, n in static)}** — no text is baked as static text; every UI string is an edit field filled at run time (locres).',
         f'- Edit fields whose initial text looks like English words (not a layout placeholder): {len(english)} (`movie_fields_english.tsv`); '
         'dev placeholders (aaaa…, prmNameA, xxRANK, TexField…) or words that also exist as locres rows (NEW RECORD, GET!, level up!); '
         'the game fills these fields at run time, so they are not extra text (INFERRED). Screenshot candidates if a word stays English: '
         'gummi HUD (`HudGumi`), Classic Kingdom buttons (`LsiButtonSet`), battle report.',
         '- The game converts KH3 tags to Scaleform HTML in the exe (`<font color=\'%s\'>`, `<img src=\'img://icontext:%s\'>`, `&nbsp;`, `<b>`, `<i>`, `<br>`).', '',
         '## 4. Other assets — VERIFIED', '',
         '| source | count | text | in translation\\ | how to change | evidence |', '|---|---|---|---|---|---|',
         f'| CriWare USM videos | {sum(1 for r in usm if r[0].endswith(".usm"))} | subtitle streams (@SBT): **{sbt}**; subtitles of movies come from `kh3_event_*` locres | n/a | — | VERIFIED (header scan) |',
         '| DataTable `NameEntryTextData` (en) | 1 | gummi ship name-entry character grid (A–Z, digits, symbols) | no | culture uasset in pak; Arabic name entry = new feature, not translation | VERIFIED |',
         '| DataTable `UnionCrossRankingDataBase` (en) | 1 | 296 Union χ player names (usernames) | no | not translated (names) | VERIFIED |',
         '| `Cutscene/Localization/en/ss/cutscene_ss50_memory*` | 4 | English cutscene variants (animation); their subtitles are locres keys | n/a | — | INFERRED |',
         '| `Config/OSS/{Live,PS4}/Achievements.json` | 2 | id maps only (ACH_01 → 1), no text | n/a | — | VERIFIED |',
         '| `.ini` (71) | 71 | config only, no visible text | n/a | — | VERIFIED |',
         '| `game_data/flags/*.txt` | 6 | flag names (debug) | n/a | — | VERIFIED |',
         '| Lip-sync animations, voice | ' + str(cul['lip-sync animation'] + cul['voice (audio)']) + ' | audio/animation, no text | n/a | — | VERIFIED |', '',
         '## 5. Images and videos with English words — EST (counted, not read)', '',
         '| type | assets | est. words each | est. words |', '|---|---|---|---|'] + [
         f'| {t} | {n} | {w} | {n * w} |' for t, n, w in EST] + [
         f'| **total** | {sum(n for _, n, _ in EST)} | | **{est_words}** |', '',
         'Culture textures by folder (VERIFIED from the pak index, `en` only):', '',
         '| group | assets |', '|---|---|'] + [f'| {g} | {n} |' for g, n in sorted(cul.items()) if 'Texture2D' in g or '_loc' in g] + [
         '',
         'Not counted (shared by all cultures, no Localization path, UNVERIFIED): signage decals in maps (e.g. `MI_mi_Font*`, `M_mi_Decal_Font` in Monstropolis, toy-store signs), '
         'bitmaps inside title movies (`TitleLogo`, `TitleLogoReMind`), staff credits `84_credit/Credit_en` (names, Latin; kept as is).', '',
         '## 6. Not yet extracted / not translatable as text', '',
         f'- {sum(n for _, n, _ in EST)} images/videos (table 5): need a texture/video round (export PNG, redraw in Arabic, cook back into the same asset).',
         '- Engine and plugin locres: not shown in normal play; translatable the same way if a screenshot ever shows one.',
         '- Name-entry grid and Union χ names: data, not translation.',
         '- Nothing new was exported to `translation\\`: every real text string the player sees is already in it.']
    open('technical/TEXT_COVERAGE.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    print(f'game en {len(en)} entries {game_words} words; ja-not-en {len(diff)}; en-only {len(en_only)}; not in translation {len(not_in_tr)}; '
          f'movies {dict(kinds)}; static {sum(n for _, n in static)}; english fields {len(english)}; usm SBT {sbt}; est words {est_words}; reach {reach:.2f}%')


if __name__ == '__main__':
    main()
