# PROJECT_MAP — KH3 Arabic (start here)

Single entry point for any new AI session or person. Sections ending in "(auto)" are rewritten by `tools\update_map.py` (run by `tools\refresh.bat`); all other sections are edited by hand. **Every round must update sections 3, 4 and 8 before stopping.**

## 1. What the project is

Arabic (RTL) localization of KINGDOM HEARTS III + Re Mind (Steam, UE 4.17, Scaleform UI) on PC.
Delivered only as an added mod pak in `Content\Paks\~mods\` (rebuilt `en` .locres + TresFont with Segoe UI Arabic); original game files are never changed.
Text is pre-shaped (presentation forms) and stored in visual order, because Scaleform does no Arabic shaping or bidi.

## 2. Roles and rules

Full supervisor instructions: [docs/SUPERVISOR.md](docs/SUPERVISOR.md). Key rules:
- **User / supervisor:** gives round instructions and approvals, runs the game, takes screenshots, decides glossary and distribution.
- **Executor (Claude Code):** writes only in `C:\filessss\mewo\kh3fm-arabic\`; never modifies original game files; never runs the game; never deletes `extracted\` or `out\builds\`; no uploads, git local only.
- Font = **Segoe UI Regular** (`C:\Windows\Fonts\segoeui.ttf`), never Noto, never Plex.
- Install into `~mods` only with explicit approval; **only one pak of ours in `~mods` at any time**; record SHA256 before/after.
- Output: details in `state\LAST_REPORT.md` (overwritten each round, first line `round: <NAME>`); 3 lines per task appended to `state\PROGRESS.md`; terminal reply = one line "...".
- Stop and ask only if blocked 3 times or evidence conflicts.
- No HTML outputs; all human-readable reports are Markdown. Every round ends with `tools\refresh.bat` and `tools\secret_check.py` (no key, no game binaries in git).

## 3. Current phase, last round, next step

- **Phase:** BUILD-5 installed (2026-10-10): the REVIEW-1 and REVIEW-2 corrections are in the game (`pakchunk99-arabic_P.pak`, sha e43d8f97...). 95.3 % of rows installed (16,415 / 17,222); the 807 `todo` rows carry a `skip:` note. Verified 0.6 %.
- **Last round:** BUILD-5 (2026-10-10). The BUILD-4 pipeline unchanged (`tools\build_build5.py` wraps `build_build4.py`: same movie patches, TresFont, line breaking, no `<p align>`) on the current TSVs; 45 entries differ from BUILD-4 (list in `out\builds\BUILD-5\diff_vs_build4.tsv`, incl. row 15964); 73 files SHA256 PASS, round trip 16,391 exact + 24 same-visual + 0 fail; installed via `SWAP_TO_BUILD5.bat`. Details: `state\LAST_REPORT.md`.
- **Next step:** screenshots per `technical\BUILD5_CHECKLIST.md` (8 places); supervisor decisions on `review\UNSURE_REVIEW2.md`.
- **Public repository (PUBLISH-1, 2026-10-10):** https://github.com/exelight7/KH3RM_AR set up (Arabic-only translation, tools, docs); pre-release `v0.5-test (BUILD-5)` prepared. See section 10.
- **Release v0.8.0 (RELEASE-080, 2026-10-10):** installer `KH3RM_AR_Setup_v0.8.0.exe` (WPF .NET 8, self-contained, embeds the BUILD-5 pak sha e43d8f97...); 22 self tests PASS; assets and notes in `out\release\v0.8.0\`; creating the GitHub Release needs `gh auth login` by the user (tag v0.8.0, pre-release).

## 4. Decisions already made

| date | decision | source |
|---|---|---|
| 2026-10-10 | BUILD-5 = the BUILD-4 pipeline unchanged on the reviewed text (no build logic change); the swap script pins the sha of the pak file that is installed | docs/rounds/BUILD-5.md |
| 2026-10-08 | Font = Segoe UI Regular (weight 400), never Noto Sans Arabic, never IBM Plex | user; RECON_KH3 header |
| 2026-10-08 | Culture `en` is replaced (our pak overrides `Localization/Game/en/*.locres`); English voice unaffected | PIPE-1, RECON_KH3 §8 |
| 2026-10-08 | Scaleform pre-shaping: presentation forms U+FE70–FEFC + visual (reversed) order per line; confirmed in-game by ARABIC-TEST-1 variant A | SHAPER_SPEC, ARABIC-TEST-1 screenshot |
| 2026-10-08 | No HTML outputs; review pages are Markdown (`review\md\`), fixes via `review\corrections\*.tsv` | ORG-2 |
| 2026-10-08 | Mod method: unencrypted pak v4, Zlib, mount `../../../`, name `pakchunk99-*_P.pak` in `Content\Paks\~mods\`; no `_0_P` moves needed | LOAD-TEST PASS |
| 2026-10-08 | Join fix lives in the font, not in the movies: Arabic initial/medial forms get a straight 18-unit stroke before the join tip (letterSpacing 2 at 30 pt = 17.07 units) | ARABIC-TEST-2 |
| 2026-10-08 | Arabic glyphs go into `$sougei` (id 3) and `$KH2Menu` (id 4, GAME SETTINGS header); `$KH2Menu` scale matched to its cap height (×204/174) | ARABIC-TEST-2 |
| 2026-10-08 | `ReMind` (visible text of `Re<icon(..)>Mind`) allowed as Latin in AR text | ARABIC-TEST-2 |
| 2026-10-08 | Screenshots are sent in the supervisor chat only (not saved in `screenshots\`); `SCREENSHOT_LOG.tsv` entries use file = `chat` and the supervisor's verdict | user, GLOSS-1 |
| 2026-10-08 | Glossary source of truth = `translation\glossary.tsv`; `glossary.md` / `GLOSSARY_PROPOSALS.md` are generated; only `approved` terms used in bulk; rule order: correct Arabic → English pronunciation for names → most common usage → shortest; same EN = same AR | user, GLOSS-1 |
| 2026-10-08 | KH2-only rules not carried over (Latin bans, ya/alef-maqsura, `<X 5E>`, LV→مس, width shortenings, forced transliterations → pending); Arabic `،`/`؟` only after a screenshot proves they render, ASCII `,` `?` until then | user, GLOSS-1 |
| 2026-10-08 | Kingdom Hearts = كينغدوم هارتس; CONFIG = الضبط; Option stays الخيارات | user, GLOSS-1 |
| 2026-10-08 | Munny = موني in all forms (Munny Pouch = كيس موني); Organization XIII = منظمة XIII (Latin XIII allowed), the Organization = المنظمة, Real Organization XIII = منظمة XIII الحقيقية; LV / Lv. = مستوى, Next LV = المستوى التالي; Olympus = أوليمبوس (all compounds) | user, GLOSS-2 |
| 2026-10-08 | Piglet = بيغليت; Finkelstein = فينكلشتاين; Equip = تجهيز; Sulley = سولي; Shotlock = التصويب المثبت; Cure/Cura/Curaga/Curaza = كيور/كيورا/كيوراغا/كيورازا; The Neighborhood = الحي السكني; Moogle/Moogles = same word (موغل / الموغل); magic names follow KH2 style incl. -za tier (فايرازا …) | supervisor, GLOSS-2 |
| 2026-10-08 | 17 pending glossary conflicts closed: Hollow Bastion = حصن هولو, Destiny Island(s) = جزر المصير, Limit = ليميت, Lucky Lucky = لكي لاكي, Full Bloom = الإزهار, Journal = اليوميات, Postern = البوابة الخلفية, Jump = قفز, Auto = تلقائي, Release = التحرير, Hang On = تمسك, Whirli-Goof = غوفي الدوار; Abilities/Master/Question/Materials keep both forms by context; KH2-constraint rows with 0 KH3 rows = status `kh2-only` | supervisor, TRANS-1 |
| 2026-10-08 | menus_ui style: clear MSA, short labels, imperative help lines, ASCII `,` `?`, no harakat/tatweel; Latin per the TRANS-2 policy (see below); same EN = same AR; rows empty / icon-only / numbers / native-script stay `todo` with note `skip: <reason>` | supervisor, TRANS-1 |
| 2026-10-08 | **Latin policy (final, replaces the allowed_latin whitelist):** the game font renders every Latin letter, digit, Roman numeral and Greek letter of the EN text, so any Latin/Roman/Greek token in AR must appear verbatim in the EN of the same row (validator ERR). Keep as in EN: acronyms (HDR LOD DOF FXAA TXAA BGM AP HP MP UFO AR CDA MVP PC PS4 DLC), brands (PlayStation, Epic Games, Re Mind), rank/set letters, single-letter suffixes, sector codes, title numerals (KINGDOM HEARTS Ⅲ, II.9; words stay كينغدوم هارتس), Greek letters, URLs, Latin units like `p`. Exception: Arabic where clearly more natural and short and the EN is a plain word, or where the glossary approves Arabic (EXP = خبرة, LV = مستوى, EZ/PRO Codes) | supervisor, TRANS-2 |
| 2026-10-08 | TRANS-1 executor choices accepted: Stock count column = المخزون, Warp (fast travel) = انتقال سريع (second approved forms next to the KH2 command Stock = تخزين / Warp = التحول), plural rows use `one`/`other` with "{0} من + noun" | supervisor, TRANS-2 |
| 2026-10-08 | Glossary TRANS-2: Flan = بودينغ, The Flantastic Seven = البودينغ السبعة الرائعون, Surge = التسارع (الاندفاع is KH2's Dash), Standard Mode = الوضع العادي, Teeny Ship α/β keep the Greek letter, AP stays Latin (row removed), Musical = موسيقي, Grind = طحن, Heartless Hunter/Harrier/Menacer/Destroyer/Obliterator = صائد/مطارد/مهدد/مدمر/ماحق البلا قلب; all other TRANS-1 proposed terms approved | supervisor, TRANS-2 |
| 2026-10-08 | items_abilities style: weapon/item/magic names from the glossary; descriptions imperative or third person as the EN; "..." and food lines from one template each; amount words slight..incredible = طفيفة صغيرة متوسطة كبيرة هائلة مذهلة; `/G /M /P /S` codes, VGA/SRS/STR codes, `+` suffix kept Latin as in EN | executor, TRANS-2 (to be confirmed) |
| 2026-10-09 | **Scale locked = F1 (final):** `$sougei` K = 256/2048 (1/8), DY = −5 (baseline of the `$sougei` Latin glyphs); every other class gets the same Arabic-to-cap-height ratio (K = 1/8 × cap/174, DY = its 'H' baseline): `$KH2Menu` K 0.14655 DY 0, `$jimakuNE` K 0.15805 DY 14, `$JimakuJP` K 0.14511 DY 11; join extension +18 units in all classes | `~mods` held the F1 pak (sha 302d95d1…; no SWAP_LOG existed) + title screenshot PASS, TEST50 |
| 2026-10-09 | Shaper = UAX #9 per line (paragraph RTL): numbers after Arabic follow W2 (4-1 shows 1-4, 50% shows %50, #1 shows 1#); "80 HP"..."HP 80" give the same visual line (unshape picks one) | executor, TEST50 (screenshot check) |
| 2026-10-09 | Round prompts are saved verbatim in `docs\rounds\<ROUND>.md` | user, TEST50 |
| 2026-10-09 | Elemental Resistance uses element nouns, not spell names: مقاومة النار / الجليد / الصاعقة / الماء / الهواء / الظلام (glossary rows "X Resistance"); Donald Fire/Blizzard/Thunder/Cure = دونالد فاير / بليزارد / ثاندر / كيور (KH2 order; Donald Aero = دونالد إيرو by the same pattern); 14239 = أول فيض من المشاعر (title text, not the Surge term); the 39 TRANS-2 proposed terms approved as they are; EXP stays خبرة | supervisor, SWAP-1 |
| 2026-10-09 | **Arabic comma `،` is allowed (proven in `$jimakuNE`)**: no space before, one after; ASCII `,` stays in numbers, Latin runs, tags/args/plural syntax; `؟` stays ASCII `?` until a screenshot proves it. Applied by `tools\comma_fix.py` (210 rows). Journal/tutorials style: imperative for tutorials, narrative MSA for the journal; rows with no `<br>` in EN get none in AR | supervisor, TRANS-3 |
| 2026-10-09 | Arabic hashtags in the journal: translated, words joined with `_` | supervisor, BUILD-1 |
| 2026-10-09 | Conv hoist: a row with text inside `<conv(..)>` keeps one `<conv(X)>` at the row start and `<conv(off)>` at the end; the shaper shapes the inside (Arabic conv groups in mid-row stay an error) | supervisor, BUILD-1 |
| 2026-10-09 | Film titles: Frozen = ملكة الثلج, Toy Story = حكاية لعبة (common Arabic dub titles, glossary approved); Tangled = متشابك pending, supervisor to verify | supervisor, BUILD-1 |
| 2026-10-09 | Line breaking (SHAPER_SPEC §7): every line wider than its text field is broken at spaces by measured width (also lines between EN `<br>`), field per namespace in `technical\FIELD_WIDTHS.tsv`; no known field = unbroken; adjacent icons are one atom (drawn order kept) | executor, BUILD-1 (to be confirmed in-game) |
| 2026-10-09 | Full builds are named `pakchunk99-arabic_P.pak`; `state\INSTALLED.tsv` lists the installed rows (STATS "installed") | supervisor / executor, BUILD-1 |
| 2026-10-09 | **Magic names in Arabic (KH3 only):** Fire/Fira/Firaga/Firaza = نار / نار قوية / نار كبرى / نار قصوى; Blizzard..aza = جليد / جليد قوي / جليد أكبر / جليد أقصى; Thunder..aza = صاعقة / صاعقة قوية / صاعقة كبرى / صاعقة قصوى; Cure..aza = شفاء / شفاء قوي / شفاء أكبر / شفاء أقصى; Aero..aza = ريح / ريح قوية / ريح كبرى / ريح قصوى; Water..aza = ماء / ماء قوي / ماء أكبر / ماء أقصى; Donald X = X دونالد; compounds take the definite form (تعزيز النار, سوار النار الكبرى); Dark Firaga = نار كبرى مظلمة; replaces the GLOSS-2/SWAP-1 transliterations (KH2 glossary file unchanged) | user, FULL-1 |
| 2026-10-09 | Help-text fields (`MainLibrary#68` = `CodeMenu#26`: ability, customize and premium descriptions) show at most 2 Arabic lines: rows with more are reflowed at build time (`shaper.reflow`, FIELD_WIDTHS `max_lines`); AR text keeps the EN `<br>` count | executor, FULL-1 (screenshot: line 3 clipped) |
| 2026-10-09 | `review\script\` is the reference script for translation and review (story order from the Theater table, speaker codes from keys) | user, FULL-1 |
| 2026-10-09 | LV label stays مستوى (final); the party LV field CampMenu #335 is widened left (xMin 86.95 px) by shipping one patched movie (CampMenu, `_0_P` base) in our pak | user, TRANS-4 |
| 2026-10-09 | Story dialogue style: natural MSA with a light spoken feel, no dialect; character voices kept; subtitles near EN length, same `<br>` count; ASCII `?`; puns/idioms by meaning (listed as unsure); italic tags never split a joining Arabic word; song lyrics in own MSA wording (to be confirmed) | user / executor, TRANS-4 |
| 2026-10-09 | `<p align>` in text drops the line; flush-left kept for now (alignment test cancelled; the ALIGN_RIGHT hook stays in `build_build1.py` for a later nbsp-padding test) | supervisor, REVIEW-1 |
| 2026-10-09 | Heartbinder = رابط القلب (Dream Heartbinder = رابط قلب الحلم unchanged; Pixel/'Ohana/Pride/Ocean keep the pattern رابط قلب X, executor assumption); Altair = الطائر; Datascape = عالم البيانات, Datascapes = عوالم البيانات | supervisor, REVIEW-1 |
| 2026-10-09 | `؟` (U+061F) is a validator ERR until a screenshot proves it; known typos live in `translation\typo_patterns.tsv` (WARN TYPO, whole-word regex) | supervisor, REVIEW-1 |
| 2026-10-09 | Buzz Lightyear = باز لايتير; Keyblade wielder (fem) = حاملة كيبلايد (second form, feminine); the other TRANS-4 proposed terms approved as they are | supervisor, REVIEW-1 |
| 2026-10-09 | Hashtags (journal and Re Mind): words in Arabic, multiword tags joined with `_`, the U+FFE0 marker and tags otherwise exact; validator WARN HASHTAG catches a Latin hashtag token in a hashtag row | supervisor, TRANS-6 |
| 2026-10-09 | Pose category "Action" (14589) = الحركة (motion noun from Flowmotion), not الفعل; Chirithy as a friend's name takes no vocative | supervisor, TRANS-6 |
| 2026-10-09 | Subtitles and field/battle voice break at `92_message/Subtitle #1` ($jimakuNE 38 pt, 7,545 units; the field word-wraps by itself, in visual order for Arabic, so every line is pre-broken); lines counted per `<pb>` page; design capacity 2 lines (EN), box 4; rows over it are listed, never shortened or reflowed | executor, BUILD-4 (to be confirmed in-game) |
| 2026-10-09 | Namespaces with multi-line EN but no known field break at their widest EN line ended by `<br>` in mid-sentence (else the widest EN line of those keys); recorded as "(EN widest)"..."!" so it fits HudRight #109 without widening it; Re Mind/subtitle rows use the glossary Power of Waking and keep Kingdom Hearts masculine; REVIEW-2 fixes only real errors (no taste edits) | executor, REVIEW-2 |
| 2026-10-10 | Publishing: every round must end with `tools\publish.bat` after `refresh.bat` and `secret_check`; PROJECT_MAP sections 3, 4, 7, 8 must be updated BEFORE publishing; a new Release is created only when a new BUILD is installed AND at least its checklist screenshots were reviewed by the supervisor. Only `public_repo\` (clone of github.com/exelight7/KH3RM_AR, branch main, never force-push) is ever pushed; the private repo and its history never | user approval, PUBLISH-1 |
| 2026-10-10 | Installer: C# WPF .NET 8 in `tools\installer\` (original XAML art only; optional `art\background.png` slot), self-contained single file, detects Steam (registry + libraryfolders.vdf + appmanifest 2552450) and Epic (LauncherInstalled.dat), writes only `~mods\pakchunk99-arabic_P.pak`, refuses while the game runs; unsigned (SmartScreen note in the release) | user approval, RELEASE-080 |

## 5. Folders and key files (auto)

| path | what |
|---|---|
| `CHANGELOG.md` | Changelog |
| `LICENSE_TODO.md` | License — undecided |
| `PROJECT_MAP.md` | PROJECT_MAP — KH3 Arabic (start here) |
| `README.md` | تعريب Kingdom Hearts III + Re Mind |
| `REMOVE_ARABIC.bat` | chcp 65001 >nul |
| `SWAP_TO_BUILD1.bat` | chcp 65001 >nul |
| `SWAP_TO_BUILD2.bat` | chcp 65001 >nul |
| `SWAP_TO_BUILD3.bat` | chcp 65001 >nul |
| `SWAP_TO_BUILD4.bat` | chcp 65001 >nul |
| `SWAP_TO_BUILD5.bat` | chcp 65001 >nul |
| `SWAP_TO_F1.bat` | chcp 65001 >nul |
| `SWAP_TO_F2.bat` | chcp 65001 >nul |
| `SWAP_TO_TEST50.bat` | chcp 65001 >nul |
| `docs\` | project docs: INDEX (doc list), SUPERVISOR (full supervisor instructions) |
| `docs\INDEX.md` | Docs index |
| `docs\SUPERVISOR.md` | Supervisor instructions (full copy) |
| `extracted\` | read-only decrypted copies of game files + pak index (gitignored, never deleted) |
| `font\` | reserved for font files (empty; Segoe UI is read from C:\Windows\Fonts) |
| `out\` | build outputs: out\builds\<round>\ paks, pakroots, verify tables (gitignored, never deleted) |
| `public_repo\` | (no description) |
| `review\` | review pages (Markdown), corrections, validation report; **`review\script\` = the reference script for translation and review** (story order by the Theater table + TIPS pages, `tools\make_script.py`) |
| `review\FLAGS.md` | Flagged rows |
| `review\INDEX.md` | Review index |
| `review\RULES.md` | Review workflow |
| `review\UNSURE_REVIEW2.md` | UNSURE_REVIEW2 (REVIEW-2: items not changed or changed on an assumption) |
| `review\VALIDATION.md` | VALIDATION |
| `review\review_dialogue.tsv` | TSV, columns: id, EN, AR, status, flags, note |
| `review\review_items_abilities.tsv` | TSV, columns: id, EN, AR, status, flags, note |
| `review\review_journal.tsv` | TSV, columns: id, EN, AR, status, flags, note |
| `review\review_menus_ui.tsv` | TSV, columns: id, EN, AR, status, flags, note |
| `review\review_remind.tsv` | TSV, columns: id, EN, AR, status, flags, note |
| `review\review_subtitles_cutscenes.tsv` | TSV, columns: id, EN, AR, status, flags, note |
| `review\review_tutorials.tsv` | TSV, columns: id, EN, AR, status, flags, note |
| `screenshots\` | optional, gitignored; screenshots are sent in the supervisor chat (log file = chat) |
| `state\` | round log, last report, stats, screenshot log |
| `state\INSTALLED.tsv` | TSV, columns: id, ar_sha1, build |
| `state\LAST_REPORT.md` | latest round report (overwritten each round) |
| `state\PROGRESS.md` | round log, 3 lines per task (source of the round history below) |
| `state\SCREENSHOT_LOG.tsv` | TSV, columns: date, round, string_ids, screenshot_file, result |
| `state\STATS.md` | STATS |
| `state\SWAP_LOG.tsv` | TSV, columns: time, action, hash, result |
| `technical\` | recon, tag inventory, shaper spec, text counts, field widths, text coverage (TEXT_COVERAGE.md) |
| `technical\BUILD1_CHECKLIST.md` | قائمة فحص BUILD-1 |
| `technical\BUILD2_CHECKLIST.md` | قائمة فحص BUILD-2 |
| `technical\BUILD3_CHECKLIST.md` | قائمة فحص BUILD-3 |
| `technical\BUILD5_CHECKLIST.md` | قائمة فحص BUILD-5 |
| `technical\FIELD_WIDTHS.tsv` | TSV, columns: prefix, keys, movie, field, font, font_id, size_pt, x0, x1, y0, y1, max_lines, reflow, evidence |
| `technical\RECON_KH3.md` | RECON_KH3 — Kingdom Hearts III + Re Mind (Steam), read-only recon |
| `technical\SHAPER_SPEC.md` | SHAPER_SPEC — Arabic pre-shaper for KH3 Scaleform text |
| `technical\TAGS.md` | TAGS — markup in KH3 English text (VERIFIED from `extracted\text_en.tsv`, 17,222 entries) |
| `technical\TEST50_CHECKLIST.md` | قائمة فحص TEST50 |
| `technical\TEXT_COUNTS.tsv` | TSV, columns: level, name, category, entries, empty, unique_texts, words, chars |
| `technical\TEXT_COVERAGE.md` | TEXT_COVERAGE — every source of visible text (FULL-1) |
| `technical\theater_order.tsv` | TSV, columns: event, theater_scene_key |
| `tools\` | all scripts (Python 3.12, run from the project root) + repak |
| `tools\TOOLS.md` | Tools (official sources only) |
| `tools\apply_corrections.py` | Apply review\corrections\*.tsv (header: id old_AR new_AR reason) to translation\<cat>\<file>.tsv. |
| `tools\build1_rows.py` | One-time (BUILD-1): write review\corrections\build1_conv.tsv (the 12 tutorial control lists with <conv> groups, |
| `tools\build_arabictest1.py` | ARABIC-TEST-1 build: NEW GAME (kh3_menu.title/menu_0002) in 3 variants + TresFont with Segoe UI Arabic in $sougei. |
| `tools\build_arabictest2.py` | ARABIC-TEST-2 build: title screen in Arabic (translation\ rows with status != todo, shaped) for kh3_menu + kh3_settings, |
| `tools\build_build1.py` | BUILD-1 build: every translated row of every category (status != todo, AR not empty) shaped into the en .locres, |
| `tools\build_build2.py` | BUILD-2 (FULL-1): the full build of tools\build_build1.py (every translated row, line breaking) with the FULL-1 |
| `tools\build_build3.py` | BUILD-3 (TRANS-4): the BUILD-2 full build plus |
| `tools\build_build4.py` | BUILD-4: the first full build with every translated row (all categories: story dialogue, subtitles, Re Mind, |
| `tools\build_build5.py` | BUILD-5: the BUILD-4 pipeline unchanged (tools\build_build4.py: same movie patches, TresFont, line breaking, no <p align>) |
| `tools\build_test50.py` | TEST50 build: 50 test rows (menus, items, equipment, abilities, plural/acronym/set-letter rows, tutorials, |
| `tools\comma_fix.py` | TRANS-3: ASCII ',' used as Arabic punctuation -> '،' in translated AR rows. Usage: comma_fix.py [--apply] |
| `tools\font_census.py` | Read-only (TEST50): font classes of every text field in the game's Scaleform movies. |
| `tools\full1_magic.py` | One-time (FULL-1 Part B): magic names in Arabic (user decision FULL-1, KH3 only; KH2 glossary file unchanged). |
| `tools\gfx_edittext.py` | Read-only: list every DefineEditText (tag 37) in Scaleform SwfMovie .uexp files: id, variable name, font |
| `tools\gfx_fonts.py` | Read-only: list fonts inside a Scaleform GFx movie embedded in a SwfMovie .uexp. |
| `tools\gfx_imports.py` | Read-only: for each Scaleform SwfMovie .uexp, list fonts it imports (ImportAssets/ImportAssets2, tags 57/71) |
| `tools\gfx_layout.py` | Read-only (BUILD-4): where a Scaleform movie places its characters. For every DefineSprite (tag 39) and the root |
| `tools\gloss3_apply.py` | One-time (TRANS-1 part 1): apply supervisor decisions on the pending glossary conflicts. Do not re-run. |
| `tools\gloss_hits.py` | TRANS-2 helper: glossary terms (approved, not type menu unless exact row match) that occur in a dump file. |
| `tools\import_kh2_glossary.py` | One-time/idempotent (GLOSS-1): import translation\kh2_glossary.md (finished KH2 project, Arabic Markdown tables) |
| `tools\locres.py` | UE4 .locres reader/writer (legacy v0 and compact v1, as shipped by KH3 / UE 4.17). |
| `tools\make_glossary.py` | translation\glossary.tsv (source of truth) -> recount kh3_count/example_ids from translation\<cat>\*.tsv EN |
| `tools\make_public.py` | Regenerate public_repo\ (a clone of github.com/exelight7/KH3RM_AR) from the private project. Never copies game files, |
| `tools\make_release.py` | Prepare out\release\ for a GitHub Release: the installed BUILD pak, SHA256.txt, INSTALL_AR.bat, REMOVE_AR.bat, AR_MESSAGES.txt. |
| `tools\make_review.py` | Generate review\md\<category>_NN.md (300 rows/page, game order), review\INDEX.md, review\FLAGS.md |
| `tools\make_script.py` | Generate review\script\ (FULL-1 Part E): the reference script for translation and review, Markdown only. |
| `tools\make_swap_scripts.py` | SWAP-1/TEST50/BUILD-1/FULL-1/TRANS-4/BUILD-4: generate SWAP_TO_F1.bat, SWAP_TO_F2.bat, SWAP_TO_TEST50.bat, SWAP_TO_BUILD1.bat, |
| `tools\merge_translation.py` | Merge translation\<category>\*.tsv back into one pipeline TSV (namespace,key,source_hash,text,category,file) for `locres.py tsv-import`. |
| `tools\pak_footer.py` | Read-only: parse UE4 .pak footers (magic 0x5A6F12E1) and print version/encryption info. |
| `tools\pak_index.py` | Read-only: decrypt and parse UE4 pak v4 indexes -> TSV (pak, path, size, compressed_size, compression, encrypted). |
| `tools\preview_text.py` | Offline preview: draw a shaped string with the glyphs of a (rebuilt) TresFont, the way Scaleform lays it out |
| `tools\public_check.py` | Check public_repo\ before every publish. Fails on: forbidden path/extension, EN column or a Latin sentence of 6+ words |
| `tools\publish.bat` | Every round ends with this (after refresh.bat and secret_check). Publishes to github.com/exelight7/KH3RM_AR, branch main, never forced. |
| `tools\refresh.bat` | end-of-round pipeline: merge check, tests, corrections, validate, review pages, script, stats, map, secret check |
| `tools\remind_map.py` | Read-only: summarise extracted/pak_index.tsv per pak and flag Re Mind (DLC) content. |
| `tools\review2_page.py` | REVIEW-2 helper: page N (300 rows) in story order = review\script order (dialogue, subtitles, Re Mind in story) then the |
| `tools\review2_sub.py` | REVIEW-2 helper: substring fixes. Usage: python -I tools\review2_sub.py N file ; file lines 'id<TAB>old_fragment<TAB>new_fragment<TAB>reason' |
| `tools\scan_magic.py` | Read-only: count plaintext signatures inside pak files (uasset, locres, zlib, ttf/otf). |
| `tools\secret_check.py` | Fail if the AES key or a game binary is tracked by git (or staged). Checks the index, not the working tree. |
| `tools\setrow.py` | Fix one translated row in place: python -I tools\setrow.py <id> <AR> [note]  (menus_ui only; TRANS-1 helper) |
| `tools\shaper.py` | Arabic pre-shaper for KH3 Scaleform text (technical/SHAPER_SPEC.md §1-6; §8 checks in tools/test_shaper.py). |
| `tools\split_translation.py` | One-time/idempotent: split translation\en_source.tsv into translation\<category>\<file>.tsv. |
| `tools\stats.py` | Write state\STATS.md. translated = status in translated/reviewed/verified; reviewed = reviewed/verified; |
| `tools\tag_inventory.py` | Read-only: inventory of markup in the English locres export. |
| `tools\test_corrections.py` | unit tests for apply_corrections.py |
| `tools\test_public_check.py` |  |
| `tools\test_shaper.py` | unit tests for shaper.py: SHAPER_SPEC §9a (U1-U12), §9b (the 20 TAGS.md examples T1-T20 + T21/T22), |
| `tools\test_validate.py` | unit tests for validate.py |
| `tools\text_counts.py` | Read-only: entry/word counts per category for the English locres export (extracted/text_en.tsv). |
| `tools\text_coverage.py` | Read-only (FULL-1 Part D): inventory of every source of player-visible text in the installed game. |
| `tools\trans1_report.py` | TRANS-1: write state\LAST_REPORT.md (data parts generated from translation\menus_ui). One-time helper. |
| `tools\trans2_report.py` | TRANS-2: write state\LAST_REPORT.md (data parts generated from translation\ and review\corrections\applied). One-time helper. |
| `tools\trans4_page.py` | TRANS-4 helper: story dialogue and cutscene subtitles page by page in the order of review\script\ (script_NNN.md, |
| `tools\trans5_page.py` | TRANS-5 helper: story dialogue and cutscene subtitles page by page in the order of review\script\ (script_NNN.md, |
| `tools\trans_page.py` | TRANS-1 helper. `dump N` prints the rows of menus_ui page N (300 rows, game order) that still need a human translation |
| `tools\tresfont.py` | Scaleform TresFont (UE4 SwfMovie .uasset/.uexp) parser + writer, down to individual glyph edges. |
| `tools\tsvlib.py` | Shared helpers for the translation TSVs (ORG-1). Plain TSV, no quoting; text is already escaped like en_source.tsv. |
| `tools\update_map.py` | Regenerate the "(auto)" sections of PROJECT_MAP.md: numbers (from state\STATS.md, so run stats.py first), |
| `tools\validate.py` | Validate translated rows against EN. Writes review\VALIDATION.md; flags are reused by make_review.py. |
| `translation\` | translation TSVs per category/file (EN + AR + status), glossary |
| `translation\GLOSSARY_CONFLICTS.md` | Glossary conflicts (KH2 glossary → KH3) |
| `translation\GLOSSARY_PROPOSALS.md` | Glossary proposals — KH3-new and Re Mind terms |
| `translation\allowed_latin.txt` | history only (TRANS-1 whitelist); the LATIN rule now compares each row with its own EN |
| `translation\en_source.tsv` | TSV, columns: namespace, key, source_hash, text, category, file |
| `translation\glossary.md` | Glossary — KH3 Arabic |
| `translation\glossary.tsv` | TSV, columns: en, ar, type, source, status, kh3_count, example_ids, note |
| `translation\kh2_glossary.md` | مسرد مصطلحات KH2FM (المصدر الوحيد للحقيقة لأسماء الأعلام) |
| `translation\typo_patterns.tsv` | TSV, columns: pattern, correct, note |

## 6. How to run things

All commands from the project root (`C:\filessss\mewo\kh3fm-arabic`).
- **Refresh everything** (merge check, tests, corrections, validation, review pages, stats, this map, secret check): `tools\refresh.bat`
- **Shape a string / run the shaper tests:** `python -I tools\shaper.py "نص"..."installed" column after `tools\refresh.bat`).
- **BUILD-2:** `python -I tools\build_build2.py` → `out\builds\BUILD-2\` (same outputs; help-field reflow from `technical\FIELD_WIDTHS.tsv` `max_lines`); install `SWAP_TO_BUILD2.bat`, then `python -I tools\build_build2.py --installed`.
- **BUILD-5 (current full build):** `python -I tools\build_build5.py` → `out\builds\BUILD-5\` (BUILD-4 pipeline on the current TSVs, `diff_vs_build4.tsv`); install `SWAP_TO_BUILD5.bat`, then `python -I tools\build_build5.py --installed`. repak output is not byte-reproducible between runs: a rebuild gives a new sha, so regenerate the swap script (`tools\make_swap_scripts.py`) after the last build.
- **BUILD-4:** `python -I tools\build_build4.py` → `out\builds\BUILD-4\` (all translated rows, Subtitle/EN-widest line breaking, 3 patched LV movies, `movie_verify.tsv`, `overflow.tsv` = rows over field capacity); `--fields` regenerates the BUILD-4 rows of `technical\FIELD_WIDTHS.tsv`; install `SWAP_TO_BUILD4.bat`, then `python -I tools\build_build4.py --installed`. repak orders files differently per run, so a rebuild has a new pak SHA (per-file SHA identical): rebuild → regenerate the swap script.
- **Where a movie places a field (neighbour gaps):** `python -I tools\gfx_layout.py <movie.uexp> <char id>`
- **BUILD-3:** `python -I tools\build_build3.py` → `out\builds\BUILD-3\` (BUILD-2 + patched CampMenu movie, `movie_verify.tsv`, align test on row 15729); install `SWAP_TO_BUILD3.bat`, then `python -I tools\build_build3.py --installed`.
- **Story translation pages:** `python -I tools\trans4_page.py dump|apply N [file]` (script page N in story order, dialogue + subtitles).
- **Text inventory (read-only):** `python -I tools\text_coverage.py` → `technical\TEXT_COVERAGE.md` + `technical\text_coverage\*.tsv`.
- **Master script:** `python -I tools\make_script.py` → `review\script\INDEX.md` (story), `TIPS.md`, pages (also run by `tools\refresh.bat`).
- **Build the TEST50 test pak:** `python -I tools\build_test50.py` → `out\builds\TEST50\pakchunk99-test50_P.pak` + `pak_verify_sha256.tsv` + `rows.tsv` (needs font_fields.tsv). Older: `tools\build_arabictest2.py` (F1/F2 title paks)
- **Measure text fields of a movie:** `python -I tools\gfx_edittext.py <movie.uexp>...`
- **Offline join/size preview:** `python -I tools\preview_text.py <TresFont.uasset> 3 30 2 out.png "نص"`
- **Swap the test pak (double-click in the project root, close the game first):** `SWAP_TO_BUILD1.bat` / `SWAP_TO_TEST50.bat` / `SWAP_TO_F1.bat` / `SWAP_TO_F2.bat` delete our `pakchunk99-*_P.pak` from `~mods`, copy the BUILD-1 pak, the TEST50 pak or the ARABIC-TEST-2 F1/F2 pak from `out\builds\`, verify SHA256 against the build and print Arabic + English "Done" (it asks for admin rights only if the copy fails for permissions). `REMOVE_ARABIC.bat` deletes our pak and the empty `~mods`. All three refuse to run while KINGDOM HEARTS III is running and append to `state\SWAP_LOG.tsv` (time, action, hash, result). Scripts are generated by `tools\make_swap_scripts.py` (pure ASCII; messages in `tools\swap_msgs\`). Other paks: copy by hand into `C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods\`, only one of ours at a time (`technical\RECON_KH3.md` §12).
- **Commit:** after `tools\refresh.bat` exits 0; `tools\secret_check.py` must PASS.
- **Installer / release (RELEASE-080):** build the EXE: `cd tools\installer` then `dotnet publish -c Release -o ..\..\out\release\vX\publish` (needs .NET 8 SDK; embeds `out\builds\BUILD-5\pakchunk99-arabic_P.pak`, override with `-p:PakPath=...`; update `Core.ExpectedSha` and `Version` for a new BUILD). Tests: `KH3RM_AR_Setup.exe --selftest out.txt`; screenshots: `--render ar|en out.png`; icon: `--icon app.ico`. GitHub CLI 2.102.0 (official zip, sha ae64e556...) is in `tools\gh-2.102.0\x\bin\gh.exe` (gitignored); release: `gh release create v0.8.0 --prerelease --notes-file out\release\v0.8.0\RELEASE_NOTES.md <assets>` after `gh auth login` (done by the user).

## 7. Numbers (auto)

From `state\STATS.md` (regenerated by `tools\stats.py`).

| category | rows | translated | installed | reviewed | verified-by-screenshot |
|---|---|---|---|---|---|
| dialogue | 2298 | 2213 (96.3%) | 2213 (96.3%) | 2213 (96.3%) | 0 (0.0%) |
| items_abilities | 2334 | 2160 (92.5%) | 2160 (92.5%) | 2160 (92.5%) | 3 (0.1%) |
| journal | 628 | 615 (97.9%) | 615 (97.9%) | 615 (97.9%) | 0 (0.0%) |
| menus_ui | 3849 | 3605 (93.7%) | 3605 (93.7%) | 3604 (93.6%) | 94 (2.4%) |
| remind | 1163 | 1126 (96.8%) | 1126 (96.8%) | 1126 (96.8%) | 0 (0.0%) |
| subtitles_cutscenes | 6336 | 6083 (96.0%) | 6083 (96.0%) | 6083 (96.0%) | 1 (0.0%) |
| tutorials | 614 | 613 (99.8%) | 613 (99.8%) | 613 (99.8%) | 0 (0.0%) |
| TOTAL | 17222 | 16415 (95.3%) | 16415 (95.3%) | 16414 (95.3%) | 98 (0.6%) |

## 8. Open questions

- BUILD-5 screenshots (`technical\BUILD5_CHECKLIST.md`, 8 places; incl. level-up line 15964, rows 01091/05448, party card level label): subtitle line order and 3-line rows (03474, 03581, 06647), field voice in the Subtitle field (assumed), save card and gummi LV labels; from BUILD-3: party-card مستوى and help boxes still unconfirmed.
- Row 15964 (LV UP!) is installed in BUILD-5 (1,067 of 1,621 units in HudRight #109); confirm by screenshot. Supervisor review still open: lyrics (own MSA wording), unsure rows (`review\UNSURE_REVIEW2.md`, 13 items), the Re Mind batch.
- Row 05955 uses the feminine «حاملة كيبلايد» (glossary second form); its GLOSS warning is accepted.
- Field guesses to confirm in-game: field/battle voice = Subtitle #1; 49 "(EN widest)" namespaces (tutorial popups, game-over hints, gummi menus, mission/settings help) break at their widest mid-sentence EN line; settings graphics/keyboard and the streaming notice have only engine-wrapped EN paragraphs (no width evidence).
- Images/videos with English words: 315 assets ≈ 958 words (`technical\TEXT_COVERAGE.md` §5), later texture phase; signage decals in maps not counted.
- `؟` still unproven (ASCII `?` kept, now a validator ERR); tutorial control lists in the flush-left Game Help field.
- Glossary: Tangled = متشابك (supervisor to verify); 51 TRANS-3 proposed terms; tutorial line "جرب إلقاء نار" keeps the bare command name.
- Installer is unsigned (SmartScreen warning); no art file supplied yet (`tools\installer\art\`); Epic detection is tested on fake files only.
- Publishing: license undecided (`LICENSE_TODO.md`); the GitHub repo still carries its default GPL v2 `LICENSE` (kept, not our decision); credits list in the public README is a placeholder.
- GPT unsure list (in-game checks): `review\gpt\UNSURE_batch1.md` (local, untracked).
- Re Mind (TRANS-5): hashtags now Arabic (TRANS-6); music titles transliterated; spirit names transliterated like Necho Cat (13 proposed glossary terms); Action pose category = الحركة (TRANS-6); Re Mind menu/Data Greeting/Slideshow screens not yet seen in-game.
- Typo WARN 15203: «بلغ المعلمان» is past tense (reached), a false positive of the sentence-start «بلغ» pattern; left as is.

## 9. Round history (auto)

- 2026-10-08 **RECON-1** (3 entries) — last: T3-6 BLOCKED on AES decision; T7 ~mods + _P documented, _0_P conflict; T8 RECON_KH3.md written. STOP: ask user.
- 2026-10-08 **RECON-2** (18 entries) — last: T6 STOP: report in state\LAST_REPORT.md; no blockers.
- 2026-10-08 **PIPE-1** (18 entries) — last: STOP: all 6 tasks PASS/DONE; report in state\LAST_REPORT.md; no blockers.
- 2026-10-08 **ARABIC-TEST-1** (3 entries) — last: install: no ~mods/old pak found (empty "mods"..."ORG-1: project structure"..."ORG-2: markdown review, corrections tool".
- 2026-10-08 **ARABIC-TEST-2** (24 entries) — last: STOP: F1 installed, waiting for F1/F2 screenshots; report in state\LAST_REPORT.md.
- 2026-10-08 **GLOSS-1** (24 entries) — last: STOP: committed "..."; report in state\LAST_REPORT.md.
- 2026-10-08 **GLOSS-2** (6 entries) — last: T5 close: refresh.bat exit 0 (validate 0 ERR), secret_check PASS, PROJECT_MAP 3/4/8 + CHANGELOG updated; committed.
- 2026-10-08 **TRANS-1** (44 entries) — last: STOP: final refresh.bat + secret_check, commit "..."; report in state\LAST_REPORT.md.
- 2026-10-08 **TRANS-2** (32 entries) — last: STOP: final refresh.bat + secret_check, commit "..."; report in state\LAST_REPORT.md.
- 2026-10-09 **SWAP-1** (9 entries) — last: T3 STOP: report in state\LAST_REPORT.md.
- 2026-10-09 **TEST50** (21 entries) — last: STOP: TEST50 installed, waiting for screenshots per technical\TEST50_CHECKLIST.md.
- 2026-10-09 **TRANS-3** (12 entries) — last: open: conv-group rows, hashtag style, 52 proposed terms.
- 2026-10-09 **BUILD-1** (15 entries) — last: STOP: BUILD-1 installed, waiting for screenshots per technical\BUILD1_CHECKLIST.md.
- 2026-10-09 **FULL-1** (21 entries) — last: STOP: BUILD-2 installed, waiting for screenshots per technical\BUILD2_CHECKLIST.md and the LV / alignment decisions.
- 2026-10-09 **TRANS-4** (103 entries) — last: STOP: BUILD-3 installed, waiting for screenshots per technical\BUILD3_CHECKLIST.md; story text translated (88.8 %); next: Re Mind batch, BUILD-4.
- 2026-10-09 **REVIEW-1** (24 entries) — last: T8 close: Commit: REVIEW-1: GPT review batch 1 applied.
- 2026-10-09 **TRANS-6** (3 entries) — last: T3-T5: validator WARN HASHTAG + test; refresh.bat 0 ERR, secret_check PASS; commit TRANS-6.
- 2026-10-09 **BUILD-4** (14 entries) — last: STOP: commit "..."; waiting for screenshots per technical\BUILD4_CHECKLIST.md and the 15964 / HudRight #109 decision.
- 2026-10-10 **REVIEW-2** (37 entries) — last: stats: reviewed 95.3 percent (16,414 of 17,222).
- 2026-10-10 **BUILD-5** (4 entries) — last: T4 close: refresh 0 ERR, secret_check PASS, PROJECT_MAP 3 4 6 7 8 + CHANGELOG, commit.
- 2026-10-10 **PUBLISH-1** (6 entries) — last: T8 close: refresh 0 ERR, secret_check PASS, private commit (no push).
- 2026-10-10 **RELEASE-080** (3 entries) — last: T3 release prep: gh 2.102.0 official zip (sha ae64e556...) in tools\gh-2.102.0, not logged in; assets + RELEASE_NOTES.md ready; waiting for user gh auth login.

## 10. Public repository

- **URL:** https://github.com/exelight7/KH3RM_AR (branch `main`; pushing and Releases there are approved, standing, for this one repository only; never force-push; no other remote).
- **Public:** README, PROJECT_MAP/CHANGELOG copies, docs, technical docs, `state\STATS.md` + `PROGRESS.md`, `translation\ar\<category>\*.tsv` (Arabic only: id, namespace, key, source_hash, AR, status, note), glossary, `review\RULES.md`, our scripts in `tools\`, swap/install `.bat` files; the built pak only as a GitHub Release asset.
- **How to publish:** after `tools\refresh.bat` and `tools\secret_check.py` pass and sections 3, 4, 7, 8 are updated, run `tools\publish.bat` (make_public.py, public_check.py, commit `sync: <round>` in `public_repo\`, push). `public_repo\` is gitignored here. Authentication is done by the user in the browser (Git Credential Manager).
- **Release:** `python -I tools\make_release.py BUILD-N` fills `out\release\` (pak, SHA256.txt, INSTALL_AR.bat, REMOVE_AR.bat, AR_MESSAGES.txt); create it only when that BUILD is installed and its checklist screenshots were reviewed by the supervisor.
