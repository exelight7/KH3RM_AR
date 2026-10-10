r"""One-time/idempotent (GLOSS-1): import translation\kh2_glossary.md (finished KH2 project, Arabic Markdown tables)
into translation\glossary.tsv as source=KH2 and write translation\GLOSSARY_CONFLICTS.md.
Rows with another source (KH3-new, ReMind) are kept as they are.
"A / B" -> "أ / ب" rows are split when both sides have the same number of parts; "A / B" -> one Arabic = synonyms.
Descriptive/compositional rows ("X names", "Fire/Blizzard Boost", templates with + or \n) are skipped (stay in kh2_glossary.md).
Conflicts (same EN, several AR) -> every form status=pending; the KH2 decision table of 2026-10-08 wins over older lines.
Then run tools\make_glossary.py (counts, glossary.md)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import ROOT, GLOSSARY, GCOLS, read_tsv, write_tsv
from make_glossary import count_terms
from make_review import esc

SRC = os.path.join(ROOT, 'translation', 'kh2_glossary.md')
ARABIC = re.compile('[؀-ۿ]')
DECISIONS = 'قرارات GLOSSARY (2026-10-08)'
KH2C = 'KH2 constraint, revisit'

SECTION_TYPES = [
    ('الأسماء المعتمدة', 'character'), ('شخصيات', 'character'), ('الشخصيات', 'character'), ('Worlds', 'world'),
    ('مناطق', 'place'), ('أماكن', 'place'), ('عالم الظلال', 'place'), ('كيبلايد', 'item'), ('أسلحة', 'item'),
    ('عناصر', 'item'), ('دروع', 'item'), ('أطقم', 'item'), ('Items', 'item'), ('قدرات', 'ability'), ('هجمات', 'ability'),
    ('سلوكيات', 'ability'), ('فئات', 'ability'), ('Gameplay', 'term'), ('sys.bar', 'menu'), ('قوائم', 'menu'),
    ('أوامر', 'menu'), ('رسائل نظام', 'menu'), ('إعدادات', 'menu'), ('sysB20', 'menu'),
]
CHARACTERS = set('''Sora|Donald|Goofy|Riku|Kairi|Mickey|Auron|Gopher|Pence|Dewey|Tinker Bell|Seifer|Setzer|Vivi|Axel|Saïx|DiZ|Rai
|Ansem the Wise|Maleficent|Yen Sid|Pete|Chiro|Minnie|Daisy|Pluto|Chip|Dale|Aqua|Ven|Xehanort|Pain|Panic|Willy|Jagular|Sark
|Tron|Rabbit|Eeyore|Tigger|Roo|Owl|Iago|Abu|Jafar|Genie|Carpet|Aladdin|Jasmine|Scar|Simba|Nala|Mufasa|Rafiki|Timon|Pumbaa
|Shenzi|Banzai|Ed|Belle|Beast|Cogsworth|Lumiere|Mrs. Potts|Xaldin|Jack Sparrow|Barbossa|Elizabeth|Will Turner|Davy Jones
|Cortez|Bootstrap Bill|Ariel|Flounder|Sebastian|Ursula|Eric|King Triton|Xemnas|Zexion|Lexaeus|Luxord|Demyx|Xigbar|Vexen
|Marluxia|Larxene|Naminé|Hercules|Hades|Megara|Phil|Pegasus|Wonderboy|Leon|Cloud|Yuffie|Aerith|Tifa|Cid|Sephiroth|Scrooge
|Hayner|Olette|Selphie|Rikku|Yuna|Paine|Fuu|Squall Leonhart|Huey|Louie|Jiminy Cricket|Chicken Little|Flora|Fauna
|Merryweather|Daisy Duck|Horace Horsecollar|Clarabelle Cow|Clara Cluck|Dr. Finkelstein|The Mayor|Oogie Boogie|Santa Claus
|Jetsam|Flotsam|Vanessa|Ienzo|Even|Braig|Dilan|Aeleus|Philoctetes|Hera|Zeus|Captain Li Shang|Chien-Po|Yao|Ling|Fa Mulan
|Tung-Shao|Wendy|Peter Pan|Stitch|Roxas|Jack|Mulan|Ping|Merlin|Mushu|Shan-Yu|Oogie|Zero|The Queen|Will|Triton|Pooh
|Piglet|Kanga|Cerberus|Tiny Fairy|The Flying Boy'''.replace('\n', '').split('|'))
WORLDS = {'Agrabah', 'Twilight Town', 'Destiny Islands', 'Hollow Bastion', "Beast's Castle", 'Olympus Coliseum',
          'The Land of Dragons', '100 Acre Wood', 'The Hundred Acre Wood', 'Pride Lands', 'Atlantica', 'Disney Castle',
          'Timeless River', 'Halloween Town', 'Port Royal', 'Space Paranoids', 'The World That Never Was', 'Radiant Garden',
          'Never Land', 'Christmas Town', 'Castle Oblivion', 'Underworld', 'End of Sea', 'World ZZ', 'World FA'}
MAGIC = {'Fire', 'Fira', 'Firaga', 'Firagun', 'Blizzard', 'Blizzara', 'Blizzaga', 'Thunder', 'Thundara', 'Thundaga',
         'Thundagun', 'Cure', 'Magnet', 'Reflect', 'Magnega', 'Reflega', 'Faith', 'Stop', 'Magic'}
PLACES = {'realm of light', 'realm of darkness', 'realm of nothingness', 'Chamber of Repose', 'Chamber of Waking',
          'Underdrome', 'Zero District', "Villain's Vale", 'postern', 'bailey', 'candy shop', 'Armor Shop', 'Accessory Shop',
          'Station of Awakening', 'The World of Nothing', 'Hall of Empty Melodies', 'Garden of Assemblage', 'Treasure Isle',
          "Memory's Contortion", 'Christmas', 'Nothing', 'Naught', 'Big Ben', "The King's Den", "king's den"}
ITEMS = {'Olympus Stone', 'Hades Cup', 'Paradox Cup', 'Hades Paradox Cup', 'Titan Cup', 'Cerberus Cup', 'medallion',
         'Aztec gold', 'Claymore', 'Gummi', 'Gummi Ship', 'Material Gummi', 'Deco-Gummi', 'Blueprint', 'Teeny Ship',
         'Teeny Ships', 'Slash Gummies', 'Optional Gummi', 'Support Gummi', 'Elixir', 'Full Bloom', 'Save the King',
         'Twilight Shard', 'Twilight Gem', 'Twilight Crystal', 'Shards', 'Stones', 'Gems', 'orbs', 'Materials',
         'Light Cycle', 'solar sailer', 'Munny', 'Munny Pouch', 'Keyblade', 'Shaman\'s Relic', 'Dense Crystal',
         'Circle of Life', 'Fenrir', 'Ukulele'}
TERMS = {'Heartless', 'Nobody', 'Dusk', 'Dusks', 'Organization XIII', 'Organization <X 5E>', 'Struggle tournament',
         'Twilight Disciplinary Committee', 'Klepto Club', 'seven wonders of Twilight Town', 'seven wonders', 'ghost train',
         'haunted mansion', 'Haunted mansion', 'User', 'de-rezz', 'hakuna matata', 'enchantress', 'master', 'rose',
         'parley', 'Moogle', 'Gauge', 'Shop', 'Journal', 'Struggle Battle R', 'Restoration at N%', 'the usual spot',
         'the usual place', 'Your Majesty', 'Rucksack', 'blondie', 'MCP', 'DTD', 'Master Control Program',
         'Secret Ansem Report', 'Free Development', 'Slash Gauge', 'EX-Formation', 'Kingdom Hearts', 'Windsday',
         "Somebody-I-Don't-Know", 'hunny', 'honey', 'Lv.', 'Final Fantasy III..X-2', 'Absent Silhouette', 'recon',
         'Struggle Battle Rule', 'Tutorial:', 'Land in <world>', 'Proceed through <gummi route>'}
LIMITS = {'Comet Rain', 'Flare Force', 'Duck Flare', 'Rocket Flare', 'Megaduck Flare', 'Teamwork', 'Knocksmash', 'Duo Raid',
          'Cosmo Boost', 'Howling Moon', 'Twin Howl', 'Stalwart Fang', 'Outcry', 'Last Howl', 'Overdrive', 'Shooting Star',
          'Banishing Blade', 'Spiral', 'Dragonblaze', 'Trick Fantasy', 'Speedster', 'Trickster', 'Downbeat', 'Synchronization',
          'Finale', "King's Pride", 'Proud Roar', 'Complete Compilement', 'Setup', 'Cluster Code', 'Eternal Session',
          'Last Saber', 'Master Hearts', "All's End", 'Trinity Limit', 'Trinity', 'Ultima', 'Major Drive', 'FPS Mode',
          'Firecracker', 'Sonic Rave', 'Sonic', 'Rave', 'Strike Raid', 'Strike', 'Judgment', 'Last Arcanum',
          'Final Arcana', 'Arcana', 'Bash', 'Infinity', 'Impact', 'Leave', 'Depart', 'Fail-Safe', 'Key Counter',
          'Groundshaker', 'Healing Light', 'Dark Aura', 'Reversal', 'Zantetsuken', 'Stunt Dodge', 'Reprogram',
          'Whirli-Goof', 'Grind', 'Auto', 'Limit Form', 'Reaction Command', 'Drive Form', 'Limit', 'Summon', 'Valor Form',
          'Wisdom Form', 'Master Form', 'Final Form', 'Antiform', 'Drive', 'Valor', 'Wisdom', 'Master', 'Final'}
# raw EN cell -> (EN, AR) fixes for KH2 shorthand rows
ROW_FIX = {
    'the usual spot / place': ('the usual spot / the usual place', None),
    'Cerberus / Titan Cup': ('Cerberus Cup / Titan Cup', None),
    'Station of Serenity / Calling': ('Station of Serenity / Station of Calling', None),
    'Twilight Shard / Gem / Crystal': ('Twilight Shard / Twilight Gem / Twilight Crystal', None),
    'Optional / Support Gummi': ('Optional Gummi / Support Gummi', None),
    'Leave / Depart / Fail-Safe / Key Counter': (None, 'غادر / غادر / صمام الأمان / الرد بالمفتاح'),
    'Whirli-Goof / -ra / -ga': ('Whirli-Goof', None),
    'Moogle (ranks)': ('Moogle', 'موغل'),
    'Lv.': (None, 'مستوى'),
    'Willy (Pete´s steamboat)': ('Willy', 'ويلي'),
}
SKIP_ROW = re.compile(r'(?:Heartless|Nobody|Limit) names|behavior lines|descriptions|seven wonders titles|talk line|variants'
                      r'|\\n|\+|Drive Forms|Shops:|heights/common|/ .* Map$')
SKIP_PART = re.compile(r'[A-Za-z]/[A-Za-z"]|\bNN\b|\.\.\.|^[-–]|\d×')
# KH2-only constraints (Latin ban, <X 5E>, LV->مس, cell-width shortenings): pending, revisit for KH3
KH2_CONSTRAINT = {'Organization XIII', 'Organization <X 5E>', 'LV', 'Lv.', 'Next LV', 'MCP', 'DTD', 'FPS Mode',
                  'Final Fantasy III..X-2', 'World ZZ', 'World FA', 'LT', 'Hollow Bastion', 'Musical', 'Full Bloom',
                  'Journal', 'Munny', '360° Spin', 'Master Control Program', 'Jump to World Map?'}


def clean(s):
    s = s.replace('**', '').replace('`', '').replace('´', "'").replace('’', "'").strip()
    return re.sub(r'\s+', ' ', s)


PAREN = re.compile(r'\s*\((?:[^()]*[؀-ۿ][^()]*|Forms|tt|×\d|id \d+|Bear|inv\.|synthesis|in a sentence|s|\+|±'
                   r'|town defence device|sys \d+|wm \d+|Fujin|Raijin)\)')


def section_type(sub, head):
    for txt in (sub, head):
        for k, t in SECTION_TYPES:
            if k in txt:
                return t
    return 'term'


def entry_type(en, sect):
    for names, t in ((CHARACTERS, 'character'), (WORLDS, 'world'), (MAGIC, 'magic'), (PLACES, 'place'), (ITEMS, 'item'),
                     (TERMS, 'term'), (LIMITS, 'ability')):
        if en in names:
            return t
    return sect


def parse():
    """-> (entries [en, ar, type, status, note, from_decisions], skipped raw rows)"""
    out, skipped, head, sub, cols = [], [], '', '', None
    for line in open(SRC, encoding='utf-8').read().split('\n'):
        if line.startswith('#'):
            head, sub, cols = line.lstrip('# ').strip(), '', None
            continue
        if line.startswith('**') and len(line) < 90:
            sub = line.strip('* :')
            continue
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if all(set(c) <= set('-: ') for c in cells):
            continue
        if any(c in ('الإنجليزي', 'EN', 'English') for c in cells):
            e = next(i for i, c in enumerate(cells) if c in ('الإنجليزي', 'EN', 'English'))
            cols = (e, e + 1)
            continue
        e, a = cols or (0, 1)
        if len(cells) <= a:
            continue
        raw_en = cells[e].replace('`', '').replace('**', '').strip()
        en_raw, ar_raw = clean(cells[e]), clean(cells[a])
        note = clean(' | '.join(c for i, c in enumerate(cells) if i not in (e, a)))
        fix = ROW_FIX.get(raw_en) or ROW_FIX.get(en_raw)
        if fix:
            en_raw, ar_raw = fix[0] or en_raw, fix[1] or ar_raw
        en = re.sub(r'\s*×\d+', '', PAREN.sub('', en_raw)).strip()
        if not re.search('[A-Za-z]', en) or ARABIC.search(en) or SKIP_ROW.search(en):
            skipped.append(en_raw)
            continue
        status = 'approved'
        if re.match('معل[ّ]?ق', ar_raw) or 'للمراجعة' in note + ar_raw or 'قرار معلق' in note or head.startswith('قرارات معلقة'):
            status = 'pending'
        m = re.match(r'معل[ّ]?ق:?\s*(.*?)(?:\s*\(الحالي[^:]*: (.*)\))?$', ar_raw)
        if m:
            ar_raw = m.group(1).replace('— لم يُعتمد بعد', '').strip()
            if m.group(2):
                note = f'KH2 in game: {m.group(2)}; ' + note
        if ' — ' in ar_raw:
            ar_raw, rest = ar_raw.split(' — ', 1)
            note = (rest + '; ' + note).strip('; ')
        if en != en_raw:  # qualifier dropped from EN -> drop it from AR too
            ar_raw = PAREN.sub('', ar_raw).strip()
        ens, ars = [x.strip() for x in en.split(' / ')], [x.strip() for x in ar_raw.split(' / ')]
        if len(ens) == len(ars):
            pairs = list(zip(ens, ars))
        elif len(ars) == 1:
            pairs = [(x, ars[0]) for x in ens]  # synonyms
        elif len(ens) == 1:
            pairs = [(en, ars[0])]
            note = f'KH2 alt forms: {ar_raw}; ' + note
        else:
            skipped.append(en_raw)
            continue
        decision = head.startswith(DECISIONS)
        st = section_type(sub, head)
        src_note = f'KH2 {head[:40]}' + (f' / {sub[:30]}' if sub else '')
        for en1, ar1 in pairs:
            if SKIP_PART.search(en1.replace('I/O', 'IO')):
                skipped.append(en1)
            elif en1 and ar1:
                out.append([en1, ar1, entry_type(en1, st), status, f'{src_note}; {note}'.strip('; ')[:220], decision])
    return out, skipped


def build(rows):
    """-> (glossary dicts, conflicts [(en, kind, kept forms, dropped forms, entries)])"""
    by = {}
    for x in rows:
        by.setdefault(x[0].lower(), []).append(x)
    result, conflicts = [], []
    for lst in by.values():
        if any(x[5] for x in lst):  # KH2 decision table 2026-10-08 wins over older lines
            decided = [x for x in lst if x[5]]
            dropped = sorted({x[1] for x in lst} - {x[1] for x in decided})
            if dropped:
                conflicts.append((lst[0][0], 'resolved in KH2 (decision table 2026-10-08)', [x[1] for x in decided], dropped, lst))
            lst = decided
        forms = []
        for x in lst:
            if x[1] not in [f[1] for f in forms]:
                forms.append(x)
        if len(forms) > 1:
            conflicts.append((forms[0][0], 'open', [f[1] for f in forms], [], forms))
        for en, ar, t, st, note, dec in forms:
            if len(forms) > 1:
                st, note = 'pending', 'conflict, see GLOSSARY_CONFLICTS.md; ' + note
            if en in KH2_CONSTRAINT:
                st, note = 'pending', f'{KH2C}; ' + note
            result.append({'en': en, 'ar': ar, 'type': t, 'source': 'KH2', 'status': st,
                           'kh3_count': '0', 'example_ids': '', 'note': note.replace('\t', ' ')})
    return result, conflicts


# Cross-entry conflicts and typo-looking entries found by reading kh2_glossary.md (not detectable per EN key).
# (EN, forms with origin, recommendation, reason)
MANUAL = [
    ('Kingdom Hearts', 'كينغدوم هارتس (batchF, sys 1438/14132, approved) / كينغدم هارتس (old id 13584; KH3 title test 13801)',
     'كينغدوم هارتس', 'user decision GLOSS-1 task 4; English pronunciation "dom"; KH2 approved'),
    ('Config / Option', 'Config = الضبط (KH2 batch 8, sys 13846-14002) / Option = الخيارات (KH2 batch 1, id 1106)',
     'CONFIG = الضبط, Option = الخيارات', 'user decision GLOSS-1 task 4: different EN terms keep different Arabic'),
    ('Munny', 'مال (sys, save-slot width 2026-10-01) / موني (tt 13749, batchG/batchI) / الموني (Munny Pouch كيس الموني) / مميونة (كيس المميونة, batch 11/15 text)',
     'موني', 'English pronunciation; most common in KH2 dialogue (tt); مال was a KH2 cell-width shortening'),
    ('Destiny Islands / Destiny Island', 'جزيرة المصير (world id 532) / جزيرة القدر (batch 16 area names)',
     'جزر المصير', 'correct Arabic: EN is plural ("Islands"); المصير is the established KH2 world word; same world = same Arabic'),
    ('Hollow Bastion', 'حصن هولو (id 533, "shortened") / هولو باستيون (batch 15 dialogue)',
     'هولو باستيون', 'English pronunciation for a name; حصن هولو was a KH2 width shortening'),
    ('Fire / Blizzard / Thunder (element words)', 'فاير / بليزارد / ثاندر (spells) vs النار / البرد / الصاعقة (Fire Bangle عصبة النار, Blizzard Armlet ساعد البرد, Thunder Trinket خرزة الصاعقة)',
     'spell names transliterated (فاير/بليزارد/ثاندر); plain elements in item names translated', 'KH2 already does this; keep, but record it as one rule'),
    ('Pete / Phil / Cid / Pain / Will', 'بيت (= house, cf. بيت بوه) / فيل (= elephant) / سيد (= mister) / بين (= between) / ويل (= woe)',
     'keep KH2 forms; disambiguate in context only if a screenshot shows confusion', 'English pronunciation wins; alternatives (بيييت, فِل) would need harakat, which are banned'),
    ('Piglet', 'بيركيت (KH2 batch 3, Piglet\'s House بيت بيركيت) — typo-looking',
     'بيغليت', 'correct pronunciation "Pig-let"; بيركيت looks like a typo'),
    ('Rikku', 'ريكا (KH2 jm, chosen to differ from Riku ريكو)', 'ريكو (pronunciation) vs ريكا (distinction)',
     'pronunciation says ريكو but it collides with Riku; KH3 count decides if it matters'),
    ('Drive Gauge Powered Up!', 'ارتفع ععداد الدرايف! (batch 7, id 2788) — typo: doubled ع', 'ارتفع عداد الدرايف!', 'typo'),
    ('Equip', 'تجهيز (batch 1) / تجهيز هذه القدرة. (batch 8 row "Pulsing Thunder / Equip / Don\'t equip this ability." is misaligned)',
     'تجهيز', 'the batch 8 row maps 3 EN cells onto shifted Arabic; تجهيز هذه القدرة. belongs to "Equip this ability."'),
    ('Faith', 'فيث — KH2 note contains stray characters ("كال桧طع")', 'فيث', 'note typo only; form is fine'),
    ('Olympus', 'أولمبيا in KH2 compounds (Olympus Coliseum كولوسيوم أولمبيا, Olympus Stone حجر أولمبيا) / KH3 proposal أوليمبوس',
     'أوليمبوس (KH3 world, Mount Olympus جبل أوليمبوس)', 'correct Arabic: أولمبيا is Olympia, a different place; decide whether the KH2 compounds follow'),
    ('Dr. Finklestein / Dr. Finkelstein', 'EN spelled two ways in KH2 (Finklestein\'s Lab / Dr. Finkelstein); Arabic فينكلشتاين both times',
     'فينكلستاين', 'English pronunciation "Fink-el-steen" (no German ش)'),
]
RECOMMEND = {
    'abilities': ('القدرات (title) / قدرات (inline)', 'article only; choose by context (menu title = definite)'),
    'jump to world map?': ('الانتقال إلى خريطة العالم?', 'ASCII ? until a screenshot proves ؟ renders (GLOSS-1 rule)'),
    'cerberus': ('سيربيروس', 'character name; the cup is كأس سيربيروس (separate term Cerberus Cup)'),
    'postern': ('البوابة الخلفية', 'correct Arabic for a castle gate; KH2 kept الباب الخلفي only for width'),
    'master': ('الإتقان (Drive Form) / السيد (Beast\'s master)', 'two senses; keep both, context decides'),
    'whirli-goof': ('غوفي الدوار', 'KH2 decision pending width check; correct Arabic word order'),
    'release': ('التحرير', 'command names in KH2 mostly definite; shortest is تحرير — most common usage decides'),
    'hang on': ('تمسك', 'shortest; لا تفلت is a different line (Grab On/Hang On pair)'),
    'jump': ('قفز', 'shortest, matches Jump! = قفز!'),
    'question': ('سؤال (QUESTION title) / اسأل (command)', 'two senses (noun title vs verb command)'),
    'auto': ('تلقائي', 'matches Auto Valor/Auto Limit = تلقائي:; آلي kept only for width'),
    'materials': ('المواد', 'definite as a menu title; مواد inline'),
    'munny': ('موني', 'see Munny below'),
    'dtd': ('دي تي دي', 'only form in KH2; KH3 has no Latin ban, pending'),
    '100 acre wood': ('غابة المئة فدان', 'world name; the other forms are map/landing labels'),
    'equip': ('تجهيز', 'see Equip below (misaligned KH2 row)'),
    'journal': ('اليوميات', 'KH2 يوميات only for badge width; definite is the title form'),
    'trinity': ('ترينتي', 'resolved in KH2'),
    'rai': ('راي', 'qualifier only'),
}


def write_conflicts(conflicts, path):
    terms = {c[0] for c in conflicts} | {'Kingdom Hearts', 'Config', 'Option', 'Munny', 'Destiny Islands', 'Destiny Island',
                                         'Hollow Bastion', 'Fire', 'Blizzard', 'Thunder', 'Pete', 'Phil', 'Cid', 'Pain', 'Will',
                                         'Piglet', 'Rikku', 'Riku', 'Equip', 'Faith', 'Drive Gauge', 'Dr. Finkelstein', 'Olympus'}
    cnt = count_terms(terms)
    L = ['# Glossary conflicts (KH2 glossary → KH3)', '',
         'Generated by `tools\\import_kh2_glossary.py` (GLOSS-1). Every term below has status `pending` in `translation\\glossary.tsv` '
         'until the user decides. Recommendations follow the rule order: correct Arabic → English pronunciation for names → '
         'most common usage → shortest. **Nothing here is decided.**', '',
         '## 1. Same EN, more than one Arabic form inside the KH2 glossary', '',
         '| EN | forms (KH2 origin) | KH3 rows | recommended | reason | state |', '|---|---|---|---|---|---|']
    for en, kind, kept, dropped, ents in conflicts:
        forms = ' · '.join(f'{esc(x[1])} ({esc(x[4].split(";")[0])})' for x in ents)
        rec, why = RECOMMEND.get(en.lower(), (kept[0], 'only form left after KH2 decision table') if dropped else ('—', ''))
        state = 'resolved in KH2: ' + esc(' / '.join(kept)) if dropped else 'pending'
        L.append(f'| {esc(en)} | {forms} | {cnt[en][0]} | {esc(rec)} | {esc(why)} | {state} |')
    L += ['', '## 2. Cross-entry conflicts, ambiguities and typo-looking entries', '',
          '| EN | forms (KH2 origin) | KH3 rows | recommended | reason |', '|---|---|---|---|---|']
    for en, forms, rec, why in MANUAL:
        n = ' + '.join(f'{t.strip()} {cnt[t.strip()][0]}' for t in re.split(r' / |\(', en)
                       if t.strip() in cnt) or '—'
        L.append(f'| {esc(en)} | {esc(forms)} | {n} | {esc(rec)} | {esc(why)} |')
    L += ['', 'Kingdom Hearts and Config/Option were decided by the user in GLOSS-1 (task 4) and are applied to the title-screen rows; '
          'they are listed for the record.', '']
    open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))


def main():
    rows, skipped = parse()
    kh2, conflicts = build(rows)
    for d in kh2:  # user decisions GLOSS-1 task 4
        if d['en'] in ('Kingdom Hearts', 'Config'):
            d['status'], d['note'] = 'approved', 'user decision GLOSS-1; ' + d['note']
    keep = []
    if os.path.exists(GLOSSARY):
        keep = [dict(zip(GCOLS, r)) for r in read_tsv(GLOSSARY)[1:] if r[3] != 'KH2']
    write_tsv(GLOSSARY, [GCOLS] + [[d[c] for c in GCOLS] for d in kh2 + keep])
    write_conflicts(conflicts, os.path.join(ROOT, 'translation', 'GLOSSARY_CONFLICTS.md'))
    print(f'import_kh2_glossary: parsed={len(rows)} skipped_rows={len(skipped)} kh2_entries={len(kh2)} '
          f'conflicts={len(conflicts)} kept_other={len(keep)}')


if __name__ == '__main__':
    main()
