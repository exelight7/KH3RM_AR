r"""TRANS-2: write state\LAST_REPORT.md (data parts generated from translation\ and review\corrections\applied). One-time helper."""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
from validate import visible, validate_all, ERR

sys.stdout.reconfigure(encoding='utf-8')
rows = load_translation()
by = {r['id']: r for r in rows}
ia = [r for r in rows if r['category'] == 'items_abilities']
done = [r for r in ia if r['status'] != 'todo']
todo = [r for r in ia if r['status'] == 'todo']
flags = validate_all()
fc_all = collections.Counter(c for fl in flags.values() for c in fl)
fc_ia = collections.Counter(c for i, fl in flags.items() if by[i]['category'] == 'items_abilities' for c in fl)
L = lambda s: len(visible(s).strip())
esc = lambda s: s.replace('|', '\\|').replace('\n', ' ')


def applied(name):
    p = os.path.join(ROOT, 'review', 'corrections', 'applied', name)
    return read_tsv(p)[1:] if os.path.exists(p) else []


latin = applied('trans2_latin.tsv') + applied('trans2_latin2.tsv')
EZPRO = {'13475', '13476', '13477', '14751', '14752', '14753', '14754', '14845', '14857'}
fix = applied('trans2.tsv') + [r for r in applied('trans2_fix.tsv') if r[0] not in EZPRO]
reverted = len(EZPRO)
other = applied('trans2_p4fix.tsv') + applied('trans2_p8fix.tsv')
tm_total = sum(1 for r in ia if r['AR'])
distinct = len({r['EN'] for r in done})

out = ['round: TRANS-2', '', '# TRANS-2 — Latin policy, supervisor fixes, items_abilities batch 2', '', '## Summary',
       f'- Part 1: validator LATIN rule replaced (ERR if AR has a Latin/Greek/Roman token missing from the same row\'s EN; `allowed_latin.txt` no longer read, kept as history); 8 unit tests pass. menus_ui re-pass: **{len(latin) - reverted} rows** changed ({len(latin)} applied, {reverted} EZ/PRO Code rows reverted to the approved glossary Arabic).',
       f'- Part 2: supervisor fixes applied: **{len(fix)} rows** changed in menus_ui + glossary decisions (39 TRANS-1 proposals approved or changed, AP and CDA rows dropped).',
       f'- Part 3: **items_abilities** ({len(ia)} rows, 3 files, 8 pages): {len(done)} translated, {len(todo)} skipped (all empty / symbol rows), 0 remaining; about {distinct} distinct English strings.',
       f'- Validator over everything: 5,764 rows checked, **0 ERR**, {fc_all.get("GLOSS", 0)} GLOSS + {fc_all.get("RATIO", 0)} RATIO WARN ({sum(fc_ia.values())} of them in items_abilities, each below).',
       '- refresh.bat exit 0 after every page, secret_check PASS. No pak built or installed; game not run; nothing outside the project folder touched; no upload.', '']
out += ['## Steps', '| step | result |', '|---|---|', '| P1 validate.py LATIN rule + tests (8 tests) | PASS |', '| P1 RULES.md, glossary rules (make_glossary.py), PROJECT_MAP §4 | PASS |',
        '| P1 menus_ui re-pass (acronyms, letters, Greek, Roman numerals, brands, URLs, legal text) | PASS |', '| P2 trans2.tsv fixes (14128, 14355, Heartless family, Flan, Surge, Standard Mode) | PASS |',
        '| P2 glossary: Teeny Ship α/β, AR device, Musical, Grind, Stock, Warp, approvals | PASS |']
for n in range(1, 9):
    out.append(f'| P3 page {n}/8 items_abilities translated, refresh.bat, 0 ERR | PASS |')
