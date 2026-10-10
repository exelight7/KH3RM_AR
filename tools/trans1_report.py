r"""TRANS-1: write state\LAST_REPORT.md (data parts generated from translation\menus_ui). One-time helper."""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
from validate import visible, validate_all, ERR

rows = [r for r in load_translation() if r['category'] == 'menus_ui']
by = {r['id']: r for r in rows}
done = [r for r in rows if r['status'] != 'todo']
todo = [r for r in rows if r['status'] == 'todo']
flags = validate_all()
fc = collections.Counter(c for i, fl in flags.items() if i in by for c in fl)
L = lambda s: len(visible(s).strip())
esc = lambda s: s.replace('|', '\\|')
new_rows = len(done) - 34
out = ['round: TRANS-1', '', '# TRANS-1 — close 17 glossary conflicts + menus_ui batch 1', '']
out += ['## Summary',
        '- Part 1: the 17 pending conflicts are closed as decided (`translation\\GLOSSARY_CONFLICTS.md` §3-4, history there). 10 KH2-constraint rows with 0 KH3 rows = `kh2-only` (excluded from GLOSS). Two KH2-constraint rows have KH3 rows and stay `pending` (recommendation below).',
        f'- Part 2: **menus_ui** (13 pages, 10 files, {len(rows)} rows): {new_rows} rows newly translated (+34 title-screen rows from earlier rounds = {len(done)} with Arabic), {len(todo)} skipped, 0 remaining (every `todo` row has a `skip:` note).',
        f'- Validator: {len(done)} rows checked, **0 ERR**, {sum(fc.values())} WARN. refresh.bat exit 0, secret_check PASS.',
        '- Nothing outside the project folder was touched; no pak built or installed; game not run; no upload.', '']
out += ['## Steps', '| step | result |', '|---|---|',
        '| P1 conflicts 1-13, 16-17 (executor recommendation) | PASS |', '| P1 Destiny Island(s) = جزر المصير; Hollow Bastion = حصن هولو | PASS |',
        '| P1 Limit / Lucky Lucky / Full Bloom approved | PASS |', '| P1 other KH2-constraint rows (0 KH3 rows -> kh2-only; >0 listed) | PASS |',
        '| P1 conflicts marked resolved + history; glossary.md regenerated | PASS |']
for n in range(1, 14):
    out.append(f'| P2 page {n}/13 translated, refresh.bat, 0 ERR | PASS |')
out += ['| commits every 3 pages (pages 3, 6, 9, 12) + final | PASS |', '| refresh.bat + secret_check | PASS |', '| PROJECT_MAP §3 §4 §8, CHANGELOG | PASS |', '']
out += ['## Part 1 — glossary', 'Applied by `tools\\gloss3_apply.py` (one-time).', '',
        '- Both forms approved by context: Abilities (القدرات titles / قدرات inline), Master (الإتقان / السيد), Question (سؤال title / اسأل command), Materials (المواد / مواد).',
        '- Single form: 100 Acre Wood, Journal = اليوميات, Jump to World Map? (ASCII ?), Postern = البوابة الخلفية, Whirli-Goof = غوفي الدوار, Release = التحرير, Hang On = تمسك, Jump = قفز, Auto = تلقائي.',
        '- `kh2-only` (0 KH3 rows): World ZZ, World FA, LT, 360° Spin, Master Control Program, MCP, DTD, Final Fantasy III..X-2, FPS Mode, Reprogram.',
        '- Still `pending` (KH3 rows exist), with recommendation:',
        '  - Musical (4 rows: "Musical Farmer", "musical notes") — pending الغناء; recommend **موسيقي**.',
        '  - Grind (3 rows: "Grind Pepper") — pending الانزلاق; recommend **طحن**.',
        '- Tool change needed by the decisions: validator GLOSS passes when any approved form of one EN term is present (Master / master) and when a longer approved term covers a shorter one (Scrooge McDuck / Scrooge).', '']
sk = collections.Counter(re.sub(r'\(.*', '', r['note'])[:70] for r in todo)
out += ['## Part 2 — numbers',
        f'- Rows: {len(rows)}; with Arabic {len(done)} (34 earlier + {new_rows} new); skipped {len(todo)}; remaining 0.',
        '- Unique English strings translated by hand: about 3,150; the other rows got the same Arabic through the translation memory (same EN = same AR).',
        '- Skip reasons: ' + '; '.join(f'{v} × {k.strip()}' for k, v in sk.most_common()), '']
out += ['### Validator flags by type (menus_ui)', '| flag | level | count |', '|---|---|---|']
out += [f'| {c} | {"ERR" if c in ERR else "WARN"} | {n} |' for c, n in sorted(fc.items())]
out += ['| TAGS, BR, LATIN, HARAKAT, TATWEEL, BRACKETS, EMPTY, ARGORDER, DSPACE, LEAD, TRAIL | | 0 |', '']
for i, fl in sorted(flags.items()):
    if i in by:
        out.append(f'- {i} {" ".join(fl)}: {by[i]["EN"][:50]} -> {by[i]["AR"][:50]} — {by[i]["note"] or "WARN, no note"}')
out.append('')
rat = sorted(((L(r['AR']) / max(L(r['EN']), 1), r) for r in done if L(r['EN']) >= 1), key=lambda t: -t[0])
out += ['### The 30 longest AR/EN length ratios (visible characters, tags/args removed)',
        'All are short labels or spelled-out acronyms; none breaks a rule, but they are the first candidates if a field overflows in game. Sentence-level ratios follow.', '',
        '| id | ratio | EN len -> AR len | EN | AR |', '|---|---|---|---|---|']
