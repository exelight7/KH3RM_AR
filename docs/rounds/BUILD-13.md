round: BUILD-13 (prompt as given)

REPORT RULE: write the FULL report to state\LAST_REPORT.md (first line "round: BUILD-13"..."done + <path>".
ARABIC RULE: Arabic only via Write/Edit or read from project files; never inside shell commands, sed or heredocs. No U+FFFD.
ROLE: Claude Code, Sonnet 5.5, MEDIUM effort. Work only in C:\filessss\mewo\kh3fm-arabic\ and ~mods via the approved swap script only. Never run the game, never touch original game files, no AES key, no publish, no push, no installer rebuild, no reset/clean, no tag 1.0.0. Do not change build_build4.py logic. If usage nears the limit: finish the current step, commit, write the resume point to state\PROGRESS.md, stop. Never leave a half-built pak installed.
APPROVAL (user, in chat): run SWAP_TO_BUILD13.bat yourself, ONLY via: powershell.exe -NoProfile -Command "..." (never Git Bash).
START: pwd; git status (tracked clean); archive state\LAST_REPORT.md to state\reports_archive\LAST_REPORT_before_BUILD-13.md; save this prompt as docs\rounds\BUILD-13.md. Installed now: BUILD-12 (2cdb5b7b...95cd), images IMAGES-MASS5 (d5b39c12...ff21). The 22 REVIEW6 fixes are already in translation\ (do not re-apply).
TASKS:
1. Read review\gpt\R2\proposals.tsv (read only; never edit anything under review\gpt\). Make review\corrections\build13_round.tsv (id, old_AR, new_AR, reason) by script, ONLY these ids:
   a) direct: 01263, 01427, 03884, 02003, 02021, 02461, 02552, 02913, 02938, 03679, 04039, 12893, 13534, 14837, 15516.
   b) only if the new wording agrees with translation\glossary.tsv (Strike, Faith, Kupo coin, parley, Sonic entries): 13217, 13397, 16172, 16321, 13474, 14822, 14158, 14550. If the glossary disagrees or is ambiguous for a term, skip every id of that term and report it.
   Do NOT apply 15955, 15956, 15964, 16359, 16607, 15466, 16619 or any other GPT row.
   For every id: old_AR equals current AR exactly (else skip and report); validate.py check() logic on new_AR: 0 ERR, no new flag, tags/args/<br> identical, no U+061F, no U+FFFD.
2. refresh.bat (apply, 0 ERR). Confirm git diff of translation\ vs the previous commit is exactly the applied ids (0 unintended changes).
3. tools\build_build13.py as a thin copy of build_build12.py (PREV = BUILD-12). Same verification as BUILD-12 (list = hash-list = unpack SHA256, locres re-parse, round trip fail 0, validate 0 ERR, overflow vs the 15 known rows, new overflow none). Diff BUILD-12 vs BUILD-13 = the 22 REVIEW6 ids plus the applied build13 ids exactly; report ids and count. Pin hash via tools\make_swap_scripts.py, generate SWAP_TO_BUILD13.bat (pure ASCII, CRLF).
4. Confirm the game is not running (tasklist). Run the swap with the command form above. Verify installed SHA256 = pin; images pak unchanged (d5b39c12...ff21). Run python -I tools\build_build13.py --installed.
5. PROJECT_MAP 3,4,8, CHANGELOG, MANIFEST note (Round 2 merged), refresh.bat 0 ERR, secret_check PASS, private commit "BUILD-13". No publish. Report: BUILD-13 SHA256, applied ids, skipped ids with reasons, STATS, the open questions list (REVIEW6 doubts, GPT R2 questions 00953 and 01363, deferred 15466 and 16619).
Then stop.
