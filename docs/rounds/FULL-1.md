OUTPUT RULES: work silently. Details in state\LAST_REPORT.md (overwrite; first line "round: FULL-1"..."done + file path". Stop and ask only if blocked 3 times or evidence conflicts. This is a long round: if the usage limit is close, finish the current step, commit, write the exact resume point in PROGRESS.md, stop.
START: pwd; save this prompt as docs\rounds\FULL-1.md; read PROJECT_MAP.md, state\PROGRESS.md, technical\FIELD_WIDTHS.tsv, technical\RECON_KH3.md, the BUILD-1 report.
APPROVALS: INSTALL out\builds\BUILD-2\pakchunk99-arabic_P.pak via the swap-script method (add SWAP_TO_BUILD2.bat; delete our pak first; verify SHA256; log). Downloads only from official tool pages (record URL, version, SHA256) if a text source needs a reader.

PART A — screenshots (chat, 2026-10-09, BUILD-1 pak). PASS (joined, RTL, correct): title screen incl. CONFIG = الضبط (13772 verified now) and version line الإصدار; settings camera page (labels, values عادي/تلقائي, sliders, help line); game settings tabs (اللغات، العرض، الرسومات، الصوت، وحدة التحكم، لوحة المفاتيح، قبل البث...، الخروج من اللعبة) with display page values and two-line help; difficulty dialog (all 4 modes + two-line description); pause (متابعة / تخطي المشهد); premium menu list (row names with icons, معطل, HP/MP/AP Latin kept, الاستحقاقات); battle command menu (هجوم، السحر، أغراض، ???); main menu (all items, location line, objective, character names, موني, الوقت). Log in SCREENSHOT_LOG.tsv (file chat) and mark every row visible in these screens verified; report the new verified count and %.
FAILS / issues seen:
 1. Party status panel: the LV label shows "ستوى" (first letter clipped): مستوى is wider than its field. Do NOT change the text yet: measure the field width and report exact numbers + options that fit (e.g. مس, م., smaller form) for the user to choose.
 2. Premium menu help (row "الضربة القاتلة"..."اضبط وضع عرض الشاشة." + second line). Investigate whether alignment can be set safely from text (e.g. <p align> in Scaleform HTML, if the field is html) or only by editing movies. Report evidence and options; change nothing in movies this round.
 Not issues: English subtitles (dialogue not translated yet); PAUSE/COMMANDS/OLYMPUS graphics (textures, later phase).

PART B — user decision: magic names in Arabic (KH3 only; KH2 glossary unchanged):
Fire/Fira/Firaga/Firaza = نار / نار قوية / نار كبرى / نار قصوى; Blizzard..aza = جليد / جليد قوي / جليد أكبر / جليد أقصى; Thunder..aza = صاعقة / صاعقة قوية / صاعقة كبرى / صاعقة قصوى; Cure..aza = شفاء / شفاء قوي / شفاء أكبر / شفاء أقصى; Aero..aza = ريح / ريح قوية / ريح كبرى / ريح قصوى; Water..aza = ماء / ماء قوي / ماء أكبر / ماء أقصى. Donald Fire/Blizzard/Thunder/Cure/Aero = نار دونالد / جليد دونالد / صاعقة دونالد / شفاء دونالد / ريح دونالد. Apply to every compound (Fire Boost = تعزيز النار, Dark Firaga = نار كبرى مظلمة, element/resistance rows stay as already set). Update glossary.tsv (replace the transliterated forms, note "..."), fix all translated rows via review\corrections\full1_magic.tsv. If a command-menu field is too narrow for a tier name, report it (do not shorten silently).

PART C — BUILD-2: rebuild with Parts A/B fixes, verify list/extract/SHA256, install as approved. Short Arabic checklist technical\BUILD2_CHECKLIST.md (max 4 places: premium menu help, party LV label (unchanged, for the record), ability description, command menu magic list).

PART D — 100% text inventory (read-only). Goal: prove that every piece of text the player can see is accounted for.
 1. Every pak: list every asset that can hold text: all .locres of every localization target (not only Game) and culture, .locmeta, StringTables, DataTables/CurveTables with FText, .ini text, Scaleform .gfx/.uasset movies (static DefineText/EditText initial text, button labels baked in movies), RawBinaries, any custom SE text format, CriWare .usm subtitle tracks (check whether subtitles are inside the USM files or come from locres), textures with English text (count by type, already 212 known).
 2. For each source: count of strings/words, whether it is already in translation\, how it could be changed through a ~mods pak, and evidence level.
 3. Compare en against ja for every text key: list keys present in ja but missing or empty in en (possible text we are not covering).
 4. Output technical\TEXT_COVERAGE.md: a table per source with coverage % and a single headline number "...", plus the list of anything not yet extracted with the reason.
 5. Anything new that is real translatable text: export into translation\ (new category folders, same TSV columns), so review pages and stats include it.

PART E — master script for review and translation, Markdown only, in review\script\:
 1. Story-ordered script of all dialogue, cutscene subtitles, in-game banter, battle lines and Re Mind: ordered by world/event/scene using key structure (e.g. event and cut ids) and any order data you find (sequence tables, level/event lists). Columns: | id | scene | speaker | EN | AR |. Speaker from data if it exists (speaker tables, key prefixes, voice file names); otherwise "—". 300 rows per page, one index file review\script\INDEX.md (world → scene → page links, row counts, translated %).
 2. Separate review\script\TIPS.md style pages for loading tips, hints, game-over hints, tutorials, journal entries, menus and settings, in game order, same columns (speaker omitted).
 3. tools\make_script.py regenerates all of it; add it to refresh.bat so AR updates appear automatically.
 4. Document in PROJECT_MAP §5 and docs\INDEX.md that review\script\ is the reference script for translation and review.

FINALLY: refresh.bat (0 ERR), secret_check, PROJECT_MAP §3 §4 §5 §6 §7 §8, CHANGELOG, commit "...".
Then stop.
