# REVIEW5-Q1 (round prompt, saved verbatim in summary)

REPORT RULE (mandatory): write the FULL report to state\LAST_REPORT.md (overwrite; first line "round: REVIEW5-Q1"..."done + <path>".

ARABIC RULE: Arabic file content only via Write/Edit; never inside shell commands or heredocs. Existing Arabic comes from project files by id. Follow translation\glossary.tsv (locked entries win). Check no U+FFFD.

ROLE: Claude Code, Sonnet 5.5, HIGH effort. Work only in C:\filessss\mewo\kh3fm-arabic\ and public_repo\. No game, no ~mods, no builds, no installs, no AES key, no force-push, no reset/clean, no tag 1.0.0, no cloud_repo. Never publish English game text or review\ data. If usage nears the limit: finish the current page, commit, write the resume point to state\PROGRESS.md, stop.

START: pwd; git status (tracked clean, else stop); archive state\LAST_REPORT.md to state\reports_archive\LAST_REPORT_before_REVIEW5-Q1.md; save this prompt as docs\rounds\REVIEW5-Q1.md; read PROJECT_MAP 3,4,8, review\RULES.md, glossary.tsv, review\DECISIONS_ANSWERED.md, docs\rounds\CODEX-REVIEW4-HANDOFF.md.

TASK 0 (tiny): reword public FAQ line 6 (template used by make_public.py) so it no longer mentions REMOVE_AR.bat: say to remove via the installer or delete the two pak files from Content\Paks\~mods. Write/Edit only. README untouched. Publish with tools\publish.bat at the END of the round (public_check must PASS).

TASK 1: SPLIT. Take all 16,415 translated rows (status translated/reviewed; exclude the 807 skip rows and the 42 image strings) in ascending id order and cut them into 4 consecutive quarters of equal row count (differ by at most 1). Write review\split\Q1_ids.tsv ... Q4_ids.tsv (id only, one per line) and review\split\MANIFEST.md (boundaries first/last id, counts, owners: Q1 = Claude, Q2 = GPT, Q3 and Q4 = reserved, nobody touches them). Verify: no id in two files, union = all 16,415. Commit "REVIEW5 split".

TASK 2: REVIEW Q1 ONLY (you own Q1 only; never open a correction for an id outside Q1_ids.tsv). Work in pages of 300 following review\md or find_text order. Check each row against its EN: meaning, addressee gender, glossary and locked terms, repeated lines identical to the same EN elsewhere, imperative spelling, tags/args untouched, no U+061F, ASCII ?. Do NOT re-apply or revert any of the 137 Codex corrections or the 5 BUILD9_proposed rows. Do NOT decide DECISIONS_NEEDED items, the 64 context items or Tangled: copy doubtful ones to review\REVIEW5_Q1_QUESTIONS.md (id, EN, current AR, doubt in one line). Real fixes go to review\corrections\review5_q1_<page>.tsv (id, old_AR, new_AR, reason) with Arabic taken from existing rows or written with Write/Edit and validated; run tools\validate.py logic on every new_AR. Run apply_corrections after each page; refresh.bat 0 ERR. Commit per page. Keep a per-page line in review\REVIEW5_Q1_LOG.md (page, rows read, fixes, doubts).

TASK 3: REPORT counts: rows read, fixes applied, doubts, validator result, STATS. Do NOT build a pak or release: fixes wait for BUILD-9 (which will also take the 5 BUILD9_proposed rows and the accepted GPT Q2 fixes). PROJECT_MAP 3,4,8, CHANGELOG, refresh.bat 0 ERR, secret_check PASS, private commit "REVIEW5-Q1", then publish (FAQ only).

Then stop.
