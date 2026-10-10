# BUILD-5 (round prompt, saved verbatim in substance)

ROLE: sole executor (Claude Code, Sonnet 5.5, medium effort). Write only in C:\filessss\mewo\kh3fm-arabic\. Never modify original game files; never run the game; never delete extracted\ or out\builds\. Do not upload anything; git local only. No HTML anywhere. Font = Segoe UI Regular (F1 scale, locked).
OUTPUT RULES: work silently. Details in state\LAST_REPORT.md (overwrite; first line "round: BUILD-5"..."done + file path". Stop and ask only if blocked 3 times or evidence conflicts.
START: pwd; git status (must be clean); save this prompt as docs\rounds\BUILD-5.md; read PROJECT_MAP.md, state\PROGRESS.md, tools\build_build4.py, the BUILD-4 and REVIEW-2 reports.
ARABIC STRINGS RULE: never rely on Arabic typed in this prompt; all Arabic comes from project files.
APPROVALS: INSTALL out\builds\BUILD-5\pakchunk99-arabic_P.pak via the swap-script method (add SWAP_TO_BUILD5.bat; delete our pak first; verify SHA256; log to SWAP_LOG.tsv).
TASKS:
1. Rebuild with exactly the BUILD-4 pipeline (same movie patches for CampMenu, SaveLoad, HudGumi, same TresFont, same line-breaking rules, no <p align>) from the current translation\ TSVs (REVIEW-1 and REVIEW-2 corrections, row 15964 shortened). Do not change any build logic.
2. Verify: list / hash-list / unpack SHA256 for every file; re-parse: changed entries per locres, keys and hashes unchanged; round trip exact / same-visual / fail (fail must be 0); validator 0 ERR. Report which rows differ from the installed BUILD-4 pak (count by locres, 15 examples id | BUILD-4 | BUILD-5). Report installed % from state\INSTALLED.tsv and re-run the row-overflow check for the changed rows only.
3. Install as approved. Update technical\BUILD4_CHECKLIST.md into technical\BUILD5_CHECKLIST.md (Arabic, max 8 short places, same places as BUILD-4, plus: level-up line after a level up, a corrected dialogue line example from REVIEW-2 such as ids 01091 and 05448, and the party card level label).
4. refresh.bat (0 ERR), secret_check, PROJECT_MAP sections 3 4 6 7 8, CHANGELOG, commit "...".
Then stop.
