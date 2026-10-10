ROLE: sole executor (Claude Code, Sonnet 5.5, medium effort). Work in C:\filessss\mewo\kh3fm-arabic\ (private project) and public_repo\ . Never modify original game files; never run the game; never delete extracted\ or out\builds\. Never force-push. No passwords or tokens.
START: pwd; git status (clean, else stop); save this prompt as docs\rounds\SYNC-BUILD7.md; read PROJECT_MAP.md, docs\CLOUD_WORKFLOW.md, docs\rounds\FINAL-1.md.
APPROVALS: standing: pull from the private repo exelight7/KH3RM_AR_work main; push to https://github.com/exelight7/KH3RM_AR main; create release 0.8.2 (pre-release, tag without "v"; asset name pattern KH3RM_AR_Setup_v0.8.2.exe). Install BUILD-7 via SWAP_TO_BUILD7.bat (same safety rules). gh is at tools\gh-2.102.0\x\bin\gh.exe (if not logged in, stop and tell the user the login command).
TASKS:
1. Check with gh that all cloud pull requests (1 to 6) are merged in KH3RM_AR_work main; if one is open, stop and tell the user. Run tools\sync_cloud.bat; report corrections applied/refused per file (refused = old_AR mismatch; list ids); validate 0 ERR.
2. Align the glossary with the corrected rows (supervisor decisions): Diving Strike = the ability-row form, Powerwild and Frost Serpent = the bestiary-row forms, Monsters Inc = the short form used in the menu rows (no "limited"..."supervisor SYNC-BUILD7". Read the exact Arabic from the translation rows, never type it.
3. Build BUILD-7 with the BUILD-6 pipeline unchanged (tools\build_build7.py wrapper); verify list/hash-list/unpack SHA256; round trip fail = 0; overflow check on changed rows (the shortened Risk label must fit); report rows that differ from BUILD-6 (count by locres, 20 examples); install via SWAP_TO_BUILD7.bat; BUILD7_CHECKLIST.md (Arabic, max 4 places).
4. Installer 0.8.2 with the BUILD-7 pak embedded, selftest all green, screenshots.
5. Release 0.8.2 (pre-release) with the same 5 assets as 0.8.1; notes Arabic then English with "what changed" (cloud second-pass review of all dialogue, menus, items, tutorials and journal: total corrections, numbers from state\STATS.md); verify with gh release view.
6. tools\publish.bat (README numbers); run public_check; the English text must never reach the public repo. Report the public commit id.
7. refresh.bat, secret_check, PROJECT_MAP 3 4 6 7 8, CHANGELOG, private commit, then run sync_cloud so the private repo is current.
Then stop.
