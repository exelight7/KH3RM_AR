# Changelog

## 2026-10-13 — CODEX-REVIEW4-4

مراجعة 4305 سطرا؛ تطبيق 19 تصحيحا لغويا في المصدر، وإبقاء 24 مسألة سياقية دون تخمين. التفاصيل في docs/rounds/CODEX-REVIEW4-4.md. اجتازت فحوص المشروع مع صفر أخطاء مانعة؛ التصحيحات تحتاج بناء واختبارا لاحقا.

## 2026-10-13 — CODEX-REVIEW4-3

مراجعة 4305 سطرا؛ تطبيق 32 تصحيحا لغويا في المصدر، وإبقاء 14 مسألة سياقية دون تخمين. التفاصيل في docs/rounds/CODEX-REVIEW4-3.md. اجتازت فحوص المشروع مع صفر أخطاء مانعة؛ التصحيحات تحتاج بناء واختبارا لاحقا.

## 2026-10-13 — CODEX-REVIEW4-2

مراجعة 4306 سطرا؛ تطبيق 49 تصحيحا لغويا في المصدر، وإبقاء 12 مسألة سياقية دون تخمين. التفاصيل في docs/rounds/CODEX-REVIEW4-2.md. اجتازت فحوص المشروع مع صفر أخطاء مانعة؛ التصحيحات تحتاج بناء واختبارا لاحقا.

## 2026-10-13 — CODEX-REVIEW4-1

مراجعة 4324 سطرا؛ تطبيق 37 تصحيحا لغويا في المصدر، وإبقاء 14 مسألة سياقية دون تخمين. التفاصيل في docs/rounds/CODEX-REVIEW4-1.md. اجتازت فحوص المشروع مع صفر أخطاء مانعة؛ التصحيحات تحتاج بناء واختبارا لاحقا.

## README-AR (2026-10-11)
- Public README, TESTER_GUIDE, FAQ, bug report template and LICENSE_TODO are Arabic only; `make_public.py` and `tools\public_templates\README.md` generate them. Release 0.8.3 notes rewritten in Arabic (pre-release kept, assets untouched).

## RELEASE-083b (2026-10-11)
- Release 0.8.3 now carries 3 assets: the unchanged v0.8.2 installer, text pak (BUILD-7) and SHA256SUMS.txt; one note line added.

## 0.8.3 (2026-10-11, pre-release, docs and tools only)
- Docs and tools: TESTER_GUIDE, FAQ, bug report template, `find_text`, `apply_feedback`, skip audit.
- NO change to the translation or the pak: identical to 0.8.2 (BUILD-7, SHA256 f9e23f373ce52a5e9c6690d264b7228d43d0e28aa55d9d76386514db511e82d7).
- The Arabic text of TESTER_GUIDE and FAQ is under review.

## RELEASE-083 (2026-10-11)
- Release 0.8.3 (pre-release, no assets) and public sync; text pak unchanged = BUILD-7.

## LIGHT-3 (2026-10-11)
- Read-only evidence: row 10847 recommendation B; `technical/IMAGES2_PREP.md` (16 minigame HUDs + 5 unreadable); colour-tag join check PASS. No translation, build or publish change.

## LIGHT-2 (2026-10-11)
- Public sync check (read-only, temp folder): 4 files only in temp, 4 differ; public_check PASS. `review/DECISIONS_NEEDED.md` (19 open items). `docs/INSTALLER_0.9.0_PLAN.md` (docs only). No translation, build or publish change.

## FINISH-TRANS (2026-10-11)
- `tools/skip_audit.py`: `review/SKIP_AUDIT.tsv` (807 skipped rows classified), `SKIP_SUSPECTS.tsv`, `SAME_AS_EN.tsv`; `tools/stats.py`: "Translatable coverage" line (100.0%). No translation edits.

## TESTER-KIT (2026-10-10)
- `tools/find_text.py` (Arabic with/without ال, pre-shaped input via the shaper, `--ids`, `--around`), `tools/apply_feedback.py` -> `review/FEEDBACK_REPORT.md`, tests for both (added to refresh.bat), `state/FEEDBACK_TEMPLATE.tsv`.
- `docs/TESTER_GUIDE.md`, `FAQ.md`, `.github/ISSUE_TEMPLATE/bug_report.yml` (public; added to make_public).
- 0.9.0 draft: real counts (5 unreadable HUD textures, 47 styled logos, 16 minigame HUDs).

