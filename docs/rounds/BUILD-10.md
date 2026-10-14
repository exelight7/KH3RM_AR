round: BUILD-10 (prompt saved)

REPORT RULE: full report to state\LAST_REPORT.md (first line "round: BUILD-10"..."done + <path>".
ARABIC RULE: Arabic file content only via Write/Edit; none in shell commands.
ROLE: Sonnet 5.5, LOW effort, SMALL work. Only kh3fm-arabic and ~mods via the approved swap script. No game run, no original files, no AES key, no publish/push/installer rebuild/reset/clean/tag. build_build4.py logic unchanged.
APPROVAL: may run SWAP_TO_BUILD10.bat (game not running).

TASKS
1. review\corrections\build10_round.tsv (id, old_AR, new_AR, reason) from review\gpt\Q3\proposals.tsv, ONLY:
   a) direct: 08565 08607 08713 08734 09171 09233 09816 09966 10042 10082 10197 10294
   b) glossary-gated: 10502 10521 10517 11557 11568 12476 12489 (Constellation/Crystal = glossary word, Special+ as row 10650; skip + report on failure or disagreement with 10663/10650/10656; skip 10521 if 10502 skipped).
   Not 10882, 10883, 11500, any other GPT row, nor 17169 (already applied).
   old_AR == current AR else skip; validate.check on new_AR: 0 ERR, no new flags, tags/args identical, no U+061F, no U+FFFD.
2. tools\refresh.bat (0 ERR); confirm Codex 137, Q1 9, BUILD-9 13 fixes untouched.
3. tools\build_build10.py thin wrapper like build_build9.py; build; verify as BUILD-9; diff BUILD-9 vs BUILD-10 (applied ids + 17169); pin hash with make_swap_scripts.py -> SWAP_TO_BUILD10.bat (ASCII, CRLF).
4. Game not running; cmd /c ".\SWAP_TO_BUILD10.bat <NUL"..."BUILD-10". No publish. Report SHA256, rows changed, skipped ids, STATS.
