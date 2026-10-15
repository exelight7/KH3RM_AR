# HUD-SOFTEN (round prompt, saved verbatim in substance)

REPORT RULE: write the FULL report to state\LAST_REPORT.md (first line "round: HUD-SOFTEN"..."done + <path>".
ARABIC RULE: Arabic only via Write/Edit or read from project files; never in shell commands. No U+FFFD.
ROLE: Claude Code, Sonnet 5.5, MEDIUM effort, SMALL work. Work only in C:\filessss\mewo\kh3fm-arabic\ and ~mods via approved swap script only. Never run the game, never touch original game files, no AES key, no publish, no push, no installer rebuild, no downloads, no reset/clean. Do not change movies, the text pak (BUILD-17) or fonts. Own renderer only.
OWNER FEEDBACK on IMAGES-MASS10 (installed): the HUD words are good and solid but look PIXELATED (jagged). Goal: keep most of the crispness but smooth the stair-steps.
APPROVAL: run the swap script ONLY via: powershell.exe -NoProfile -Command "..." (escape as `$env:Path from PowerShell).
START: pwd; git status (tracked clean); archive state\LAST_REPORT.md to state\reports_archive\LAST_REPORT_before_HUD-SOFTEN.md; save this prompt as docs\rounds\HUD-SOFTEN.md. Installed now: BUILD-17 (58bad877...858c), IMAGES-MASS10 (2dfb6baf...ba34).
TASKS:
1. Keep each word's MASS10 recipe (font, stroke, outline, pad, snap) and vary ONLY the edge: hard:3, hard:4, hard:6, hard:8, hard:12, plus supersampled antialias (render at 4x, box-downscale, then mild hard:2) and a solid outline softened by a 1-step alpha ramp. Use the existing simulator to measure on the magnified in-game look: edge % vs English, crisp %, AND a new jaggedness metric (e.g. count of 1-px stair-step corners along the word contour or contour curvature noise after magnification). Choose per word the candidate that keeps edge >= 110% of English and crisp >= 75% of English with the LOWEST jaggedness; joins intact, readable, margins as before.
2. Build IMAGES-MASS11 with full verification as MASS10 (checks.tsv 0 FAIL, list/hash-list/unpack, uexp re-parse, only HudStatusTxt/HudStatusCA differ from MASS10). Sheets: English | MASS9 | MASS10 | MASS11 (raw 1x and simulated in-game 2x, bar and dark) in out\builds\IMAGES-MASS11\ref\. Pin hash, SWAP_TO_IMAGES_MASS11.bat (pure ASCII, CRLF), confirm game not running (tasklist), install, verify SHA256 = pin, text pak unchanged, run texture_text.py --installed. Rollbacks: SWAP_TO_IMAGES_MASS10.bat (solid) or SWAP_TO_IMAGES_MASS9.bat (soft).
3. PROJECT_MAP 3,4,8, CHANGELOG, refresh.bat 0 ERR, secret_check PASS, private commit "HUD-SOFTEN". No publish. Report the metric table and the chosen edge per word.
Then stop.