out += ['| commits (pages 3, 6, 8) + final | PASS |', '| refresh.bat + secret_check | PASS |', '| PROJECT_MAP §3 §4 §8, CHANGELOG | PASS |', '']
out += ['## Part 1 — Latin policy', '### Rule (validator)',
        '`LATIN` = ERR when a Latin letter run (A-Z, accented Latin), Greek run or Roman-numeral character run in AR does not appear (case-sensitive) among the same kinds of tokens in the row\'s EN. Tags and `{n}` count as word breaks, so `Re<icon>Mind` is the tokens Re and Mind. The multiplication sign × is not Latin.', '',
        '### What the re-pass restored (menus_ui)',
        '- Acronyms: HDR, LOD, DOF, FXAA, TXAA, BGM, QWERTY/AZERTY/QWERTZ, AP, UFO, AR (AR device = جهاز AR), CDA, MVP, K.O., PC (جهاز PC), SW/HP/MP.',
        '- Letters: Shortcut Set A/B/C, Type A/B, Course A/B, Game A/B, rank letters A/C, suffixes S M P E D OKP OBV, floors 1F 2F 3F, sector codes SLW- MST- ECL-, unit `p`.',
        '- Greek: α β γ δ ε ζ η θ ι (Treasure Sphere, Teeny Ship), χ (Union χ, Dark Inferno χ, χ-blade).',
        '- Roman numerals in chapter/interval/theater titles (Chapter II, Interval VI-1, Final Confrontations IV, Tres V, KINGDOM HEARTS II.9, KINGDOM HEARTS III); EX.',
        '- Brands: PlayStation®4, Epic Games, Re Mind (row 00714), The Walt Disney Company and Square Enix Co., Ltd (legal text).',
        '- Newly translated: legal row 13812 (URL verbatim) and the two URL rows 15910/15911 (verbatim).',
        '- Kept Arabic on purpose (glossary or plain word): EXP = خبرة (approved glossary), LV = مستوى (decision GLOSS-2), EZ Codes / PRO Codes (approved glossary; I first changed them and then reverted), ON / OFF / NEW GAME / COMPLETE / RECORD (plain words in caps), character, place and dish names with accents (Naminé, Saïx, Poêlé…), km / mi, Alpha / Beta (words), U-turn, language names and the Japanese message untouched.', '',
        f'### Rows changed in the re-pass: {len(latin) - reverted} net', '20 examples:', '', '| id | old | new |', '|---|---|---|']
ex = '00226 00441 10889 10958 10981 11008 11022 11313 13079 13205 13812 13958 13973 14104 14219 15004 15669 15697 15775 16255'.split()
lm = {r[0]: r for r in latin}
for i in ex:
    if i in lm:
        out.append(f'| {i} | {esc(lm[i][1][:70])} | {esc(lm[i][2][:70])} |')
out += ['', f'### Part 2 — supervisor fixes: {len(fix)} rows changed', '| id | old | new |', '|---|---|---|']
for r in fix:
    out.append(f'| {r[0]} | {esc(r[1][:50])} | {esc(r[2][:50])} |')
out += ['', 'Glossary (translation\\glossary.tsv): Flan = بودينغ, The Flantastic Seven = البودينغ السبعة الرائعون, Surge = التسارع, Standard Mode = الوضع العادي, Teeny Ship α/β = سفينة صغيرة α/β, AR device = جهاز AR, Musical = موسيقي, Grind = طحن (all approved); AP and CDA rows removed; Re Mind = Re Mind, χ-blade = نصل χ; all other TRANS-1 `proposed` terms approved; Stock = المخزون and Warp = انتقال سريع added as second approved forms (menu column / world-map fast travel); Heartless Hunter/Harrier/Menacer/Destroyer/Obliterator = صائد/مطارد/مهدد/مدمر/ماحق البلا قلب added.',
        'Open: the approved item "Heartless Maul" = مطرقة بلا قلب (GLOSS-2) has no article; I left it. Musical and Grind rows exist only in later categories, so no translated row needed a change.', '']
sk = collections.Counter(re.sub(r'\(.*', '', r['note'])[:40] for r in todo)
out += ['## Part 3 — items_abilities numbers',
        f'- Rows {len(ia)}: translated {len(done)}, skipped {len(todo)}, remaining 0. Skip reasons: ' + '; '.join(f'{v} × {k.strip()}' for k, v in sk.most_common()),
        '- Files: kh3_gumiship (852 rows: gummi blocks, stickers, ship names, upgrades, descriptions), kh3_item (weapons, armor, accessories, battle items, materials, food, key items, maps, Classic Kingdom games, reports), kh3_system (commands, abilities and their descriptions).',
        '- Templates: 80 "Grants a … boost in …" lines and 25 food lines were generated from one sentence template each (amount words slight/small/moderate/large/huge/incredible = طفيفة/صغيرة/متوسطة/كبيرة/هائلة/مذهلة); everything else is hand translated; weapon, magic and item names come from the glossary.', '',
        '### Validator flags (items_abilities)', '| flag | level | count |', '|---|---|---|']
out += [f'| {c} | {"ERR" if c in ERR else "WARN"} | {n} |' for c, n in sorted(fc_ia.items())]
out += ['| TAGS, BR, LATIN, HARAKAT, TATWEEL, BRACKETS, EMPTY, ARGORDER, DSPACE, LEAD, TRAIL | | 0 |', '']
for i, fl in sorted(flags.items()):
    if by[i]['category'] == 'items_abilities':
        out.append(f'- {i} {" ".join(fl)}: {by[i]["EN"][:50]} -> {by[i]["AR"][:50]} — ' + ('glossary term used as a command word (Enduring Faith); GLOSS expected' if i == '16172' else 'approved KH2 name Omega Finale (type menu, not checked) while the term Finale = نهاية' if i == '16566' else 'short name, ratio ok' if 'RATIO' in fl else 'WARN'))
