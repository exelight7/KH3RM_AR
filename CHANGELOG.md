# Changelog

## 2026-10-31 — PLAN-1.0.0 (documents only)

Road to 1.0.0 recorded (docs/rounds/PLAN-1.0.0.md): next pre-release is 1.0.0-rc.2; in-game verification by the focused checklist technical/RC_CHECKLIST.md (62 places). No build, translation, installer or release change.

## 2026-10-31 — MAINT-1 (maintenance, no new build)

Repaired PROJECT_MAP.md and CHANGELOG.md (backtick prefix on every line and path escapes lost as control characters since BATCH-234); PROJECT_MAP auto sections 7 and 9 refreshed again (they had stopped updating). Same escape damage fixed in three tool comments. New guards: update_map.py fails on missing auto headings, public_check.py refuses damaged text files; new tools/repair_docs.py for the private copies. Data-dependent tests skip in a public clone. No translation, pak, installer or release change.

## 2026-10-16 — RELEASE-099 (release candidate 0.9.9)

Windows now downloads as a self-contained folder ZIP, with every runtime/native dependency beside the installer; Linux is packaged as the full publish folder in tar.gz. Disabled single-file bundling, bundle compression and native-library self-extraction; omitted debug symbols. Built with SDK 8.0.426 and bundled .NET 8.0.32, included IBM Plex Sans Arabic OFL. BUILD-18 and IMAGES-MASS11 are byte-identical to 0.9.8; no translation/font/image changes. Windows selftest 37/37 before and after ZIP extraction; all archive members verified by SHA. README layout preserved, download version/link and operation cell updated. The owner's VT 0/70 screenshot covers only the previous test apphost (8a56394e...b665), not the 0.9.9 package; the new apphost (e7753cc7...2452) has zero overlay and no .NET bundle. Exact Zillya heuristic unconfirmed, Defender unavailable, installer unsigned, Linux not runtime-tested. Release URL: https://github.com/exelight7/KH3RM_AR/releases/tag/0.9.9 . No game install or 1.0.0 release.

## 2026-10-16 — RELEASE-098 (release 0.9.8)

