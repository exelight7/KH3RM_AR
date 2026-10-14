`# PROJECT_MAP — KH3 Arabic (start here)
`
`Single entry point for any new AI session or person. Sections ending in "(auto)" are rewritten by `tools\update_map.py` (run by `tools\refresh.bat`); all other sections are edited by hand. **Every round must update sections 3, 4 and 8 before stopping.**
`
`## 1. What the project is
`
`Arabic (RTL) localization of KINGDOM HEARTS III + Re Mind (Steam, UE 4.17, Scaleform UI) on PC.
`Delivered only as an added mod pak in `Content\Paks\~mods\` (rebuilt `en` .locres + TresFont with Segoe UI Arabic); original game files are never changed.
`Text is pre-shaped (presentation forms) and stored in visual order, because Scaleform does no Arabic shaping or bidi.
`
`## 2. Roles and rules
`
`Full supervisor instructions: [docs/SUPERVISOR.md](docs/SUPERVISOR.md). Key rules:
`- **User / supervisor:** gives round instructions and approvals, runs the game, takes screenshots, decides glossary and distribution.
`- **Executor (Claude Code):** writes only in `C:\filessss\mewo\kh3fm-arabic\`; never modifies original game files; never runs the game; never deletes `extracted\` or `out\builds\`; no uploads, git local only.
`- Font = **Segoe UI Regular** (`C:\Windows\Fonts\segoeui.ttf`), never Noto, never Plex.
`- Install into `~mods` only with explicit approval; **only one pak of ours in `~mods` at any time**; record SHA256 before/after.
`- Output: details in `state\LAST_REPORT.md` (overwritten each round, first line `round: <NAME>`); 3 lines per task appended to `state\PROGRESS.md`; terminal reply = one line "...".
`- Stop and ask only if blocked 3 times or evidence conflicts.
`- Review reports remain Markdown; user-approved Graphify map HTML/SVG is the exception (2026-10-13). Every round ends with `tools\refresh.bat` and `tools\secret_check.py` (no key, no game binaries in git).
`
`## 3. Current phase, last round, next step