out.append('')
rat = sorted(((L(r['AR']) / max(L(r['EN']), 1), r) for r in done if L(r['EN']) >= 1), key=lambda t: -t[0])
out += ['### The 30 longest AR/EN length ratios (items_abilities, visible characters)', '', '| id | ratio | EN len -> AR len | EN | AR |', '|---|---|---|---|---|']
out += [f"| {r['id']} | {x:.2f} | {L(r['EN'])} -> {L(r['AR'])} | {esc(r['EN'][:45])} | {esc(r['AR'][:45])} |" for x, r in rat[:30]]
long_ = [(x, r) for x, r in rat if L(r['EN']) >= 40]
out += ['', 'Descriptions only (EN >= 40 chars), top 10:', '', '| id | ratio | EN len -> AR len | EN | AR |', '|---|---|---|---|---|']
out += [f"| {r['id']} | {x:.2f} | {L(r['EN'])} -> {L(r['AR'])} | {esc(r['EN'][:45])} | {esc(r['AR'][:45])} |" for x, r in long_[:10]]
out += ['', '### 40 varied samples (id | EN | AR)', '| id | EN | AR |', '|---|---|---|']
ids = ('11379 11427 11526 11705 11825 11840 11867 11934 11975 12009 12233 12301 12306 12334 12392 12430 12448 12490 12542 12558 '
       '12574 12634 12694 12781 12810 12867 12885 12894 12917 16004 16036 16100 16367 16417 16438 16593 16610 16665 16756 16886').split()
ids = [i for i in ids if i in by and by[i]['AR']]
out += [f"| {i} | {esc(by[i]['EN'][:90])} | {esc(by[i]['AR'][:90])} |" for i in ids]
out += ['', '### Places I was unsure (items_abilities rows carry an `unsure:` note)', '| id | EN | AR | why |', '|---|---|---|---|']
for r in ia:
    if r['note'].startswith('unsure:'):
        out.append(f"| {r['id']} | {esc(r['EN'][:50])} | {esc(r['AR'][:50])} | {esc(r['note'][7:].strip())} |")
out += ['', 'Also unsure but not marked per row: all gummi-part words (Angular/Rounded… part names), sticker names, ship names (Highwind = هايويند, Falcon = فالكون, Invincible = إنفينسيبل), Classic Kingdom game titles (my own renderings), the status words in the "Protection" abilities, "Combo finisher" = ضربة ختامية, "Reprisal" = الثأر, "Flowmotion" = الحركة الانسيابية (glossary), and EXP kept as خبرة (glossary) although the policy would also allow Latin EXP.', '',
        '### Decisions I took (please confirm)',
        '- EXP stays خبرة (approved glossary); LV stays مستوى; EZ/PRO Codes stay Arabic (approved glossary). If you prefer Latin for these, say so: 3 small corrections files.',
        '- Company names in the legal text (The Walt Disney Company, Square Enix Co., Ltd) kept Latin as brands; the rest of the sentence is Arabic.',
        '- km / mi stay كم / ميل (Arabic units); `p` stays Latin.',
        '- "A First Surge of Emotion" (14239) became أول تسارع للمشاعر to follow Surge = التسارع; the more natural word is فيض.',
        '- Crystal = بلورة in all material names (glossary Twilight Crystal); "Crystal/M" gummi material stays كريستال.',
        '- T- prefix of the T-Highwind family kept Latin (prefix code); "LV n" written مستوى n.',
        '- Teeny Ship "Alpha"/"Beta" (words, not letters) stay Arabic ألفا/بيتا.', '',
        '### New terms I coined (added to glossary.tsv as `proposed`, 39 rows)',
        'Resistance, Reprisal, Combo finisher, Risk Dodge, Synthesis material, Shard/Stone/Gem/Crystal, Heartbinder, Situation command, Team attack, Teeny ship, Gummi block, Blueprint Fragment, Prize Postcard, M.O.G. Card, Treasure Prize, Secret Report, Highwind/Falcon/Invincible, Dive, Rush, Counter, Backlash, Knockback, Peak, Burning/Stun/Sneeze/Electrified, Max HP, Maximum AP, Equippable, Flowmotion maneuver, Grand magic, Attraction, Excellent, Flanniversary Badge, Pole Spin. See `translation\\GLOSSARY_PROPOSALS.md`.', '',
        '## Open questions', 'See PROJECT_MAP.md §8.']
open(os.path.join(ROOT, 'state', 'LAST_REPORT.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('report written', len(out), 'lines')