GitHub pre-release 0.9.8 (https://github.com/exelight7/KH3RM_AR/releases/tag/0.9.8) with six assets: installer 0.9.8 for Windows (single file, sha256 187cfd3910cff5e0386ae9e84a387854b3c7ad5c8b558f1326d26ea92e6452ce) and Linux (tar.gz, 985d8343072af5adbce5899cbb587a856c7581afc3d6a976a9bff0b6c831ecf3), the BUILD-18 text pak (dde67ce6...e527), the optional IMAGES-MASS11 images pak (7b37f84b...c964), the Windows folder zip (fae022fe08bd3a8419f78af4e67de583e5b1acaa7cf380283348302664550279) and SHA256SUMS.txt (now 5 lines, the zip included). Since 0.9.2: 98 rows corrected (44 in BUILD-13, 54 from the full language review in BUILD-15), IBM Plex Sans Arabic + Segoe UI Bold headers (513 rows rewrapped, overflow 15 -> 11), battle HUD words enlarged (BUILD-17) and drawn from a 2x texture (BUILD-18), small image text sharpened (MASS6-MASS11: 368 of 385 boxes over the readability bar). Installer `--selftest` 37 / 37 PASS on the single-file and folder exe. README: version, build and links only.

## 2026-10-16 — HUD-VECTOR (BUILD-18)

BUILD-18 text pak (sha256 dde67ce67b7d93bf95835a0126e317e003e3a2a51370321da51ce48035afe527, 5,103,489 B): the battle HUD words Focus, Max and Charge (HudStatus and the Caribbean HudStatusCA) are drawn from a new texture `HudStatusTxtAR` (BC7 512x128) that holds each word at 2 texels per screen pixel at 1080p, instead of magnifying the old 256x128 cells x1.20-1.45. The movies get one new image tag, new fill matrices for the three word shapes and the texture path in their reference list; everything else is byte-identical to BUILD-17 (same translation, same fonts, same label positions and sizes). New tools `tools\hud_hires.py` and `tools\build_build18.py`. Simulated edge sharpness 158-168 % of English at 1080p (MASS11: 111-127 %). Images pak stays IMAGES-MASS11. Installed (`SWAP_TO_BUILD18.bat`), not published; rollback `SWAP_TO_BUILD17.bat`.

## 2026-10-15 — HUD-SOFTEN (IMAGES-MASS11)

IMAGES-MASS11 images pak (sha256 7b37f84b390db3d62fe837892a99bbe3fe4ae7cccf9bc67a119decb3d643c964, 41,493,315 B): the HUD words Focus, Max, Charge, Air (HudStatusTxt and CA) keep their MASS10 recipe but get softer edges (Focus hard:1.5, Max hard:1, Charge hard:1, Air hard:12) to smooth the stair-steps of MASS10, chosen by lowest contour jaggedness with magnified edge >= 110 % and crisp >= 75 % of English. New renderer tokens aa:<k> and ramp:<alpha>[:out]; new jaggedness metric and `hud_sheet.py soften`. Only the two HUD textures differ from MASS10. Text pak stays BUILD-17. Not published.

## 2026-10-15 — HUD-CRISP (IMAGES-MASS10)

IMAGES-MASS10 images pak (sha256 2dfb6baff273fc0320c687b3c0afac988703e83d5b9682a8ede61cb84f83ba34, 41,491,910 B): the battle HUD words Focus, Max, Charge and Air (HudStatusTxt and HudStatusTxtCA) are redrawn with hard edges (new effect `hard:<k>`, a solid outline, 2 px for Focus/Max/Air) so they stay crisp after BC7 compression and the movie's x1.20-1.45 magnification. They were chosen by a new simulator in `tools\hud_sheet.py` (`crisp` / `trial`). Focus stays IBM Plex; Max, Charge and Air use Segoe Bold/Semibold. Only the two HudStatusTxt textures differ from IMAGES-MASS9. Installed (`SWAP_TO_IMAGES_MASS10.bat`), not published; rollback `SWAP_TO_IMAGES_MASS9.bat`.

## 2026-10-15 — HUD-PLEX (IMAGES-MASS9)

IMAGES-MASS9 images pak (sha256 abe75ddd6ee0e1522ec8f217d88a4826cdc4ba89a88655c1c58906bbc9245573, 41,494,688 B): the battle HUD words Focus, Charge and Air are now drawn in IBM Plex Sans Arabic (Regular, the only weight available locally) instead of Segoe UI Bold, in HudStatusTxt and HudStatusTxtCA. Max stays Segoe Bold: no Plex Regular version kept its letters joined at that size. New effect `face:plex` and a joined-letters check in `tools\texture_text.py`. All other image text stays Segoe; only the two HudStatusTxt textures differ from IMAGES-MASS8. Installed (`SWAP_TO_IMAGES_MASS9.bat`), not published; text pak stays BUILD-17. Rollback: `SWAP_TO_IMAGES_MASS8.bat`.

## 2026-10-15 — HUD-SCALE (BUILD-17 + IMAGES-MASS8)

BUILD-17 text pak (sha256 58bad87725b3e1029cb7fb4a31258a0fda97eca5d3d4192d1562ed3bc4f9858c, 5,088,344 B) = BUILD-16 plus the two battle HUD movies HudStatus and HudStatusCA, which now draw the gauge words larger: Focus x1.45 (59x20 -> 86x29 px at 1920x1080), Max with its badge plate x1.25 (the flash effect still zooms about the word), Charge x1.20. Only the label shapes and the Max placements change (170 bytes per movie, same size and structure); no text row and no font byte differs from BUILD-16. IMAGES-MASS8 images pak (sha256 917d92733f1e7808007bc089aa067e7b12973d3ddc6ae1045532908baea282e0, 41,494,852 B): the Focus and Max cells are pre-sharpened for the magnification (new effect `sharp:`); only the two HudStatusTxt textures differ from IMAGES-MASS7. Both installed (`SWAP_TO_BUILD17.bat`, `SWAP_TO_IMAGES_MASS8.bat`), not published. Rollback: `SWAP_TO_BUILD16.bat` then `SWAP_TO_IMAGES_MASS7.bat`.

## 2026-10-15 — FOCUS-FIX (IMAGES-MASS7)

IMAGES-MASS7 images pak (sha256 dabd8b855cb83d3aa0b529bcccbcb5a80fc04ac382ed57346b6ae25aa3b38bad, 41,494,952 B): the battle HUD gauge words are bigger and cleaner. The HudStatus movie draws them 1:1 from HudStatusTxt / HudStatusTxtCA cells (Focus 59x20 px at 1920x1080), so each word now uses its whole cell, stretched wider where the cell height is the limit. Focus text 35x11 -> 50x13 px, Charge 31x9 -> 48x13, Max 42x10 -> 45x12, Air 34x10 -> 36x12. A leftover tick of the English outline beside Focus and Charge is gone. Only the two HudStatusTxt textures differ from IMAGES-MASS6. Installed (`SWAP_TO_IMAGES_MASS7.bat`), not published; text pak BUILD-16 unchanged.

## 2026-10-15 — IMAGES-MASS6

IMAGES-MASS6 images pak (sha256 a6b6d55625de72f2948c581f445ab6298a44f5fb644f60bbf72743a83f19aa55, 41,494,329 B): small image text redrawn heavier and cleaner. The battle HUD gauge words (Focus, Max, Air, Charge) now use Segoe UI Bold (Focus, Max, Air also with a thin contrast halo). Of the 385 boxes under the readability bar in IMAGES-MASS5, 368 now pass (bold / semibold face, letter spacing, pixel-grid hinting of stems and dots), 10 tiny labels measure better but stay under, 7 are kept (6 would cover an icon). New tools\images_sharpen.py, plan in technical\images_sharpen_plan.tsv. Only the 107 files of textures with changed boxes differ from IMAGES-MASS5. Installed (`SWAP_TO_IMAGES_MASS6.bat`), not published; text pak BUILD-16 unchanged.

## 2026-10-15 — BUILD-16

BUILD-16 text pak (sha256 5ff72110e9ab7c8cca443ce6d7c9b5d27b209bde395a904d6cf81ba08ca1ec5f, 4,888,484 B) = BUILD-15 with the ya glyphs (U+064A, FEF1, FEF2 in $jimakuNE and $sougei) restored to the BUILD-14 Plex form (dots back under the bowl, owner option B); every translation row (all 54 BUILD-15 fixes) and every other glyph unchanged, diff vs BUILD-15 = the two TresFont files. The clipped-dots problem of isolated / final ya in subtitles may return. Installed (`SWAP_TO_BUILD16.bat`), not published; images pak unchanged.

## 2026-10-15 — BUILD-15

BUILD-15 text pak (sha256 11c078410b74471d8a078707ac20035de6d3fa1910e5237a69992a068a17b79f, 4,888,464 B) = BUILD-14 + (1) ya dots fix inside IBM Plex Sans Arabic: the two dots of isolated / final ya (U+064A, FEF1, FEF2) moved up into the bowl in $jimakuNE and $sougei (they hung 23 px below the baseline in 38 pt subtitles and could be cut off); letter shapes, advances and every other glyph unchanged; (2) full language review of all 16,415 rows + image strings: 54 rows corrected (grammar, consistency, translation, spelling, dialogue), 8 questions for the owner. No line rewrapped by the font change; overflow the same 11 rows. Installed (`SWAP_TO_BUILD15.bat`), not published; images pak unchanged.

## 2026-10-14 — BUILD-14-FONTS

BUILD-14 text pak (sha256 a7d2eacd7bf7f790d91b57568e184ab45b0266112baa98532380c661d6bf5f92, 4,888,611 B) = BUILD-13 text with the owner-approved font swap: Arabic in $sougei and $jimakuNE drawn with IBM Plex Sans Arabic Regular (1.1.0, OFL 1.1), in $KH2Menu with Segoe UI Bold; $JimakuJP unchanged; the game's own Latin / digit / HP glyphs unchanged in every class. Line breaks recomputed with the new advances: 513 rows rewrapped, no translation changed; overflow rows 15 -> 11 (03474 06647 10704 15160 now fit). New entry point `tools\build_build14.py` + `tools\font_swap_adapter.py` (hash-pinned prepared TresFont from the GPT FONT round). Installed (`SWAP_TO_BUILD14.bat`), not published; images pak unchanged and still Segoe-rendered. Rollback: `SWAP_TO_BUILD13.bat`.

## 2026-10-14 — BUILD-13

BUILD-13 text pak (sha256 3675a16aefe35a70010e1c721de0701f7709b589b1987fb1a4860653bf78fd7c, 4,890,254 B) = BUILD-12 + 44 rows: the 22 REVIEW6-Q2Q3 fixes + 22 accepted GPT R2 proposals (addressee number / gender 01263 01427 02003 03884 04039; grammar 02021 02461 02913 03679; wording 02552 02938 12893 13534 14837 15516; glossary forms 13217 13397 13474 14158 14822 16172 16321). 14550 skipped (Sonic Diver, identical string 10615 unchanged). Installed, not published; images pak unchanged. Round 2 of the split review merged.

## 2026-10-14 — REVIEW6-Q2Q3

Second independent review of quarters Q2 and Q3 (8,208 rows, 28 pages of 300). 22 source corrections applied (gender of speakers / addressees in 04426, 09464, 09488, 09518, 09718, 09785, 09969; pronoun gender 04599; passive wording 08010; Hydra 09676; Aero gummi series 11415-11426), 6 doubts kept in `review/REVIEW6_QUESTIONS.md`. No build, no install, no publish: the fixes wait for BUILD-13 together with the accepted GPT round-2 proposals.

## 2026-10-14 — BATCH-234 (release 0.9.2)

BUILD-12 text pak (sha256 2cdb5b7b7ee79f5432f488aa86f1a2cf724eaf6983c0077f797dd831e62795cd, 4,890,318 B) = BUILD-11 + 14 corrections: 2 from the glyph scan (U+2015 has no glyph in $KH2Menu, now U+2014 as in EN: 04638, 08847) and 12 from the evidence decisions in review\BATCH3_DECISIONS.md (07579, 14373, 14763, 14858, 14859, 09126, 08362, 11245, 06084, 10882, 10883, 11500). Glyph coverage: every Arabic character of 16,415 rows is in all 4 TresFont classes (review\BATCH2_GLYPHS.md). IMAGES-MASS5 images pak (sha256 d5b39c12c25f34108b97d9d8c6056374800bcd6a9727bb26f82a01941a0bff21, 41,494,619 B): 137 of the 522 under-the-bar MASS3 boxes enlarged where the box has room and no artwork beside the old text gets covered (tools\images_enlarge.py); 385 remain; 30 textures changed, 398 files byte-identical to IMAGES-MASS4. Air gauge: already shows the I0013 word since IMAGES-MASS2 (the BUGFIX-1 note was wrong); unchanged. Installer 0.9.2 (37/37 selftest), folder zip as sixth asset. Both paks installed (sha = pins).

## 2026-10-14 — BUGFIX-1

BUILD-11 (installed, not published): the native Windows quit message box drew our pre-shaped Arabic reversed. New hook in tools\build_build11.py: ids in translation\raw_logical_ids.tsv (15656, 15657, 15999) are emitted as raw logical Arabic; everything else is BUILD-10 (3 entries differ). Yes / No are shared with Scaleform and unchanged. sha256 8aa9b0e816e61a303f8b1f36e03fa90caf5c2d0a4ed90e1b7bd0a812ffeb7f91. Water review in review\BUGFIX1_WATER.md (no mistranslation found).

## 2026-10-14 — UPLOAD-FOLDER-ZIP

Uploaded KH3RM_AR_Setup_v0.9.1_windows-x64-folder.zip (sha256 df26c6b459963a1f10adb2e174b9e5297b56bcc0c4578943f7c21d199539552d) to pre-release 0.9.1 and appended an Arabic note to its description.

## 2026-10-14 — AV-FALSEPOS

نسخة المثبت 0.9.1 كمجلد (غير مدمجة في ملف واحد وغير مضغوطة، ذاتية الاحتواء) للفحص ضد الإيجابيات الكاذبة لمضادات الفيروسات: `out/release/v0.9.1-folder/` وملف zip بجانبه؛ نجح الفحص الذاتي. لم ترفع ولم تنشر، وأصول الإصدار الحالية لم تتغير. أضيف `docs/INSTALL_MANUAL.md` لدليل التثبيت اليدوي.

## 2026-10-14 — RELEASE-091

الإصدار التجريبي 0.9.1: حزمة النص BUILD-10 (42 سطرا تغير عن 0.9.0: 22 من BUILD-9 و20 من BUILD-10) وحزمة الصور IMAGES-MASS4. أعيدت محاولة الصور الـ23 الباقية: 17 صورة ليس فيها نص يترجم (أزرار وعدادات وأسماء مفاتيح ورمز قلب)، وأعيد رسم اسم كايري في شعار واجهتها (لوحة الاسم بنيت من جديد حول النص العربي بلا حواف مقطوعة، والومضة المموهة أعيد توليدها من الشعار الجديد) وكلمة المضاعف في صورة شرح أسلحة سفينة الغامي. 4 صور تبقى بالإنجليزية لأن كلماتها بارتفاع 4-5 بكسل لا تقرأ بالعربية: فحص وضوح جديد يقيس تباين الخط (75% على الأقل) واتصال الحروف عند الحجم الحقيقي. صورة شرح واحدة أعيد رسمها لأن سطرها صحح في BUILD-9؛ بقية الصور القديمة مطابقة بايتا ببايت. المجموع 213 من 234 صورة في الخطة (91.0%)، أي 213 من 217 صورة فيها نص (98.2%). المثبت 0.9.1 لـWindows وLinux، ونجحت فحوصه الذاتية الـ37.

## 2026-10-14 — BUILD-10

بناء BUILD-10 لحزمة النص وتثبيته: يضم 19 تصحيحا من مراجعة GPT للربع الثالث (12 معتمدة مباشرة و7 بعد مطابقة المسرد: الكوكبات والبلورة والمخطط الخاص+) إضافة إلى تصحيح 17169 من الربع الرابع. تجاوزت كل التصحيحات فحص old_AR والمدقق والمسرد بلا تخط. لم تطبق 10882 و10883 و11500 ولا بقية صفوف GPT. التحقق كما في BUILD-9: 73 ملفا PASS، لا فشل في الدورة الكاملة، 0 أخطاء، والفيضان نفسه 15 صفا بلا جديد. لم ينشر.

## 2026-10-14 — REVIEW5-Q4

راجع Claude الربع الرابع (4103 صفوف، من 12884 إلى 17222: القوائم والخرائط والمسرح والقائمة المميزة والألعاب المصغرة وقصة هاتف الغامي والتقارير والمسرد والشخصيات وملاحظات الأعداء والإعدادات والأوامر والقدرات وتلميحات الهزيمة والدروس) صفا صفا مقابل النص الأصلي في 14 صفحة. طبق تصحيح محلي واحد (نطاق إبراز اللون في سطر 17169 من الدروس)، وبقيت خمسة بنود شك في REVIEW5_Q4_QUESTIONS.md (13402 و14360 و14373 ومجموعة 15494-15497 و14763). لم تلمس تصحيحات Codex الـ137 ولا صفوف BUILD-9 ولا بنود القرارات والصفوف السياقية وTangled. بلا بناء ولا تثبيت ولا نشر: التصحيح ينتظر البناء القادم.

## 2026-10-14 — BUILD-9

بناء BUILD-9 لحزمة النص وتثبيته: يضم تصحيحات REVIEW5-Q1 التسعة و13 تصحيحا جديدا (خمسة من قرارات DECIDE-19 وثمانية من مراجعة GPT للربع الثاني). لم يُنشر شيء بعد.

## 2026-10-13 — REVIEW5-Q1

قسمت الصفوف المترجمة (16415) إلى أربعة أرباع متتالية بحسب المعرف، وراجع Claude الربع الأول (4104 صفوف) صفا صفا مقابل النص الأصلي. طبقت تسعة تصحيحات محلية (عدد المخاطب، التذكير والتأنيث، كلمة ناقصة، توحيد سطرين مكررين)، وبقيت ثلاثة أسئلة للمشرف. لا بناء ولا إصدار جديد: التصحيحات تنتظر BUILD-9. كما عدلت سطر الأسئلة الشائعة عن الإزالة بحيث يشير إلى المثبّت أو حذف ملفي الحزمة يدويا.

## 2026-10-13 — PUBLIC-CLEANUP

ملفات bat في جذر المستودع العام (18 ملفا) لا تعمل إلا داخل المشروع الخاص، فأوقف make_public نسخها وحذفت من المستودع العام. دليل المختبر يشرح الإزالة عبر المثبّت أو بحذف ملفي pak يدويا. لم يتغير README، وبقي إصدار 0.9.0 بخمسة ملفات.

## 2026-10-13 — PUBLISH-090

نشر الإصدار 0.9.0 كإصدار تجريبي (pre-release) على GitHub بخمسة ملفات (مثبت Windows، حزمة Linux، حزمة النص BUILD-8، حزمة الصور، SHA256SUMS) وتطابقت الأحجام والبصمات. قبل المستخدم تعديل سطري README (49 و59) ودفع المستودع العام. أضيف إلى ملاحظات الإصدار أن صورتي SpecialShip_02 وHelpItem30402 (PS4) لم تشاهدا داخل اللعبة بعد وأن حزمة الصور اختيارية.

## 2026-10-13 — RELEASE-090

حزمة الصور IMAGES-MASS3: أعيد رسم صورتين أخريين (لوحة التحكم في نسخة PS4 من صورة الرقص، وكلمات لعبة السفينة)، فصار المجموع 211 من 234 صورة (90.2%)، وهذا كل الصور القابلة لإعادة الرسم؛ الصور الـ23 الباقية مذكورة مع سببها. ثبتت الحزمة عبر سكربت التبديل وطابقت بصمتها، وبقيت حزمة النص BUILD-8. أعيد بناء المثبت 0.9.0 لـWindows وLinux بالحزمة الجديدة ونجحت اختباراته الذاتية كلها. كتبت خطة الطريق إلى 1.0.0. توقف النشر قبل الرفع لأن README المولد يغير صياغة سطرين، فلم ينشر شيء.

## 2026-10-13 — INSTALL-8

تثبيت BUILD-8 (حزمة النص) وIMAGES-MASS2 (حزمة الصور) في مجلد ~mods عبر سكربتي التبديل، والتحقق من SHA256 للحزمتين. تحديث INSTALLED وSTATS وسجل التبديل، وإعادة كتابة قائمة الفحص في خمسة أسطر نعم/لا. لم ينشر شيء.

## 2026-10-13 — DECIDE-19

اختيارات مقترحة لبنود DECISIONS_NEEDED التسعة عشر مع الأدلة، وخمسة أسطر مقترحة للبناء القادم في ملف منفصل خارج التصحيحات. لم يعدل أي نص ترجمة ولا بناء ولا نشر.

## 2026-10-13 — OPUS-090

بناء BUILD-8 لحزمة النص: الاختلاف الوحيد عن BUILD-7 هو 136 سطرا صححتها المراجعة اللغوية. حزمة الصور IMAGES-MASS2: 16 صورة جديدة من واجهات الألعاب المصغرة وإعادة رسم «الهواء»، فصار المجموع 209 من 234 صورة في الخطة (89.3%). مثبت 0.9.0 يضم الحزمتين مع خانة اختيارية لحزمة الصور ونجحت فحوصه الذاتية الـ37. كل ذلك مبني فقط: لم يثبت في اللعبة ولم ينشر بعد.

## 2026-10-13 — README-POLISH

تحسين واجهة README واختصارها، إزالة الشكر وإخلاء المسؤولية، تنزيل مباشر للنظامين وخريطة Graphify مستقلة أسفل الصفحة.

## 2026-10-13 — INSTALLER-CROSSPLATFORM

مثبت 0.8.3 بواجهة Avalonia وصورة المستخدم لـWindows وLinux؛ حقوق الصورة في GitHub فقط؛ حزمة BUILD-7 لم تتغير. بنيت نسختا النظامين وعوينت الواجهة على Windows؛ تشغيل Linux لم يفحص على جهاز Linux.

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
