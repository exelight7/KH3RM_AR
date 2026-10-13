## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"..."<A>" "<B>"..."<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).


## Project review and publishing context (2026-10-13)

- The user adopted Graphify for the whole project. The local `graphify-out` graph may contain private source context; never export it wholesale. The public snapshot is `docs/graph/graph.json`; use `graphify query "translation pipeline" --graph docs/graph/graph.json` in a public clone.
- The user authorized a complete four-batch translation review, local reports, and sanitized GitHub reports after each batch. Resume from `review/codex_full_review/manifest.json`, per-part ledgers and `state/LAST_REPORT.md`; public reports are `docs/rounds/CODEX-REVIEW4-N.md`.
- All source comparisons remain private. Public `translation/ar` exports and reports contain Arabic only, without English game lines or private review ledgers.
- Use correction TSVs and the existing refresh/publish workflow. Preserve prior glossary decisions; unresolved scene-dependent wording stays unchanged and is reported.
- Review reports stay Markdown. User-approved HTML/SVG are for the interactive Graphify map and its separate footer section in README. No game installation or new release is authorized by this review request.
