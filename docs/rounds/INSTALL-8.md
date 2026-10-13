# INSTALL-8 (prompt)

REPORT RULE: write the FULL report to state\LAST_REPORT.md (first line "round: INSTALL-8"..."done + <path>".
ARABIC RULE: Arabic file content only via Write/Edit; check no U+FFFD.
ROLE: Sonnet 5.5, LOW effort, SMALL work. Only C:\filessss\mewo\kh3fm-arabic\ and, via approved swap scripts, game ~mods. No original game files, no running the game, no AES key, no publish/push, no cleaning untracked files.
APPROVAL: run SWAP_TO_BUILD8.bat and SWAP_TO_IMAGES_MASS2.bat now.

TASKS:
1. Check the game exe is not running.
2. Run both swap scripts via cmd /c from the project root; only our two pak names change in ~mods (list before/after); verify SHA256: text 45f043de4a4832b1ace0c34f43f2d09e96123d9aaff72768e04524d9ee70e381, images bc546502a712675520b70d738b65be5835372fa2ec61fec04a04296e49a0dd29.
3. Run python -I tools\build_build8.py --installed and python -I tools\texture_text.py --installed; confirm SWAP_LOG.tsv has the new rows.
4. Rewrite technical\IMAGES_MASS2_CHECKLIST.md: max 5 yes/no lines in simple Arabic naming the screen, plus one line: play normally, send a screenshot only if something looks wrong. Put the full text in the report.
5. tools\refresh.bat (0 ERR), secret_check PASS, PROJECT_MAP sections 3, 4, 8, CHANGELOG, private commit "INSTALL-8". No publish.