## LIGHT-1 (2026-10-10)
- `stats.py` / `make_review.py`: category "images" (18 rows of `images_strings.tsv`, own row after TOTAL; other numbers unchanged); `tsvlib.load_images_strings`. Validator on those rows: 0 flags.
- `docs/RELEASE_DRAFT_0.9.0.md` (AR + EN, not published), `tools/fill_release_notes.py` (dry run), supervisor test report section in `technical/IMAGES_MASS_CHECKLIST.md`.

## IMAGES-MASS (2026-10-10)
- Images pak `pakchunk98-arabic-images_P.pak` (194 textures, 1,240 text boxes; installed beside the text pak, not released): command menu headers of all 14 world styles + the dance/ship copies, chain/shotlock/Data Greeting/Premium/Slideshow labels, 128 of 150 Game Help pictures, 25 area banners, 9 Classic Kingdom LCD textures, 11 shared HUD textures (English cell only). 193 of the 234-texture repaint plan = 82.5 %; the rest listed with reasons in `technical/IMAGES_STILL_ENGLISH.tsv`.
- `tools/texture_text.py` mass pipeline: erase box separate from the text box, fills `heal` (screenshot labels), `inpaint` (plates), `holes` + effect `knockout` (cut-out plates), row-gradient fill colour, 1 px stroke for text >= 24 px, linked/grouped sizes, `tpl:` template sources, per-texture checks (re-parse, size/format/mips, changed blocks, >= 2 px margin, no pixel changed outside the boxes) and before/after sheets.
- New: `tools/images_tutorial_rects.py`, `tools/images_banner_rects.py`, `technical/images_work/`, `translation/images_strings.tsv` (18 strings with no translation row), `technical/IMAGES_MASS_CHECKLIST.md`, `SWAP_TO_IMAGES_MASS.bat`, `REMOVE_IMAGES.bat`; `tools/stats.py` reports "...".

## SYNC-BUILD7 (2026-10-10)
- Cloud second-pass review synced (`tools\sync_cloud.bat`, PRs 1-6 merged): 69 correction files, 182 rows changed, 16,106 rows noted "...". `tools/apply_corrections.py`: an id corrected by two parallel cloud files is merged (identical results, or a check mark plus one real change); two different real changes still refuse.
- Glossary aligned with the corrected rows (Diving Strike, Powerwild, Frost Serpent, Monsters Inc), approved, note "supervisor SYNC-BUILD7".
- BUILD-7 (`tools/build_build7.py`, the BUILD-6 pipeline unchanged): 182 entries differ from BUILD-6; pak sha f9e23f37…, 4,889,918 B; 73 files SHA256 PASS, round trip 0 fail; installed with `SWAP_TO_BUILD7.bat`; `technical/BUILD7_CHECKLIST.md` (4 places).
- Installer 0.8.2 (embeds BUILD-7; 22/22 self tests PASS); GitHub pre-release **0.8.2** with 5 verified assets; public README points at 0.8.2.

## FINAL-1 part 2 (2026-10-10)
- Image inventory: `tools/images_inventory.py` → `technical/IMAGES_INVENTORY.tsv` (324 textures with English: 26 area banners, 89 Scaleform `_loc`, 150 tutorial pictures, 2 key atlases, 25 logos, 9 LSI, 23 shared HUD textures), `technical/IMAGES_PLAN.md`; movie bitmaps and TexturePump lists checked (no baked text).
- `tools/texture_codec.py`: UE4.17 Texture2D read/write (uexp + ubulk), BC7/DXT5/BC4/BGRA decode + block-patch encode; byte-identical round trip on 18 textures.
- `tools/texture_text.py` + `technical/images_rects.tsv`: Arabic repaint (background fill, sampled colours, Segoe UI, pre-shaped RTL).
- Pilot pak `pakchunk98-arabic-images_P.pak` (3 textures, 16 text boxes) installed next to BUILD-6 with the new `SWAP_TO_IMAGES_PILOT.bat` / `REMOVE_IMAGES_PILOT.bat`; `technical/IMAGES_PILOT_CHECKLIST.md`. Not released.

