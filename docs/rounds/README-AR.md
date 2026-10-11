# Round README-AR (prompt, saved verbatim in substance)

REPORT RULE: write the full report to state\LAST_REPORT.md (first line `round: README-AR`) before finishing; the chat final message is exactly one line: `done + <repo url>`.

ARABIC RULE: Arabic file content may be written directly in UTF-8 with Write/Edit. Never put Arabic inside shell commands, heredocs or echo. Read each file back: no U+FFFD, no reversed or garbled words. Terms follow translation\glossary.tsv.

ROLE: work only in the project root and public_repo\. No game folder, no ~mods, no builds, no installer rebuild, no pak changes, no downloads. Never print the AES key. Never force-push. No tag 1.0.0. Do not touch the private cloud repo. Do not edit translation TSVs, glossary.tsv or review\corrections.

APPROVALS: tools\publish.bat push to exelight7/KH3RM_AR main; edit notes of release 0.8.3 (and 0.8.2, 0.8.1, 0.8.0 only if their notes contain English-only text) with gh release edit, keeping the pre-release flag.

TASKS:
1. Public README rewritten as Arabic only (no HTML tags, no English section, no English game text): pitch, screenshot, what is translated, download, 4-step install, manual install, removal, status table from state\STATS.md (honest: 0.6 % verified in game), roadmap, known limits, how to report, rights note, credits, build from source in 3 lines.
2. TESTER_GUIDE, FAQ, bug_report.yml and other AR+EN public docs converted to Arabic only; list any leftover English prose.
3. tools\make_public.py and templates generate the Arabic-only README and docs; run public_check.py on a temp output first.
4. Release 0.8.3 notes in Arabic (same translation as 0.8.2, BUILD-7, docs and tools only, unofficial, no images pack, SHA256 of the pak); keep pre-release; fix the SHA256SUMS.txt/ui_*.png mention if confusing; no re-upload.
5. tools\refresh.bat (0 ERR), secret_check PASS, tools\publish.bat (public_check must PASS). Verify public main has the commit, list changed files, check raw README starts with the Arabic title.
6. PROJECT_MAP sections 3, 4, 7 (decision: public README and docs are Arabic only), 8, CHANGELOG, private commit `README-AR`.
