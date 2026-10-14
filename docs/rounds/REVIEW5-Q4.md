# REVIEW5-Q4 (round prompt, saved verbatim)

REPORT RULE (mandatory): write the FULL report to state\LAST_REPORT.md (overwrite; first line "round: REVIEW5-Q4"..."done + <path>".

ARABIC RULE: Arabic file content only via Write/Edit; never inside shell commands or heredocs. Existing Arabic comes from project files by id. Follow translation\glossary.tsv (locked entries win). Check no U+FFFD.

ROLE: Claude Code, Sonnet 5.5, HIGH effort. Work only in C:\filessss\mewo\kh3fm-arabic\. No game, no ~mods, no builds, no installs, no publish, no push, no AES key, no reset/clean, no tag 1.0.0, no cloud_repo. If usage nears the limit: finish the current page, commit, write the resume point to state\PROGRESS.md, stop.

START: pwd; git status (tracked clean, else stop); archive state\LAST_REPORT.md to state\reports_archive\LAST_REPORT_before_REVIEW5-Q4.md; save this prompt as docs\rounds\REVIEW5-Q4.md; read PROJECT_MAP 3,4,8, review\RULES.md, glossary.tsv, review\DECISIONS_ANSWERED.md, review\split\MANIFEST.md, review\REVIEW5_Q1_LOG.md.

TASKS:
1. Update review\split\MANIFEST.md: Q3 = GPT, Q4 = Claude (this round). You own Q4 only (ids in review\split\Q4_ids.tsv); never open a correction for an id outside it.
2. Review Q4 in pages of 300 with the same checks as REVIEW5-Q1: meaning vs EN, addressee gender/number, glossary and locked terms, repeated EN lines identical, imperative spelling, tags/args untouched, no U+061F, ASCII ?. Do NOT touch the 137 Codex corrections, the 13 BUILD-9 rows, or decide DECISIONS_NEEDED, the 64 context items, Tangled or puns: put doubts in review\REVIEW5_Q4_QUESTIONS.md (id, EN, current AR, doubt). Real fixes to review\corrections\review5_q4_<page>.tsv (id, old_AR, new_AR, reason), validated with validate.py check() logic; apply_corrections and refresh.bat 0 ERR after each page; commit per page; per-page line in review\REVIEW5_Q4_LOG.md.
3. Report counts (rows read, fixes, doubts), STATS. No build, no install. PROJECT_MAP 3,4,8, CHANGELOG, refresh.bat 0 ERR, secret_check PASS, private commit "REVIEW5-Q4".

Then stop.