## FINAL-1 part 1 (2026-10-10)
- Row 05051 fixed (`review/corrections/applied/final1_fix.tsv`, REVIEW-3 wording).
- BUILD-6 (`tools/build_build6.py`, the BUILD-5 pipeline unchanged): 6 entries differ from BUILD-5 (01392 01505 03913 05051 05962 06084); pak sha f6e8be85…, 4,889,997 B; 73 files SHA256 PASS, round trip 0 fail, validate 0 ERR; installed with the new `SWAP_TO_BUILD6.bat`; `technical/BUILD6_CHECKLIST.md` (6 places).
- Installer 0.8.1 (embeds BUILD-6; 21/21 self tests PASS); GitHub pre-release **0.8.1** with 5 verified assets.
- Public README: Download points at 0.8.1 (`RELEASE` in `tools/make_public.py`), roadmap (0.8.x text fixes, 0.9.0 images, 1.0.0 after full testing).

## REVIEW-3 (2026-10-10)
- 5 rows corrected (`review\corrections\applied\review3.tsv`): 01505 Isla de Muerta (KH2 form), 05962, 01392, 03913, 06084. Row 05050 skipped (fragment is in 05051). 01302/01304 unchanged (addressee not clearly male). Glossary: KH3 form retired.
- `review\UNSURE_REVIEW2.md` marked resolved. Not installed: needs BUILD-6 / v0.8.1.

## RELEASE-080 (2026-10-10)
- Installer `tools/installer/` (WPF .NET 8, single self-contained EXE, embedded BUILD-5 pak, SHA256 check, Steam/Epic detection, Arabic/English UI, original XAML art, `--selftest`/`--render`/`--icon`); release v0.8.0 (pre-release) prepared in `out/release/v0.8.0/`; README Download section; `tools/gh-*` ignored.

## PUBLISH-1 (2026-10-10)
- Public repository https://github.com/exelight7/KH3RM_AR: `tools/make_public.py` (Arabic-only export), `tools/public_check.py` + tests, `tools/publish.bat`, `tools/make_release.py`, README (Arabic + English), pre-release `v0.5-test (BUILD-5)`.

