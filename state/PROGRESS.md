2026-10-08 RECON-1 T1 install: KH3+ReMind app 2552450 build 14790811, 67 GiB, 142 pak v4, no ~mods.
2026-10-08 RECON-1 T2 engine: UE 4.17 custom, pak v4, AES-encrypted index on all paks; community key route documented, not used.
2026-10-08 RECON-1 T3-6 BLOCKED on AES decision; T7 ~mods + _P documented, _0_P conflict; T8 RECON_KH3.md written. STOP: ask user.
2026-10-08 RECON-2 T1 result: 555,921 entries -> extracted\pak_index.tsv (counts match repak list); only index + 71 .ini encrypted.
2026-10-08 RECON-2 T1 Re Mind: text in pakchunk0 *_dlc.locres; data mainly pakchunk1_s11/19/20/46/48/49/51/54 + voice_7_P -> extracted\remind_map.tsv.
2026-10-08 RECON-2 T2 text: 627 locres + 13 locmeta exported to extracted\locres\ (original paths, sizes match); none in _0_P paks.
2026-10-08 RECON-2 T2 cultures: ja(native) en fr it de es ko zh-Hant, no unused slot; en = 67 files, 17,222 entries, 125,538 words -> technical\TEXT_COUNTS.tsv.
2026-10-08 RECON-2 T2 parser: tools\locres.py round-trip 627/627 byte-identical; StringTables none; 2 culture DataTables.
2026-10-08 RECON-2 T3 fonts: UI/subtitles = Scaleform GFx TresFont (pakchunk0 + ko/zh-Hant variants), aliases $sougei/$jimakuNE/$JimakuJP/$KH2Menu.
2026-10-08 RECON-2 T3 Arabic: 0 Arabic glyphs in all 10 game fonts (only engine Slate fallback NotoNaskhArabicUI, unused by UI).
2026-10-08 RECON-2 T3 plan: Segoe UI Regular (sha256 8134dbcd...) into rebuilt TresFont; pre-shaped reversed text; recorded, not copied.
2026-10-08 RECON-2 T4 tags: <br> <i(on/off)> <icon(X)> <color(X)>..<color> <pb(s)> <b> <nbsp> <conv> {0-4} |plural.
2026-10-08 RECON-2 T4 examples: 20 real strings with file|namespace|key -> technical\TAGS.md.
2026-10-08 RECON-2 T4 validator rule written (TAGS.md section 3) for PIPE/translation rounds.
2026-10-08 RECON-2 T5 images: Localization/en/TexturePump absent; ja TexturePump = streaming lists, no images.
2026-10-08 RECON-2 T5 count: 212 en text textures: logo 25, title 26, menus 2, tutorial 150, other 9.
2026-10-08 RECON-2 T5 not counted: bitmaps baked in Scaleform movies (title logo etc.), UNVERIFIED.
2026-10-08 RECON-2 T6 RECON_KH3.md rewritten: sections 3-6 VERIFIED, font decision Segoe UI Regular, Noto/OFL mention removed.
2026-10-08 RECON-2 T6 PIPE-1 plan: TSV import, TSV-level byte-identical check, test pak v4 + hash check, TresFont container round-trip.
2026-10-08 RECON-2 T6 STOP: report in state\LAST_REPORT.md; no blockers.
2026-10-08 PIPE-1 T1 TSV: tools\locres.py tsv-export/tsv-import; translation\en_source.tsv = 67 en files, 17,222 rows (namespace,key,source_hash,text,category,file).
2026-10-08 PIPE-1 T1 rebuild: all 627 locres rebuilt from out\builds\PIPE-1\tsv\all_627.tsv (+67 from en_source.tsv) -> 627/627 SHA256 identical, PASS.
2026-10-08 PIPE-1 T1 decision: original locres = structure template (order, 1,175 empty namespaces, UTF-16 flags); TSV supplies text, hash is checked not rewritten.
2026-10-08 PIPE-1 T2 edits: kh3_menu.title/menu_0002 NEW GAME, kh3_tutorial.tut/title_0010 TUTORIALS, kh3_event_bt.bt001a/op0010010sr0_1 -> [AR-TEST-1..3].
2026-10-08 PIPE-1 T2 build: out\builds\PIPE-1\artest\en_artest.tsv -> artest\pakroot\ (67 en locres, original mount paths).
2026-10-08 PIPE-1 T2 verify: re-parse of all 67 files -> exactly 3 entries differ (3 files), keys/hashes/order/UTF-16 flags unchanged, PASS.
2026-10-08 PIPE-1 T3 game paks: all 142 v4, Zlib; locres pak pakchunk0 mounts ../../../ (paths KINGDOM HEARTS III/Content/...) -> out\builds\PIPE-1\game_pak_mounts.tsv.
2026-10-08 PIPE-1 T3 pak: repak 0.2.3 pack V4/Zlib/mount ../../../ -> out\builds\PIPE-1\pakchunk99-artest_P.pak (67 en locres, 881,923 B, sha256 0b5dd910...).
2026-10-08 PIPE-1 T3 verify: list 67 entries, hash-list + unpack SHA256 = inputs 67/67 PASS; index unencrypted (mods need no key: DOC, UNVERIFIED). Not installed.
2026-10-08 PIPE-1 T4 TresFont: tools\tresfont.py parses uasset/uexp/GFX/DefineCompactedFont down to glyph edges; 3 files (6 parts) rebuilt byte-identical, PASS.
2026-10-08 PIPE-1 T4 format: glyph = SInt15 bbox, contours of H/V/L/C edges (4-bit type, 2-8 B), 256 units/em; our encoder matches SE's edge choice on 4.3M edges (100%).
2026-10-08 PIPE-1 T4 Arabic size: Segoe UI U+0600-06FF/FB50-FDFF/FE70-FEFF/digits = 585 glyphs ~88 KB per font; TresFont ~4.35 -> ~4.53 MB, fits a ~mods pak.
2026-10-08 PIPE-1 T5 spec: technical\SHAPER_SPEC.md: tokenizer (atoms/style tags), forms + lam-alef, UAX#9 RTL per line, style re-emit, plural, own line breaking.
2026-10-08 PIPE-1 T5 tests: 12 core unit tests + 22 tag tests from TAGS.md examples (T1-T20 + Re<icon>Mind, nbsp).
2026-10-08 PIPE-1 T5 open: engine word-wrap/alignment with reversed text, plural rules for culture en -> ARABIC-TEST.
2026-10-08 PIPE-1 T6 RECON_KH3.md: mount points, Paks full path, §9 PIPE-1 results (TSV, pak, TresFont format/size), §10 LOAD-TEST click-by-click.
2026-10-08 PIPE-1 T6 next: LOAD-TEST by user (copy pak to ~mods, screenshots S1-S3, remove); then ARABIC-TEST + build tools\shaper.py.
2026-10-08 PIPE-1 STOP: all 6 tasks PASS/DONE; report in state\LAST_REPORT.md; no blockers.
2026-10-08 ARABIC-TEST-1 build: tools\shaper.py (forms, lam-alef, RTL, tests PASS); 189 Segoe UI glyphs added to TresFont $sougei only (0 existing changed).
2026-10-08 ARABIC-TEST-1 paks: NEW GAME = لعبة جديدة as A visual / B logical / C shaped-unreversed; 3 entries each, SHA256 9/9 PASS, only 1 locres entry + $sougei differ.
2026-10-08 ARABIC-TEST-1 install: no ~mods/old pak found (empty "mods" only) -> created ~mods, copied A (sha c776c2f9...); checklist RECON §11; STOP for screenshots.
2026-10-08 ORG-1 T1-T3 translation\<cat>\<file>.tsv (73 files, 17,222 rows, id=5-digit game order); merge_translation.py --check byte-identical PASS; validate.py + 6 unit tests PASS; make_review.py -> review\html.
2026-10-08 ORG-1 T4-T6 stats.py -> state\STATS.md; SCREENSHOT_LOG.tsv (LOAD-TEST id 13770 PASS); tools\refresh.bat; README (AR/EN), CHANGELOG, docs\INDEX, review\RULES, glossary template, LICENSE_TODO.
2026-10-08 ORG-1 T7-T8 git init local, .gitignore + secret_check.py PASS (129 tracked), commit "..."; refresh.bat run OK. STOP.
2026-10-08 ORG-2 T1 HTML removed: review\html deleted + untracked, make_review.py HTML code gone; no-HTML rule in review\RULES.md and docs\INDEX.md; README links fixed.
2026-10-08 ORG-2 T2-T3 make_review.py -> review\md\<cat>_NN.md (61 pages, 300 rows, largest 87,313 B), review\INDEX.md, review\FLAGS.md (0 flagged, nothing translated yet).
2026-10-08 ORG-2 T4-T5 apply_corrections.py + 4 unit tests PASS, in refresh.bat before validate; screenshots\ gitignored, naming rule in RULES.md, LOAD-TEST file = unrecorded.
2026-10-08 ORG-2 T6 refresh.bat exit 0, secret_check PASS; committed "...".
2026-10-08 ARABIC-TEST-2 T1 screenshot: SCREENSHOT_LOG.tsv + ARABIC-TEST-1 / 13770 / 20261008_ARABIC-TEST-1_01.png / PASS joins+RTL+no boxes, FAIL gaps + small size.
2026-10-08 ARABIC-TEST-2 T1 stats: id 13770 status verified (AR لعبة جديدة as seen in-game), counted as verified-by-screenshot.
2026-10-08 ARABIC-TEST-2 T1 note: the png is not in screenshots\ yet (user to copy it there).
2026-10-08 ARABIC-TEST-2 T2 measure: tools\gfx_edittext.py on live Title (s5_0_P), GameHelp (s7_0_P), SettingMenu (s58_0_P) -> out\builds\ARABIC-TEST-2\ref\edittext_fields.tsv (61 fields).
2026-10-08 ARABIC-TEST-2 T2 result: only Title field 61 (menu items, $sougei 30 pt) has letterSpacing 2.00; all others 0; no ActionScript sets letterSpacing.
2026-10-08 ARABIC-TEST-2 T2 hypothesis CONFIRMED: 2 px / 30 pt em = 17.07 TresFont units per glyph vs Segoe join tip 8.75 units (tapered) -> 1-2 px gaps.
2026-10-08 ARABIC-TEST-2 T3 join fix: 46 initial/medial forms get an 18-unit straight stroke before the join tip (same y -14..153, baseline); lam-alef unchanged (never joins left).
2026-10-08 ARABIC-TEST-2 T3 fonts: Arabic also added to $KH2Menu (id 4: GAME SETTINGS header + GameHelp symbols), scale x204/174 to match its caps; 189 glyphs per font.
2026-10-08 ARABIC-TEST-2 T3 check: tresfont.ttf_glyphs edit hook keeps ARABIC-TEST-1 font byte-identical; preview_text.py: TEST-1 17 pinched columns, F1 none.
2026-10-08 ARABIC-TEST-2 T4 translate: 34 rows status translated (30 kh3_menu.title, 4 kh3_settings.top), tags/icons kept; validate 0 flags.
2026-10-08 ARABIC-TEST-2 T4 scope: all title menu items + help lines except Re Mind menu items (logo with icons, kept EN); GAME SETTINGS, button_0010/0020/0050.
2026-10-08 ARABIC-TEST-2 T4 rule: "ReMind" added to translation\allowed_latin.txt (visible text of Re<icon(..)>Mind); help lines listed in LAST_REPORT for review.
2026-10-08 ARABIC-TEST-2 T5 build: tools\build_arabictest2.py -> pakchunk99-arabictest2F1_P.pak (302d95d1..., 3,694,281 B) and F2 x1.15 (5e60bd3a..., 3,694,678 B).
2026-10-08 ARABIC-TEST-2 T5 verify: list/hash-list/unpack SHA256 8/8 PASS; 30+4 entries changed only; fonts 3/4 gained only new codes; F1 vs F2 locres identical.
2026-10-08 ARABIC-TEST-2 T5 install: arabictest1 moved ~mods -> out\builds\old (c776c2f9... before/after); F1 copied to ~mods (302d95d1... both); only one pak of ours.
2026-10-08 ARABIC-TEST-2 T6 markdown: make_review.esc escapes \ ` * _ | < (backslash first); self-check in make_review.py.
2026-10-08 ARABIC-TEST-2 T6 pages: review\md regenerated, 61 pages; game text with * _ ` no longer renders as formatting.
2026-10-08 ARABIC-TEST-2 T6 scope: EN and AR columns both escaped; FLAGS.md uses the same esc().
2026-10-08 ARABIC-TEST-2 T7 map: PROJECT_MAP.md (9 sections) at root; docs\SUPERVISOR.md = full copy of this round's supervisor instructions.
2026-10-08 ARABIC-TEST-2 T7 tool: tools\update_map.py rewrites only "(auto)" sections (folder map, numbers from STATS.md, round history); in refresh.bat after stats.
2026-10-08 ARABIC-TEST-2 T7 rule: docs\INDEX.md + review\RULES.md: every round updates PROJECT_MAP.md sections 3, 4, 8 before stopping.
2026-10-08 ARABIC-TEST-2 T8 checklist: RECON_KH3.md §12 (fields table, fix, paks, click-by-click F1 -> F2 -> remove).
2026-10-08 ARABIC-TEST-2 T8 refresh.bat + secret_check run; commit "...".
2026-10-08 ARABIC-TEST-2 STOP: F1 installed, waiting for F1/F2 screenshots; report in state\LAST_REPORT.md.
2026-10-08 GLOSS-1 T0 file fix: KH2 glossary already at translation\kh2_glossary.md (untracked, sha 48a21ee6...), rename not needed; glossary.md restored from HEAD (sha 0b3c484f...).
2026-10-08 GLOSS-1 T0 check: kh2_glossary.md = Arabic KH2FM glossary (1,282 lines); git status D glossary.md resolved; nothing else in translation\ touched.
2026-10-08 GLOSS-1 T0 note: glossary.md was later regenerated by tools\make_glossary.py (final sha 55b0cdd1...).
2026-10-08 GLOSS-1 T1 glossary.tsv: tools\import_kh2_glossary.py -> 1,006 KH2 entries (956 approved, 50 pending); 74 descriptive/compositional KH2 rows skipped (stay in kh2_glossary.md).
2026-10-08 GLOSS-1 T1 counts: tools\make_glossary.py fills kh3_count + 3 example ids (whole word, any case, rows) and writes glossary.md (tables by type, approved first).
2026-10-08 GLOSS-1 T1 result: 600 of 1,234 entries found in KH3 EN; make_glossary added to refresh.bat.
2026-10-08 GLOSS-1 T2 rules: KH2-only rules section in glossary.md and review\RULES.md (Latin bans, ، ؟, ya rule, <X 5E>, LV->مس, width shortenings, forced transliterations).
2026-10-08 GLOSS-1 T2 pending: 22 entries with note "..." (Organization XIII, LV, MCP, DTD, FPS Mode, Munny, Journal, ...).
2026-10-08 GLOSS-1 T2 open check: Arabic comma/question mark only after a screenshot; ASCII , ? until then (PROJECT_MAP §8).
2026-10-08 GLOSS-1 T3 conflicts: translation\GLOSSARY_CONFLICTS.md, 16 same-EN conflicts (14 open, 2 resolved by KH2 decision table) + 14 cross-entry/typo items.
2026-10-08 GLOSS-1 T3 examples: Munny مال/موني, Destiny Islands المصير/القدر, Hollow Bastion, Olympus أولمبيا, Piglet بيركيت typo, Auto آلي/تلقائي, Postern.
2026-10-08 GLOSS-1 T3 state: all conflict forms status pending; recommendations follow rule order; nothing decided.
2026-10-08 GLOSS-1 T4 title rows: review\corrections\gloss1_title.tsv applied: 13772, 13775 CONFIG الخيارات -> الضبط; 13801 كينغدم -> كينغدوم هارتس.
2026-10-08 GLOSS-1 T4 status kept (translated); 13770 untouched (verified); validate 34 checked, 0 flags.
2026-10-08 GLOSS-1 T4 glossary: Kingdom Hearts and Config approved (user decision); Option stays الخيارات.
2026-10-08 GLOSS-1 T5 proposals: 212 KH3-new + 16 Re Mind terms (characters, worlds, places, Keyblades, magic, systems) in glossary.tsv, status proposed, one Arabic + reason each.
2026-10-08 GLOSS-1 T5 candidates from char_name/map/item/command keys + capitalized EN n-grams (938 candidates >=3 rows); translation\GLOSSARY_PROPOSALS.md generated, sorted by count.
2026-10-08 GLOSS-1 T5 top: Darkness 175, Light 169, Organization 127, Terra 95, Rapunzel 92, Combo 86, Boo 79, Ansem 75.
2026-10-08 GLOSS-1 T6 validator: WARN GLOSS (approved non-menu term in EN as written or ALL CAPS, Arabic missing; leading ال optional; ambiguous one-word terms skipped).
2026-10-08 GLOSS-1 T6 tests: test_validate.py test_gloss (13 asserts) PASS, 7/7 tests OK; old 13801 text would flag GLOSS, new text clean.
2026-10-08 GLOSS-1 T6 scale: 667 approved terms checked per row via first-word index; full validate < 1 s.
2026-10-08 GLOSS-1 T7 screenshot policy: RULES.md + PROJECT_MAP §4; SCREENSHOT_LOG ARABIC-TEST-1 file -> chat.
2026-10-08 GLOSS-1 T7 PROJECT_MAP §3, §4, §8 updated; CHANGELOG; refresh.bat exit 0; secret_check PASS.
2026-10-08 GLOSS-1 STOP: committed "..."; report in state\LAST_REPORT.md.
2026-10-08 GLOSS-2 T1 decisions: A, B and C applied to glossary.tsv (3 rows removed, 228 proposals approved, notes tagged); allowed_latin.txt + XIII; rules text updated.
2026-10-08 GLOSS-2 T1 result: 1,231 entries = 1,190 approved, 41 pending, 0 proposed; GLOSSARY_CONFLICTS.md resolved items marked + history.
2026-10-08 GLOSS-2 T2 corrections: 34 AR rows scanned, no retired form; review\corrections\gloss2.tsv header-only, 0 applied.
2026-10-08 GLOSS-2 T3 generated: glossary.md and GLOSSARY_PROPOSALS.md regenerated (proposals 0 + 0).
2026-10-08 GLOSS-2 T4 pending: 17 conflicts listed with recommendations in LAST_REPORT.md and GLOSSARY_CONFLICTS.md §4 (+15 KH2-constraint rows).
2026-10-08 GLOSS-2 T5 close: refresh.bat exit 0 (validate 0 ERR), secret_check PASS, PROJECT_MAP 3/4/8 + CHANGELOG updated; committed.
2026-10-08 TRANS-1 T1 glossary: 17 conflicts closed per supervisor (tools\gloss3_apply.py); Hollow Bastion/Destiny Islands/Limit/Lucky Lucky/Full Bloom approved; 10 KH2-constraint rows with 0 KH3 rows -> status kh2-only; Musical + Grind (KH3 rows) stay pending.
2026-10-08 TRANS-1 T1 tools: validate.py GLOSS accepts any approved form when one EN has several (Master/master); make_glossary knows kh2-only; tools\trans_page.py (dump/apply per page, translation memory for same EN).
2026-10-08 TRANS-1 T2 page 1/13 menus_ui translated (224 lines, ids 00001-00301): validate 0 flags.
2026-10-08 TRANS-1 T2 page 1 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 1 unsure rows: 4 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 2/13 menus_ui translated (ids 00302-00601): validate 0 flags (validator: longer glossary term covers a shorter one, e.g. Scrooge McDuck).
2026-10-08 TRANS-1 T2 page 2 tools: refresh.bat exit 0; character names from glossary; 4 unsure rows.
2026-10-08 TRANS-1 T2 page 2 unsure rows: 4 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 3/13 menus_ui translated (282 lines, first/last id 00602 10769 ): validate: 900 checked, 1 RATIO fixed-noted, 1 BR fixed; now 0 ERR
2026-10-08 TRANS-1 T2 page 3 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 3 unsure rows: 1 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 4/13 menus_ui translated (259 lines, first/last id 10770 11069 ): validate: checked=1193 flagged=5 errors=0
2026-10-08 TRANS-1 T2 page 4 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 4 unsure rows: 3 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 5/13 menus_ui translated (211 lines, first/last id 11070 11369 ): validate: checked=1489 flagged=30 errors=28
2026-10-08 TRANS-1 T2 page 5 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 5 unsure rows: 3 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 6/13 menus_ui translated (245 lines, first/last id 11370 13268 ): validate: checked=1788 flagged=1 errors=0
2026-10-08 TRANS-1 T2 page 6 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 6 unsure rows: 2 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 7/13 menus_ui translated (228 lines, first/last id 13269 13568 ): validate: checked=2058 flagged=2 errors=0
2026-10-08 TRANS-1 T2 page 7 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 7 unsure rows: 1 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 8/13 menus_ui translated (158 lines, first/last id 13569 13871 ): validate: checked=2267 flagged=2 errors=0
2026-10-08 TRANS-1 T2 page 8 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 8 unsure rows: 0 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 9/13 menus_ui translated (255 lines, first/last id 13873 14171 ): validate: checked=2558 flagged=5 errors=0
2026-10-08 TRANS-1 T2 page 9 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 9 unsure rows: 1 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 10/13 menus_ui translated (264 lines, first/last id 14172 14742 ): validate: checked=2856 flagged=7 errors=0
2026-10-08 TRANS-1 T2 page 10 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 10 unsure rows: 2 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 11/13 menus_ui translated (262 lines, first/last id 14743 15643 ): validate: checked=3137 flagged=8 errors=0
2026-10-08 TRANS-1 T2 page 11 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 11 unsure rows: 2 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 12/13 menus_ui translated (209 lines, first/last id 15644 15940 ): validate: checked=3401 flagged=9 errors=0
2026-10-08 TRANS-1 T2 page 12 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 12 unsure rows: 2 (note column starts with "unsure:").
2026-10-08 TRANS-1 T2 page 13/13 menus_ui translated (181 lines, first/last id 15946 16344 ): validate: checked=3601 flagged=9 errors=0
2026-10-08 TRANS-1 T2 page 13 tools: refresh.bat exit 0; same-EN rows filled from translation memory; empty/tag-only/symbol rows marked skip.
2026-10-08 TRANS-1 T2 page 13 unsure rows: 2 (note column starts with "unsure:").
2026-10-08 TRANS-1 T3 close: menus_ui 13/13 pages done; 3,567 new rows translated, 248 skipped (note skip:), 0 remaining; 73 coined terms added to glossary.tsv as proposed.
2026-10-08 TRANS-1 T3 close: GLOSSARY_CONFLICTS.md §4 rewritten (17 closed, Musical + Grind pending with recommendation); PROJECT_MAP §3 §4 §8 + CHANGELOG updated.
2026-10-08 TRANS-1 STOP: final refresh.bat + secret_check, commit "..."; report in state\LAST_REPORT.md.
2026-10-08 TRANS-2 P1 validator: LATIN = ERR if AR has a Latin/Greek/Roman token missing from the row's EN (tags count as word breaks); allowed_latin dependence removed (file kept as history); tests extended; RULES.md + glossary rules text updated.
2026-10-08 TRANS-2 P1 re-pass menus_ui: 190 rows restored to Latin per policy (acronyms, rank/set letters, sector codes, Greek, Roman numerals in titles, PlayStation, Epic Games, PC, CDA, AR, UFO, MVP, K.O., p, legal text with companies + URL rows); corrections trans2_latin*.tsv applied.
2026-10-08 TRANS-2 P1 re-pass kept Arabic on purpose: EXP = خبرة, LV = مستوى, EZ/PRO Codes (approved glossary), plain words in caps (ON, OFF, NEW GAME), character/place/dish names, km/mi, Alpha/Beta words.
2026-10-08 TRANS-2 P2 supervisor fixes: 14128, 14355, Heartless family, Flan = بودينغ, Surge = التسارع, Standard Mode = الوضع العادي, Teeny Ship α/β, Musical = موسيقي, Grind = طحن; AP/CDA rows dropped, all other proposed terms approved; Stock = المخزون and Warp = انتقال سريع added as approved forms.
2026-10-08 TRANS-2 P2 applied via review\corrections\trans2.tsv (26 rows) + trans2_fix.tsv; refresh.bat exit 0, validate 0 ERR.
2026-10-08 TRANS-2 P3 page 1/8 items_abilities translated (300 rows, ids 11379-11678, gummi block names + /G /M /P codes verbatim): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 1 tools: refresh.bat exit 0; trans_page.py got --cat= and cross-category translation memory; tools\gloss_hits.py lists glossary terms in a dump.
2026-10-08 TRANS-2 P3 page 1 unsure: gummi part words without glossary entries (Vernier, Radome, Parabola, Typhoon/Hurricane/Tempest, Chocochick, Plush, Dazzle).
2026-10-08 TRANS-2 P3 page 2/8 items_abilities translated (ids 11679-11978: sticker/ship/upgrade names, gummi descriptions): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 2 tools: refresh.bat exit 0; /S /P codes, VGA/SRS/STR, SW, HP, T- prefix kept Latin as in EN; LV written مستوى.
2026-10-08 TRANS-2 P3 page 2 unsure: ship names (Highwind/Falcon/Invincible transliterated), Craft Airplane, Peak = الذروة, Flank = هجوم جانبي.
2026-10-08 TRANS-2 P3 page 3/8 items_abilities translated (ids 11979-12278: gummi part descriptions, ship blueprints, first weapons from the glossary): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 3 tools: refresh.bat exit 0; helper scratch scripts read the glossary for item names; 150 rows skipped (empty/symbols).
2026-10-08 TRANS-2 P3 page 3 unsure: Heartless in descriptions written البلا قلب (article, supervisor pattern); Heart of a Hero = قلب البطل (not in glossary).
2026-10-08 TRANS-2 P3 page 4/8 items_abilities translated (ids 12279-12578: keyblade formchange lines, staffs, shields, armor, accessories, battle items): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 4 tools: refresh.bat exit 0; the 80 "..." lines generated from one template (amount words slight..incredible = طفيفة..مذهلة) with <br> count kept.
2026-10-08 TRANS-2 P3 page 4 unsure: "Resistance" = مقاومة (no glossary entry); Master Belt/Ring = السيد; Force Ring = خاتم الطاقة; Flanniversary Badge = شارة ذكرى البودينغ.
2026-10-08 TRANS-2 P3 page 5/8 items_abilities translated (ids 12579-12878: materials, synthesis-material lines, ingredients, dishes, key items): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 5 tools: refresh.bat exit 0; Crystal = بلورة (glossary Twilight Crystal) so 12577 fixed via trans2_p4fix.tsv; dish names reuse menus_ui Arabic (+ kept).
2026-10-08 TRANS-2 P3 page 5 unsure: material adjectives (Betwixt = برزخية, Writhing = متلوية, Lucid = صافية), Heartbinder = رابط قلب, Damascus = الدمشقي.
2026-10-08 TRANS-2 P3 page 6/8 items_abilities translated (ids 12880-16351: key items, map names, Classic Kingdom games, reports, first 200 commands + 7 abilities): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 6 tools: refresh.bat exit 0; map names reuse menus_ui place names; Dive = غوص in all dive commands; Rush = اجتياح (Dash stays اندفاع).
2026-10-08 TRANS-2 P3 page 6 unsure: command names without glossary entries (Counter family = الرد, Backlash = رد الفعل, Knockback = الإزاحة, Plasma Surge = تسارع البلازما per Surge rule).
2026-10-08 TRANS-2 P3 page 7/8 items_abilities translated (ids 16359-16651: abilities, command descriptions, Donald/Goofy finishers, MP-cost lines): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 7 tools: refresh.bat exit 0; MP Cost lines follow the TRANS-1 pattern "تكلفة MP: {0}"; Combo finisher = ضربة ختامية, Flowmotion = الحركة الانسيابية (glossary).
2026-10-08 TRANS-2 P3 page 7 unsure: ability names with no glossary entry (about 150), status words Cloud/Stun/Electric protection, HP/MP Walker = HP/MP بالمشي, Reprisal = الثأر.
2026-10-08 TRANS-2 P3 page 8/8 items_abilities translated (ids 16652-16885: ability descriptions): validate 0 ERR.
2026-10-08 TRANS-2 P3 page 8 tools: refresh.bat exit 0; pass-through of every tag and <br> count; "بـ"+tag written without tatweel.
2026-10-08 TRANS-2 P3 page 8 unsure: halberd = الرمح الفأسي, honeycoat = تغطي بالعسل, Nano Arms morph line, "stagger" = تعثر.
2026-10-08 TRANS-2 T4 close: items_abilities 8/8 pages done; 2,160 rows translated, 174 skipped, 0 remaining; 39 coined terms added to glossary.tsv as proposed; 31 rows carry unsure notes.
2026-10-08 TRANS-2 T4 close: PROJECT_MAP §3 §4 §8 + CHANGELOG updated; state\LAST_REPORT.md written by tools\trans2_report.py.
2026-10-08 TRANS-2 STOP: final refresh.bat + secret_check, commit "..."; report in state\LAST_REPORT.md.
2026-10-09 SWAP-1 T1 swap scripts: SWAP_TO_F1.bat, SWAP_TO_F2.bat, REMOVE_ARABIC.bat (tools\make_swap_scripts.py, tools\swap_msgs\); not run on the real game folder.
2026-10-09 SWAP-1 T1 tools: tested on temp copies (game check, delete, copy, SHA256, log, rd); ASCII-only bat after a UTF-8 parse bug deleted 6 root files, restored from git.
2026-10-09 SWAP-1 T1 unsure: admin re-launch path (arg elev) not exercised; process match is "...".
2026-10-09 SWAP-1 T2 fixes: trans2b.tsv 44 rows (Resistance = element nouns, Donald spells, 14239), glossary 39 proposed approved + 10 new rows.
2026-10-09 SWAP-1 T2 tools: apply_corrections 44 applied; validate 0 ERR (GLOSS WARN 5 -> 36 from newly approved terms).
2026-10-09 SWAP-1 T2 unsure: Donald Aero = دونالد إيرو chosen by pattern (not requested).
2026-10-09 SWAP-1 T3 close: refresh.bat exit 0, secret_check PASS, PROJECT_MAP §3 §4 §6 §8 + CHANGELOG updated.
2026-10-09 SWAP-1 T3 tools: commit "...".
2026-10-09 SWAP-1 T3 STOP: report in state\LAST_REPORT.md.
2026-10-09 TEST50 T0 round prompt saved verbatim as docs\rounds\TEST50.md; docs\INDEX.md lists docs\rounds\ (every round prompt is saved there); uncommitted TEST50 work copied to out\builds\TEST50\wip\ (kept, all own work of this round).
2026-10-09 TEST50 T0b swap scripts: make_swap_scripts.py had a CR and a backspace byte in two `type` paths (running/badhash messages never shown); paths now built from chr(92) via @MSG@; SWAP_TO_TEST50.bat added (same template).
2026-10-09 TEST50 T0b test (temp folder only, real ~mods untouched): swap OK + SHA256, hash mismatch -> copy deleted + message, game running -> message, remove OK; foreign pak kept; 4 SWAP_LOG rows; commit "...".
2026-10-09 TEST50 T1 lock: state\SWAP_LOG.tsv did not exist (swap scripts never run on the game); ~mods held pakchunk99-arabictest2F1_P.pak (sha 302d95d1..., = F1 build) -> F1 locked: $sougei K=256/2048 (1/8), DY=-5; other classes same Arabic-to-cap ratio.
2026-10-09 TEST50 T1 screenshot: SCREENSHOT_LOG row (chat, PASS); verified 13770 13771 13772 13777 13778 13788 15638 15660 (button_0020 = icon+Confirm/Cancel row); 13772 seen as الخيارات (old pak), re-check الضبط.
2026-10-09 TEST50 T1 open: which CONFIG key the title shows (menu_0004 13772 assumed, menu_0007 13775 same text, not marked).
2026-10-09 TEST50 T2 shaper: tools\shaper.py full SHAPER_SPEC §2-6 (style state per char, conv/icon/{n}/plural atoms, <br>/<pb>/newline lines, UAX #9 W1-W7 N1-N2 I L1 L2 L4); tools\test_shaper.py U1-U12, T1-T22, 30 real rows exact.
2026-10-09 TEST50 T2 round trip over all 5,735 translated rows: 5,728 exact, 7 "..." rows (80 HP) give the same visual line as "HP 80" (UAX #9 not injective), 0 fail; T2 <I(off)> typo normalised to <i(off)>.
2026-10-09 TEST50 T2 note: number runs after Arabic follow UAX #9 (4-1 shows as 1-4, 50% as %50, #1 as 1#) = standard RTL display; screenshot check.
2026-10-09 TEST50 T3 fonts: tools\font_census.py -> 1,089 movies, 1,165 text fields (out\builds\TEST50\ref\font_fields.tsv); classes $sougei $KH2Menu $jimakuNE $JimakuJP (+ local KH2 WI CLASSIC in MobileLsi only).
2026-10-09 TEST50 T3 letterSpacing in menu/help/subtitle movies: only Title field 61 (2 px @30 pt -> 18 units); others 0 or negative; join +18 kept for all 4 classes (F1 value, verified in-game).
2026-10-09 TEST50 T3 TresFont: 189 Arabic glyphs added to $jimakuNE (270->459) and $JimakuJP (7,932->8,121), $sougei/$KH2Menu as F1; re-parse: every original glyph and non-font tag unchanged.
2026-10-09 TEST50 T4 rows: 50 test rows (main menu 15, items 8, equipment 6, abilities 9, plural, acronym, set letter, 3 Game Help rows, 6 opening subtitles) + 34 title rows; 9 rows newly translated, ، ؟ in 4.
2026-10-09 TEST50 T4 build: tools\build_test50.py -> pakchunk99-test50_P.pak 3,881,308 B sha a26a7691...; 9 files list/hash-list/unpack SHA256 PASS; exactly 84 entries changed in 7 locres.
2026-10-09 TEST50 T4 install: SWAP_TO_TEST50.bat on the real ~mods: arabictest2F1 (302d95d1...) deleted, test50 copied, SHA256 a26a7691... verified, SWAP_LOG.tsv OK.
2026-10-09 TEST50 T5 technical\TEST50_CHECKLIST.md (Arabic): 9 groups with path in game, ids, what to check; way back via SWAP_TO_F1 / SWAP_TO_TEST50 / REMOVE_ARABIC.
2026-10-09 TEST50 T5 groups: title, opening subtitles, main menu, items, equipment, abilities, shortcut set A, synthesis plural, Game Help Combat Basics.
2026-10-09 TEST50 T5 unsure: exact order of op001 narration vs bt052 chess scene after NEW GAME; 00046 dialog trigger; 16701 ability may not be owned early.
2026-10-09 TEST50 T6 close: refresh.bat exit 0 (test_shaper added; validate 5,773 checked 0 ERR), secret_check PASS; PROJECT_MAP §3 §4 §6 §8, SHAPER_SPEC status, RECON §13, CHANGELOG updated.
2026-10-09 TEST50 T6 tools: commit "..."; report state\LAST_REPORT.md.
2026-10-09 TEST50 STOP: TEST50 installed, waiting for screenshots per technical\TEST50_CHECKLIST.md.
2026-10-09 TRANS-3 T1 log: SCREENSHOT_LOG entry (chat); 00723 status verified; 13772 back to translated, note 'verify in TEST50 title screenshot'.
2026-10-09 TRANS-3 T1 tools: direct TSV edit, no code.
2026-10-09 TRANS-3 T1 unsure: none.
2026-10-09 TRANS-3 T2 comma: tools\comma_fix.py dry-run then apply: 210 rows / 227 commas changed; RULES.md + glossary rule text updated; ؟ stays ASCII.
2026-10-09 TRANS-3 T2 tools: validate 0 ERR after apply; logged in review\corrections\LOG.md.
2026-10-09 TRANS-3 T2 unsure: none.
2026-10-09 TRANS-3 T3 tutorials pages 1-3: 601 translated, 11 conv-group rows skipped (shaper cannot place Arabic inside <conv>), 2 other skips; hashtags n/a; glossary terms used.
2026-10-09 TRANS-3 T3 journal pages 1-3: all rows translated; hashtags translated to Arabic with underscores; ؟ avoided (ASCII ?).
2026-10-09 TRANS-3 T3 tools: refresh.bat run per page; fixes via review\corrections\trans3_p*.tsv; commit a7ba84f.
2026-10-09 TRANS-3 T4 report: state\LAST_REPORT.md written; total 40.6 % (6,986/17,222).
2026-10-09 TRANS-3 STOP: final refresh + secret_check + commit 'TRANS-3: comma rule, tutorials, journal'.
2026-10-09 TRANS-3 open: conv-group rows, hashtag style, 52 proposed terms.
2026-10-09 BUILD-1 T1 line breaking: shaper.wrap()/meter()/gaps() break logical lines at spaces (never in tags, {n}, plural, conv groups, LTR runs) to the measured field width; field table technical\FIELD_WIDTHS.tsv (10 namespace groups: game help, Gummiphone story/glossary/reports/characters/enemies/help line, loading posts, item and ability descriptions).
2026-10-09 BUILD-1 T1 tools: tools\build_build1.py (profiles/meters from the rebuilt TresFont, margin 0.97, icon 1.25 em, {n} = '0000'); test_shaper.py Wrap tests (fixed advances + 9 real long rows) PASS; adjacent icons are now one atom (diagrams keep order), round trip unchanged.
2026-10-09 BUILD-1 T1 unsure: no wrap field found for kh3_tutorial.tut popups, game-over hints, gummi items, menus/mission lines (left unbroken); over-wide lines between EN <br> are broken too (help paragraphs).
2026-10-09 BUILD-1 T2 conv: whole-row <conv(X)>..<conv(off)> pair kept, inside shaped (shaper CONV); mid-row Arabic conv groups still an error (none in the data).
2026-10-09 BUILD-1 T2 rows: 12 control lists translated (tools\build1_rows.py -> review\corrections\build1_conv.tsv, applied); film titles Frozen = ملكة الثلج, Toy Story = حكاية لعبة (13 rows, build1_films.tsv); glossary +Frozen +Toy Story (approved), Tangled = متشابك (proposed, supervisor to verify).
2026-10-09 BUILD-1 T2 tests: test_conv_rows (12 rows: conv at both ends, exact round trip, icon clusters kept) PASS; validate 0 ERR.
2026-10-09 BUILD-1 T3 build: tools\build_build1.py -> pakchunk99-arabic_P.pak 4,047,105 B sha 0f27502d...; 6,998 translated rows shaped (6,989 exact round trip, 9 same-visual), 482 rows broken by width, 6,967 entries changed in 16 locres (+ TresFont, 4 classes).
2026-10-09 BUILD-1 T3 verify: repak list = 18 files, hash-list = input = unpacked SHA256 for all 18 PASS; changed entries per locres = expected; fonts: only the 189 Arabic codes added per class; every output Arabic code point in all 4 classes, no missing character.
2026-10-09 BUILD-1 T3 unsure: 116 ability rows have 3 lines while CampMenu#149 holds 2 (field identity uncertain, no ability row needed a break); 8 secret reports exceed 24 lines (EN wraps to 30+ too: the field scrolls).
2026-10-09 BUILD-1 T4 install: SWAP_TO_BUILD1.bat (tools\make_swap_scripts.py, done_BUILD1 message) on the real ~mods: test50 (a26a7691...) deleted, pakchunk99-arabic_P.pak copied, SHA256 0f27502d... verified, SWAP_LOG.tsv OK; ~mods holds only this pak.
2026-10-09 BUILD-1 T4 installed rows: build_build1.py --installed -> state\INSTALLED.tsv (6,998 of 6,998 rows match the installed pak); stats.py installed column (40.6 %).
2026-10-09 BUILD-1 T4 checklist: technical\BUILD1_CHECKLIST.md (Arabic, 6 places: title, main menu, items+equipment, abilities, game help Save Points + control lists, Gummiphone story + Sora file).
2026-10-09 BUILD-1 T5 close: refresh.bat exit 0 (9 shaper tests OK, validate 6,998 checked 0 ERR), secret_check PASS; PROJECT_MAP §3 §4 §6 §8 by hand, §7 with the installed column (stats.py); SHAPER_SPEC status §7 built; CHANGELOG; docs\INDEX lists BUILD-1.md.
2026-10-09 BUILD-1 T5 tools: report state\LAST_REPORT.md; commit "...".
2026-10-09 BUILD-1 STOP: BUILD-1 installed, waiting for screenshots per technical\BUILD1_CHECKLIST.md.
2026-10-09 FULL-1 T0 start: prompt saved docs\rounds\FULL-1.md; PROJECT_MAP, PROGRESS, FIELD_WIDTHS, RECON_KH3, BUILD-1 report read.
2026-10-09 FULL-1 A screenshots: SCREENSHOT_LOG row (chat, BUILD-1 pak); 90 rows set verified (title 13772 + version, camera config page, settings tabs/display, difficulty, pause, premium list, command menu, main menu); location/objective/munny/time rows not marked (key not identifiable).
2026-10-09 FULL-1 A1 LV label: CampMenu#335 instance articleLv, $sougei 16 pt right-aligned, 43 px = 624 units inner; ستوى 620 fits, مستوى 770 does not (matches the screenshot); text unchanged, options in the report.
2026-10-09 FULL-1 A2 help field: premium = CodeMenu#26 (CoTxaHelpText), abilities/customize = MainLibrary#68 (tres.rsl.HelpText placed as HelpText in CampMenu), both 1108x123 px @23 pt, no mask; max_lines 2 + shaper.reflow (rows over 2 lines joined and re-broken at field width); 2 rows shortened (full1_fit.tsv).
2026-10-09 FULL-1 A2 tools: shaper.reflow + test_reflow; build_build1 profiles read FIELD_WIDTHS max_lines; ability row moved from CampMenu#149 to MainLibrary#68; kh3_camp.customize detail_1 added (same field).
2026-10-09 FULL-1 A3 alignment: exe tag converter table (b br color->font color, icon->img, conv i pb nbsp) has no align tag; GFx HTML parser strings (P ALIGN) exist; no AS sets htmlText; options in report, nothing changed.
2026-10-09 FULL-1 B magic: tools\full1_magic.py -> review\corrections\full1_magic.tsv 136 rows applied (spells, tiers, Donald, compounds, gummi, equipment, descriptions); glossary.tsv 31 terms set (note "...").
2026-10-09 FULL-1 B width: command field HudCommand#18 2,304 units (#23 2,573); widest tier name صاعقة قصوى 1,515, Dark Firaga 1,668: all fit.
2026-10-09 FULL-1 B unsure: tutorial "جرب إلقاء نار" kept as the bare command name; Blizzard Blades unified to نصال الجليد (12294 had شفرات).
2026-10-09 FULL-1 C build: tools\build_build2.py (build_build1 with BUILD/OUT/PAK set) -> out\builds\BUILD-2\pakchunk99-arabic_P.pak 4,046,332 B sha 2ce95c73...; 18 files list/hash-list/unpack SHA256 PASS; 6,967 entries changed in 16 locres; 155 help-field rows reflowed, OVERHEIGHT only the 8 known secret reports.
2026-10-09 FULL-1 C install: SWAP_TO_BUILD2.bat (make_swap_scripts.py, done_BUILD2 message, same template as BUILD1): BUILD-1 pak 0f27502d... deleted, BUILD-2 copied, SHA256 2ce95c73... verified (Get-FileHash), SWAP_LOG row OK; ~mods holds only this pak.
2026-10-09 FULL-1 C installed rows: build_build2.py --installed -> state\INSTALLED.tsv (build BUILD-2).
2026-10-09 FULL-1 C checklist: technical\BUILD2_CHECKLIST.md (Arabic, 4 places: premium help, party LV record, ability description, battle magic list).
2026-10-09 FULL-1 D inventory: tools\text_coverage.py -> technical\TEXT_COVERAGE.md + technical\text_coverage\*.tsv; Game en 17,222 entries / 125,538 words all in translation\ (0 missing); Engine 5,186 + plugins 68 entries not game-visible; no StringTables, no UI/UI_HUD locres, 0 static text tags in 276 movies, 0 USM subtitle streams (180 files).
2026-10-09 FULL-1 D en vs ja: 255 ja keys blank (one space) in en: 116 Latin sub-labels of the ja UI, 139 ja-only interjections; 163 en-only keys; images/videos 315 assets ≈ 958 words (EST); headline reachable = 99.2 % by words; nothing new exported to translation\ (no new real text found).
2026-10-09 FULL-1 E script: tools\make_script.py -> review\script\INDEX.md (story: 9,488 rows, 349 scenes, 32 pages; cutscenes ordered by the Theater table technical\theater_order.tsv, 264 events + 45 placed by world/number; then field/battle voice per world) + TIPS.md (7,734 rows, 26 pages; loading, game-over hints, tutorials, journal, items, menus).
2026-10-09 FULL-1 E speaker: no speaker-name table in the game (FsTable_* = footstep sounds); speaker = voice code in the key (sr, do, go, 98 codes) or field-voice prefix (sora_); added to refresh.bat; PROJECT_MAP §5 + docs\INDEX name review\script\ as the reference script.
2026-10-09 FULL-1 E unsure: events not in the Theater (bt001a, ra301a, ss99x memory scenes, Re Mind ew95x...) are placed after the same world's lower Theater event; check their order when translating.
2026-10-09 FULL-1 F close: refresh.bat exit 0 (validate 6,998 checked 0 ERR, make_script in the pipeline), secret_check PASS; PROJECT_MAP §3 §4 §6 §8 by hand, §5 §7 auto; SHAPER_SPEC §7b; CHANGELOG; docs\INDEX.
2026-10-09 FULL-1 F tools: report state\LAST_REPORT.md; commit "...".
2026-10-09 FULL-1 STOP: BUILD-2 installed, waiting for screenshots per technical\BUILD2_CHECKLIST.md and the LV / alignment decisions.
2026-10-09 TRANS-4 T0 start: prompt saved docs\rounds\TRANS-4.md; PROJECT_MAP, PROGRESS, FULL-1 report, FIELD_WIDTHS, script INDEX, glossary, RULES read.
2026-10-09 TRANS-4 P1.1 LV field: CampMenu (_0_P copy = extracted\assets, sha 025ff3d2...) #335 xMin 96.1 -> 86.95 px (1739 twips; 52.15 px = 770.4 units inner at 16 pt); re-parse: 2 bytes differ, only #335 bounds, 1075 tags same; patched sha c9709841...
2026-10-09 TRANS-4 P1.1 layout: label ink 129.9..178 px vs خبرة ink 62..89.6 (gap 40.3 px, field boxes 7.85 px apart); level digits (#343, max 99 = 2 digits) start at 180.6, unchanged; level-up HUD (HudRight#109, row 15964) clips 1994 vs 1621 units, HudGumi#255 clips مستوى 770 vs 709 (not patched).
2026-10-09 TRANS-4 P1.2 align test: row 15729 (kh3_settings.display detail_0010) built text wrapped in <p align="right">..</p> (build_build1.ALIGN_RIGHT); twin row 15738 unchanged.
2026-10-09 TRANS-4 P1.3 build: tools\build_build3.py -> out\builds\BUILD-3\pakchunk99-arabic_P.pak 4,192,835 B sha 2834d65a...; 20 files list/hash-list/unpack SHA256 PASS; 6,967 entries changed in 16 locres + CampMenu uasset (unchanged) / uexp (patched) + TresFont.
2026-10-09 TRANS-4 P1.3 install: SWAP_TO_BUILD3.bat (make_swap_scripts.py): BUILD-2 2ce95c73... deleted, BUILD-3 copied, SHA256 2834d65a... verified, SWAP_LOG OK; INSTALLED.tsv 6,998/6,998; technical\BUILD3_CHECKLIST.md (4 places).
2026-10-09 TRANS-4 P2 page 1: script_001 (bt001a, bt052a Gambit, yt021a/gm022a Prelude, Olympus he101a-he111a) 285 rows translated (tools\trans4_page.py dump/apply).
2026-10-09 TRANS-4 P2 page 1 check: refresh.bat exit 0, validate 0 ERR, 0 flags on the new rows.
2026-10-09 TRANS-4 P2 page 1 unsure: Hades puns (I's/T's, Sparta, Oy vey, H-ster), Break a leg, hotheads; terms Titans = التيتان, The Fates = ربات القدر, Meg = ميغ, Styx = نهر ستيكس.
2026-10-09 TRANS-4 P2 page 2: script_002 (Olympus he111a-he119a, Realm of Darkness dw151a-dw153a, yt154a start) 249 rows translated + 5 from TM; 44 Re Mind rows (he119r) left for the remind batch.
2026-10-09 TRANS-4 P2 page 2 check: refresh.bat exit 0, validate 0 ERR; 2 RATIO WARN (short exclamations سنوقفك! / كفى!, kept).
2026-10-09 TRANS-4 P2 page 2 unsure: "...", "Nut-Meg", "bolt boy", "sunspot"; terms Master Aqua = المعلمة أكوا, Pandora's Box = صندوق باندورا.
2026-10-09 TRANS-4 P2 page 3: script_003 (yt154a A Fresh Start, gm155a Heart Within a Heart, Twilight Town tt201a-tt207a) 291 rows translated (13 via TM).
2026-10-09 TRANS-4 P2 page 3 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 3 unsure: Hayner "underprecedented" (malapropism lost); terms Sleeping Worlds = عوالم النوم, Ansem's Code = شفرة أنسيم, datascape = فضاء البيانات, Data-Sora = سورا الرقمي, A-hyuck = آهيوك.
2026-10-09 TRANS-4 P2 page 4: script_004 (Twilight Town tt207a-tt212a, Radiant Garden rg232a, Toy Box ts252a start) 287 rows translated (14 via TM).
2026-10-09 TRANS-4 P2 page 4 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 4 unsure: "...", "...", tarte aux fruits in Arabic, order/border pun (نظام/ظلام), "..."; Mr. McDuck = السيد ماكدك, pretzels = الكعك المملح.
2026-10-09 TRANS-4 P2 page 5: script_005 (Toy Box ts252a-ts260a) 289 rows translated (8 via TM).
2026-10-09 TRANS-4 P2 page 5 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 5 unsure: Buzz Lightyear = باز يطير (Arabic dub name), "dino-napped" = اختطف, Babies and Toddlers = قسم الرضع والأطفال, Slinky = سلينكي, Bahamut = باهاموت, "..." = أول الزيهانورتات.
2026-10-09 TRANS-4 P2 page 6: script_006 (Toy Box ts260a-ts271a, gm291a/rg292a A Replica for Roxas, Corona ra301a start) 291 rows translated (21 via TM).
2026-10-09 TRANS-4 P2 page 6 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 6 unsure: "dread-and-breakfast" = فندق الرعب, "...", "..."; replicas = النسخ, Gothel's "flower" = زهرتي.
2026-10-09 TRANS-4 P2 page 7: script_007 (Kingdom of Corona ra301a-ra317a) 290 rows translated (13 via TM).
2026-10-09 TRANS-4 P2 page 7 check: refresh.bat exit 0, validate 0 ERR; 1 RATIO WARN (05257 هرب., kept).
2026-10-09 TRANS-4 P2 page 7 unsure: "Gesundheit" = يرحمك الله (name/sneeze joke), "has-been" = المنتهي, "Blondie" = يا شقراء, "sidekicks" = مساعدي.
2026-10-09 TRANS-4 P2 page 8: script_008 (Corona ra317a-ra326a, Radiant Garden rg331a, kg332a Vexen, Monstropolis mi351a-mi353a) 292 rows translated (23 via TM).
2026-10-09 TRANS-4 P2 page 8 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 8 unsure: Healing Incantation lyrics (own wording), "Kitty" = بسبس, K-I-D = ط-ف-ل, CDA kept Latin (EN acronym), "butterball" = مكور.
2026-10-09 TRANS-4 P2 page 9: script_009 (Monstropolis mi353a-mi373a) 290 rows translated (20 via TM).
2026-10-09 TRANS-4 P2 page 9 check: refresh.bat exit 0; 1 ERR (04932 lost its <br>) fixed via review\corrections\trans4_p009.tsv, validate 0 ERR; RATIO WARN on short lines kept.
2026-10-09 TRANS-4 P2 page 9 unsure: Monsters, Incorporated = شركة المرعبين المحدودة, "racket" pun = المضرب, contact-lens joke, "..." = إلى غير رجعة, "insignificant speck" = النكرة التافه.
2026-10-09 TRANS-4 P2 page 10: script_010 (Monstropolis mi373a-mi374a, gm431a Ienzo Checks In, Arendelle fz451a-fz459a incl. Let It Go) 292 rows translated (18 via TM).
2026-10-09 TRANS-4 P2 page 10 check: refresh.bat exit 0, validate 0 ERR; GLOSS 02581 fixed (trans4_p010.tsv); italic tags never split a joining Arabic word (scan of all TRANS-4 rows: 0).
2026-10-09 TRANS-4 P2 page 10 unsure: Let It Go lyrics (own MSA wording, "..." = دعها تمضي), "..." = اقرأ الأجواء يا صغير, "islander" = ابن الجزر.
2026-10-09 TRANS-4 P2 page 11: script_011 (Arendelle fz459a-fz471c incl. "...", Realm of Darkness dw382a) 293 rows translated (31 via TM).
2026-10-09 TRANS-4 P2 page 11 check: refresh.bat exit 0, validate 0 ERR, no new flags; split-tag scan 0.
2026-10-09 TRANS-4 P2 page 11 unsure: snowman song lyrics (own wording), "feisty-pants" = يا عنيدة, "..." = غوفي الأخضر, "..." = المرة الثانية هي الحاسمة.
2026-10-09 TRANS-4 P2 page 12: script_012 (dw382a, gm383a Merlin, tt501a/tt506a, 100 Acre Wood po502a-po505a, yt381a A Quick Review, kg433a Organization's Origins, Caribbean ca401a start) 280 rows translated (12 via TM).
2026-10-09 TRANS-4 P2 page 12 check: refresh.bat exit 0, validate 0 ERR, no new flags; tatweel/split check now run before each apply.
2026-10-09 TRANS-4 P2 page 12 unsure: pirate song lyrics (own wording, "yo ho"..."Sufferin' sassafras" = يا للمصيبة, "...", "Organization Rehash" = المنظمة المكررة, "benched" = مقاعد الاحتياط.
2026-10-09 TRANS-4 P2 page 13: script_013 (The Caribbean ca401a-ca411a) 291 rows translated (24 via TM).
2026-10-09 TRANS-4 P2 page 13 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 13 unsure: Black Pearl = اللؤلؤة السوداء, Brethren Court = مجلس الإخوة, Isla de Muerta = جزيرة الموتى, the Pirate Code = الشريعة, "Savvy?" = مفهوم?, "the sparrow" in the song = العصفور.
2026-10-09 TRANS-4 P2 page 14: script_014 (The Caribbean ca411a-ca420b, Realm of Darkness dw432a, Twilight Town tt482a-tt483a start) 293 rows translated (19 via TM).
2026-10-09 TRANS-4 P2 page 14 check: refresh.bat exit 0, validate 0 ERR; 3 RATIO WARN on short lines (01974, 02012, 07404) kept.
2026-10-09 TRANS-4 P2 page 14 unsure: "..." = ارفعوا الراية, "hearties" = رفاق قلبك, "your nibs" = يا صاحبة الجلالة, "Harridan" = أيتها الشمطاء, "whelp" = الجرو, Endeavour = إنديفور, "..." = إنها مجرد تجارة رابحة.
2026-10-09 TRANS-4 P2 page 15: script_015 (Twilight Town tt483a-tt484a Atonement, San Fransokyo bx551a-bx558a) 270 rows translated (23 via TM).
2026-10-09 TRANS-4 P2 page 15 check: refresh.bat exit 0, validate 0 ERR; GLOSS 00961 (Keyblades) fixed via trans4_p015.tsv.
2026-10-09 TRANS-4 P2 page 15 unsure: metropolitan/cosmopolitan/Not-apolitan pun, "..." = أبطال الكيبلايد الثلاثة, Geek's Quarterly = مجلة المهووسين الفصلية, freeze-nado = إعصار التجميد, Microbots = الروبوتات الدقيقة, shugyo = الشوغيو.
2026-10-09 TRANS-4 P2 page 16: script_016 (San Fransokyo bx558a-bx564a, gm571a A Guiding Key, di572a start) 295 rows translated (30 via TM).
2026-10-09 TRANS-4 P2 page 16 check: refresh.bat exit 0, validate 0 ERR; RATIO WARN on short lines only.
2026-10-09 TRANS-4 P2 page 16 unsure: Darkubes = المكعبات المظلمة (glossary), The Replica Program = برنامج النسخ, Goofy's "arch-nemenies"..."walking balloon" = البالون الماشي.
2026-10-09 TRANS-4 P2 page 17: script_017 (di572a/dw602a-dw603a/di604a Aqua's return, rg611a-rg612a Vexen and Demyx, Castle Oblivion dp651a-dp656a Ven wakes, yt661a-yt662a guardians gather, tt663a, tt671a start) 270 rows translated (23 via TM); 19 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 17 check: refresh.bat exit 0, validate 0 ERR; GLOSS 07784 fixed (trans4_p017.tsv).
2026-10-09 TRANS-4 P2 page 17 unsure: "..." = ثلاثة أنصاف تصنع واحدا كاملا, "Venty-Wenty" = فينتي الصغير, "yesterday's toast" = في خبر كان, "benched" = مقاعد الاحتياط.
2026-10-09 TRANS-4 P2 page 18: script_018 (tt671a Lea and Isa, di672a-di673a, Keyblade Graveyard kg701a-kg702d, bt711a, The Final World ew752a/ew754a, he803a-he805a, bx806a, kg851a-kg852b) 280 rows translated (36 via TM); 12 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 18 check: refresh.bat exit 0, validate 0 ERR; GLOSS 03731 fixed (trans4_p018.tsv).
2026-10-09 TRANS-4 P2 page 18 unsure: "..." = هل حفظت ذلك?, Zettaflare = زيتافلير, "Checkmate" = كش ملك, "upside-down tears" = الدموع المقلوبة.
2026-10-09 TRANS-4 P2 page 19: script_019 (Keyblade Graveyard kg853a-kg873a: Riku Replica, Demyx, Luxord, Larxene, Marluxia, Vanitas, Terra, Roxas and Xion return, Lea and Isa) 275 rows translated (34 via TM); 22 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 19 check: refresh.bat exit 0, validate 0 ERR; RATIO WARN on short lines only.
2026-10-09 TRANS-4 P2 page 19 unsure: "..." = لا أحد يقصي آكسل, "also-ran" = أيها الخاسر, "Big Bad" = الشرير الأكبر, "heart tank" = خزان قلب, Isa = إيسا (no glossary entry).
2026-10-09 TRANS-4 P2 page 20: script_020 (Keyblade Graveyard kg874a-kg878b, Scala ad Caelum bt901a-bt908a, The Final World ew755a Naminé) 260 rows translated (32 via TM); 34 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 20 check: refresh.bat exit 0, validate 0 ERR; RATIO WARN on short lines only.
2026-10-09 TRANS-4 P2 page 20 unsure: Stopza = ستوبزا, "half-pints" = أنصاف, "..." = حبكات تحتاج إلى ترتيب, "..." = يا لك من ثعلب ماكر.
2026-10-09 TRANS-4 P2 page 21: script_021 (The Final World ew753a, the girl who waits) 44 rows translated (4 via TM); 254 Re Mind rows on this page left for the remind batch.
2026-10-09 TRANS-4 P2 page 21 check: refresh.bat exit 0, validate 0 ERR.
2026-10-09 TRANS-4 P2 page 21 unsure: "a Nobody"/"a somebody" pun = لا أحد / أحد ما. Cutscene story (base game) complete; next pages are field and battle voice.
2026-10-09 TRANS-4 P2 page 22: script_022 (bt904a) 1 row translated; 299 Re Mind rows on this page left.
2026-10-09 TRANS-4 P2 page 23: script_023 (Secret Forest sf231a/sf481a Kairi and Lea, ss921a Sora leaves, ss931a Luxu and the Foretellers, ss991a-ss992a The Story So Far) 189 rows translated (16 via TM); 97 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 23 check: refresh.bat exit 0, validate 0 ERR; GLOSS 05987 fixed (trans4_p023.tsv); GLOSS 05955 kept (Kairi: feminine حاملة كيبلايد).
2026-10-09 TRANS-4 P2 page 23 unsure: Luxu = لوكسو, Ava = آفا, recap titles DEPARTURES/MEMORIES = الانطلاق / الذكريات, "..." = ما دام يعمل فلا داعي لإصلاحه.
2026-10-09 TRANS-4 P2 page 24: script_024 (ss992a-ss995a The Story So Far recaps, field voice bt/gm/he start) 247 rows translated (10 via TM); 15 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 24 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 24 unsure: recap titles TWILIGHT/DAWN/DARKNESS = الشفق / الفجر / الظلام, "metamorphatizing" = يتحورل, "..." = من المقلاة إلى النار, "World ho!" = عالم في الأفق!
2026-10-09 TRANS-4 P2 page 25: script_025 (field voice he: Goofy/Hercules/Sora/Meg/Zeus, Thebes townsfolk, Twilight Town townsfolk, tt Donald) 296 rows translated (5 via TM).
2026-10-09 TRANS-4 P2 page 25 check: refresh.bat exit 0; 1 ERR (09747 lost its <br>) fixed via trans4_p025.tsv, validate 0 ERR.
2026-10-09 TRANS-4 P2 page 25 unsure: "..." = من لا شيء إلى كل شيء, "..." = الزيتونة الكبرى, Golden Hercs = تماثيل هرقل الذهبية, Picky Palates = الأذواق الصعبة, "STRUGGLE!" = الصراع!
2026-10-09 TRANS-4 P2 page 26: script_026 (field voice tt Goofy/Scrooge/Sora/shop ducks/Moogle/friends, ts Toy Box party and toys, ra Corona start) 272 rows translated (11 via TM); 21 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 26 check: refresh.bat exit 0, validate 0 ERR; GLOSS 10202 fixed (trans4_p026.tsv).
2026-10-09 TRANS-4 P2 page 26 unsure: Moogle "kupo" = كوبو, Flynn's "mist me" pun = تبخرت فرصتك, "rotten egg" = بيضة فاسدة, "..." (Hamm) = أنا خنزيركم.
2026-10-09 TRANS-4 P2 page 27: script_027 (field voice ra: Rapunzel/Sora/Donald/Flynn/Goofy, Corona townsfolk, kg start) 273 rows translated (9 via TM).
2026-10-09 TRANS-4 P2 page 27 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 27 unsure: "mutton chop" (pet name) = يا عزيزي, "..." idiom kept literal, Maximus "......" kept as is.
2026-10-09 TRANS-4 P2 page 28: script_028 (field voice kg Goofy/Sora, mi CDA/Donald/Goofy/Mike/Randall/Sulley, fz Anna/Donald/Elsa/Goofy start) 240 rows translated (12 via TM); 37 Re Mind rows left.
2026-10-09 TRANS-4 P2 page 28 check: refresh.bat exit 0, validate 0 ERR; RATIO WARN on short lines only.
2026-10-09 TRANS-4 P2 page 28 unsure: photo call "Say scream!" = قولوا "صراخ", Laugh Floor = طابق الضحك (glossary), "..." = رجلا أولاف تركضان.
2026-10-09 TRANS-4 P2 page 29: script_029 (field voice fz Goofy/Kristoff/Marshmallow/Olaf/Sora + talk, po 100 Acre Wood chat and talk, ca Donald start) 285 rows translated (18 via TM).
2026-10-09 TRANS-4 P2 page 29 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 29 unsure: Marshmallow's broken speech kept simple, "snow cones" = مثلجات الثلج المبشور, "I-hide-and-you-seek" = أنا-أختبئ-وأنت-تبحث, "Tiggers" = التيغرات.
2026-10-09 TRANS-4 P2 page 30: script_030 (field voice ca Donald/Goofy/Jack/Luxord/Sora + talk incl. Gibbs, Port Royal townsfolk) 297 rows translated (5 via TM).
2026-10-09 TRANS-4 P2 page 30 check: refresh.bat exit 0, validate 0 ERR, no new flags.
2026-10-09 TRANS-4 P2 page 30 unsure: "swashbuckliest" = أمهر مقاتل بالسيف, "Port Royally-Short-On-Decent-Men"..."island-ness" = جزيريتها, "deck swab" = ممسح سطح, "pigeon" (pet name) = يا حمامتي, barnacles = البرنقيلات.
2026-10-09 TRANS-4 P2 page 31: script_031 (Port Royal townsfolk end, field voice bx: Baymax/Donald/Fred/Go Go/Goofy/Hiro/Honey Lemon/Sora/Wasabi + talk, San Fransokyo townsfolk) 299 rows translated (9 via TM).
2026-10-09 TRANS-4 P2 page 31 check: refresh.bat first exit 1 (test_shaper cap: 22 same-visual round trips > 20; 13 new ones are italic lines split by <pb> whose adjacent tags come back reordered, visual identical); cap changed to max(20, exact/100) in tools\test_shaper.py; refresh.bat exit 0, validate 0 ERR.
2026-10-09 TRANS-4 P2 page 31 unsure: "Gracias" = غراسياس, Krei Tech = كراي تك, Flash Tracer = فلاش تريسر (glossary), "..." = تقليد للأبطال الستة, takoyaki/ramen transliterated.
2026-10-09 TRANS-4 P2 page 32: script_032 (San Fransokyo townsfolk end, The Final World ew chat + the nine "star"..."Big Hero 9" = الأبطال التسعة, "Mr. I-Rideshare..."..."Goofy enough for ya?" = مضحكة بما يكفي, daruma/sukiyaki/udon transliterated.
2026-10-09 TRANS-4 F report: state\LAST_REPORT.md (BUILD-3 SHA table, LV layout gaps, 15936/level-up fields, per-world counts, 40 samples, 93 unsure rows, 27 proposed terms); glossary.tsv +27 proposed (TRANS-4).
2026-10-09 TRANS-4 F close: PROJECT_MAP §3 §4 §6 §8 by hand (§5 §7 auto), CHANGELOG, docs\INDEX; refresh.bat + secret_check; commit "...".
2026-10-09 TRANS-4 STOP: BUILD-3 installed, waiting for screenshots per technical\BUILD3_CHECKLIST.md; story text translated (88.8 %); next: Re Mind batch, BUILD-4.
2026-10-09 REVIEW-1 T1 corrections: review1_gpt.tsv built from gpt_corrections_batch1.tsv; supervisor changes on 15164, 15372-15375, 17002/17004/17032 (8 rows).
2026-10-09 REVIEW-1 T1 corrections: apply_corrections: 210 applied, 0 refused (no old_AR mismatch).
2026-10-09 REVIEW-1 T1 corrections: Log in review\corrections\LOG.md; file moved to applied\.
2026-10-09 REVIEW-1 T2 glossary: Heartbinder, Altair, Datascape(s) set approved (note supervisor decision REVIEW-1); Dream Heartbinder + 4 named variants added; Buzz Lightyear and fem. wielder were already in the baseline.
2026-10-09 REVIEW-1 T2 glossary: The 26 TRANS-4 proposed terms were already approved in the baseline commit; 51 TRANS-3 proposals stay proposed.
2026-10-09 REVIEW-1 T2 glossary: review1_gloss.tsv: 8 rows applied; review1_buzz.tsv (row 06525 باز يطير -> باز لايتير) was already applied in the baseline.
2026-10-09 REVIEW-1 T3 validator: ERR QMARK for U+061F; translation\typo_patterns.tsv (10 patterns) loaded as WARN TYPO; 9 unit tests OK.
2026-10-09 REVIEW-1 T3 validator: Hits: 46 QMARK rows (dialogue) fixed via review1_typos.tsv; 1 TYPO hit (15203, past tense, false positive, left).
2026-10-09 REVIEW-1 T3 validator: validate: 0 ERR.
2026-10-09 REVIEW-1 T4 status: 6,895 rows translated -> reviewed in menus_ui/items/tutorials/journal (+97 verified stay = 6,992 GPT rows).
2026-10-09 REVIEW-1 T4 status: Note 'reviewed_by GPT Sol 6.1 + supervisor, REVIEW-1' appended.
2026-10-09 REVIEW-1 T4 status: STATS: translated 88.8%, installed 39.4%, reviewed 40.6%, verified 0.6%.
2026-10-09 REVIEW-1 T5 unsure: review\gpt\UNSURE_batch1.md written (section of gpt_summary.md).
2026-10-09 REVIEW-1 T5 unsure: Altair and Datascapes marked RESOLVED.
2026-10-09 REVIEW-1 T5 unsure: File is local/untracked (review/gpt/ in .gitignore).
2026-10-09 REVIEW-1 T6 align: ALIGN_RIGHT usage for 15729 already removed from tools\build_build3.py in the baseline; hook in build_build1.py kept.
2026-10-09 REVIEW-1 T6 align: PROJECT_MAP section 4 records the decision.
2026-10-09 REVIEW-1 T6 align: No build run.
2026-10-09 REVIEW-1 T7 BUILD-4 todo: PROJECT_MAP section 8: (a) save card + HudGumi#255 widen, (b) 15964, (c) story + Re Mind.
2026-10-09 REVIEW-1 T7 BUILD-4 todo: Row 15964 changed to مستوى أعلى! via review1_ui.tsv.
2026-10-09 REVIEW-1 T7 BUILD-4 todo: Not built.
2026-10-09 REVIEW-1 T8 close: refresh.bat exit 0 (0 ERR), secret_check PASS (342 files).
2026-10-09 REVIEW-1 T8 close: PROJECT_MAP sections 3 4 8 (7 auto), CHANGELOG updated.
2026-10-09 REVIEW-1 T8 close: Commit: REVIEW-1: GPT review batch 1 applied.
2026:10:09 TRANS-5 start: docs\rounds\TRANS-5.md saved; tools\trans5_page.py (remind rows: story order of review\script, then menu/gamehelp/mobile/extraload/camp rows by id; 4 pages of 300). Apply replaces U+061F by ASCII ?.
2026:10:09 TRANS-5 remind page 1 (he119r/dp072a/kg852r/ew953a-979a/kg951a-952a): 284 rows translated; Lost Master = معلم مفقود (glossary plural).
2026:10:09 TRANS-5 remind page 1 check: refresh.bat exit 0, validate 0 ERR (QMARK/TAGS/BR/GLOSS fixed by direct row edit).
2026:10:09 TRANS-5 remind page 2 (kg952a-kg878r, bt971a-bt903r): 287 rows translated. Unsure: "..." (Demyx, sitar/ID) = كل الأشخاص الرائعين يملكون واحدا; "half-pints" = صغار; "Zex...er, Ienzo" = زيك... أقصد، إينزو.
2026:10:09 TRANS-5 remind page 2 check: refresh.bat exit 0, validate 0 ERR; GLOSS 04519 fixed.
2026:10:09 TRANS-5 remind page 3 (kg974a-ss945a Yozora/secret episode, fieldvoice, extraload, gamehelp, Data Greeting menu): 292 rows translated. Unsure: Hashtags kept as in EN (Latin, allowed); "Battalion somethin'" = باتاليون شيء ما; Cid "broken record" = أسطوانة معطلة; Yozora "Commander" = أيها القائد.
2026:10:09 TRANS-5 remind page 3 check: refresh.bat exit 0, validate 0 ERR; GLOSS 06406 fixed; RATIO on short lines kept.
2026:10:09 TRANS-5 remind page 4 (Data Greeting + Slideshow menus, spirits, gummi, effects, mobile DLC descriptions; 263 rows): translated. Unsure: music titles transliterated (Hand in Hand ~Attraction Flow~, Tangled à la Mode); Action pose category = الفعل (glossary form).
2026:10:09 TRANS-5 remind page 4 check: refresh.bat exit 0 after fixing harakat in 2 rows (14721, 14723), validate 0 ERR.
2026:10:09 TRANS-5 remind done: 1,126 translated, 37 skipped (EN is a single space), 0 other remaining.
2026-10-09 TRANS-6 T1 fixes: 02552 vocative removed, 14589 = الحركة, 5 Latin hashtag rows (07865-07869) now Arabic.
2026-10-09 TRANS-6 T2 remaining rows: 168 todo-with-EN checked; 1 translated (15672), 167 skip (icons/placeholders/symbols/native script).
2026-10-09 TRANS-6 T3-T5: validator WARN HASHTAG + test; refresh.bat 0 ERR, secret_check PASS; commit TRANS-6.
2026-10-09 BUILD-4 T1 fields: subtitles + field/battle voice = 92_message/Subtitle #1 ($jimakuNE 38 pt, 1,124 px, wordwrap = engine wraps in visual order, so every line pre-broken; JimakuJP #2-#7 = ja twins); lines counted per <pb> page; gummi blocks = EditGumi #385; 49 namespaces without a field -> EN-widest rows (tools\build_build4.py --fields).
2026-10-09 BUILD-4 T1 tools: build_build1.profile falls back to a shorter prefix whose keys match; page_lines(); FIELD_WIDTHS 'reflow' column (FULL-1 help fields only); tools\gfx_layout.py (placements, neighbours).
2026-10-09 BUILD-4 T1 result: 3 subtitle rows need 3 lines (EN design 2, box holds 4) + 01917 (EN itself 3); 2 EN-widest rows over EN lines; 8 known secret reports; nothing shortened (out\builds\BUILD-4\overflow.tsv).
2026-10-09 BUILD-4 T2 LV: SaveLoad #43 (save card, left-aligned 15 pt) xMin -2 -> -19.1 px, label ends 3.98 px before the level number; HudGumi #255 xMin -2 -> -5.15 px (771 units >= 770); CampMenu #335 as BUILD-3; re-parse: only those RECTs differ.
2026-10-09 BUILD-4 T2 base: SaveLoad/HudGumi have no _0_P copy (pakchunk0_s7 base pak = newest), extracted read-only into extracted\assets; CampMenu from the _0_P pak.
2026-10-09 BUILD-4 T2 FAIL: row 15964 «مستوى أعلى!» needs 1,797 $KH2Menu units, HudRight #109 holds 1,621 (12 pt, 76 px inner): ~4.1 px clipped each side; not changed (no approval to patch HudRight, nothing shortened silently).
2026-10-09 BUILD-4 T3 build: pakchunk99-arabic_P.pak 4,889,975 B sha ae9d609a...; 16,415 rows shaped (16,391 exact, 24 same-visual, 0 fail); 16,376 entries changed in 64 locres; 73 files list/hash-list/unpack SHA256 PASS; no <p align>.
2026-10-09 BUILD-4 T3 note: repak packs files in a varying order, so the pak SHA differs per run with identical inputs (per-file SHA identical); the installed pak is the last build.
2026-10-09 BUILD-4 T4 install: SWAP_TO_BUILD4.bat (make_swap_scripts.py): BUILD-3 2834d65a... deleted, BUILD-4 copied, SHA256 ae9d609a... verified (Get-FileHash), SWAP_LOG OK; INSTALLED.tsv 16,415 / 16,415.
2026-10-09 BUILD-4 T4 checklist: technical\BUILD4_CHECKLIST.md (Arabic, 8 places: title, 2-line subtitles he102a, long subtitles he111a/he118a, field/battle voice he + level-up 15964, Game Help shotlock page, Gummiphone story, save card LV, gummi guide LV).
2026-10-09 BUILD-4 T4 unsure: field voice field assumed; exact place of the gummi battle-level guide on the world map; 3-line subtitle rows need a screenshot.
2026-10-09 BUILD-4 T5 close: refresh.bat exit 0 (validate 16,415 checked, 0 ERR), secret_check PASS; PROJECT_MAP §3 §4 §6 §8 by hand (§5 §7 auto), CHANGELOG, docs\INDEX (BUILD-4 prompt + checklist).
2026-10-09 BUILD-4 T5 report: state\LAST_REPORT.md (SHA table 73 files + pak, changed per locres, field table, 15 over-capacity rows with EN/AR, LV gaps, 15964 FAIL numbers).
2026-10-09 BUILD-4 STOP: commit "..."; waiting for screenshots per technical\BUILD4_CHECKLIST.md and the 15964 / HudRight #109 decision.

2026-10-10 REVIEW-2 T1: 15964 = level word + "!" (1,067 units <= 1,621 HudRight #109), review2_ui.tsv applied.
2026-10-10 REVIEW-2 tool: tools
eview2_page.py (dump/fix/mark/flags N; pages = 300 translated rows in story order, 32 pages).
2026-10-10 REVIEW-2 page 1: 300 rows reviewed, 1 fix (03461 meaning); refresh 0 ERR.
2026-10-10 REVIEW-2 page 2: 300 rows reviewed, 2 fixes (grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 3: 300 rows reviewed, 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 4: 300 rows reviewed, 1 fix (grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 5: 300 rows reviewed, 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 6: 300 rows reviewed, 1 fix (meaning); refresh 0 ERR.
2026-10-10 REVIEW-2 page 7: 300 rows reviewed, 4 fixes (2 gender, 1 grammar, 1 meaning); refresh 0 ERR.
2026-10-10 REVIEW-2 page 8: 300 rows reviewed, 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 9: 300 rows reviewed, 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 10: 300 rows reviewed, 3 fixes (2 meaning, 1 grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 11: 300 rows reviewed, 1 fix (grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 12: 300 rows reviewed, 1 fix (grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 13: 300 rows reviewed, 1 fix (meaning); refresh 0 ERR.
2026-10-10 REVIEW-2 page 14: 300 rows reviewed, 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 15: 300 rows reviewed, 2 fixes (1 grammar, 1 meaning); refresh 0 ERR.
2026-10-10 REVIEW-2 page 16: 300 rows reviewed, 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 17: 300 rows reviewed, 1 fix (grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 18: 300 rows reviewed, 6 fixes (4 grammar, 1 gender, 1 meaning/consistency); refresh 0 ERR.
2026-10-10 REVIEW-2 page 19: 300 rows reviewed, 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 20: 300 rows reviewed, 7 fixes (3 consistency, 2 gender/grammar, 2 grammar); refresh 0 ERR. TODO remaining Re Mind rows 06388,04368 use قوة الاستيقاظ.
2026-10-10 REVIEW-2 page 21: 300 rows reviewed, 5 fixes (consistency); refresh 0 ERR.
2026-10-10 REVIEW-2 page 22: 300 rows reviewed, 2 fixes (grammar, consistency); refresh 0 ERR.
2026-10-10 REVIEW-2 page 23: 300 rows reviewed, 1 fix (gender/grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 24: 300 rows reviewed (field/town voice), 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 25: 300 rows reviewed (field voice), 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 26: 300 rows reviewed (field voice), 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 27: 300 rows reviewed (field voice), 1 fix (meaning); refresh 0 ERR.
2026-10-10 REVIEW-2 page 28: 300 rows reviewed (field voice), 1 fix (style); refresh 0 ERR.
2026-10-10 REVIEW-2 page 29: 300 rows reviewed (field/town voice), 1 fix (grammar); refresh 0 ERR.
2026-10-10 REVIEW-2 page 30: 300 rows reviewed (field/town voice), 0 fixes; refresh 0 ERR.
2026-10-10 REVIEW-2 page 31: 300 rows reviewed (field voice, extraload, gamehelp, menu), 2 fixes (grammar, gender); refresh 0 ERR.
2026-10-10 REVIEW-2 page 32: 121 rows reviewed (menu, mobile), 0 fixes; refresh 0 ERR. All 32 pages done.
2026-10-10 REVIEW-2 close: 44 rows corrected + 15964; 10 typo patterns; review/UNSURE_REVIEW2.md (13); LAST_REPORT.md written; PROJECT_MAP 3 4 8, CHANGELOG updated; BUILD-5 needed.
2026-10-10 REVIEW-2 resume: none, review complete (9,421 rows). Next BUILD-5.
2026-10-10 REVIEW-2 stats: reviewed 95.3 percent (16,414 of 17,222).
2026-10-10 BUILD-5 T1 rebuild: tools\build_build5.py (BUILD-4 pipeline unchanged), pak e43d8f97, 4,890,011 B, 73 files.
2026-10-10 BUILD-5 T2 verify: SHA256 73 PASS, round trip 16,391 exact + 24 same-visual + 0 fail, 45 entries differ from BUILD-4, 0 overflow among them.
2026-10-10 BUILD-5 T3 install: SWAP_TO_BUILD5.bat OK (first try hit a stale hash, removed, second OK), INSTALLED 16,415 (95.3 %); BUILD5_CHECKLIST.md written.
2026-10-10 BUILD-5 T4 close: refresh 0 ERR, secret_check PASS, PROJECT_MAP 3 4 6 7 8 + CHANGELOG, commit.
2026-10-10 PUBLISH-1 T1 make_public: tools\make_public.py writes public_repo\ (Arabic-only translation, docs, tools, README template); 17,222 rows exported, key lines and quoted English phrases scrubbed.
2026-10-10 PUBLISH-1 T2 public_check: tools\public_check.py + test_public_check.py PASS (forbidden paths, EN column, Latin sentences in AR, key, 25 MB, shared history).
2026-10-10 PUBLISH-1 T3 clone: github.com/exelight7/KH3RM_AR cloned (had only LICENSE GPL v2 + stub README, kept LICENSE); public_repo\ in .gitignore; publish.bat written.
2026-10-10 PUBLISH-1 T4-T5 push+release: pushed bd4d553 to exelight7/KH3RM_AR main (no auth prompt); README Arabic+English; out\release\ prepared (pak sha e43d8f97 = installed copy, SHA256.txt, INSTALL_AR.bat, REMOVE_AR.bat tested on a temp tree); gh not installed, Release left to the user (steps in LAST_REPORT).
2026-10-10 PUBLISH-1 T6-T7 rules+verify: tools\publish.bat, RULES.md and PROJECT_MAP 3 4 8 10; ls-remote shows main; 190 files on origin/main, forbidden scan clean.
2026-10-10 PUBLISH-1 T8 close: refresh 0 ERR, secret_check PASS, private commit (no push).
2026-10-10 RELEASE-080 T1 installer: tools\installer (WPF .NET 8, NuGet.config for nuget.org), embeds BUILD-5 pak (sha e43d8f97 = ~mods copy = SWAP_LOG), original XAML art, ar/en UI, app.ico drawn by us; EXE 70.9 MB.
2026-10-10 RELEASE-080 T2 tests: --selftest 22/22 PASS (steam vdf/acf, epic dat, browse, process check, install/remove on temp tree); ui_ar.png and ui_en.png rendered with --render.
2026-10-10 RELEASE-080 T3 release prep: gh 2.102.0 official zip (sha ae64e556...) in tools\gh-2.102.0, not logged in; assets + RELEASE_NOTES.md ready; waiting for user gh auth login.
2026-10-10 REVIEW-3 T1-T5: review3.tsv applied (5 rows: Isla de Muerta 01505, 05962, 01392, 03913, 06084); glossary KH3 form retired; row 05050 skipped (text is in 05051).
2026-10-10 REVIEW-3 T6-T7: 01302/01304 unchanged (addressee not clearly male); UNSURE_REVIEW2.md marked resolved.
2026-10-10 REVIEW-3 T8 close: refresh, secret_check, PROJECT_MAP 3 4 8 + CHANGELOG, private commit. BUILD-6 / v0.8.1 needed to install.
2026-10-10 FINAL-1 T1 fix: review\corrections\final1_fix.tsv (05051 fragment found exactly once, built from code points) applied by apply_corrections.py.
2026-10-10 FINAL-1 T1 note: the tool layer turns \uXXXX in a command into Arabic before Python sees it, so fragments were decoded from hex code points instead.
2026-10-10 FINAL-1 T1 result: 05051 now reads the REVIEW-3 wording; status reviewed kept.
2026-10-10 FINAL-1 T2 build: tools\build_build6.py (BUILD-5 wrapper + diff report), pak f6e8be85, 4,889,997 B, 73 files list/hash-list/unpack PASS.
2026-10-10 FINAL-1 T2 verify: round trip 16,391 exact + 24 same-visual + 0 fail; validate 0 ERR; 6 entries differ from BUILD-5 (01392 01505 03913 05051 05962 06084, 1 per locres).
2026-10-10 FINAL-1 T2 install: SWAP_TO_BUILD6.bat OK (Get-FileHash f6e8be85 = build = SWAP_LOG), INSTALLED 16,415; technical\BUILD6_CHECKLIST.md (6 places).
2026-10-10 FINAL-1 T3 installer: tools\installer 0.8.1 (Core.Version, ExpectedSha f6e8be85 = ~mods = SWAP_LOG, csproj PakPath BUILD-6); EXE 70,903,487 B sha 0e4cb475.
2026-10-10 FINAL-1 T3 tests: --selftest 21/21 PASS (ALL PASS); ui_ar.png / ui_en.png rendered with version 0.8.1.
2026-10-10 FINAL-1 T3 assets: out\release\v0.8.1\ (exe, pak, SHA256SUMS.txt, ui_ar.png, ui_en.png, RELEASE_NOTES.md).
2026-10-10 FINAL-1 T4 release: gh release create 0.8.1 --prerelease, title "0.8.1 (pre-release)"..."what changed since 0.8.0" (REVIEW-3 5 rows, 05051, STATS numbers), SmartScreen/legal/font notes kept.
2026-10-10 FINAL-1 T5 public: README template {{VER}} = RELEASE 0.8.1 in make_public.py, roadmap section (ar+en), docs\INDEX + PROJECT_MAP 3 4 6 8 + CHANGELOG before publishing; refresh 0 ERR, secret_check PASS.
2026-10-10 FINAL-1 T5 publish: publish.bat exit 0, public commit 739e622 (sync: FINAL-1), 211 files on origin/main, no pak/uasset/exe; only docs/img/ui_ar.png as image.
2026-10-10 FINAL-1 T6 close: refresh 0 ERR, secret_check PASS, LAST_REPORT part 1, private commit "...".
2026-10-10 FINAL-1 PART 1 DONE; resume point = PART 2 step 7 (image inventory).
2026-10-10 FINAL-1 T7 inventory: tools\images_inventory.py; 324 textures with English (title 26, scaleform_loc 89, tutorial 150, menus 2, logo 25, other 9, shared 23) in technical\IMAGES_INVENTORY.tsv; words read by eye from the contact sheets (technical\images_words.tsv).
2026-10-10 FINAL-1 T7 checks: 561 movies hold only external image refs (1009/1008) and one empty JPEG tag; 287 TexturePump assets are cutscene streaming lists (no pixels); 42 textures keep English (brands, keys, credits).
2026-10-10 FINAL-1 T7 plan: technical\IMAGES_PLAN.md (Markdown); contact sheets out\builds\IMAGES\ref\sheet_*.png (private).
2026-10-10 FINAL-1 T8 codec: tools\texture_codec.py (Texture2D uexp/ubulk, texture2ddecoder 1.0.6 + etcpak 0.9.15, block-patch encode); TOOLS.md with wheel SHA256.
2026-10-10 FINAL-1 T8 proof: byte-identical round trip on 18 textures (BC7 +/- mips, DXT5, BGRA +/- mips, BC4 with ubulk); full re-encode = same size, pixel diff reported (out\builds\IMAGES\roundtrip.tsv).
2026-10-10 FINAL-1 T8 fix: ubulk mip offsets are relative to BulkDataStartOffset (found by the BC4 test).
2026-10-10 FINAL-1 T9 renderer: tools\texture_text.py (fill clear/vlerp/fit/flat, sampled fill/outline/glow, Segoe UI BASIC layout on shaper output, 1x hinted below 24 px so dots/hamza stay); rects in technical\images_rects.tsv.
2026-10-10 FINAL-1 T10 pilot: pakchunk98-arabic-images_P.pak 307,669 B sha 75a94461 (HudCmdTextTT01_loc, mapName_tt01, HelpItem01600; 16 boxes); 6 files list/hash-list/unpack PASS, uexp re-parse PASS.
2026-10-10 FINAL-1 T10 install: SWAP_TO_IMAGES_PILOT.bat OK next to BUILD-6 (f6e8be85 unchanged); REMOVE_IMAGES_PILOT.bat tested (text pak kept), pilot reinstalled; technical\IMAGES_PILOT_CHECKLIST.md (Arabic, 3 places).
2026-10-10 FINAL-1 T11 close: refresh 0 ERR, secret_check PASS, PROJECT_MAP 3 4 6 8 + CHANGELOG + LAST_REPORT part 2, private commit "...".
2026-10-10 FINAL-1 T11 publish: publish.bat with IMAGES_PLAN.md, IMAGES_PILOT_CHECKLIST.md and the new tools only (no textures, sheets, uasset/uexp/ubulk or pak).
2026-10-10 FINAL-1 DONE; next: user screenshots of the pilot, then IMAGES-MASS -> 0.9.0 -> screenshots -> 1.0.0.
2026-10-10 CLOUD-PREP T1 make_cloud: tools\make_cloud.py regenerates cloud_repo\ (translation EN+AR, review incl. md/script/corrections, 16 Python tools + 4 tests, PROJECT_MAP, docs, state numbers; 322 files) and runs the secret scan on the result.
2026-10-10 CLOUD-PREP T1 cloud_check: tools\cloud_check.py = merge check + validate (0 ERR) + 4 unit test files + secret scan, ASCII PASS/FAIL; PASS in cloud_repo and in a copy under a path with spaces, output byte-identical after make_script/make_review/make_glossary/stats re-run.
2026-10-10 CLOUD-PREP T1 linux: no WSL on this PC (simulated: static scan for Windows-only calls and open() without encoding = clean, -X warn_default_encoding = 0 warnings); the real Linux run is the GitHub Action. apply_corrections.py now also reads review\corrections\cloud\ (checked rows -> reviewed + note), 1 new test.
2026-10-10 CLOUD-PREP T2 cloud_secret_check: tools\cloud_secret_check.py (forbidden paths/extensions, AES key read in memory and never printed, files over 25 MB, shared private history, --list mode for git ls-tree output).
2026-10-10 CLOUD-PREP T2 tests: tools\test_cloud_secret_check.py (6 tests: clean tree, 21 forbidden samples, list mode, key + size, key never in output, shared-history detection) PASS; added to refresh.bat.
2026-10-10 CLOUD-PREP T2 note: make_cloud calls it on every regeneration and aborts on any hit.
2026-10-10 CLOUD-PREP T3 CLOUD_RULES.md: 10 short rules (read PROJECT_MAP, one range only, corrections in review\corrections\cloud\<page>.tsv, cloud_check after each page, text rules, UNSURE_CLOUD.md, commit per page + state\CLOUD_PROGRESS.md, PR per range, no main, tools\ untouched).
2026-10-10 CLOUD-PREP T3 seeds: review\UNSURE_CLOUD.md, review\CLOUD_BUGS.md, state\CLOUD_PROGRESS.md created (cloud-owned, sync copies them back).
2026-10-10 CLOUD-PREP T3 decision: checked-but-unchanged rows are listed with new_AR == old_AR so apply_corrections can mark them reviewed without hand-editing TSVs.
2026-10-10 CLOUD-PREP T4 TASKS.md: review\cloud\TASKS.md generated by make_cloud: ranges 1-8 / 9-16 / 17-24 / 25-32 = 2400 / 2400 / 2400 / 2288 rows (9488 total) with the 8 review-focus points.
2026-10-10 CLOUD-PREP T4 branches: cloud/range-1..4, one PR each.
2026-10-10 CLOUD-PREP T4 scope: dialogue + cutscene subtitles in story order only (script_001-032); tips/menus not included.
2026-10-10 CLOUD-PREP T5 workflow: .github\workflows\check.yml (push + pull_request, ubuntu-latest, setup-python 3.x, python -I tools/cloud_check.py, contents: read, no secrets).
2026-10-10 CLOUD-PREP T5 note: branch protection needs a paid plan for private repos on some plans; the red check is visible on the PR, merge stays the user's decision.
2026-10-10 CLOUD-PREP T5 included in make_cloud FILES so it is pushed with the repo.
2026-10-10 CLOUD-PREP T7 sync: tools\sync_cloud.py/.bat: ff-only pull, replay new cloud corrections from applied\cloud\ (old_AR must match, else nothing applied and ids reported), report unexplained TSV differences, validate 0 ERR, make_cloud, cloud_check, commit sync, push (never forced, --no-push).
2026-10-10 CLOUD-PREP T7 docs: docs\CLOUD_WORKFLOW.md (7 steps export, cloud session, PR review, merge, sync, BUILD-7, release; Arabic summary).
2026-10-10 CLOUD-PREP T7 decision: sync replays corrections instead of copying changed TSVs (never overwrites local changes silently).
2026-10-10 CLOUD-PREP T8 PROJECT_MAP: section 4 cloud-review decision (1.0.0 LOCKED), cloud corrections rule and the general note "..." (no row marked verified); sections 3 and 8 updated.
2026-10-10 CLOUD-PREP T8 review\RULES.md: cloud-review paragraph added.
2026-10-10 CLOUD-PREP T8 refresh.bat: runs test_cloud_secret_check.py.
2026-10-10 CLOUD-PREP T6 repo: gh repo create exelight7/KH3RM_AR_work --private; gh repo view = PRIVATE; cloud_repo\ git init (no shared history with the private project), commit b1ffb1c "...", pushed to main (323 files).
2026-10-10 CLOUD-PREP T6 verify: git ls-tree -r origin/main --name-only = 323 paths, cloud_secret_check --list PASS (no forbidden path); GitHub Action check on the first push ran on ubuntu-latest: success (19 s).
2026-10-10 CLOUD-PREP T6 note: this was the real Linux test of all cloud tools; no tool needed changes; no tool is Windows-only (tools\*.bat and game/build tools are simply not exported).
2026-10-10 CLOUD-PREP T9 close: refresh 0 ERR, secret_check PASS, sync_cloud run, private commit "..." (private only, public repo not touched).
2026-10-10 CLOUD-PREP T9 next: user starts the 4 cloud sessions (CLOUD_RULES.md), merges PRs, tools\sync_cloud.bat, BUILD-7.
2026-10-10 CLOUD-PREP DONE.
2026-10-10 SYNC-BUILD7 T1 sync: gh pr list = PRs 1-6 MERGED; sync_cloud first run refused (51 ids corrected by two parallel cloud files, no old_AR mismatch; nothing applied); apply_corrections now merges identical results and check mark + one real change (no id had two different real changes); re-run applied 69 files, 182 rows really changed, validate 0 ERR, cloud_repo pushed.
2026-10-10 SYNC-BUILD7 T2 glossary: Diving Strike / Powerwild / Frost Serpent / Monsters Inc aligned to rows 16013 / 00640 / 00657 / 13658 (Arabic read from the rows), approved, note "supervisor SYNC-BUILD7".
2026-10-10 SYNC-BUILD7 T3 BUILD-7: tools\build_build7.py; sha f9e23f37..., 73 files PASS, round trip 16391 exact + 24 same-visual + 0 fail, overflow 15 rows = BUILD-6 set (16359 Risk Dodge fits), 182 entries differ from BUILD-6; installed via SWAP_TO_BUILD7.bat (before f6e8be85, after f9e23f37); technical\BUILD7_CHECKLIST.md.
2026-10-10 SYNC-BUILD7 T4 installer 0.8.2: csproj PakPath + Core.ExpectedSha + SelfTest label; first publish still embedded BUILD-6 (csproj path edit missed), fixed and rebuilt; selftest 22 PASS; ui_ar/ui_en rendered.
2026-10-10 SYNC-BUILD7 T5 release 0.8.2 (pre-release): 5 assets, sizes/SHA256 match SHA256SUMS.txt (gh release view).
2026-10-10 IMAGES-MASS cat 1 (command/HUD headers + menus) DONE: 21 textures in technical\images_rects.tsv (16 HudCmdText* incl. hud_dance/hud_specialship copies, HudLeft CHAIN, ShootLockTxt MAX + glow layer, Hologram DATA GREETING (2 pieces x 2 sizes, diamonds kept), CodeMenu COMPLETE!/RANK UP! (! and UP pieces emptied, phrase in one piece), SlideShowTx 8 labels) + pilot TT01 re-rendered with the stroke rule; checks all PASS (out\builds\IMAGES-MASS\checks.tsv). Plates HE01/FZ01 = fill inpaint. Minigame HUD (16 scaleform_loc, priority 3) moved after cat 5 as cat 1b.
RESUME IMAGES-MASS: next = cat 2 tutorial pictures (150 HelpItem*, one rect list per image id, platform copies reuse it). Build: python -I tools\texture_text.py mass.
2026-10-10 IMAGES-MASS cat 2 checkpoint: tutorial ids done = HelpItem01400 01600 01700 01800 55900 56000 60200_2 60400 (+10101_1_kb keep: key names); spec technical\images_work\tutorial_spec.tsv, generator tools\images_tutorial_rects.py; renderer: erase box, heal fill, tpl sources. RESUME: next ids 56100 60700 then the platform-copy ids (00300 ...).
2026-10-10 IMAGES-MASS cat 2 checkpoint 2: 41 of 76 ids done or kept (to 30402); RESUME next = 30501 30601 30700 30701 30703_1 30703_2 30704 30705 40100.. (spec technical\images_work\tutorial_spec.tsv).
2026-10-10 IMAGES-MASS cat 2 (tutorial pictures) DONE: 128 of 150 HelpItem textures repainted (65 ids; 1,039 boxes; checks all PASS); English kept: 21 textures (11 ids with no readable/English words: camera-only HUDs, key names, 5-6 px gummi HUD) + ps4/HelpItem30402 (PS4 layout differs, PC never loads it); 56100 letter grid kept (ship-name character set). New strings I0001-I0008 in translation\images_strings.tsv.
RESUME IMAGES-MASS: next = cat 3 area banners (25 mapName_*; tt01 = pilot, done).
2026-10-10 IMAGES-MASS cat 3 (area banners) DONE: 24 mapName_* + pilot tt01 = 25 of 25 (mi01 Monsters, Inc. = world logo, kept); tools\images_banner_rects.py (2-line Arabic for 2+ words, same size; bx/ts plates = cut-out text, fill holes + effect knockout; mi stencil letters only, splatter kept); checks PASS.
RESUME IMAGES-MASS: next = cat 4 LSI (9 textures) and key atlases (IconText*_km = keep by plan: key names).
2026-10-10 IMAGES-MASS cat 4 (LSI + key atlases) DONE: 9 of 9 LSI textures (12 boxes, 1 px outline to match the bold LCD lettering; E/F letters kept); key atlases IconText_km / IconTextSub_km = keep (key names, plan). New strings I0009-I0012.
RESUME IMAGES-MASS: next = cat 5 shared HUD textures (14), then cat 1b minigame HUDs (16).
2026-10-10 IMAGES-MASS cat 5 (shared HUD) DONE: 11 of 14 repainted (English cell only; other-language cells untouched): autosave_01, HudStatusTxt, HudStatusTxtCA, HudCamera03, HudCodeInfo_text, HudKeyhole_02, ItemListLibrary_bmpIcon, MarkLibrary_01, HudBlackPearlChase_02, Hud_LuxordText (VS kept), battlereport_01. Kept: HudRight03 (no English text found in the 64x64 texture, heart icon only), HudKairi_01 (name painted over an ornament with a matching glow copy), SpecialShip_02 (LV/MAX 6-8 px, unreadable). New strings I0013-I0018.
RESUME IMAGES-MASS: next = cat 1b minigame HUDs (16 scaleform_loc, priority 3), then pak + install + docs.
2026-10-10 IMAGES-MASS close: pak 233ef228 installed (SWAP_TO_IMAGES_MASS.bat), checklist, stats 193/234 = 82.5 %, refresh 0 ERR. RESUME IMAGES-MASS: cat 1b minigame HUDs (16, see technical\IMAGES_STILL_ENGLISH.tsv 'not yet'), then rebuild (texture_text.py mass), update the pinned sha in tools\make_swap_scripts.py, reinstall.
2026-10-11 README-AR public README, TESTER_GUIDE, FAQ, issue template, LICENSE_TODO and release 0.8.3 notes are Arabic only; make_public.py + README template generate them; PROJECT_MAP/CHANGELOG updated.

2026-10-13 CODEX-REVIEW4-1 review: 4324 rows read and ledgered; 148 audited skips, 14 context questions preserved.
2026-10-13 CODEX-REVIEW4-1 apply: 36 canonical corrections + 1 image-source corrections; original source columns and untargeted Arabic unchanged.
2026-10-13 CODEX-REVIEW4-1 checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.

2026-10-13 CODEX-REVIEW4-2 review: 4306 rows read and ledgered; 196 audited skips, 12 context questions preserved.
2026-10-13 CODEX-REVIEW4-2 apply: 49 canonical corrections + 0 image-source corrections; original source columns and untargeted Arabic unchanged.
2026-10-13 CODEX-REVIEW4-2 checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.

2026-10-13 CODEX-REVIEW4-3 review: 4305 rows read and ledgered; 227 audited skips, 14 context questions preserved.
2026-10-13 CODEX-REVIEW4-3 apply: 32 canonical corrections + 0 image-source corrections; original source columns and untargeted Arabic unchanged.
2026-10-13 CODEX-REVIEW4-3 checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.

2026-10-13 CODEX-REVIEW4-4 review: 4305 rows read and ledgered; 236 audited skips, 24 context questions preserved.
2026-10-13 CODEX-REVIEW4-4 apply: 19 canonical corrections + 0 image-source corrections; original source columns and untargeted Arabic unchanged.
2026-10-13 CODEX-REVIEW4-4 checks: mandatory refresh PASS, 0 ERR, secret_check PASS; public checkpoint ready.

- CODEX-REVIEW4: اكتملت 4/4؛ 17240 مدخلا، 137 تصحيحا، 64 سياقا معلقا. نشرت الدفعات الأربع مستقلة.

2026-10-13 INSTALLER-CROSSPLATFORM ui: Avalonia 0.8.3, user-selected artwork, credits in GitHub only.
2026-10-13 INSTALLER-CROSSPLATFORM build: win-x64 and linux-x64 published locally with unchanged BUILD-7 payload; Windows UI previewed, Linux runtime not available.
2026-10-13 INSTALLER-CROSSPLATFORM publish: update current 0.8.3 with additive installer assets; preserve all previous release assets.

2026-10-13 README-POLISH design: centered header, installer screenshot, direct Windows/Linux downloads and compact installation.
2026-10-13 README-POLISH content: remove thanks and corporate disclaimers from README; retain technical release status and standalone Graphify footer.
2026-10-13 README-POLISH publish: update generator template and both README copies; documentation only.

2026-10-13 OPUS-090 A BUILD-8: build_build8.py (BUILD-7 pipeline), pak 45f043de 4,890,167 B, 73 files PASS, round trip 0 fail, overflow same 15; differs from BUILD-7 in exactly the 136 corrected rows; SWAP_TO_BUILD8.bat (not installed).
2026-10-13 OPUS-090 B IMAGES-MASS2: 16 minigame HUD textures (104 boxes, strings I0019-I0042) + I0013 re-render; pak bc546502 40,442,423 B, 210 textures, 420 files PASS; 209/234 = 89.3 %; SWAP_TO_IMAGES_MASS2.bat, technical\IMAGES_MASS2_CHECKLIST.md (not installed).
2026-10-13 OPUS-090 C installer 0.9.0: both paks embedded, images checkbox (default off), per-pak SHA256 install/remove, 37/37 selftest PASS; win-x64 + linux-x64 in out\release\v0.9.0 (Linux not run on Linux).
2026-10-13 OPUS-090 D/E: PROJECT_MAP 3/4/8, CHANGELOG, README template (0.9.0, BUILD-8), make_public temp run + public_check PASS, vault notes; refresh 0 ERR, secret_check PASS; private commit. RESUME: user installs BUILD-8 (+ IMAGES-MASS2) from cmd and confirms -> build_build8.py --installed -> publish.bat -> gh release create 0.9.0 (commands in state\LAST_REPORT.md).
2026-10-13 RELEASE-090 1 IMAGES-MASS3: of the 25 plan textures not repainted, 2 repainted (ps4 HelpItem30402 control panel, rows 16121/16150-16152; SpecialShip_02 LV/MAX/NEXT/OBJECTIVE in the movie's sprite regions, rows 13279/15771/13280/13294), 23 KEEP ENGLISH with written reasons (HudKairi_01 repaint test rejected: hard cut edges); pak d8d13948 41,083,305 B, 212 textures, 0 FAIL, 424 files list/hash-list/unpack PASS, all 420 MASS2 files byte-identical; 211/234 = 90.2 % = 100 % of repaintable; SWAP_TO_IMAGES_MASS3.bat.
2026-10-13 RELEASE-090 2 install: SWAP_TO_IMAGES_MASS3.bat from cmd, ~mods images pak = d8d13948 (pin), text pak still BUILD-8 45f043de; build_build8.py --installed 16415/16415, texture_text.py --installed PASS.
2026-10-13 RELEASE-090 3 installer 0.9.0 rebuilt (IMAGES-MASS3 embedded), win-x64 + linux-x64, 37/37 selftest PASS; out\release\v0.9.0 refreshed (exe, tar.gz, 2 paks, SHA256SUMS 4 lines, Arabic RELEASE_NOTES 0 placeholders).
2026-10-13 RELEASE-090 4/5 README: make_public into TEMP, public_check PASS, but README differs in 2 wording lines (49, 59, from the OPUS-090 D template edit) besides value lines -> STOP before publishing: no publish.bat, no push, no release.
2026-10-13 RELEASE-090 6/7: docs\ROADMAP_TO_1.0.0.md (Arabic), PROJECT_MAP 3/4/8, CHANGELOG; refresh, secret_check, private commit. RESUME: user says yes/no to README lines 49/59 -> (no: revert those 2 template lines) -> tools\refresh.bat -> tools\publish.bat -> gh release create 0.9.0 --prerelease with the 5 assets of out\release\v0.9.0 (command in state\LAST_REPORT.md).
2026-10-13 REVIEW5-Q1 1 split: 16,415 translated/reviewed/verified rows (807 todo + 42 image strings excluded) cut by ascending id into Q1..Q4 (4,104/4,104/4,104/4,103), review\split\Q*_ids.tsv + MANIFEST.md (Q1 = Claude, Q2 = GPT, Q3/Q4 reserved); union and no-overlap checks PASS. FAQ line 6 reworded (REMOVE_AR.bat no longer mentioned).
2026-10-13 REVIEW5-Q1 2 review of Q1 only: 14 pages, 4,104 rows read, 9 fixes applied (00114, 00828, 00874, 00979, 02373, 02487, 02534, 02882, 04043; files review\corrections\applied\review5_q1_*.tsv), 3 doubts in review\REVIEW5_Q1_QUESTIONS.md (00770, 01201, 01626); 137 Codex rows, 5 BUILD9_proposed rows, DECISIONS/context/Tangled rows untouched; refresh 0 ERR after every page.
2026-10-13 REVIEW5-Q1 3: no build, no install, no release (fixes wait for BUILD-9); PROJECT_MAP 3/4/8, CHANGELOG, refresh, secret_check PASS, private commit REVIEW5-Q1, publish (FAQ + generated docs). RESUME: BUILD-9 takes review5_q1 fixes + 5 BUILD9_proposed rows + accepted GPT Q2 fixes.
2026-10-14 RELEASE-091 1 IMAGES-MASS4: 23 keep items retried; 17 NO-TEXT by pixel inspection; HudKairi_01 repainted (new plate grown from the text + 4 plate rows into the cleaned bar, right edge feathered, flash copy regenerated by a fitted blur model) and HelpItem50300 partly (row 10693, 18 px, contrast 244); 4 gummi pictures unreadable (contrast 134-136 < 192); new readability gate + trial mode in texture_text.py; pak e8ebf70a 41,492,782 B, 214 textures, 0 FAIL, 428 files PASS, 423 MASS3 files byte-identical, HelpItem50600 changed on purpose (row 10694 reworded in BUILD-9).
2026-10-14 RELEASE-091 2/3 figures N 213 / M 17 / K 4 = 213 of 217 textures with text (98.2 %), plan 213/234 (91.0 %); SWAP_TO_IMAGES_MASS4.bat from cmd, ~mods images = e8ebf70a (pin), text still BUILD-10 89e00ead; build_build10.py --installed 16415/16415, texture_text.py --installed PASS.
2026-10-14 RELEASE-091 4-7 installer 0.9.1 (BUILD-10 + IMAGES-MASS4) win-x64 + linux-x64, 37/37 selftest PASS; out\release\v0.9.1 (5 assets + Arabic notes); README 5 value/link lines only ({{BUILD}} placeholder), public_check PASS on TEMP; refresh 0 ERR, secret_check PASS, publish.bat, pre-release 0.9.1; PROJECT_MAP 3/4/8, CHANGELOG, ROADMAP status. RESUME: in-game check of the Kairi name and the 42 changed rows; decision on the 522 earlier image boxes under the readability bar.
2026-10-14 BATCH-234 2a/2b glyphs: all Arabic of 16,415 shaped rows in all 4 TresFont classes; U+2015 missing in $KH2Menu -> 04638 / 08847 fixed (batch2_dash.tsv); air gauge already shows the I0013 word since IMAGES-MASS2 (no repaint needed, BUGFIX-1 note was wrong).
2026-10-14 BATCH-234 3 decisions: review\BATCH3_DECISIONS.md, 77 ids, 12 fixed (batch3_review.tsv, validate check() clean), 65 kept; refresh 0 ERR.
2026-10-14 BATCH-234 4 IMAGES-MASS5 d5b39c12...: 137 of 522 under-bar boxes enlarged (385 remain), 0 FAIL, 428 files PASS; BUILD-12 2cdb5b7b...: diff vs BUILD-11 = 14 corrected ids; both installed (sha = pins); installer 0.9.2 37/37; release 0.9.2.
