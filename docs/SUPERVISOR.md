# Supervisor instructions (full copy)

Source: the supervisor's message for round ARABIC-TEST-2, 2026-10-08, copied verbatim below. No separate supervisor file existed in the project before this round; when a new round message changes the standing rules (ROLE / OUTPUT RULES / START), replace this copy and note the round here.

---

ROLE: sole executor (Claude Code, Opus 5.5, high effort). Write only in C:\filessss\mewo\kh3fm-arabic\. Never modify original game files; never run the game; never delete extracted\ or out\builds\. Do not upload anything; git local only. Font = Segoe UI Regular (C:\Windows\Fonts\segoeui.ttf), never Noto, never Plex.
OUTPUT RULES: work silently. Details in state\LAST_REPORT.md (overwrite; first line "round: ARABIC-TEST-2"..."done + file path". Stop and ask only if blocked 3 times or evidence conflicts.
START: pwd; read state\PROGRESS.md, technical\SHAPER_SPEC.md, RECON_KH3.md sections 9-11, tools\build_arabictest1.py.
SCREENSHOT RESULT (ARABIC-TEST-1, variant A, title menu): PASS = letters joined correctly, right-to-left order correct, no boxes. FAIL = small visible gaps between joined letters (joins broken), Arabic looks smaller than the English caps. Hypothesis (unverified): the field's letterSpacing (2) inserts space after every glyph.
APPROVALS: INSTALL out\builds\ARABIC-TEST-2\pakchunk99-arabictest2F1_P.pak into Content\Paks\~mods\ approved. Before that move pakchunk99-arabictest1_P.pak from ~mods to out\builds\old\ (record SHA256 before/after). Only one pak of ours in ~mods at any time.
TASKS:
1. Log the screenshot: SCREENSHOT_LOG.tsv entry ARABIC-TEST-1 / id 13770 / file 20261008_ARABIC-TEST-1_01.png / result as above. Mark id 13770 verified in stats.
2. Measure: for every text field on the title screen (Title movie + its help/footer fields), record font class, size, letterSpacing, alignment. Confirm or reject the letterSpacing hypothesis with numbers.
3. Join fix in the font only (do not edit the Title movie): for Arabic glyphs that connect to the next letter (initial/medial forms, lam-alef where relevant), extend the joining stroke on the connecting side by the measured gap amount so joins stay closed with letterSpacing 2 and simply overlap when letterSpacing is 0. Same stroke thickness and baseline as the original join. Apply to the $sougei additions. If another font class is used on this screen by the strings below, add Arabic glyphs there too and report which.
4. Translate the whole title screen (test values; glossary decides later): NEW GAME = لعبة جديدة, LOAD = تحميل, CONFIG = الخيارات, SPECIAL = خاص, Downloadable Content = المحتوى الإضافي, GAME SETTINGS = إعدادات اللعبة, Confirm = تأكيد, Cancel = إلغاء, "..." = ابدأ اللعبة من البداية. Also translate the help line shown for each other menu item (simple clear Arabic) and list them in the report for my review. Keep every tag/icon atom exactly. Write them into the translation\ TSVs with status "translated"..."*", "_"..."ARABIC-TEST-2: join fix, title screen, project map".
Then stop.


## Latest authorization — 2026-10-13

The user's newer instruction adopts Graphify project-wide and requests complete translation review in four batches, detailed reports on the local device and GitHub after every batch, and a separate interactive-map section at the bottom of README. This explicitly supersedes the historical no-HTML/no-upload limits for the public graph and sanitized review reports only. Game installation and releases remain outside this request. Full EN/AR comparisons remain private.