## BUILD-5 (2026-10-10)
- Rebuild with the unchanged BUILD-4 pipeline (`tools/build_build5.py`) from the reviewed TSVs: 45 entries differ from BUILD-4 (REVIEW-2 corrections + row 15964 shortened to fit HudRight #109); pak sha e43d8f97…, 4,890,011 B; 73 files SHA256 PASS, round trip 0 fail; installed with `SWAP_TO_BUILD5.bat`; `state/INSTALLED.tsv` 16,415 rows.
- `technical/BUILD5_CHECKLIST.md` replaces BUILD4_CHECKLIST (8 places + level-up line, corrected dialogue rows, party card level label).
## REVIEW-2 (2026-10-10)
- Linguistic pass over all translated dialogue, cutscene subtitles, field/town voice and Re Mind rows (9,421 rows, 32 pages, new `tools/review2_page.py`, `tools/review2_sub.py`): all set to `reviewed`; 44 rows corrected (grammar 15, gender 11, meaning 9, consistency 7, style 2) in `review/corrections/applied/review2_p*.tsv`.
- Row 15964 (level-up line) shortened to the level word + "!" (1,067 of 1,621 units, fits HudRight #109): `review2_ui.tsv`.
- `translation/typo_patterns.tsv` +10 patterns; `review/UNSURE_REVIEW2.md` (13 items). Project reviewed 42.3 % to 95.3 %. BUILD-5 is needed to install the REVIEW-1/REVIEW-2 corrections.

## BUILD-4 (2026-10-09)
- First full build: every translated row (16,415 = 95.3 %: story dialogue, subtitles, Re Mind, GPT corrections, new glossary forms) shaped into the `en` locres (`tools\build_build4.py`); pak sha ae9d609a…, 4,889,975 B, installed with the new `SWAP_TO_BUILD4.bat`; `state\INSTALLED.tsv` 16,415 rows; `technical\BUILD4_CHECKLIST.md` (8 places).
- Line breaking: cutscene subtitles and field/battle voice = `92_message/Subtitle #1` ($jimakuNE 38 pt, engine word-wrap on), gummi block descriptions = `EditGumi #385`, 49 namespaces without a known field broken at their widest mid-sentence EN line (`FIELD_WIDTHS.tsv`, `--fields`); lines counted per `<pb>` page; `reflow` column (FULL-1 help fields only); profile falls back to a shorter matching prefix. Rows over capacity listed in `out\builds\BUILD-4\overflow.tsv`, nothing shortened.
- LV labels widened left (RECT only): save card `SaveLoad #43` (xMin −2 → −19.1 px) and gummi guide `HudGumi #255` (−2 → −5.15 px) besides CampMenu #335; new read-only `tools\gfx_layout.py` (placements, neighbour gaps).
- Row 15964 still clips in `HudRight #109` (1,797 of 1,621 units): open question.

## TRANS-6 (2026-10-09)
- Re Mind fixes (`review\corrections\trans6_fix.tsv`): 02552 no vocative before Chirithy, 14589 Action = الحركة, 5 Latin hashtag rows (07865-07869) translated to Arabic with `_` joins.
- Row 15672 (Japanese-text sentence about the Epic Games Launcher) translated; the other 167 todo rows with symbol/icon/placeholder/native-script EN stay `skip:`.
- Validator: WARN HASHTAG (Latin hashtag token in a hashtag row) + unit test.

## TRANS-5 (2026-10-09)
- Re Mind batch: 1,126 of 1,163 `remind` rows translated (story events in script order, Data Greeting/Slideshow menus, Game Help, Yozora and Limitcut/secret episode lines, field voice, hashtags); 37 blank-EN rows skipped. Project 90.4 % -> 95.3 %. New helper `tools\trans5_page.py` (4 pages; apply turns U+061F into ASCII ?). 13 new proposed glossary terms. No pak rebuild.

## REVIEW-1 (2026-10-09)
- GPT Sol 6.1 review batch 1 (menus_ui, items_abilities, tutorials, journal; 6,992 rows): 210 corrections applied (`review\corrections\applied\review1_gpt.tsv`, 8 with supervisor changes); 6,895 rows `translated` -> `reviewed` (note "...").
- Glossary: Heartbinder = رابط القلب, Altair = الطائر, Datascape(s) = عالم/عوالم البيانات, Buzz Lightyear = باز لايتير, wielder (fem) = حاملة كيبلايد; 8 rows via `review1_gloss.tsv`; row 15964 = مستوى أعلى!.
- Validator: ERR QMARK (U+061F; 46 dialogue rows fixed via `review1_typos.tsv`), WARN TYPO from `translation\typo_patterns.tsv` + unit tests.
- Alignment test cancelled (`<p align>` drops the line); no ALIGN_RIGHT rows in BUILD-3 config. `.gitignore`: `.codex/`, `.serena/`, `review/gpt/`.

## TRANS-4 (2026-10-09)
- BUILD-3 (`tools\build_build3.py`): CampMenu #335 (party LV label) widened left, xMin 96.1 → 86.95 px (2 bytes, `_0_P` movie shipped in our pak), so مستوى fits. Align test `<p align="right">` on row 15729 only. Pak sha 2834d65a…, installed with the new `SWAP_TO_BUILD3.bat`; `technical\BUILD3_CHECKLIST.md`.
- Story batch: all base-game cutscene subtitles (6,077 rows, 274 scenes) and field/battle voice (2,213 rows) translated in story order with `tools\trans4_page.py`. Project 40.6 % → 88.8 %. Fixes in `review\corrections\trans4_p*.tsv`; 27 proposed glossary terms.
- `test_shaper.py`: same-visual round-trip cap scales with the number of rows.

## FULL-1 (2026-10-09)
- BUILD-1 screenshots logged (chat): 90 rows verified (title incl. CONFIG = الضبط, camera config, game settings, difficulty, pause, premium list, command menu, main menu); total verified 98 (0.6 %).
- Help-text field found: ability/customize descriptions = `MainLibrary#68` (tres.rsl.HelpText), premium menu = `CodeMenu#26`, both 1108×123 px at 23 pt; `FIELD_WIDTHS.tsv` gains `max_lines` (2); `shaper.reflow()` + test; 155 rows reflowed, 2 premium rows shortened (`review\corrections\full1_fit.tsv`).
- Party LV label measured (`CampMenu#335`, 624 units): مستوى does not fit; options listed, text unchanged. Alignment investigated (exe tag converter has no align tag); nothing changed in movies.
- Magic names in Arabic (user decision): 136 rows (`review\corrections\full1_magic.tsv`, `tools\full1_magic.py`), 31 glossary terms.
- BUILD-2 (`tools\build_build2.py`): `pakchunk99-arabic_P.pak` sha 2ce95c73…, installed with the new `SWAP_TO_BUILD2.bat`; `technical\BUILD2_CHECKLIST.md`.
- 100 % text inventory: `tools\text_coverage.py` → `technical\TEXT_COVERAGE.md` (99.2 % of visible words are locres text, all in `translation\`; 0 USM subtitle streams, 0 static movie text; images/videos ≈ 958 words).
- Master script: `tools\make_script.py` → `review\script\` (story order from the Theater table, speaker codes; TIPS pages), run by `tools\refresh.bat`.

## BUILD-1 (2026-10-09)
- Line breaking (SHAPER_SPEC §7): `shaper.wrap()` + `meter()`; field widths per namespace in `technical\FIELD_WIDTHS.tsv` (game help, Gummiphone, loading posts, item/ability descriptions); 482 rows broken.
- Conv hoist: whole-row `<conv(..)>` pair kept, inside shaped; 12 tutorial control lists translated; adjacent icons kept in order (one atom).
- Film titles: Frozen = ملكة الثلج, Toy Story = حكاية لعبة (13 rows, glossary approved); Tangled = متشابك pending supervisor check.
- Full build `tools\build_build1.py`: all 6,998 translated rows, 6,967 locres entries changed, TresFont 4 classes; `pakchunk99-arabic_P.pak` (sha 0f27502d…) installed with `SWAP_TO_BUILD1.bat`; `state\INSTALLED.tsv` + installed column in STATS.
- `technical\BUILD1_CHECKLIST.md` (Arabic, 6 places).

## TRANS-3 (2026-10-09)
- Arabic comma `،` rule (210 rows / 227 commas), RULES.md and glossary rule updated; tools\comma_fix.py.
- tutorials 601/614 and journal 615/628 translated; 12 conv-group rows skipped; 52 proposed glossary terms.
- Screenshot log: 00723 verified; 13772 back to translated. Project total 40.6 %.

## TEST50 — 2026-10-09
- SWAP-1b: tools/make_swap_scripts.py had a CR and a backspace byte in the "game running" / "hash mismatch" message paths (messages never shown); paths now built with chr(92); SWAP_TO_TEST50.bat added; tested on a temp folder (4 cases).
- tools/shaper.py: full SHAPER_SPEC §2-6 (style tags as per-character state, conv/icon/{n}/plural atoms, <br>/<pb>/newline lines, UAX #9 W1-W7 N1-N2 I L1 L2 L4, ، ؟); unshape() round trip; tools/test_shaper.py (U1-U12, T1-T22, 30 real rows, all translated rows) in refresh.bat.
- tools/font_census.py: font class / size / letterSpacing of every movie text field; TresFont Arabic set now also in $jimakuNE and $JimakuJP (tools/build_test50.py).
- Title screenshot logged; 8 title rows verified; F1 scale locked; 9 rows translated (6 opening subtitles, 3 Game Help rows; ، ؟ in 4).
- out/builds/TEST50/pakchunk99-test50_P.pak (50 test rows + 34 title rows) built, verified, installed; technical/TEST50_CHECKLIST.md; docs/rounds/TEST50.md (round prompts are saved in docs/rounds/).

## SWAP-1 — 2026-10-09
- SWAP_TO_F1.bat, SWAP_TO_F2.bat, REMOVE_ARABIC.bat (generated by tools/make_swap_scripts.py, messages in tools/swap_msgs/): game-running check, delete only pakchunk99-*_P.pak in ~mods, copy + SHA256 verify, Arabic/English result, admin only on permission failure, log to state/SWAP_LOG.tsv.
- review/corrections/trans2b.tsv (44 rows): Resistance with element nouns, Donald spells, 14239 restored.
- translation/glossary.tsv: 39 proposed terms approved; 10 new approved rows (6 "X Resistance", 4 "Donald X"); Surge note about 14239.

## TRANS-2 — 2026-10-08
- tools/validate.py: LATIN = ERR when a Latin/Greek/Roman token in AR is missing from the row's own EN (no allowed_latin.txt); tests extended; RULES.md, glossary rules (make_glossary.py) and PROJECT_MAP §4 updated.
- translation/menus_ui: re-pass (181 rows net restored to Latin policy, URL/legal rows translated) + supervisor fixes (26 + 1 rows); review/corrections/trans2*.tsv applied and logged.
- translation/glossary.tsv: supervisor decisions (Flan, Surge, Standard Mode, Teeny Ship α/β, Musical, Grind, Heartless family, Stock/Warp second forms), TRANS-1 proposals approved, AP and CDA rows dropped, 39 new `proposed` terms.
- translation/items_abilities: all 2,334 rows handled (2,160 translated, 174 skipped, 0 remaining); tools/trans_page.py (--cat=, cross-category translation memory), tools/gloss_hits.py, tools/trans2_report.py.

## TRANS-1 — 2026-10-08
- translation/menus_ui/*.tsv: all 3,849 rows handled — 3,567 translated (draft), 248 skipped with `skip:` note (empty, icon/arg-only, numbers, native script, URL, ordinal suffix), 0 remaining; 25 rows carry `unsure:` notes.
- translation/glossary.tsv: 17 pending conflicts closed, 10 KH2-only rows (`kh2-only`), Musical + Grind pending, 73 coined terms `proposed`; GLOSSARY_CONFLICTS.md §4 rewritten.
- tools: validate.py (GLOSS accepts any approved form of one EN term, a longer term covers a shorter one, plural `|plural(` brackets, header typo), make_glossary.py (`kh2-only`), trans_page.py / setrow.py / gloss3_apply.py (TRANS-1 helpers), tests extended.

## GLOSS-2 — 2026-10-08
- translation/glossary.tsv: user and supervisor decisions applied (Munny, Organization XIII, LV, Olympus, Piglet, Finkelstein, Equip, Sulley, Shotlock, Cure, Neighborhood, Moogle); 212 KH3-new + 16 Re Mind proposals approved; retired forms removed (3 rows dropped); 41 KH2 rows still pending.
- allowed_latin.txt: XIII; glossary rules (make_glossary.py, review/RULES.md) updated; review/corrections/gloss2.tsv (0 rows: no translated row used a retired form).
- GLOSSARY_CONFLICTS.md: resolved items marked, history and the 17 still-pending conflicts listed; GLOSSARY_PROPOSALS.md now empty.

## GLOSS-1 — 2026-10-08
- KH2 glossary restored as translation/kh2_glossary.md (reference); translation/glossary.md restored from git, then regenerated.
- translation/glossary.tsv = source of truth (1,006 KH2 entries + 228 KH3-new/Re Mind proposals); tools/import_kh2_glossary.py, tools/make_glossary.py; GLOSSARY_CONFLICTS.md, GLOSSARY_PROPOSALS.md.
- KH2-only rules documented (glossary.md, review/RULES.md); validator WARN GLOSS + tests; title screen: CONFIG = الضبط, Kingdom Hearts = كينغدوم هارتس.
- Screenshot policy: screenshots sent in the supervisor chat, logged with file = chat.

## ARABIC-TEST-2 — 2026-10-08
- Join fix in TresFont: Arabic initial/medial forms extended 18 units for the menu field's letterSpacing 2; Arabic also in $KH2Menu.
- Title screen + GAME SETTINGS/Confirm/Cancel translated (34 rows, test values); test paks F1/F2 (+15 % glyphs), F1 installed.
- Review pages escape Markdown characters; PROJECT_MAP.md (entry point) + tools/update_map.py; docs/SUPERVISOR.md.

## ORG-1 — 2026-10-08
- Project structure, git (local only).
- translation/<category>/<file>.tsv split from en_source.tsv (17,222 rows, AR empty); tools/merge_translation.py (byte-identical check).
- tools/validate.py + tests, tools/make_review.py (offline HTML review), tools/stats.py, tools/secret_check.py, tools/refresh.bat.
