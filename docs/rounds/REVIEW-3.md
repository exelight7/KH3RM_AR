# REVIEW-3 (prompt summary; Arabic given as \uXXXX escapes in the original, decoded in Python)
ROLE sole executor; write only in kh3fm-arabic (not public_repo, no publishing); no game folder/~mods; never run the game; never delete extracted\ or out\builds\; no HTML.
Tasks via review\corrections\review3.tsv + tools\apply_corrections.py (substring replace, exactly once per row else skip and report):
1. Isla de Muerta: KH2 form (إيسلا دي مويرتا) replaces the retired KH3 form everywhere; glossary.tsv approved, note "supervisor REVIEW-3".
2. Row 05962: لا بأس به -> على ما يرام (full phrase: إن الأمر لا بأس به -> إن الأمر على ما يرام).
3. Row 01392: أليست هذه -> أليس هذا.
4. Rows 03913, 06084: وكأن ذلك صحيح -> كأن ذلك سيحدث.
5. Row 05050: أيها النكرة التافه -> أيها التافه الحقير.
6. Rows 01302/01304: change to masculine only if bx561b clearly shows a male addressee; report evidence.
7. Unchanged: 02025, 03112, 08730, 05955, 05386, 05388, 05994, 09121; mark UNSURE_REVIEW2.md resolved.
8. refresh.bat (0 ERR), secret_check, PROJECT_MAP 3 4 8 (BUILD-6 / v0.8.1 needed), CHANGELOG, private commit "...". Then stop.
Output: state\LAST_REPORT.md (first line "round: REVIEW-3"), 3 lines per task in state\PROGRESS.md, terminal one line.