- **BATCH-234 (2026-10-14, built + installed + PUBLISHED as pre-release 0.9.2):** glyph scan `tools\batch2_glyphs.py` -> `review\BATCH2_GLYPHS.md` (all Arabic of 16,415 rows in all 4 TresFont classes; U+2015 missing in $KH2Menu -> 2 rows fixed to U+2014; image strings all in segoeui.ttf; no stray Latin, no presentation forms in source); evidence decisions `review\BATCH3_DECISIONS.md` (77 ids: 12 changed, 65 kept); corrections via `tools\make_batch_corrections.py` (validate check() gate). **BUILD-12** (`tools\build_build12.py`) sha 2cdb5b7b7ee79f5432f488aa86f1a2cf724eaf6983c0077f797dd831e62795cd, 4,890,318 B: 73 files PASS, round trip 16,391 exact + 24 same-visual + 0 fail, overflow = the same 15, diff vs BUILD-11 = exactly the 14 corrected ids (asserted). **IMAGES-MASS5** (`tools\images_enlarge.py` + `texture_text.py mass`) sha d5b39c12c25f34108b97d9d8c6056374800bcd6a9727bb26f82a01941a0bff21, 41,494,619 B: 137 of 522 under-the-bar MASS3 boxes enlarged (all now READABLE), 385 remain, 214 textures 0 FAIL, 428 files list / hash-list / unpack + uexp re-parse PASS, 398 files byte-identical to MASS4. Air gauge unchanged (already the I0013 word). Both installed by swap scripts (sha = pins, both `--installed` PASS). Installer 0.9.2 (37/37 selftest, single + folder), release https://github.com/exelight7/KH3RM_AR/releases/tag/0.9.2 (6 assets). Report: `state\LAST_REPORT.md`.
- **Next step:** user checks in game the screens listed in `state\LAST_REPORT.md` (quit box, Premium Menu labels, the 14 changed rows); then the remaining ROADMAP rounds (1.0.0 still locked).
- **BUGFIX-1 (2026-10-14, built + installed, NOT published):** native Windows quit box shows Arabic reversed (Windows does its own bidi/joining on our pre-shaped text; hypothesis, to be confirmed in game). New hook in `tools\build_build11.py` (BUILD-10 pipeline + ids of `translation\raw_logical_ids.tsv` emitted as raw logical Arabic: base letters, no reversal, no wrap); ids 15656 / 15657 (kh3_settings.top dialog_0010 / dialog_0020, "...") + 15999 (kh3_system.general home_0010, game name). Yes / No (kh3_system.general choice_0001 / 0002, kh3_menu.title choice_0008 / 0009) are used by Scaleform movies (MenuRemy, HundredGame, Shop, Title, InitialSetting) and were NOT changed. **BUILD-11** sha 8aa9b0e816e61a303f8b1f36e03fa90caf5c2d0a4ed90e1b7bd0a812ffeb7f91, 4,890,296 B; 73 files PASS, round trip 16,391 exact + 24 same-visual + 0 fail, overflow = the same 15 rows, vs BUILD-10 exactly the 3 raw ids differ; installed via `SWAP_TO_BUILD11.bat` (sha = pin, images pak e8ebf70a... unchanged, `--installed` 16,415 of 16,415). Water review: `review\BUGFIX1_WATER.md` (80 rows with a water word, 7 flagged, 0 mistranslations; I0013 is الهواء in the source but the installed texture still shows the old label). Report: `state\LAST_REPORT.md`.
- **UPLOAD-FOLDER-ZIP (2026-10-14, uploaded):** folder zip (sha256 df26c6b4...39552d, 89,387,647 B, VirusTotal 0/67) added as 6th asset to existing pre-release 0.9.1 (https://github.com/exelight7/KH3RM_AR/releases/tag/0.9.1, still pre-release); notes edited (Arabic paragraph appended); SHA256SUMS.txt and the other five assets untouched.
`
`- **AV-FALSEPOS (2026-10-14, built locally, NOT published, NOT uploaded):** non-single-file, uncompressed, self-contained win-x64 installer folder `out
`elease
0.9.1-folder\` (215 files, exe + dlls + embedded paks; same Installer.csproj, only `-p:PublishSingleFile=false -p:EnableCompressionInSingleFile=false`); `--selftest` ALL PASS; zip `out
`elease\KH3RM_AR_Setup_v0.9.1_windows-x64-folder.zip` 89,387,647 B sha256 df26c6b459963a1f10adb2e174b9e5297b56bcc0c4578943f7c21d199539552d; folder exe 211,456 B sha256 eeca637b73f7f82bb70ba0f5712dcf9fa412e93ffede0300c3cdd25f5836b1ee. Existing v0.9.1 release assets untouched. `docs\INSTALL_MANUAL.md` (Arabic manual install/verify/remove) added, not linked from README. User scans the zip on VirusTotal and decides.
`- **RELEASE-091 (2026-10-14, built + installed + PUBLISHED):** public main 5c5ad06 (45 files) + GitHub pre-release **0.9.1** https://github.com/exelight7/KH3RM_AR/releases/tag/0.9.1 (tag = 5c5ad06; 5 assets, sizes + sha256 digests = SHA256SUMS, isPrerelease true: installer exe + Linux tar.gz + BUILD-10 text pak 89e00ead... + IMAGES-MASS4 images pak + SHA256SUMS). **IMAGES-MASS4** (`texture_text.py mass`, sha e8ebf70a..., 41,492,782 B, 214 textures, 1,356 boxes, checks 0 FAIL, 428 files list / hash-list / unpack + uexp re-parse PASS; 423 MASS3 files byte-identical, 1 changed on purpose = HelpItem50600 because row 10694 was reworded in BUILD-9, 4 new): the 23 keep items retried: 17 = NO-TEXT by pixel inspection (HudRight03 heart icon, 15 camera / button pictures, the keyboard key-name picture); HudKairi_01 repainted (name rebuilt on a new plate grown from the Arabic text + 4 plate rows into the cleaned base bar, right edge feathered into the ornament, blurred flash regenerated from the new emblem: glow model fit rms 0.047, core 0.111); HelpItem50300 partly repainted (row 10693 at 18 px, contrast 244, 5 / 5 components); 4 gummi tutorial pictures stay English (two HUD words at 5-6 px: contrast 134-136 < 192, components broken). New readability gate (`texture_text.py`: contrast >= 192 + continuity vs a 64 px reference) for every texture new against MASS3; trial file `technical\images_rects_trial.tsv` (`texture_text.py trial`). **Figures:** repainted N = 213, no translatable text M = 17, unreadable K = 4 -> 213 of 217 textures with text (98.2 %); plan 213 / 234 (91.0 %). Installed via `SWAP_TO_IMAGES_MASS4.bat` (sha = pin; text pak still BUILD-10, `--installed` both PASS). Installer 0.9.1 (BUILD-10 + IMAGES-MASS4, 37/37 selftest PASS). README: 5 value / link lines only (BUILD name now the `{{BUILD}}` placeholder). Report: `state\LAST_REPORT.md`.
`- **Next step:** user checks in game the Kairi HUD name and the 42 rows changed since 0.9.0, and decides about the readability finding below (section 8); then the rounds of `docs\ROADMAP_TO_1.0.0.md` (1.0.0 still locked).
`- **BUILD-10 (2026-10-14, built + installed, NOT published):** text pak `tools\build_build10.py` (BUILD-9 pipeline unchanged), sha 89e00ead0a83e5d1cb07d257d98530541da447a5849c42f84ba9759dd4c7beea, 4,890,202 B; 73 files PASS (list = hash-list = unpack), round trip 16,391 exact + 24 same-visual + 0 fail, validator 98 flagged / 0 errors, overflow = the same 15 rows (new none, gone none); vs BUILD-9 20 entries differ = the 19 GPT Q3 ids + 17169 (Q4 fix); installed sha = pin, images pak d8d13948... unchanged, `--installed` 16,415 of 16,415 shaped rows found. Corrections: `reviewrrectionsbuild10_round.tsv` (`tools\make_build10_corrections.py`). Report: `state\LAST_REPORT.md`.
`- **REVIEW5-Q4 (2026-10-14, complete locally, nothing built / installed / published):** review of quarter Q4 (ids 12884-17222, 4,103 rows read in 14 pages of 300: level/map/menu/Theater/Premium Menu/minigame texts, Gummiphone story + reports + glossary + characters + enemy notes, settings, system, commands, abilities, game-over hints, tutorials); 1 fix applied (17169: the `<color(strong)>` highlight wrapped the verb as well as the term, now only the term like 17196 / 17212 / 17217), 5 doubts kept in `review\REVIEW5_Q4_QUESTIONS.md` (13402, 14360, 14373, 15494-15497, 14763); protected rows (Codex 137, BUILD-9 13, BUILD9_proposed, DECISIONS_NEEDED, 64 context items, Tangled) not touched; repeated-EN consistency pass done (only Set / Strength / pts pairs differ, see log); refresh 0 ERR (validator 98 flagged / 0 errors, unchanged), secret_check PASS. The fix waits for the next build. Report: `state\LAST_REPORT.md`; log `review\REVIEW5_Q4_LOG.md`.
`- **BUILD-9 (2026-10-14, built + installed, NOT published):** text pak `tools\build_build9.py` (BUILD-8 pipeline unchanged), sha 23ae437a..., 4,890,263 B; 73 files PASS (list = hash-list = unpack), round trip 16,391 exact + 24 same-visual + 0 fail, validator 98 flagged / 0 errors, overflow = the same 15 rows (new none). Vs BUILD-8: 22 entries = the 9 REVIEW5-Q1 fixes + 13 new corrections `review\corrections\build9_round.tsv` (5 DECIDE-19 B rows incl. 10847 in the plural form "5 أحرف", + GPT Q2 04538, 04915, 06712, 07464, 07515, 07903, 07339 «الفناء», 08531 «قصر الجليد»; glossary-checked). Installed via `SWAP_TO_BUILD9.bat` (sha = pin; images pak still d8d13948...). Not applied: GPT 06084, 05228, the 21 GPT Q2 QUESTIONS. Report: `state\LAST_REPORT.md`.
`- **REVIEW5-Q1 (2026-10-13, complete locally, FAQ line 6 published):** review of quarter Q1 (ids 00001-04248, 4,104 rows read in 14 pages, event dialogue / camp / config / character names); 9 fixes applied (00114 addressee number, 00828 meaning, 00874 + 02487 + 02534 repeated-line wording, 00979 addressee number, 02373 meaning, 02882 dropped word, 04043 addressee gender), 3 doubts kept as questions; refresh 0 ERR (validator 98 flagged / 0 errors, unchanged), secret_check PASS. No build, no install, no release: fixes wait for BUILD-9. Report: `state\LAST_REPORT.md`; log `review\REVIEW5_Q1_LOG.md`.
`- **PUBLIC-CLEANUP (2026-10-13, PUBLISHED):** `make_public.py` no longer copies root `*.bat`; 18 .bat git-rm'd from public main (b5b5d99); `docs/TESTER_GUIDE.md` removal line now points to the installer / manual pak delete. README unchanged; release 0.9.0 still 5 assets, pre-release. Report: `state\LAST_REPORT.md`.
`- **PUBLISH-090 (2026-10-13, PUBLISHED):** README lines 49 / 59 accepted; `tools\publish.bat` pushed public main (24b0334); GitHub pre-release 0.9.0 with 5 assets (sizes + sha256 digests match SHA256SUMS), isPrerelease true: https://github.com/exelight7/KH3RM_AR/releases/tag/0.9.0. Notes say SpecialShip_02 / ps4 HelpItem30402 not yet seen in game and images pack is optional. Report: `state\LAST_REPORT.md`.
`- **RELEASE-090 (2026-10-13, built + installed, published by PUBLISH-090):** **IMAGES-MASS3** images pak (`texture_text.py mass` -> `out\builds\IMAGES-MASS3\`, sha d8d13948..., 41,083,305 B, 212 textures, 0 FAIL, 424 files PASS; the 420 MASS2 files byte-identical): ps4 `HelpItem30402` control panel + `SpecialShip_02` LV / MAX / NEXT / OBJECTIVE (sprite regions of the movie, existing rows 13279 / 15771 / 13280 / 13294) repainted; **211 / 234 = 90.2 % = 100 % of the repaintable textures**, the 23 others KEEP ENGLISH with a written reason in `technical\IMAGES_STILL_ENGLISH.tsv`. Installed via `SWAP_TO_IMAGES_MASS3.bat` (sha = pin; text pak still BUILD-8 45f043de...). Installer 0.9.0 rebuilt with IMAGES-MASS3 (37/37 selftest PASS); `out\release\v0.9.0\` ready (5 assets + Arabic notes). **Publishing stopped:** the generated README changes 2 wording lines (49, 59; from the OPUS-090 D template edit) besides value lines, so no push and no release. Plan: `docs\ROADMAP_TO_1.0.0.md`. Report: `state\LAST_REPORT.md`.
`- **Next step:** the rounds of `docs\ROADMAP_TO_1.0.0.md` (0.9.0 is out; no 1.0.0 tag yet).
`
`- **INSTALL-8 (2026-10-13, installed, NOT published):** `SWAP_TO_BUILD8.bat` + `SWAP_TO_IMAGES_MASS2.bat` run from cmd; `~mods` now holds BUILD-8 (`pakchunk99`, sha 45f043de..., 4,890,167 B) + IMAGES-MASS2 (`pakchunk98`, sha bc546502..., 40,442,423 B), both SHA256 equal to the pins; `state\INSTALLED.tsv` / STATS updated, 2 new rows in `state\SWAP_LOG.tsv`. Checklist rewritten to 5 yes/no lines: `technical\IMAGES_MASS2_CHECKLIST.md`. Next: user plays and reports only problems; then publish / 0.9.0 on the supervisor's word.
`- **DECIDE-19 (2026-10-13, documents only):** executor choices for the 19 items of `review\DECISIONS_NEEDED.md` -> `review\DECISIONS_ANSWERED.md` (A 5, B 4, LEAVE 10) and `review\proposed\BUILD9_proposed.tsv` (5 rows: 10847, 14238, 10694 + companion 15915, 09582; old_AR = current AR for all, validator logic 0 failures). Proposed only: nothing under `review\corrections`, no translation TSV, glossary, build, install or publish change. Report: `state\LAST_REPORT.md`.
`- **Next step (DECIDE-19):** supervisor reads `review\DECISIONS_ANSWERED.md`, overrules lines if wanted, and says which rows of `BUILD9_proposed.tsv` to move to `review\corrections\` for the next build. The OPUS-090 install steps below are unchanged.
`
`- **OPUS-090 (2026-10-13, built, NOT installed, NOT published):** **BUILD-8** text pak (`tools\build_build8.py`, BUILD-7 pipeline unchanged; sha 45f043de..., 4,890,167 B; exactly the 136 CODEX-REVIEW4 text corrections differ from BUILD-7, `out\builds\BUILD-8\diff_vs_build7.tsv`; 73 files PASS, round trip 16,391 exact + 24 same-visual + 0 fail, overflow = the same 15 rows) + `SWAP_TO_BUILD8.bat`. **IMAGES-MASS2** images pak (`texture_text.py mass` -> `out\builds\IMAGES-MASS2\`, sha bc546502..., 40,442,423 B, 210 textures, 1,344 boxes, 420 files PASS): the 16 minigame HUD textures (104 boxes, sprite rects read from the movies' bitmap fills, strings I0019-I0042) + I0013 «الهواء» re-render; the other 192 textures are byte-identical to IMAGES-MASS; `SWAP_TO_IMAGES_MASS2.bat`, checklist `technical\IMAGES_MASS2_CHECKLIST.md`. Images repainted 209 / 234 = 89.3 %. **Installer 0.9.0** (Avalonia): both paks embedded, optional images checkbox (default off), per-pak SHA256 install/remove, 37/37 `--selftest` PASS; Windows + Linux built to `out\release\v0.9.0\` (Linux not run on Linux; no real install/remove run). Installed in `~mods` is still BUILD-7 + IMAGES-MASS. Report: `state\LAST_REPORT.md`.
`- **Next step (OPUS-090):** the user installs BUILD-8 (`SWAP_TO_BUILD8.bat`) and, if wanted, IMAGES-MASS2 (`SWAP_TO_IMAGES_MASS2.bat`) from cmd, checks `technical\IMAGES_MASS2_CHECKLIST.md`, confirms -> `python -I tools\build_build8.py --installed` (updates `state\INSTALLED.tsv`) -> `tools\publish.bat` -> `gh release create 0.9.0 --prerelease` (exact commands in `state\LAST_REPORT.md`).
`
`- **README-POLISH (2026-10-13):** compact visual README, direct downloads, removed thanks/disclaimers, separate Graphify footer; documentation only.
`
`- **INSTALLER-CROSSPLATFORM (2026-10-13):** installer 0.8.3 now uses Avalonia for Windows/Linux, same BUILD-7 payload; credits only in GitHub. Windows UI previewed; Linux cross-published but not run on Linux. Report: docs/rounds/INSTALLER-CROSSPLATFORM.md. Source translation corrections still await a later game build.
`
`- **CODEX-REVIEW4-4 (2026-10-13, complete locally):** 4305 rows read; 19 source corrections applied, 24 contextual questions preserved; checks PASS / 0 ERR. Report: docs/rounds/CODEX-REVIEW4-4.md; private audit: review/codex_full_review/batch_4/. Completed checkpoints: 4/4. Source corrections await a later build and visual verification.
`
`- **CODEX-REVIEW4-3 (2026-10-13, complete locally):** 4305 rows read; 32 source corrections applied, 14 contextual questions preserved; checks PASS / 0 ERR. Report: docs/rounds/CODEX-REVIEW4-3.md; private audit: review/codex_full_review/batch_3/. Completed checkpoints: 3/4. Source corrections await a later build and visual verification.
`
`- **CODEX-REVIEW4-2 (2026-10-13, complete locally):** 4306 rows read; 49 source corrections applied, 12 contextual questions preserved; checks PASS / 0 ERR. Report: docs/rounds/CODEX-REVIEW4-2.md; private audit: review/codex_full_review/batch_2/. Completed checkpoints: 2/4. Source corrections await a later build and visual verification.
`
`- **CODEX-REVIEW4-1 (2026-10-13, complete locally):** 4324 rows read; 37 source corrections applied, 14 contextual questions preserved; checks PASS / 0 ERR. Report: docs/rounds/CODEX-REVIEW4-1.md; private audit: review/codex_full_review/batch_1/. Completed checkpoints: 1/4. Source corrections await a later build and visual verification.
`
`- **CODEX-REVIEW4 (2026-10-13, active):** full linguistic review of 17,222 rows plus 18 image strings in four batches. Immutable input manifest and per-row ledgers: `review/codex_full_review/`; public Arabic reports: `docs/rounds/CODEX-REVIEW4-N.md`. Each completed batch is applied through corrections, validated, documented and published. BUILD-7 remains the installed build until separately rebuilt/tested.
`- **GRAPHIFY-ADOPT (2026-10-13):** graph-first navigation adopted in `AGENTS.md` and `CLAUDE.md`; local private graph in `graphify-out`; safe public graph in `docs/graph`, linked in a separate README footer. Details: `docs/GRAPHIFY.md`.
`
`- **README-AR (2026-10-11):** public README rewritten as Arabic only (template `tools\public_templates\README.md`, generated by `make_public.py`); `docs\TESTER_GUIDE.md`, `FAQ.md`, issue template and `LICENSE_TODO.md` (generated) converted to Arabic only; release 0.8.3 notes replaced by an Arabic text (pre-release kept, no asset touched); README link now points at 0.8.3 and the installer file `KH3RM_AR_Setup_v0.8.2.exe`. Other public files (PROJECT_MAP, CHANGELOG, PROGRESS, rounds, technical docs, RULES, SUPERVISOR, INDEX) are still English prose, listed in `state\LAST_REPORT.md`.
`- **RELEASE-083b (2026-10-11):** release 0.8.3 got 3 assets (installer v0.8.2, BUILD-7 pak, SHA256SUMS.txt; all SHA256 verified, unmodified); images pack not attached.
`- **RELEASE-083 (2026-10-11):** public sync + pre-release **0.8.3** (docs and tools only, no assets; text pak unchanged = BUILD-7 f9e23f37...): https://github.com/exelight7/KH3RM_AR/releases/tag/0.8.3 .
`- **Phase:** BUILD-7 installed and released as **0.8.2** (2026-10-10): `pakchunk99-arabic_P.pak` sha f9e23f37..., 4,889,918 B, in `~mods` via `SWAP_TO_BUILD7.bat` (the IMAGES-MASS images pak stays beside it). 95.3 % of rows installed (16,415 / 17,222); the 807 `todo` rows carry a `skip:` note. Verified 0.6 %.
`- **Round before (SYNC-BUILD7, 2026-10-10):** all 6 cloud PRs merged; `tools\sync_cloud.bat` applied the cloud second pass (69 files; 182 rows really changed: tutorials 54, Re Mind 31, items/abilities 27, menus 26, journal 26, subtitles 16, dialogue 2; 16,106 rows carry the note "..."); glossary aligned (Diving Strike, Powerwild, Frost Serpent, Monsters Inc); BUILD-7 = the BUILD-6 pipeline unchanged (`tools\build_build7.py`), 73 files SHA256 PASS, round trip 16,391 exact + 24 same-visual + 0 fail, 15 overflow rows as in BUILD-6 (none from the changed Risk label); installer 0.8.2 (22/22 self tests PASS); release **0.8.2** (pre-release, 5 assets verified): https://github.com/exelight7/KH3RM_AR/releases/tag/0.8.2 . Details: `state\LAST_REPORT.md`.
`- **FINISH-TRANS (2026-10-11):** 807 skipped rows audited (`review/SKIP_AUDIT.tsv`), 24 suspects (all benign notes), 11 AR==EN acronyms (`review/SAME_AS_EN.tsv`); translatable coverage 100.0 %. No translation edits.
`- **Last round (IMAGES-MASS, 2026-10-10, installed, NOT released):** images pak `out\builds\IMAGES-MASS\pakchunk98-arabic-images_P.pak` (sha 233ef228..., 39,154,907 B, 194 textures, 1,240 text boxes, 388 files SHA256 PASS) sits in `~mods` NEXT TO the BUILD-7 text pak (`SWAP_TO_IMAGES_MASS.bat`; `REMOVE_IMAGES.bat` deletes only the images pak). The images pak is **optional, separate and removable**; it replaced the 3-texture pilot (pilot textures re-rendered with the new stroke rule). **Images repainted: 193 of the 234-texture repaint plan = 82.5 %** (+ SlideShowTx, read full size): command headers 16 + HUD/menus 5, tutorial pictures 128 of 150, area banners 25 of 25, LSI 9 of 9, shared HUD 11 of 14. Still English with the reason: `technical\IMAGES_STILL_ENGLISH.tsv` (16 minigame HUDs = next step, styled logos, brands, unreadable or text-free pictures). New image strings (no translation row): `translation\images_strings.tsv` (I0001-I0018).
`- **What the user must screenshot:** the 6 places in `technical\IMAGES_MASS_CHECKLIST.md` (command header, shop tutorial picture, area banner, key help, LSI taxi game, battle HUD/autosave) + `technical\BUILD7_CHECKLIST.md` (4 places) + `technical\BUILD6_CHECKLIST.md` (6 places).
`- **Cloud review prep (CLOUD-PREP, 2026-10-10):** private repo `exelight7/KH3RM_AR_work` created and filled from `cloud_repo\` (`tools\make_cloud.py`, `cloud_check.py`, `cloud_secret_check.py`, `sync_cloud.bat`, GitHub Action `check`); 4 ranges of the 32 script pages in `review\cloud\TASKS.md`; details `docs\CLOUD_WORKFLOW.md`, `state\LAST_REPORT.md`. Public repo not touched.
`- **LIGHT-1 (2026-10-10):** `images_strings.tsv` validated (0 flags), "images"..."5 characters"..."id A" / "id B"); `docs\INSTALLER_0.9.0_PLAN.md` (images-pack checkbox, documentation only). No translation, build or publish change.
`- **TESTER-KIT (2026-10-10):** `tools\find_text.py`, `tools\apply_feedback.py` (+ tests, in refresh.bat), `docs\TESTER_GUIDE.md`, `FAQ.md`, issue template, `state\FEEDBACK_TEMPLATE.tsv`; public docs added to make_public. **Road map:** 0.9.0 images pack after the user's verdict; 0.9.1 the 16 minigame HUD textures; 0.9.2 docs and tester kit; 0.9.3-0.9.8 fixes from user tests; 0.9.9 release candidate for the user's full playthrough; 1.0.0 LOCKED until the user says go.
`- **Next step:** user screenshots (IMAGES-MASS checklist, BUILD-7 checklist) and the user's verdict on the images pak; 0.9.0 (with the images pak) waits for that verdict; then the 16 minigame HUD textures (resume point in `state\PROGRESS.md`) and the 47 styled logos -> user screenshots -> 1.0.0 (still LOCKED, see section 4).
`- **Public repository:** https://github.com/exelight7/KH3RM_AR (README is Arabic only; Download points at 0.8.3; roadmap 0.9.0 images pack / 0.9.1 minigame images / 0.9.2-0.9.8 test fixes / 0.9.9 RC / 1.0.0 only after the author's full playthrough). See section 10.
`- **Releases:** latest public = 0.8.3 (docs/tools, pak = 0.8.2); 0.8.0 (BUILD-5, RELEASE-080), 0.8.1 (BUILD-6, FINAL-1) and 0.8.2 (BUILD-7, SYNC-BUILD7), all pre-release, tags without "v".
`
`## 4. Decisions already made