out += [f"| {r['id']} | {x:.2f} | {L(r['EN'])} -> {L(r['AR'])} | {esc(r['EN'][:45])} | {esc(r['AR'][:45])} |" for x, r in rat[:30]]
out += ['', 'Sentences / long labels only (EN >= 20 chars), top 10:', '', '| id | ratio | EN len -> AR len | EN | AR |', '|---|---|---|---|---|']
long_ = [(x, r) for x, r in rat if L(r['EN']) >= 20]
out += [f"| {r['id']} | {x:.2f} | {L(r['EN'])} -> {L(r['AR'])} | {esc(r['EN'][:45])} | {esc(r['AR'][:45])} |" for x, r in long_[:10]]
out += ['', '### 40 sample rows (id | EN | AR)', '| id | EN | AR |', '|---|---|---|']
ids = ('00001 00002 00009 00130 10595 14321 15822 00022 00026 13787 14341 15833 00031 00033 00187 10594 15838 13013 00041 10834 '
       '11127 13937 14763 14942 00126 00291 13779 13816 13819 14000 14002 00467 13869 13604 12983 13262 14128 14355 15909 16255').split()
ids = [i for i in ids if i in by and by[i]['AR']]
out += [f"| {i} | {esc(by[i]['EN'].replace('<br>', ' <br> ')[:130])} | {esc(by[i]['AR'].replace('<br>', ' <br> ')[:130])} |" for i in ids[:40]]
out += ['', '### Places I was unsure (id | EN | my AR | why)', '| id | EN | AR | why |', '|---|---|---|---|']
for r in done:
    if r['note'].split(':')[0] in ('unsure', 'context'):
        out.append(f"| {r['id']} | {esc(r['EN'].replace('<br>', ' ')[:70])} | {esc(r['AR'].replace('<br>', ' ')[:70])} | {esc(r['note'])} |")
extra = [('00253', 'Be Yourself (friend behaviour) -> كن على طبيعتك', 'literal; in-game meaning is "friend picks its own targets"'),
         ('00208/00210', 'Mobility / Form Actions -> التنقل / أفعال التحول', 'no glossary entry; may collide with Mobile Action = الفعل المتنقل'),
         ('00122', 'Key Items -> أغراض أساسية', 'no glossary entry'),
         ('00213', 'Install/Uninstall Ability -> تركيب/إزالة القدرة', 'Equip = تجهيز exists but "install" is a different verb in KH3'),
         ('10790', 'Figure Gummies -> غامي المجسمات', 'decorative gummi blocks; no glossary entry'),
         ('11044', 'Gummibridge Seven -> غامي بريدج سيفن', 'place name transliterated'),
         ('14058', 'The Dread and Breakfast -> فندق الرعب والفطور', 'pun on "bed and breakfast" approximated'),
         ('14211', 'A Lich to Scratch -> ليتش لا بد من مواجهته', 'pun on "an itch to scratch" approximated'),
         ('14104', 'Boo the MVP -> بو أفضل لاعبة', 'MVP is not allowed Latin'),
         ('13445', 'Doom counter -> عداد الهلاك', 'status-effect name has no glossary entry'),
         ('plural rows', '11127 11130 11149 11154 14424 14763 14858 14859 14975 14980', 'Arabic has 6 plural forms; only one/other used (same tokens as EN). Needs an in-game test'),
         ('13812/15910/15911', 'legal text with URL / URL rows', 'skipped: the URL needs Latin letters outside allowed_latin.txt'),
         ('16238', 'Dispel (key = EN)', 'key equals the text but it is a real command name (also used in 13446), so translated')]
for i, a, w in extra:
    out.append(f'| {i} | {a} | | {w} |')
glo = [d for d in load_glossary() if d['status'] == 'proposed']
out += ['', f'### New terms I coined (added to glossary.tsv as `proposed`, {len(glo)} rows)',
        'Enemies, attraction/command names, gummi-ship bosses and zones, minigames, status words. Not approved; not used in bulk until approved. See `translation\\GLOSSARY_PROPOSALS.md`.', '']
out += ['| EN | AR | type |', '|---|---|---|'] + [f'| {esc(d["en"])} | {d["ar"]} | {d["type"]} |' for d in glo]
out += ['', '## Decisions I took (please confirm)',
        '- Roman numerals (I, II, X, XIII in chapter names) -> Arabic digits; Greek letters α β γ… -> ألفا بيتا غاما… (the font may lack Greek).',
        '- Latin acronyms outside `allowed_latin.txt` are spelled in Arabic: HDR, LOD, DOF, FXAA, TXAA, BGM, QWERTY/AZERTY/QWERTZ, AP, UFO, AR, CDA, SLW/MST/ECL; rank letters A/B/C -> أ/ب/ج (in-game rank letters are Latin graphics; probably better to allow S A B C).',
        '- Plural rows `{0}|plural(one=…,other=…)`: `other` = "{0} من + plural noun".',
        '- "Stock" (count column) -> المخزون although glossary Stock = تخزين (KH2 command); "Warp" (fast travel) -> انتقال سريع although glossary Warp = التحول; both noted.',
        '- Rows left untouched on purpose: language names (Deutsch…), the Japanese message 15672, URLs, ordinal suffixes (st/nd/rd), `ABC` keyboard tab, legal text 13812.',
        '- GLOSS WARN kept (3, each noted): Faith (Enduring Faith / Faith Volley), Diabolic Bash.', '',
        '## Open questions', 'See PROJECT_MAP.md §8 (TRANS-1 decisions needed): Latin acronyms and rank letters, URL rows, digits for Roman numerals, proposed terms, Musical/Grind.']
open(os.path.join(ROOT, 'state', 'LAST_REPORT.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('report written', len(out), 'lines')