- 2026-10-14 BATCH-234 (executor, within the user's round prompt): a missing glyph is checked per character of the shipped (shaped) locres text against each of the 4 TresFont classes; a non-Arabic character the row's EN also uses counts as unchanged game behaviour. Open questions are decided by evidence only (glossary lock, neighbouring rows / script order for addressee, existing row wording for puns); a fix = the current AR with one fragment replaced, gated by validate check() (no ERR, no new flag). An earlier image box may be enlarged only if the larger size fits the box, passes the readability bar and covers no artwork pixel outside the old text that the shipped size did not cover; the 0.9.x folder installer zip is a standard sixth release asset (hash in the notes, not in SHA256SUMS.txt). Swap scripts from PowerShell need the redirect quoted for cmd (`cmd /c '.\SWAP_TO_X.bat <NUL'`).
- 2026-10-14 UPLOAD-FOLDER-ZIP (user-approved): folder zip shipped as an extra asset of 0.9.1; SHA256SUMS.txt left as is, zip hash stated in the notes.
`
`- 2026-10-14 AV-FALSEPOS (executor, within the user's round prompt): antivirus false-positive mitigation variant = self-contained folder build (no single-file, no compression); built only locally, not attached to any release until the user decides after the VirusTotal scan.
`- 2026-10-14 RELEASE-091 (executor, within the user's round prompt): a texture is NO-TEXT when pixel inspection finds no words (button glyphs, counters, icons, key names); NO-TEXT textures stay in the 234 plan but are reported apart (M). Image readability = measured at the real size with the shipping renderer: 75th-percentile stroke coverage >= 192 and 8-connected components (coverage >= 128) between ref - k and ref of a 64 px rendering (k = letters with 2-3 dots; below 24 px only); every texture new against the previous images build must pass it, earlier byte-identical textures are only reported. A texture may ship partly repainted when only some of its words pass (HelpItem50300). Earlier images files must stay byte-identical except textures that draw a row reworded since (`REWORDED` in `texture_text.py`, now 10694). The README's build name is a template placeholder.
`- 2026-10-14 REVIEW5-Q4 (executor, within the user's round prompt): split owners updated to Q1 = Claude, Q2 = GPT, Q3 = GPT, Q4 = Claude (`review\split\MANIFEST.md`); Q4 rows are reviewed with the REVIEW5-Q1 checks and only unambiguous defects are corrected. A plural / singular addressee doubt, a gender doubt or a width-dependent wording (pts plural, Popcat group) goes to QUESTIONS and is not decided here; tag content scope: a highlight tag wraps the term that EN highlights, not the surrounding verb (17169).
`- 2026-10-13 REVIEW5-Q1 (executor, within the user's round prompt): the 16,415 translated / reviewed / verified rows (807 `todo` skip rows and 42 image strings excluded) are split by ascending id into 4 consecutive quarters (4,104 / 4,104 / 4,104 / 4,103; `review\split\Q1_ids.tsv` ... `Q4_ids.tsv`, `MANIFEST.md`); owners: Q1 = Claude, Q2 = GPT, Q3 and Q4 reserved (nobody touches them). An owner opens corrections only for ids of the own quarter; the 137 Codex corrections, the 5 BUILD9_proposed rows, DECISIONS_NEEDED items, the 64 context items and Tangled are never changed by a review (doubts go to `review\REVIEW5_Q1_QUESTIONS.md`). The plural rendering of the 10 identical "wait" rows stays as it is; repeated EN lines in Q1 were harmonised to the majority wording only where nothing but taste differed (rows 00874, 02487, 02534); gender/number variants were left.
`
`- PUBLIC-CLEANUP: root swap/remove .bat scripts stay private only; docs
`ounds and docs\graph left as history.
`- PUBLISH-090: 0.9.0 is a GitHub PRE-RELEASE (not 1.0.0); README lines 49 / 59 wording accepted by the user; publish.bat pushes to exelight7/KH3RM_AR main.
`- 2026-10-13 RELEASE-090 (executor, within the user's round prompt): the image plan is closed at 211 / 234; KEEP ENGLISH = 5-8 px HUD words (5 tutorial pictures), key / button names and glyph-only pictures (16), the heart-only HudRight03, and the styled HudKairi_01 name emblem (a repaint test left hard cut edges: never ship an unclean texture); minigame sprite textures are repainted only inside the sprite regions read from the movie's bitmap fills, the English-language frame decides which words count (SpecialShip_02: LV, MAX, OBJECTIVE; NEXT = default frame, repainted too); the public README may change only through its placeholders, any other line difference stops publishing.
`
`- 2026-10-13 DECIDE-19 (executor, within the user's round prompt; supervisor can overrule): of the 19 DECISIONS_NEEDED items, B for 10847 (the Name Entry screen has kana/kanji/ABC/symbol pages and no Numerals page, so "numerals"..."Remove"..."remove images pack only" button.
`
`- 2026-10-13: user requested a cleaner README without thanks or corporate disclaimers; separate rights files stay unchanged.
`
`- 2026-10-13: user authorized redesigning the current installer for Windows/Linux with the supplied Pinterest image; rights in GitHub, not application UI. Current release 0.8.3; no new game build or installation.
`
`
`CODEX-REVIEW4-4: prior glossary decisions retained; selected corrections applied; unresolved scene/gender/pun choices remain unchanged.
`
`CODEX-REVIEW4-3: prior glossary decisions retained; selected corrections applied; unresolved scene/gender/pun choices remain unchanged.
`
`CODEX-REVIEW4-2: prior glossary decisions retained; selected corrections applied; unresolved scene/gender/pun choices remain unchanged.
`
`CODEX-REVIEW4-1: prior glossary decisions retained; selected corrections applied; unresolved scene/gender/pun choices remain unchanged.
`
`User authorization 2026-10-13: Graphify is adopted for the whole project; HTML/SVG are allowed for its interactive map and README card. Four-batch translation review and sanitized per-batch GitHub reports are authorized. Private source comparisons remain local; no new build installation or release is part of this request.
`
`| date | decision | source |
`|---|---|---|
`| 2026-10-11 | Release 0.8.3 also carries the unchanged v0.8.2 installer, pak and SHA256SUMS.txt (RELEASE-083b); images pack never attached | user, RELEASE-083b |
`| 2026-10-11 | Release 0.8.3 = docs/tools-only pre-release without assets; translation pak stays BUILD-7 (installer/files from 0.8.2) | user, RELEASE-083 |
`| 2026-10-10 | IMAGES-MASS: images pak = optional second pak `pakchunk98-arabic-images_P.pak` beside the text pak, removable alone (`REMOVE_IMAGES.bat`); repaint plan = 234 inventory textures; styled logos, brand wordmarks and keep rows untouched; text >= 24 px gets a 1 px stroke in its own colour, smaller text at 1x without stroke; format/size/mips kept, only changed 4x4 blocks re-encoded; Arabic only from translation rows / `translation\images_strings.tsv`; 0.9.0 waits for the user's verdict | supervisor, docs/rounds/IMAGES-MASS.md |
`| 2026-10-10 | BUILD-5 = the BUILD-4 pipeline unchanged on the reviewed text (no build logic change); the swap script pins the sha of the pak file that is installed | docs/rounds/BUILD-5.md |
`| 2026-10-08 | Font = Segoe UI Regular (weight 400), never Noto Sans Arabic, never IBM Plex | user; RECON_KH3 header |
`| 2026-10-08 | Culture `en` is replaced (our pak overrides `Localization/Game/en/*.locres`); English voice unaffected | PIPE-1, RECON_KH3 §8 |
`| 2026-10-08 | Scaleform pre-shaping: presentation forms U+FE70–FEFC + visual (reversed) order per line; confirmed in-game by ARABIC-TEST-1 variant A | SHAPER_SPEC, ARABIC-TEST-1 screenshot |
`| 2026-10-08 | No HTML outputs; review pages are Markdown (`review\md\`), fixes via `review\corrections\*.tsv` | ORG-2 |
`| 2026-10-08 | Mod method: unencrypted pak v4, Zlib, mount `../../../`, name `pakchunk99-*_P.pak` in `Content\Paks\~mods\`; no `_0_P` moves needed | LOAD-TEST PASS |
`| 2026-10-08 | Join fix lives in the font, not in the movies: Arabic initial/medial forms get a straight 18-unit stroke before the join tip (letterSpacing 2 at 30 pt = 17.07 units) | ARABIC-TEST-2 |
`| 2026-10-08 | Arabic glyphs go into `$sougei` (id 3) and `$KH2Menu` (id 4, GAME SETTINGS header); `$KH2Menu` scale matched to its cap height (×204/174) | ARABIC-TEST-2 |
`| 2026-10-08 | `ReMind` (visible text of `Re<icon(..)>Mind`) allowed as Latin in AR text | ARABIC-TEST-2 |
`| 2026-10-08 | Screenshots are sent in the supervisor chat only (not saved in `screenshots\`); `SCREENSHOT_LOG.tsv` entries use file = `chat` and the supervisor's verdict | user, GLOSS-1 |
`| 2026-10-08 | Glossary source of truth = `translation\glossary.tsv`; `glossary.md` / `GLOSSARY_PROPOSALS.md` are generated; only `approved` terms used in bulk; rule order: correct Arabic → English pronunciation for names → most common usage → shortest; same EN = same AR | user, GLOSS-1 |
`| 2026-10-08 | KH2-only rules not carried over (Latin bans, ya/alef-maqsura, `<X 5E>`, LV→مس, width shortenings, forced transliterations → pending); Arabic `،`/`؟` only after a screenshot proves they render, ASCII `,` `?` until then | user, GLOSS-1 |
`| 2026-10-08 | Kingdom Hearts = كينغدوم هارتس; CONFIG = الضبط; Option stays الخيارات | user, GLOSS-1 |
`| 2026-10-08 | Munny = موني in all forms (Munny Pouch = كيس موني); Organization XIII = منظمة XIII (Latin XIII allowed), the Organization = المنظمة, Real Organization XIII = منظمة XIII الحقيقية; LV / Lv. = مستوى, Next LV = المستوى التالي; Olympus = أوليمبوس (all compounds) | user, GLOSS-2 |
`| 2026-10-08 | Piglet = بيغليت; Finkelstein = فينكلشتاين; Equip = تجهيز; Sulley = سولي; Shotlock = التصويب المثبت; Cure/Cura/Curaga/Curaza = كيور/كيورا/كيوراغا/كيورازا; The Neighborhood = الحي السكني; Moogle/Moogles = same word (موغل / الموغل); magic names follow KH2 style incl. -za tier (فايرازا …) | supervisor, GLOSS-2 |
`| 2026-10-08 | 17 pending glossary conflicts closed: Hollow Bastion = حصن هولو, Destiny Island(s) = جزر المصير, Limit = ليميت, Lucky Lucky = لكي لاكي, Full Bloom = الإزهار, Journal = اليوميات, Postern = البوابة الخلفية, Jump = قفز, Auto = تلقائي, Release = التحرير, Hang On = تمسك, Whirli-Goof = غوفي الدوار; Abilities/Master/Question/Materials keep both forms by context; KH2-constraint rows with 0 KH3 rows = status `kh2-only` | supervisor, TRANS-1 |
`| 2026-10-08 | menus_ui style: clear MSA, short labels, imperative help lines, ASCII `,` `?`, no harakat/tatweel; Latin per the TRANS-2 policy (see below); same EN = same AR; rows empty / icon-only / numbers / native-script stay `todo` with note `skip: <reason>` | supervisor, TRANS-1 |
`| 2026-10-08 | **Latin policy (final, replaces the allowed_latin whitelist):** the game font renders every Latin letter, digit, Roman numeral and Greek letter of the EN text, so any Latin/Roman/Greek token in AR must appear verbatim in the EN of the same row (validator ERR). Keep as in EN: acronyms (HDR LOD DOF FXAA TXAA BGM AP HP MP UFO AR CDA MVP PC PS4 DLC), brands (PlayStation, Epic Games, Re Mind), rank/set letters, single-letter suffixes, sector codes, title numerals (KINGDOM HEARTS Ⅲ, II.9; words stay كينغدوم هارتس), Greek letters, URLs, Latin units like `p`. Exception: Arabic where clearly more natural and short and the EN is a plain word, or where the glossary approves Arabic (EXP = خبرة, LV = مستوى, EZ/PRO Codes) | supervisor, TRANS-2 |
`| 2026-10-08 | TRANS-1 executor choices accepted: Stock count column = المخزون, Warp (fast travel) = انتقال سريع (second approved forms next to the KH2 command Stock = تخزين / Warp = التحول), plural rows use `one`/`other` with "{0} من + noun" | supervisor, TRANS-2 |
`| 2026-10-08 | Glossary TRANS-2: Flan = بودينغ, The Flantastic Seven = البودينغ السبعة الرائعون, Surge = التسارع (الاندفاع is KH2's Dash), Standard Mode = الوضع العادي, Teeny Ship α/β keep the Greek letter, AP stays Latin (row removed), Musical = موسيقي, Grind = طحن, Heartless Hunter/Harrier/Menacer/Destroyer/Obliterator = صائد/مطارد/مهدد/مدمر/ماحق البلا قلب; all other TRANS-1 proposed terms approved | supervisor, TRANS-2 |
`| 2026-10-08 | items_abilities style: weapon/item/magic names from the glossary; descriptions imperative or third person as the EN; "..." and food lines from one template each; amount words slight..incredible = طفيفة صغيرة متوسطة كبيرة هائلة مذهلة; `/G /M /P /S` codes, VGA/SRS/STR codes, `+` suffix kept Latin as in EN | executor, TRANS-2 (to be confirmed) |
`| 2026-10-09 | **Scale locked = F1 (final):** `$sougei` K = 256/2048 (1/8), DY = −5 (baseline of the `$sougei` Latin glyphs); every other class gets the same Arabic-to-cap-height ratio (K = 1/8 × cap/174, DY = its 'H' baseline): `$KH2Menu` K 0.14655 DY 0, `$jimakuNE` K 0.15805 DY 14, `$JimakuJP` K 0.14511 DY 11; join extension +18 units in all classes | `~mods` held the F1 pak (sha 302d95d1…; no SWAP_LOG existed) + title screenshot PASS, TEST50 |
`| 2026-10-09 | Shaper = UAX #9 per line (paragraph RTL): numbers after Arabic follow W2 (4-1 shows 1-4, 50% shows %50, #1 shows 1#); "80 HP"..."HP 80" give the same visual line (unshape picks one) | executor, TEST50 (screenshot check) |
`| 2026-10-09 | Round prompts are saved verbatim in `docs\rounds\<ROUND>.md` | user, TEST50 |
`| 2026-10-09 | Elemental Resistance uses element nouns, not spell names: مقاومة النار / الجليد / الصاعقة / الماء / الهواء / الظلام (glossary rows "X Resistance"); Donald Fire/Blizzard/Thunder/Cure = دونالد فاير / بليزارد / ثاندر / كيور (KH2 order; Donald Aero = دونالد إيرو by the same pattern); 14239 = أول فيض من المشاعر (title text, not the Surge term); the 39 TRANS-2 proposed terms approved as they are; EXP stays خبرة | supervisor, SWAP-1 |
`| 2026-10-09 | **Arabic comma `،` is allowed (proven in `$jimakuNE`)**: no space before, one after; ASCII `,` stays in numbers, Latin runs, tags/args/plural syntax; `؟` stays ASCII `?` until a screenshot proves it. Applied by `tools\comma_fix.py` (210 rows). Journal/tutorials style: imperative for tutorials, narrative MSA for the journal; rows with no `<br>` in EN get none in AR | supervisor, TRANS-3 |
`| 2026-10-09 | Arabic hashtags in the journal: translated, words joined with `_` | supervisor, BUILD-1 |
`| 2026-10-09 | Conv hoist: a row with text inside `<conv(..)>` keeps one `<conv(X)>` at the row start and `<conv(off)>` at the end; the shaper shapes the inside (Arabic conv groups in mid-row stay an error) | supervisor, BUILD-1 |
`| 2026-10-09 | Film titles: Frozen = ملكة الثلج, Toy Story = حكاية لعبة (common Arabic dub titles, glossary approved); Tangled = متشابك pending, supervisor to verify | supervisor, BUILD-1 |
`| 2026-10-09 | Line breaking (SHAPER_SPEC §7): every line wider than its text field is broken at spaces by measured width (also lines between EN `<br>`), field per namespace in `technical\FIELD_WIDTHS.tsv`; no known field = unbroken; adjacent icons are one atom (drawn order kept) | executor, BUILD-1 (to be confirmed in-game) |
`| 2026-10-09 | Full builds are named `pakchunk99-arabic_P.pak`; `state\INSTALLED.tsv` lists the installed rows (STATS "installed") | supervisor / executor, BUILD-1 |
`| 2026-10-09 | **Magic names in Arabic (KH3 only):** Fire/Fira/Firaga/Firaza = نار / نار قوية / نار كبرى / نار قصوى; Blizzard..aza = جليد / جليد قوي / جليد أكبر / جليد أقصى; Thunder..aza = صاعقة / صاعقة قوية / صاعقة كبرى / صاعقة قصوى; Cure..aza = شفاء / شفاء قوي / شفاء أكبر / شفاء أقصى; Aero..aza = ريح / ريح قوية / ريح كبرى / ريح قصوى; Water..aza = ماء / ماء قوي / ماء أكبر / ماء أقصى; Donald X = X دونالد; compounds take the definite form (تعزيز النار, سوار النار الكبرى); Dark Firaga = نار كبرى مظلمة; replaces the GLOSS-2/SWAP-1 transliterations (KH2 glossary file unchanged) | user, FULL-1 |
`| 2026-10-09 | Help-text fields (`MainLibrary#68` = `CodeMenu#26`: ability, customize and premium descriptions) show at most 2 Arabic lines: rows with more are reflowed at build time (`shaper.reflow`, FIELD_WIDTHS `max_lines`); AR text keeps the EN `<br>` count | executor, FULL-1 (screenshot: line 3 clipped) |
`| 2026-10-09 | `review\script\` is the reference script for translation and review (story order from the Theater table, speaker codes from keys) | user, FULL-1 |
`| 2026-10-09 | LV label stays مستوى (final); the party LV field CampMenu #335 is widened left (xMin 86.95 px) by shipping one patched movie (CampMenu, `_0_P` base) in our pak | user, TRANS-4 |
`| 2026-10-09 | Story dialogue style: natural MSA with a light spoken feel, no dialect; character voices kept; subtitles near EN length, same `<br>` count; ASCII `?`; puns/idioms by meaning (listed as unsure); italic tags never split a joining Arabic word; song lyrics in own MSA wording (to be confirmed) | user / executor, TRANS-4 |
`| 2026-10-09 | `<p align>` in text drops the line; flush-left kept for now (alignment test cancelled; the ALIGN_RIGHT hook stays in `build_build1.py` for a later nbsp-padding test) | supervisor, REVIEW-1 |
`| 2026-10-09 | Heartbinder = رابط القلب (Dream Heartbinder = رابط قلب الحلم unchanged; Pixel/'Ohana/Pride/Ocean keep the pattern رابط قلب X, executor assumption); Altair = الطائر; Datascape = عالم البيانات, Datascapes = عوالم البيانات | supervisor, REVIEW-1 |
`| 2026-10-09 | `؟` (U+061F) is a validator ERR until a screenshot proves it; known typos live in `translation\typo_patterns.tsv` (WARN TYPO, whole-word regex) | supervisor, REVIEW-1 |
`| 2026-10-09 | Buzz Lightyear = باز لايتير; Keyblade wielder (fem) = حاملة كيبلايد (second form, feminine); the other TRANS-4 proposed terms approved as they are | supervisor, REVIEW-1 |
`| 2026-10-09 | Hashtags (journal and Re Mind): words in Arabic, multiword tags joined with `_`, the U+FFE0 marker and tags otherwise exact; validator WARN HASHTAG catches a Latin hashtag token in a hashtag row | supervisor, TRANS-6 |
`| 2026-10-09 | Pose category "Action" (14589) = الحركة (motion noun from Flowmotion), not الفعل; Chirithy as a friend's name takes no vocative | supervisor, TRANS-6 |
`| 2026-10-09 | Subtitles and field/battle voice break at `92_message/Subtitle #1` ($jimakuNE 38 pt, 7,545 units; the field word-wraps by itself, in visual order for Arabic, so every line is pre-broken); lines counted per `<pb>` page; design capacity 2 lines (EN), box 4; rows over it are listed, never shortened or reflowed | executor, BUILD-4 (to be confirmed in-game) |
`| 2026-10-09 | Namespaces with multi-line EN but no known field break at their widest EN line ended by `<br>` in mid-sentence (else the widest EN line of those keys); recorded as "(EN widest)"..."!" so it fits HudRight #109 without widening it; Re Mind/subtitle rows use the glossary Power of Waking and keep Kingdom Hearts masculine; REVIEW-2 fixes only real errors (no taste edits) | executor, REVIEW-2 |
`| 2026-10-10 | Publishing: every round must end with `tools\publish.bat` after `refresh.bat` and `secret_check`; PROJECT_MAP sections 3, 4, 7, 8 must be updated BEFORE publishing; a new Release is created only when a new BUILD is installed AND at least its checklist screenshots were reviewed by the supervisor. Only `public_repo\` (clone of github.com/exelight7/KH3RM_AR, branch main, never force-push) is ever pushed; the private repo and its history never | user approval, PUBLISH-1 |
`| 2026-10-10 | Installer: C# WPF .NET 8 in `tools\installer\` (original XAML art only; optional `art\background.png` slot), self-contained single file, detects Steam (registry + libraryfolders.vdf + appmanifest 2552450) and Epic (LauncherInstalled.dat), writes only `~mods\pakchunk99-arabic_P.pak`, refuses while the game runs; unsigned (SmartScreen note in the release) | user approval, RELEASE-080 |
`| 2026-10-10 | REVIEW-3: Isla de Muerta = KH2 form (KH3 form «جزيرة الموتى» retired in glossary.tsv); unchanged by decision: 02025, 03112, 08730, 05955, 05386, 05388, 05994, 09121 | supervisor, REVIEW-3 |
`| 2026-10-10 | Release tag names have NO "v": `0.8.0`, future rounds use `0.8.x` (asset file names keep `v`, e.g. `KH3RM_AR_Setup_v0.8.0.exe`); Release 0.8.0 is live as pre-release with 5 assets (sizes/SHA256 verified) | user, RELEASE-080b |
`| 2026-10-10 | BUILD-6 = the BUILD-5 pipeline unchanged (REVIEW-3 + row 05051); release 0.8.1 created on the user's explicit FINAL-1 instruction before the BUILD-6 checklist screenshots (exception to the PUBLISH-1 release rule, this round only) | user, FINAL-1 |
`| 2026-10-10 | Arabic in round prompts arrives as \uXXXX escapes; the tool layer may turn them into Arabic before Python runs, so fragments are decoded from hex code points (`chr(int(h, 16))`) | executor, FINAL-1 |
`| 2026-10-10 | Images: textures are edited in place (same format, size, mips; only changed 4x4 blocks re-encoded) and shipped in a separate optional pak `pakchunk98-arabic-images_P.pak` beside the text pak (the only case with two of our paks in `~mods`); brand wordmarks (KINGDOM HEARTS III, Re Mind, Classic Kingdom titles, VERUM REX, world logos such as Monsters, Inc.), key names, credits and language names keep English; Arabic text comes from the translation rows / glossary, drawn with Segoe UI | user, FINAL-1 |
`| 2026-10-10 | **Cloud review:** private repo `KH3RM_AR_work` (github.com/exelight7/KH3RM_AR_work, PRIVATE, EN + AR workspace for cloud Claude sessions, `cloud_repo\` here, branch main, never public); public repo `KH3RM_AR` stays Arabic-only; **1.0.0 is LOCKED until (a) cloud second-pass review of all dialogue and subtitles is merged, (b) image phase done, (c) the user says go.** Cloud sessions follow `CLOUD_RULES.md`, ranges in `review\cloud\TASKS.md`, workflow `docs\CLOUD_WORKFLOW.md`, sync `tools\sync_cloud.bat` | user, CLOUD-PREP |
`| 2026-10-10 | Cloud corrections: `review\corrections\cloud\<page>.tsv` (same 4 columns; new_AR == old_AR marks a row as checked) are applied by `apply_corrections.py` and set status reviewed (verified kept) + note `cloud review pass 2`; sync replays the cloud corrections (old_AR must match) instead of copying TSVs, so local changes are never overwritten | executor, CLOUD-PREP |
`| 2026-10-10 | General note: the user tested BUILD-5/6 in game and reported OK, no screenshots (2026-10-10); no row is marked verified because of it | user, CLOUD-PREP |
`| 2026-10-10 | Cloud sync: parallel cloud branches may correct the same id; `apply_corrections` merges identical results and a check mark (new == old) with one real change (the real change wins); two different real changes stay a refusal. Glossary aligned to the corrected rows: Diving Strike = ability-row form, Powerwild / Frost Serpent = bestiary-row forms, Monsters Inc = the short menu form (no "limited"..."needs new wording"..."أحرف") + 8 GPT Q2 ids (04538, 04915, 06712, 07464, 07515, 07903, 07339, 08531); GPT 06084 / 05228 and all other GPT rows not applied; executor ran `SWAP_TO_BUILD9.bat` itself on the user's approval | user, BUILD-9 |
`| 2026-10-14 | BUILD-10: supervisor approved 12 direct GPT Q3 ids (08565, 08607, 08713, 08734, 09171, 09233, 09816, 09966, 10042, 10082, 10197, 10294) + 7 glossary-gated (10502, 10521, 10517, 11557, 11568, 12476, 12489); all 19 passed old_AR + validate + glossary checks, 0 skipped; 10882 / 10883 / 11500 and the other GPT rows not applied; executor ran `SWAP_TO_BUILD10.bat` (sha pinned). |
| 2026-10-14 | BUGFIX-1: strings drawn by Windows itself (native message boxes) get raw logical Arabic through `translation\raw_logical_ids.tsv` (read only by `tools\build_build11.py`; `build_build4.py` unchanged); a key used by any Scaleform movie is never listed there (Yes / No stay shaped); executor ran `SWAP_TO_BUILD11.bat` on the user's approval | user, BUGFIX-1 |
`| 2026-10-11 | **Public README and public user docs (README, TESTER_GUIDE, FAQ, issue template, LICENSE_TODO, release notes) are Arabic only**; commands, file names and technical terms (Steam, Epic, SHA256, SmartScreen) stay Latin; no English game text; `make_public.py` + `tools\public_templates\README.md` generate it so a sync cannot restore the AR+EN version | user, README-AR |
`
`## 5. Folders and key files (auto)
`
`| path | what |
`|---|---|
`| `AGENTS.md` | graphify |
`| `CHANGELOG.md` | Changelog |
`| `CLAUDE.md` | graphify |
`| `CLOUD_RULES.md` | CLOUD_RULES — read this first, obey it exactly |
`| `FAQ.md` | الأسئلة الشائعة |
`| `LICENSE_TODO.md` | License — undecided |
`| `PROJECT_MAP.md` | PROJECT_MAP — KH3 Arabic (start here) |
`| `README.md` | <div align="center"> |
`| `RELEASE-090.md` | RELEASE-090 (round prompt, saved verbatim) |
`| `REMOVE_ARABIC.bat` | chcp 65001 >nul |
`| `REMOVE_IMAGES.bat` | chcp 65001 >nul |
`| `REMOVE_IMAGES_PILOT.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD1.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD10.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD2.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD3.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD4.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD5.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD6.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD7.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD8.bat` | chcp 65001 >nul |
`| `SWAP_TO_BUILD9.bat` | chcp 65001 >nul |
`| `SWAP_TO_F1.bat` | chcp 65001 >nul |
`| `SWAP_TO_F2.bat` | chcp 65001 >nul |
`| `SWAP_TO_IMAGES_MASS.bat` | chcp 65001 >nul |
`| `SWAP_TO_IMAGES_MASS2.bat` | chcp 65001 >nul |
`| `SWAP_TO_IMAGES_MASS3.bat` | chcp 65001 >nul |
`| `SWAP_TO_IMAGES_MASS4.bat` | chcp 65001 >nul |
`| `SWAP_TO_IMAGES_PILOT.bat` | chcp 65001 >nul |
`| `SWAP_TO_TEST50.bat` | chcp 65001 >nul |
`| `cloud_repo\` | (no description) |
`| `docs\` | project docs: INDEX (doc list), SUPERVISOR (full supervisor instructions) |
`| `docs\CLOUD_WORKFLOW.md` | Cloud review workflow |
`| `docs\GRAPHIFY.md` | خريطة المشروع — Graphify |
`| `docs\INDEX.md` | Docs index |
`| `docs\INSTALLER_0.9.0_PLAN.md` | Installer 0.9.0 plan - optional "..." (documentation only) |
`| `docs\INSTALL_MANUAL.md` | التثبيت اليدوي (بدون المثبت) |
`| `docs\RELEASE_DRAFT_0.9.0.md` | 0.9.0 (تجريبي) |
`| `docs\ROADMAP_TO_1.0.0.md` | الطريق إلى 1.0.0 |
`| `docs\SUPERVISOR.md` | Supervisor instructions (full copy) |
`| `docs\TESTER_GUIDE.md` | دليل المختبر |
`| `extracted\` | read-only decrypted copies of game files + pak index (gitignored, never deleted) |
`| `font\` | reserved for font files (empty; Segoe UI is read from C:\Windows\Fonts) |
`| `graphify-out\` | (no description) |
`| `out\` | build outputs: out\builds\<round>\ paks, pakroots, verify tables (gitignored, never deleted) |
`| `public_repo\` | (no description) |
`| `review\` | review pages (Markdown), corrections, validation report; **`review\script\` = the reference script for translation and review** (story order by the Theater table + TIPS pages, `tools\make_script.py`) |
`| `review\CLOUD_BUGS.md` | Tool bugs found by cloud sessions |
`| `review\DECISIONS_ANSWERED.md` | DECISIONS_ANSWERED (DECIDE-19) |
`| `review\DECISIONS_NEEDED.md` | DECISIONS_NEEDED (LIGHT-2) |
`| `review\FLAGS.md` | Flagged rows |
`| `review\INDEX.md` | Review index |
`| `review\REVIEW5_Q1_LOG.md` | REVIEW5 Q1 log |
`| `review\REVIEW5_Q1_QUESTIONS.md` | REVIEW5 Q1 questions |
`| `review\REVIEW5_Q4_LOG.md` | REVIEW5 Q4 log |
`| `review\REVIEW5_Q4_QUESTIONS.md` | REVIEW5 Q4 questions |
`| `review\RULES.md` | Review workflow |
`| `review\SAME_AS_EN.tsv` | TSV, columns: id, category, file, key, EN, AR, status, why |
`| `review\SKIP_AUDIT.tsv` | TSV, columns: id, category, file, key, EN, class, note |
`| `review\SKIP_SUSPECTS.tsv` | TSV, columns: id, category, file, key, EN, class, note |
`| `review\UNSURE_CLOUD.md` | Status as of CLEANUP-1: this file is historical; entries marked changed or resolved elsewhere may be outdated; the glossary and the translat |
`| `review\UNSURE_REVIEW2.md` | Status as of CLEANUP-1: this file is historical; entries marked changed or resolved elsewhere may be outdated; the glossary and the translat |
`| `review\VALIDATION.md` | VALIDATION |
`| `review\review_dialogue.tsv` | TSV, columns: id, EN, AR, status, flags, note |
`| `review\review_items_abilities.tsv` | TSV, columns: id, EN, AR, status, flags, note |
`| `review\review_journal.tsv` | TSV, columns: id, EN, AR, status, flags, note |
`| `review\review_menus_ui.tsv` | TSV, columns: id, EN, AR, status, flags, note |
`| `review\review_remind.tsv` | TSV, columns: id, EN, AR, status, flags, note |
`| `review\review_subtitles_cutscenes.tsv` | TSV, columns: id, EN, AR, status, flags, note |
`| `review\review_tutorials.tsv` | TSV, columns: id, EN, AR, status, flags, note |
`| `screenshots\` | optional, gitignored; screenshots are sent in the supervisor chat (log file = chat) |
`| `state\` | round log, last report, stats, screenshot log |
`| `state\CLOUD_PROGRESS.md` | Cloud progress |
`| `state\FEEDBACK_TEMPLATE.tsv` | TSV, columns: date, build, where, id_or_words, type, note |
`| `state\INSTALLED.tsv` | TSV, columns: id, ar_sha1, build |
`| `state\LAST_REPORT.md` | latest round report (overwritten each round) |
`| `state\PROGRESS.md` | round log, 3 lines per task (source of the round history below) |
`| `state\SCREENSHOT_LOG.tsv` | TSV, columns: date, round, string_ids, screenshot_file, result |
`| `state\STATS.md` | STATS |
`| `state\SWAP_LOG.tsv` | TSV, columns: time, action, hash, result |
`| `technical\` | recon, tag inventory, shaper spec, text counts, field widths, text coverage (TEXT_COVERAGE.md) |
`| `technical\BUILD1_CHECKLIST.md` | قائمة فحص BUILD-1 |
`| `technical\BUILD2_CHECKLIST.md` | قائمة فحص BUILD-2 |
`| `technical\BUILD3_CHECKLIST.md` | قائمة فحص BUILD-3 |
`| `technical\BUILD5_CHECKLIST.md` | قائمة فحص BUILD-5 |
`| `technical\BUILD6_CHECKLIST.md` | قائمة فحص BUILD-6 |
`| `technical\BUILD7_CHECKLIST.md` | قائمة فحص BUILD-7 |
`| `technical\FIELD_WIDTHS.tsv` | TSV, columns: prefix, keys, movie, field, font, font_id, size_pt, x0, x1, y0, y1, max_lines, reflow, evidence |
`| `technical\IMAGES2_PREP.md` | IMAGES2_PREP (LIGHT-3) |
`| `technical\IMAGES_INVENTORY.tsv` | TSV, columns: asset, group, size, format, mips, storage, pak, screen, english, plan, priority |
`| `technical\IMAGES_MASS2_CHECKLIST.md` | قائمة فحص الصور — الجولة 2 |
`| `technical\IMAGES_MASS_CHECKLIST.md` | قائمة فحص حزمة الصور (IMAGES-MASS) |
`| `technical\IMAGES_PILOT_CHECKLIST.md` | قائمة فحص تجربة الصور (IMAGES-PILOT) |
`| `technical\IMAGES_PLAN.md` | IMAGES_PLAN — English text inside textures (FINAL-1 part 2) |
`| `technical\IMAGES_STILL_ENGLISH.tsv` | TSV, columns: asset, group, reason |
`| `technical\RECON_KH3.md` | RECON_KH3 — Kingdom Hearts III + Re Mind (Steam), read-only recon |
`| `technical\SHAPER_SPEC.md` | SHAPER_SPEC — Arabic pre-shaper for KH3 Scaleform text |
`| `technical\TAGS.md` | TAGS — markup in KH3 English text (VERIFIED from `extracted\text_en.tsv`, 17,222 entries) |
`| `technical\TEST50_CHECKLIST.md` | قائمة فحص TEST50 |
`| `technical\TEXT_COUNTS.tsv` | TSV, columns: level, name, category, entries, empty, unique_texts, words, chars |
`| `technical\TEXT_COVERAGE.md` | TEXT_COVERAGE — every source of visible text (FULL-1) |
`| `technical\images_rects.tsv` | TSV, columns: asset, box, source, fill, align, effect, scale, pad, rotate, size, erase, note |
`| `technical\images_rects_trial.tsv` | TSV, columns: asset, box, source, fill, align, effect, scale, pad, rotate, size, erase, note |
`| `technical\images_words.tsv` | TSV, columns: asset, screen, english, plan, priority |
`| `technical\theater_order.tsv` | TSV, columns: event, theater_scene_key |
`| `tools\` | all scripts (Python 3.12, run from the project root) + repak |
`| `tools\TOOLS.md` | Tools (official sources only) |
`| `tools\apply_corrections.py` | Apply review\corrections\*.tsv (header: id old_AR new_AR reason) to translation\<cat>\<file>.tsv. |
`| `tools\apply_feedback.py` | Read a filled state\FEEDBACK.tsv (date, build, where, id_or_words, type, note) and write review\FEEDBACK_REPORT.md: |
`| `tools\build1_rows.py` | One-time (BUILD-1): write review\corrections\build1_conv.tsv (the 12 tutorial control lists with <conv> groups, |
`| `tools\build_arabictest1.py` | ARABIC-TEST-1 build: NEW GAME (kh3_menu.title/menu_0002) in 3 variants + TresFont with Segoe UI Arabic in $sougei. |
`| `tools\build_arabictest2.py` | ARABIC-TEST-2 build: title screen in Arabic (translation\ rows with status != todo, shaped) for kh3_menu + kh3_settings, |
`| `tools\build_build1.py` | BUILD-1 build: every translated row of every category (status != todo, AR not empty) shaped into the en .locres, |
`| `tools\build_build10.py` | BUILD-10: the BUILD-9 pipeline unchanged (tools\build_build4.py via the same wrapper) run on the current translation\ TSVs |
`| `tools\build_build2.py` | BUILD-2 (FULL-1): the full build of tools\build_build1.py (every translated row, line breaking) with the FULL-1 |
`| `tools\build_build3.py` | BUILD-3 (TRANS-4): the BUILD-2 full build plus |
`| `tools\build_build4.py` | BUILD-4: the first full build with every translated row (all categories: story dialogue, subtitles, Re Mind, |
`| `tools\build_build5.py` | BUILD-5: the BUILD-4 pipeline unchanged (tools\build_build4.py: same movie patches, TresFont, line breaking, no <p align>) |
`| `tools\build_build6.py` | BUILD-6: the BUILD-5 pipeline unchanged (tools\build_build4.py via the same wrapper as build_build5.py: same movie |
`| `tools\build_build7.py` | BUILD-7: the BUILD-6 pipeline unchanged (tools\build_build4.py via the same wrapper as build_build6.py: same movie |
`| `tools\build_build8.py` | BUILD-8: the BUILD-7 pipeline unchanged (tools\build_build4.py via the same wrapper as build_build7.py: same movie |
`| `tools\build_build9.py` | BUILD-9: the BUILD-8 pipeline unchanged (tools\build_build4.py via the same wrapper) run on the current translation\ TSVs |
`| `tools\build_test50.py` | TEST50 build: 50 test rows (menus, items, equipment, abilities, plural/acronym/set-letter rows, tutorials, |
`| `tools\cloud_check.py` | Cloud check (run after every page and by GitHub Actions): translation integrity + validate (0 ERR) + unit tests + secret scan. |
`| `tools\cloud_secret_check.py` | Check cloud_repo/ (or any directory / file list) before every push to the private cloud repo. Fails on: forbidden |
`| `tools\comma_fix.py` | TRANS-3: ASCII ',' used as Arabic punctuation -> '،' in translated AR rows. Usage: comma_fix.py [--apply] |
`| `tools\fill_release_notes.py` | Fill {{placeholders}} in a release-notes draft from state\STATS.md. Usage: fill_release_notes.py [draft.md] [--write] |
`| `tools\find_text.py` | Find translation rows by Arabic (as shown in the game) or English text. |
`| `tools\font_census.py` | Read-only (TEST50): font classes of every text field in the game's Scaleform movies. |
`| `tools\full1_magic.py` | One-time (FULL-1 Part B): magic names in Arabic (user decision FULL-1, KH3 only; KH2 glossary file unchanged). |
`| `tools\gfx_edittext.py` | Read-only: list every DefineEditText (tag 37) in Scaleform SwfMovie .uexp files: id, variable name, font |
`| `tools\gfx_fonts.py` | Read-only: list fonts inside a Scaleform GFx movie embedded in a SwfMovie .uexp. |
`| `tools\gfx_imports.py` | Read-only: for each Scaleform SwfMovie .uexp, list fonts it imports (ImportAssets/ImportAssets2, tags 57/71) |
`| `tools\gfx_layout.py` | Read-only (BUILD-4): where a Scaleform movie places its characters. For every DefineSprite (tag 39) and the root |
`| `tools\gloss3_apply.py` | One-time (TRANS-1 part 1): apply supervisor decisions on the pending glossary conflicts. Do not re-run. |
`| `tools\gloss_hits.py` | TRANS-2 helper: glossary terms (approved, not type menu unless exact row match) that occur in a dump file. |
`| `tools\images_banner_rects.py` | Area banners (IMAGES-MASS): technical\images_rects.tsv rows for the 25 mapName_* textures of the repaint plan. |
`| `tools\images_inventory.py` | Read-only (FINAL-1 part 2): inventory of the textures that show English text. |
`| `tools\images_tutorial_rects.py` | Tutorial pictures (IMAGES-MASS): technical\images_work\tutorial_spec.tsv -> technical\images_rects.tsv rows for every |
`| `tools\import_kh2_glossary.py` | One-time/idempotent (GLOSS-1): import translation\kh2_glossary.md (finished KH2 project, Arabic Markdown tables) |
`| `tools\locres.py` | UE4 .locres reader/writer (legacy v0 and compact v1, as shipped by KH3 / UE 4.17). |
`| `tools\make_build10_corrections.py` | BUILD-10: generate review\corrections\build10_round.tsv from review\gpt\Q3\proposals.tsv (approved ids only). |
`| `tools\make_build9_corrections.py` | BUILD-9: generate review\corrections\build9_round.tsv from review\proposed\BUILD9_proposed.tsv (+ 10847 wording from |
`| `tools\make_cloud.py` | Regenerate cloud_repo\ (git repo of the PRIVATE github.com/exelight7/KH3RM_AR_work) from the private project: exactly what a Linux |
`| `tools\make_glossary.py` | translation\glossary.tsv (source of truth) -> recount kh3_count/example_ids from translation\<cat>\*.tsv EN |
`| `tools\make_public.py` | Regenerate public_repo\ (a clone of github.com/exelight7/KH3RM_AR) from the private project. Never copies game files, |
`| `tools\make_release.py` | Prepare out\release\ for a GitHub Release: the installed BUILD pak, SHA256.txt, INSTALL_AR.bat, REMOVE_AR.bat, AR_MESSAGES.txt. |
`| `tools\make_review.py` | Generate review\md\<category>_NN.md (300 rows/page, game order), review\INDEX.md, review\FLAGS.md |
`| `tools\make_script.py` | Generate review\script\ (FULL-1 Part E): the reference script for translation and review, Markdown only. |
`| `tools\make_swap_scripts.py` | SWAP-1/TEST50/BUILD-1/FULL-1/TRANS-4/BUILD-4: generate SWAP_TO_F1.bat, SWAP_TO_F2.bat, SWAP_TO_TEST50.bat, SWAP_TO_BUILD1.bat, |
`| `tools\merge_translation.py` | Merge translation\<category>\*.tsv back into one pipeline TSV (namespace,key,source_hash,text,category,file) for `locres.py tsv-import`. |
`| `tools\pak_footer.py` | Read-only: parse UE4 .pak footers (magic 0x5A6F12E1) and print version/encryption info. |
`| `tools\pak_index.py` | Read-only: decrypt and parse UE4 pak v4 indexes -> TSV (pak, path, size, compressed_size, compression, encrypted). |
`| `tools\preview_text.py` | Offline preview: draw a shaped string with the glyphs of a (rebuilt) TresFont, the way Scaleform lays it out |
`| `tools\public_check.py` | Check public_repo\ before every publish. Fails on: forbidden path/extension, EN column or a Latin sentence of 6+ words |
`| `tools\publish.bat` | Every round ends with this (after refresh.bat and secret_check). Publishes to github.com/exelight7/KH3RM_AR, branch main, never forced. |
`| `tools\refresh.bat` | end-of-round pipeline: merge check, tests, corrections, validate, review pages, script, stats, map, secret check |
`| `tools\remind_map.py` | Read-only: summarise extracted/pak_index.tsv per pak and flag Re Mind (DLC) content. |
`| `tools\review2_page.py` | REVIEW-2 helper: page N (300 rows) in story order = review\script order (dialogue, subtitles, Re Mind in story) then the |
`| `tools\review2_sub.py` | REVIEW-2 helper: substring fixes. Usage: python -I tools\review2_sub.py N file ; file lines 'id<TAB>old_fragment<TAB>new_fragment<TAB>reason' |
`| `tools\scan_magic.py` | Read-only: count plaintext signatures inside pak files (uasset, locres, zlib, ttf/otf). |
`| `tools\secret_check.py` | Fail if the AES key or a game binary is tracked by git (or staged). Checks the index, not the working tree. |
`| `tools\setrow.py` | Fix one translated row in place: python -I tools\setrow.py <id> <AR> [note]  (menus_ui only; TRANS-1 helper) |
`| `tools\shaper.py` | Arabic pre-shaper for KH3 Scaleform text (technical/SHAPER_SPEC.md §1-6; §8 checks in tools/test_shaper.py). |
`| `tools\skip_audit.py` | FINISH-TRANS: skip audit (todo rows), suspects, AR==EN / empty-AR check. Read-only on translation TSVs. |
`| `tools\split_translation.py` | One-time/idempotent: split translation\en_source.tsv into translation\<category>\<file>.tsv. |
`| `tools\stats.py` | Write state\STATS.md. translated = status in translated/reviewed/verified; reviewed = reviewed/verified; |
`| `tools\sync_cloud.bat` | Cloud sync: pull merged cloud review work into the private project, then regenerate and push cloud_repo (private KH3RM_AR_work, main, never  |
`| `tools\sync_cloud.py` | Cloud sync (run through tools\sync_cloud.bat). Never force-pushes; only cloud_repo\ (private KH3RM_AR_work, branch main) is pushed. |
`| `tools\tag_inventory.py` | Read-only: inventory of markup in the English locres export. |
`| `tools\test_apply_feedback.py` |  |
`| `tools\test_cloud_secret_check.py` | unit tests for cloud_secret_check.py |
`| `tools\test_corrections.py` | unit tests for apply_corrections.py |
`| `tools\test_find_text.py` |  |
`| `tools\test_public_check.py` |  |
`| `tools\test_shaper.py` | unit tests for shaper.py: SHAPER_SPEC §9a (U1-U12), §9b (the 20 TAGS.md examples T1-T20 + T21/T22), |
`| `tools\test_validate.py` | unit tests for validate.py |
`| `tools\text_counts.py` | Read-only: entry/word counts per category for the English locres export (extracted/text_en.tsv). |
`| `tools\text_coverage.py` | Read-only (FULL-1 Part D): inventory of every source of player-visible text in the installed game. |
`| `tools\texture_codec.py` | UE4.17 cooked Texture2D (.uasset/.uexp[/.ubulk]) reader/writer + pixel codec (FINAL-1). |
`| `tools\texture_text.py` | Repaint English text inside a texture with Arabic (FINAL-1 pilot, IMAGES-MASS). |
`| `tools\trans1_report.py` | TRANS-1: write state\LAST_REPORT.md (data parts generated from translation\menus_ui). One-time helper. |
`| `tools\trans2_report.py` | TRANS-2: write state\LAST_REPORT.md (data parts generated from translation\ and review\corrections\applied). One-time helper. |
`| `tools\trans4_page.py` | TRANS-4 helper: story dialogue and cutscene subtitles page by page in the order of review\script\ (script_NNN.md, |
`| `tools\trans5_page.py` | TRANS-5 helper: story dialogue and cutscene subtitles page by page in the order of review\script\ (script_NNN.md, |
`| `tools\trans_page.py` | TRANS-1 helper. `dump N` prints the rows of menus_ui page N (300 rows, game order) that still need a human translation |
`| `tools\tresfont.py` | Scaleform TresFont (UE4 SwfMovie .uasset/.uexp) parser + writer, down to individual glyph edges. |
`| `tools\tsvlib.py` | Shared helpers for the translation TSVs (ORG-1). Plain TSV, no quoting; text is already escaped like en_source.tsv. |
`| `tools\update_map.py` | Regenerate the "(auto)" sections of PROJECT_MAP.md: numbers (from state\STATS.md, so run stats.py first), |
`| `tools\validate.py` | Validate translated rows against EN. Writes review\VALIDATION.md; flags are reused by make_review.py. |
`| `translation\` | translation TSVs per category/file (EN + AR + status), glossary |
`| `translation\GLOSSARY_CONFLICTS.md` | Glossary conflicts (KH2 glossary → KH3) |
`| `translation\GLOSSARY_PROPOSALS.md` | Glossary proposals — KH3-new and Re Mind terms |
`| `translation\allowed_latin.txt` | history only (TRANS-1 whitelist); the LATIN rule now compares each row with its own EN |
`| `translation\en_source.tsv` | TSV, columns: namespace, key, source_hash, text, category, file |
`| `translation\glossary.md` | Glossary — KH3 Arabic |
`| `translation\glossary.tsv` | TSV, columns: en, ar, type, source, status, kh3_count, example_ids, note |
`| `translation\images_strings.tsv` | TSV, columns: id, asset, EN, AR, status, note |
`| `translation\kh2_glossary.md` | مسرد مصطلحات KH2FM (المصدر الوحيد للحقيقة لأسماء الأعلام) |
`| `translation\typo_patterns.tsv` | TSV, columns: pattern, correct, note |
`
`## 6. How to run things
`
`All commands from the project root (`C:\filessss\mewo\kh3fm-arabic`).
`- **Refresh everything** (merge check, tests, corrections, validation, review pages, stats, this map, secret check): `tools\refresh.bat`
`- **Shape a string / run the shaper tests:** `python -I tools\shaper.py "نص"..."installed" column after `tools\refresh.bat`).
`- **BUILD-2:** `python -I tools\build_build2.py` → `out\builds\BUILD-2\` (same outputs; help-field reflow from `technical\FIELD_WIDTHS.tsv` `max_lines`); install `SWAP_TO_BUILD2.bat`, then `python -I tools\build_build2.py --installed`.
`- **BUILD-7 (current full build):** `python -I tools\build_build7.py > out\builds\BUILD-7\build.log` → `out\builds\BUILD-7\` (BUILD-4 pipeline on the current TSVs, `diff_vs_build6.tsv`); install `SWAP_TO_BUILD7.bat` (from cmd; Git Bash needs `cmd //c .\SWAP_TO_BUILD7.bat`), then `python -I tools\build_build7.py --installed`. BUILD-6: the same with `build_build6.py` / `SWAP_TO_BUILD6.bat`. BUILD-5: the same with `build_build5.py` / `SWAP_TO_BUILD5.bat`. repak output is not byte-reproducible between runs: a rebuild gives a new sha, so regenerate the swap script (`tools\make_swap_scripts.py`) after the last build.
`- **BUILD-4:** `python -I tools\build_build4.py` → `out\builds\BUILD-4\` (all translated rows, Subtitle/EN-widest line breaking, 3 patched LV movies, `movie_verify.tsv`, `overflow.tsv` = rows over field capacity); `--fields` regenerates the BUILD-4 rows of `technical\FIELD_WIDTHS.tsv`; install `SWAP_TO_BUILD4.bat`, then `python -I tools\build_build4.py --installed`. repak orders files differently per run, so a rebuild has a new pak SHA (per-file SHA identical): rebuild → regenerate the swap script.
`- **Where a movie places a field (neighbour gaps):** `python -I tools\gfx_layout.py <movie.uexp> <char id>`
`- **BUILD-3:** `python -I tools\build_build3.py` → `out\builds\BUILD-3\` (BUILD-2 + patched CampMenu movie, `movie_verify.tsv`, align test on row 15729); install `SWAP_TO_BUILD3.bat`, then `python -I tools\build_build3.py --installed`.
`- **Story translation pages:** `python -I tools\trans4_page.py dump|apply N [file]` (script page N in story order, dialogue + subtitles).
`- **Text inventory (read-only):** `python -I tools\text_coverage.py` → `technical\TEXT_COVERAGE.md` + `technical\text_coverage\*.tsv`.
`- **Master script:** `python -I tools\make_script.py` → `review\script\INDEX.md` (story), `TIPS.md`, pages (also run by `tools\refresh.bat`).
`- **Build the TEST50 test pak:** `python -I tools\build_test50.py` → `out\builds\TEST50\pakchunk99-test50_P.pak` + `pak_verify_sha256.tsv` + `rows.tsv` (needs font_fields.tsv). Older: `tools\build_arabictest2.py` (F1/F2 title paks)
`- **Measure text fields of a movie:** `python -I tools\gfx_edittext.py <movie.uexp>...`
`- **Offline join/size preview:** `python -I tools\preview_text.py <TresFont.uasset> 3 30 2 out.png "نص"`
`- **Swap the test pak (double-click in the project root, close the game first):** `SWAP_TO_BUILD1.bat` / `SWAP_TO_TEST50.bat` / `SWAP_TO_F1.bat` / `SWAP_TO_F2.bat` delete our `pakchunk99-*_P.pak` from `~mods`, copy the BUILD-1 pak, the TEST50 pak or the ARABIC-TEST-2 F1/F2 pak from `out\builds\`, verify SHA256 against the build and print Arabic + English "Done" (it asks for admin rights only if the copy fails for permissions). `REMOVE_ARABIC.bat` deletes our pak and the empty `~mods`. All three refuse to run while KINGDOM HEARTS III is running and append to `state\SWAP_LOG.tsv` (time, action, hash, result). Scripts are generated by `tools\make_swap_scripts.py` (pure ASCII; messages in `tools\swap_msgs\`). Other paks: copy by hand into `C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods\`, only one of ours at a time (`technical\RECON_KH3.md` §12).
`- **Images (FINAL-1, IMAGES-MASS):** inventory `python -I tools\images_inventory.py` (read-only) → `technical\IMAGES_INVENTORY.tsv`; codec `python -I tools\texture_codec.py info|png|roundtrip`; rects in `technical\images_rects.tsv` (tutorial rows from `technical\images_work\tutorial_spec.tsv` via `python -I tools\images_tutorial_rects.py technical\images_work\tutorial_spec.tsv [ids]`, banner rows via `python -I tools\images_banner_rects.py`); build `python -I tools\texture_text.py mass` (all, ~2 min: assets in `out\builds\IMAGES-MASS\assets\`, `checks.tsv`, `repaint_log.tsv`, before/after sheets in `ref\` (private), pak + list/hash-list/unpack SHA256 + uexp re-parse) or `mass <asset-substring>` (render + checks only); `--installed` compares `~mods`. Install `SWAP_TO_IMAGES_MASS.bat` (from cmd), remove `REMOVE_IMAGES.bat` (both touch only `pakchunk98-arabic-images_P.pak`; sha pinned in `tools\make_swap_scripts.py`: after a rebuild update it and regenerate). Images % and the still-English list come from `tools\stats.py`.
`- **Commit:** after `tools\refresh.bat` exits 0; `tools\secret_check.py` must PASS.
`- **Installer / release (RELEASE-080):** build the EXE: `cd tools\installer` then `dotnet publish -c Release -o ..\..\out\release\vX\publish` (needs .NET 8 SDK; embeds `out\builds\BUILD-7\pakchunk99-arabic_P.pak` since 0.8.2 (csproj `PakPath` default must be changed too), override with `-p:PakPath=...`; for a new BUILD update `Core.ExpectedSha`, `Core.Version`, csproj `Version` + `PakPath` and the SelfTest label). Tests: `KH3RM_AR_Setup.exe --selftest out.txt`; screenshots: `--render ar|en out.png`; icon: `--icon app.ico`. GitHub CLI 2.102.0 (official zip, sha ae64e556...) is in `tools\gh-2.102.0\x\bin\gh.exe` (gitignored); release (tag without "v"..."0.8.2 (pre-release)" --notes-file out\release\v0.8.2\RELEASE_NOTES.md <5 assets>` (user logged in), then `gh release view 0.8.2 --json assets` against `SHA256SUMS.txt`. The README download version is `RELEASE` in `tools\make_public.py`.
`
`## 7. Numbers (auto)
`
`From `state\STATS.md` (regenerated by `tools\stats.py`).
`
`| category | rows | translated | installed | reviewed | verified-by-screenshot |
`|---|---|---|---|---|---|
`| dialogue | 2298 | 2213 (96.3%) | 2213 (96.3%) | 2213 (96.3%) | 0 (0.0%) |
`| items_abilities | 2334 | 2160 (92.5%) | 2160 (92.5%) | 2160 (92.5%) | 3 (0.1%) |
`| journal | 628 | 615 (97.9%) | 615 (97.9%) | 615 (97.9%) | 0 (0.0%) |
`| menus_ui | 3849 | 3605 (93.7%) | 3605 (93.7%) | 3605 (93.7%) | 94 (2.4%) |
`| remind | 1163 | 1126 (96.8%) | 1126 (96.8%) | 1126 (96.8%) | 0 (0.0%) |
`| subtitles_cutscenes | 6336 | 6083 (96.0%) | 6083 (96.0%) | 6083 (96.0%) | 1 (0.0%) |
`| tutorials | 614 | 613 (99.8%) | 613 (99.8%) | 613 (99.8%) | 0 (0.0%) |
`| TOTAL | 17222 | 16415 (95.3%) | 16415 (95.3%) | 16415 (95.3%) | 98 (0.6%) |
`| images | 42 | 42 (100.0%) | 0 (0.0%) | 17 (40.5%) | 0 (0.0%) |
`| images | textures with English | repaint plan | repainted | no translatable text | still English (unreadable) | images repainted % | of the textures with text |
`|---|---|---|---|---|---|---|---|
`| all groups | 324 | 234 | 213 | 17 | 4 | 91.0% | 213 / 217 = 98.2% |
`
`## 8. Open questions

- BATCH-234: still open for the supervisor (no evidence in the files): 06218 / 01201 / 04052 / 09481 addressee, 11915 star name, 11596 / 11683 pattern, 11853, 12769 / 12797 recipe, 03913 vs 06084 ("As if." in two scenes now worded differently), 14975 / 14980 bare plurals on the minigame LCD (see `review\BATCH3_DECISIONS.md`). 385 image boxes stay under the readability bar (no room, or growing would cover an icon; `technical\images_enlarge_plan.tsv`): keep, or return the worst to English? BUILD-11 quit box still unseen in game (raw_logical_ids.tsv kept; rollback SWAP_TO_BUILD10.bat if the settings popup breaks). The BUGFIX-1 claim that the installed air gauge showed the old label was wrong: IMAGES-MASS2..5 all draw the I0013 word (MASS4 = MASS5 byte-identical there); I0014 CHARGE on that texture stays under the bar (no room).
- UPLOAD-FOLDER-ZIP: resolved the AV-FALSEPOS question below as 'extra asset' (the single-file exe stays the default).
`
`- AV-FALSEPOS: after the user's VirusTotal scan of the folder zip, decide whether to ship the folder variant as an extra release asset or the default.
`
`- RELEASE-091: by the new readability measure, 522 of the 1,346 drawn boxes of the earlier IMAGES-MASS3 textures (107 textures, mostly 5-11 px) are below the bar (`out\builds\IMAGES-MASS4\repaint_log.tsv`, column readability); they shipped before and stay unchanged. Supervisor: look at a few in game and say whether to keep them, enlarge where room allows, or return the worst to English. Also open: in-game check of the Kairi HUD name (flash copy included) and of the partly repainted gummi weapons picture (4 small HUD words stay English there); the 42 text rows changed since 0.9.0 are still unseen in game; Linux installer still unrun on Linux; installer install / remove never run on the real game folder.
`- REVIEW5-Q4: the 1 Q4 fix (`review\corrections\applied\review5_q4_p14.tsv`, row 17169) waits for the next build; 5 Q4 doubts in `review\REVIEW5_Q4_QUESTIONS.md` need the supervisor: 13402 / 14360 / 14373 (plural imperative where the player is addressed in the singular elsewhere), 15494-15497 (Popcat number and gender differ from 15493), 14763 vs 15593 (same EN, `نقاط` vs `من النقاط`; Premium Menu cell widths not seen in game). Q3 (GPT) is the only quarter still unreviewed.
`- BUILD-9: installed, in-game check pending (14238 title width, 10847 wording); publish waits for the supervisor. Still open: GPT Q2 06084 and 05228 (not applied), the 21 GPT Q2 QUESTIONS (`review\gpt\Q2\QUESTIONS.tsv`), 3 Q1 doubts (00770, 01201, 01626), Q3 (GPT) unreviewed; Q4 reviewed in REVIEW5-Q4 (1 fix, 5 doubts).
`- BUILD-10: installed, in-game check pending (the 19 changed rows); publish waits for the supervisor. Still open as before; GPT Q3 rows outside the 19 ids (10882, 10883, 11500 and the rest) are not applied.
- BUGFIX-1 (BUILD-11 installed): look at the native quit box in game (which of title / question / Yes / No now read correctly; Yes / No expected still reversed, shared with Scaleform) and decide the buttons (options in `state\LAST_REPORT.md`); 15999 is a best guess for the title (save_0010 / 13961 are the alternatives); 09247 (Rapunzel "It's chilly") in `review\BUGFIX1_WATER.md`; the installed I0013 texture still shows the old label (repaint pending).
`- REVIEW5-Q1: public FAQ.md line 6 reworded (REMOVE_AR.bat no longer mentioned; closed). Open: the 9 Q1 fixes (`review\corrections\applied\review5_q1_*.tsv`) wait for BUILD-9 together with the 5 BUILD9_proposed rows and the accepted GPT Q2 fixes; 3 Q1 doubts in `review\REVIEW5_Q1_QUESTIONS.md` (00770, 01201, 01626) need the supervisor; Q4 was reviewed in REVIEW5-Q4; Q3 is GPT's and still unreviewed.
`- PUBLISH-090: README lines 49 / 59 accepted and published; 0.9.0 pre-release is live. Open: in-game check of the 2 new textures, Linux runtime, DECIDE-19.
`
`- DECIDE-19: supervisor to confirm or overrule `review\DECISIONS_ANSWERED.md` and say which rows of `review\proposed\BUILD9_proposed.tsv` become corrections (10847 plural form "5 حروف"..."5 أحرف", 14238 title width not yet seen in game). 10 items stay LEAVE (need new wording from the supervisor: 11946, 03280, 03556, 03566, 07579, 04052, 00331, 10348, Tangled 15281; 02369 already resolved).
`
`- INSTALL-8: BUILD-8 + IMAGES-MASS2 installed; in-game check pending (5 yes/no lines in `technical\IMAGES_MASS2_CHECKLIST.md`); publish / 0.9.0 waits for the supervisor.
`
`- OPUS-090 (install done in INSTALL-8): the 24 new image strings I0019-I0042 need a read-through (e.g. انتهى! for FINISH, اكتمل! for CLEAR!, خفيف جدا / قوي جدا for the cooking pressure grades); the 100 Acre Wood SUMMARY plank sign is now plain Arabic lettering; the large COMPLETE box in HudSnowSlide_text1 has no sprite found in the movie (box set by hand). Linux installer still unrun on Linux; real install/remove with the installer not run. Graphify graph is a snapshot older than OPUS-090. The 19 DECISIONS_NEEDED items and 64 context items stay open (not decided).
`
`- README-POLISH: no new open questions; game verification and Linux runtime verification remain pending as previously documented.
`
`- INSTALLER-CROSSPLATFORM: Linux runtime and real install/remove checks remain pending; preserve BUILD-7 and previous release assets. Full linguistic review remains complete 4/4.
`
`
`- CODEX-REVIEW4-4: 24 context-dependent rows are listed in the batch report; changes need later build/screenshot checks.
`
`- CODEX-REVIEW4-3: 14 context-dependent rows are listed in the batch report; changes need later build/screenshot checks.
`
`- CODEX-REVIEW4-2: 12 context-dependent rows are listed in the batch report; changes need later build/screenshot checks.
`
`- CODEX-REVIEW4-1: 14 context-dependent rows are listed in the batch report; changes need later build/screenshot checks.
`
`- **CODEX-REVIEW4:** scene-dependent questions are recorded per batch in `review/codex_full_review/batch_N/unsure.tsv`. Only resolved linguistic errors are applied; screenshot verification remains separate. A full Claude handoff is written after batch 4.
`
`- README-AR: the Arabic wording of README, TESTER_GUIDE, FAQ and the 0.8.3 notes is waiting for the user's read-through. Releases 0.8.0-0.8.2 keep their old Arabic+English notes (not English-only, so not edited). Remaining English prose in public files (PROJECT_MAP, CHANGELOG, state/PROGRESS, docs/rounds, technical docs, review/RULES, docs/INDEX, docs/SUPERVISOR): translate, or accept as developer docs?
`
`- FINISH-TRANS: add HDR/LOD/DOF/FXAA/TXAA etc. to `allowed_latin.txt`? ("Tangled"..."id A"..."id B"; incl. 10847 numerals vs characters [LIGHT-3 evidence: recommend B], 14238, 11946, 16892, 02369, 10694, Tangled). Public repo is behind the private one (CHANGELOG, PROJECT_MAP, STATS, stats.py differ; 4 new files); sync only when the user says publish. Installer 0.9.0 checkbox: plan only.
`
`- Cloud review: done and merged (6 PRs, synced in SYNC-BUILD7). Open: unsure items in `review\UNSURE_CLOUD.md` and tool bugs in `review\CLOUD_BUGS.md` (supervisor to read); the parallel cloud branches corrected some ids twice (handled by `apply_corrections`, section 4).
`- BUILD-7 / 0.8.2 screenshots (`technical\BUILD7_CHECKLIST.md`, 4 places). Still open from BUILD-6 (`technical\BUILD6_CHECKLIST.md`, 6 places) and BUILD-5 (`technical\BUILD5_CHECKLIST.md`, 8 places; incl. level-up line 15964, rows 01091/05448, party card level label): subtitle line order and 3-line rows (03474, 03581, 06647), field voice in the Subtitle field (assumed), save card and gummi LV labels; from BUILD-3: party-card مستوى and help boxes still unconfirmed. Swap scripts run from Git Bash print harmless `find` errors in the game-running check (Git's `find` shadows Windows `find`): run them from cmd.
`- Row 15964 (LV UP!) is installed (BUILD-5/6) (1,067 of 1,621 units in HudRight #109); confirm by screenshot. Supervisor review still open: lyrics (own MSA wording), the Re Mind batch. (Unsure rows decided in REVIEW-3; row 05051 fixed and installed in FINAL-1; 01302/01304 addressee gender not clear from the script, left feminine.)
`- Row 05955 uses the feminine «حاملة كيبلايد» (glossary second form); its GLOSS warning is accepted.
`- Field guesses to confirm in-game: field/battle voice = Subtitle #1; 49 "(EN widest)"..."Supervisor test report" in the checklist) and the 6 screenshots (`technical\IMAGES_MASS_CHECKLIST.md`) and the user's verdict (0.9.0 waits). Open: 16 minigame HUD textures not yet repainted; 47 styled logos (plain Arabic vs. effect layers); Kairi HUD name over an ornament; 18 new image strings (`translation\images_strings.tsv`, status translated) need review; the ps4 copy of HelpItem30402 is not repainted (layout differs, PC loads the windows copy); 3D map signage and videos not covered.
`- `؟` still unproven (ASCII `?` kept, now a validator ERR); tutorial control lists in the flush-left Game Help field.
`- Glossary: Tangled = متشابك (supervisor to verify); 51 TRANS-3 proposed terms; tutorial line "جرب إلقاء نار" keeps the bare command name.
`- Installer is unsigned (SmartScreen warning); no art file supplied yet (`tools\installer\art\`); Epic detection is tested on fake files only.
`- Publishing: license undecided (`LICENSE_TODO.md`); the GitHub repo still carries its default GPL v2 `LICENSE` (kept, not our decision); credits list in the public README is a placeholder.
`- GPT unsure list (in-game checks): `review\gpt\UNSURE_batch1.md` (local, untracked).
`- Re Mind (TRANS-5): hashtags now Arabic (TRANS-6); music titles transliterated; spirit names transliterated like Necho Cat (13 proposed glossary terms); Action pose category = الحركة (TRANS-6); Re Mind menu/Data Greeting/Slideshow screens not yet seen in-game.
`- Typo WARN 15203: «بلغ المعلمان» is past tense (reached), a false positive of the sentence-start «بلغ» pattern; left as is.
`
`## 9. Round history (auto)
`
`- 2026-10-08 **RECON-1** (3 entries) — last: T3-6 BLOCKED on AES decision; T7 ~mods + _P documented, _0_P conflict; T8 RECON_KH3.md written. STOP: ask user.
`- 2026-10-08 **RECON-2** (18 entries) — last: T6 STOP: report in state\LAST_REPORT.md; no blockers.
`- 2026-10-08 **PIPE-1** (18 entries) — last: STOP: all 6 tasks PASS/DONE; report in state\LAST_REPORT.md; no blockers.
`- 2026-10-08 **ARABIC-TEST-1** (3 entries) — last: install: no ~mods/old pak found (empty "mods"..."ORG-1: project structure"..."ORG-2: markdown review, corrections tool".
`- 2026-10-08 **ARABIC-TEST-2** (24 entries) — last: STOP: F1 installed, waiting for F1/F2 screenshots; report in state\LAST_REPORT.md.
`- 2026-10-08 **GLOSS-1** (24 entries) — last: STOP: committed "..."; report in state\LAST_REPORT.md.
`- 2026-10-08 **GLOSS-2** (6 entries) — last: T5 close: refresh.bat exit 0 (validate 0 ERR), secret_check PASS, PROJECT_MAP 3/4/8 + CHANGELOG updated; committed.
`- 2026-10-08 **TRANS-1** (44 entries) — last: STOP: final refresh.bat + secret_check, commit "..."; report in state\LAST_REPORT.md.
`- 2026-10-08 **TRANS-2** (32 entries) — last: STOP: final refresh.bat + secret_check, commit "..."; report in state\LAST_REPORT.md.
`- 2026-10-09 **SWAP-1** (9 entries) — last: T3 STOP: report in state\LAST_REPORT.md.
`- 2026-10-09 **TEST50** (21 entries) — last: STOP: TEST50 installed, waiting for screenshots per technical\TEST50_CHECKLIST.md.
`- 2026-10-09 **TRANS-3** (12 entries) — last: open: conv-group rows, hashtag style, 52 proposed terms.
`- 2026-10-09 **BUILD-1** (15 entries) — last: STOP: BUILD-1 installed, waiting for screenshots per technical\BUILD1_CHECKLIST.md.
`- 2026-10-09 **FULL-1** (21 entries) — last: STOP: BUILD-2 installed, waiting for screenshots per technical\BUILD2_CHECKLIST.md and the LV / alignment decisions.
`- 2026-10-09 **TRANS-4** (103 entries) — last: STOP: BUILD-3 installed, waiting for screenshots per technical\BUILD3_CHECKLIST.md; story text translated (88.8 %); next: Re Mind batch, BUILD-4.
`- 2026-10-09 **REVIEW-1** (24 entries) — last: T8 close: Commit: REVIEW-1: GPT review batch 1 applied.
`- 2026-10-09 **TRANS-6** (3 entries) — last: T3-T5: validator WARN HASHTAG + test; refresh.bat 0 ERR, secret_check PASS; commit TRANS-6.
`- 2026-10-09 **BUILD-4** (14 entries) — last: STOP: commit "..."; waiting for screenshots per technical\BUILD4_CHECKLIST.md and the 15964 / HudRight #109 decision.
`- 2026-10-10 **REVIEW-2** (37 entries) — last: stats: reviewed 95.3 percent (16,414 of 17,222).
`- 2026-10-10 **BUILD-5** (4 entries) — last: T4 close: refresh 0 ERR, secret_check PASS, PROJECT_MAP 3 4 6 7 8 + CHANGELOG, commit.
`- 2026-10-10 **PUBLISH-1** (6 entries) — last: T8 close: refresh 0 ERR, secret_check PASS, private commit (no push).
`- 2026-10-10 **RELEASE-080** (3 entries) — last: T3 release prep: gh 2.102.0 official zip (sha ae64e556...) in tools\gh-2.102.0, not logged in; assets + RELEASE_NOTES.md ready; waiting for user gh auth login.
`- 2026-10-10 **REVIEW-3** (3 entries) — last: T8 close: refresh, secret_check, PROJECT_MAP 3 4 8 + CHANGELOG, private commit. BUILD-6 / v0.8.1 needed to install.
`- 2026-10-10 **FINAL-1** (28 entries) — last: DONE; next: user screenshots of the pilot, then IMAGES-MASS -> 0.9.0 -> screenshots -> 1.0.0.
`- 2026-10-10 **CLOUD-PREP** (27 entries) — last: DONE.
`- 2026-10-10 **SYNC-BUILD7** (5 entries) — last: T5 release 0.8.2 (pre-release): 5 assets, sizes/SHA256 match SHA256SUMS.txt (gh release view).
`- 2026-10-10 **IMAGES-MASS** (8 entries) — last: close: pak 233ef228 installed (SWAP_TO_IMAGES_MASS.bat), checklist, stats 193/234 = 82.5 %, refresh 0 ERR. RESUME IMAGES-MASS: cat 1b minigame HUDs (16, see technical\IMAGES_STILL_ENGLISH.tsv 'not yet'), then rebuild (texture_text.py mass), update the pinned sha in tools\make_swap_scripts.py, reinstall.
`- 2026-10-11 **README-AR** (1 entries) — last: public README, TESTER_GUIDE, FAQ, issue template, LICENSE_TODO and release 0.8.3 notes are Arabic only; make_public.py + README template generate them; PROJECT_MAP/CHANGELOG updated.
`- 2026-10-13 **CODEX-REVIEW4-1** (3 entries) — last: checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.
`- 2026-10-13 **CODEX-REVIEW4-2** (3 entries) — last: checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.
`- 2026-10-13 **CODEX-REVIEW4-3** (3 entries) — last: checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.
`- 2026-10-13 **CODEX-REVIEW4-4** (3 entries) — last: checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.
`- 2026-10-13 **INSTALLER-CROSSPLATFORM** (3 entries) — last: publish: update current 0.8.3 with additive installer assets; preserve all previous release assets.
`- 2026-10-13 **README-POLISH** (3 entries) — last: publish: update generator template and both README copies; documentation only.
`- 2026-10-13 **OPUS-090** (4 entries) — last: D/E: PROJECT_MAP 3/4/8, CHANGELOG, README template (0.9.0, BUILD-8), make_public temp run + public_check PASS, vault notes; refresh 0 ERR, secret_check PASS; private commit. RESUME: user installs BUILD-8 (+ IMAGES-MASS2) from cmd and confirms -> build_build8.py --installed -> publish.bat -> gh release create 0.9.0 (commands in state\LAST_REPORT.md).
`- 2026-10-13 **RELEASE-090** (5 entries) — last: 6/7: docs\ROADMAP_TO_1.0.0.md (Arabic), PROJECT_MAP 3/4/8, CHANGELOG; refresh, secret_check, private commit. RESUME: user says yes/no to README lines 49/59 -> (no: revert those 2 template lines) -> tools\refresh.bat -> tools\publish.bat -> gh release create 0.9.0 --prerelease with the 5 assets of out\release\v0.9.0 (command in state\LAST_REPORT.md).
`- 2026-10-13 **REVIEW5-Q1** (3 entries) — last: 3: no build, no install, no release (fixes wait for BUILD-9); PROJECT_MAP 3/4/8, CHANGELOG, refresh, secret_check PASS, private commit REVIEW5-Q1, publish (FAQ + generated docs). RESUME: BUILD-9 takes review5_q1 fixes + 5 BUILD9_proposed rows + accepted GPT Q2 fixes.
`- 2026-10-14 **RELEASE-091** (3 entries) — last: 4-7 installer 0.9.1 (BUILD-10 + IMAGES-MASS4) win-x64 + linux-x64, 37/37 selftest PASS; out\release\v0.9.1 (5 assets + Arabic notes); README 5 value/link lines only ({{BUILD}} placeholder), public_check PASS on TEMP; refresh 0 ERR, secret_check PASS, publish.bat, pre-release 0.9.1; PROJECT_MAP 3/4/8, CHANGELOG, ROADMAP status. RESUME: in-game check of the Kairi name and the 42 changed rows; decision on the 522 earlier image boxes under the readability bar.
`
`## 10. Public repository
`
`- **URL:** https://github.com/exelight7/KH3RM_AR (branch `main`; pushing and Releases there are approved, standing, for this one repository only; never force-push; no other remote).
`- **Public:** README, PROJECT_MAP/CHANGELOG copies, docs, technical docs, `state\STATS.md` + `PROGRESS.md`, `translation\ar\<category>\*.tsv` (Arabic only: id, namespace, key, source_hash, AR, status, note), glossary, `review\RULES.md`, our scripts in `tools\`, swap/install `.bat` files; the built pak only as a GitHub Release asset.
`- **How to publish:** after `tools\refresh.bat` and `tools\secret_check.py` pass and sections 3, 4, 7, 8 are updated, run `tools\publish.bat` (make_public.py, public_check.py, commit `sync: <round>` in `public_repo\`, push). `public_repo\` is gitignored here. Authentication is done by the user in the browser (Git Credential Manager).
`- **Release:** `python -I tools\make_release.py BUILD-N` fills `out\release\` (pak, SHA256.txt, INSTALL_AR.bat, REMOVE_AR.bat, AR_MESSAGES.txt); create it only when that BUILD is installed and its checklist screenshots were reviewed by the supervisor.
`
`## تسليم المراجعة الكاملة
`
`اكتملت 4/4 ونشرت كل دفعة؛ اقرأ review/codex_full_review/HANDOFF.md وdocs/rounds/CODEX-REVIEW4-HANDOFF.md. التصحيحات في المصدر تحتاج بناء والتحقق داخل اللعبة.
