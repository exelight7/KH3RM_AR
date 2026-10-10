# Tools (official sources only)

| Tool | Version | Source URL | File | SHA256 |
|---|---|---|---|---|
| repak (CLI) | 0.2.3 (2026-01-02) | https://github.com/trumank/repak/releases/download/v0.2.3/repak_cli-x86_64-pc-windows-msvc.zip | `repak-0.2.3/repak_cli-x86_64-pc-windows-msvc.zip` | 6720d602144d75df477a99d5bedb6ea780997546afc335901d4937cafeaa73fa (matches GitHub release digest) |
| | | | `repak-0.2.3/repak.exe` | fcd538e5994b9bb833622d425ae346f4e0692f02d4b0025114a559f9b6286022 |
| Python | 3.12.10 + pycryptodome 3.23.0, fontTools 4.65.0 | already installed | — | — |

Own scripts (read-only on the game, written this round):
- `pak_index.py` — decrypts/parses pak v4 indexes → `extracted\pak_index.tsv` (counts cross-checked against `repak list`)
- `locres.py` — .locres v0/v1 reader/writer + TSV export; `roundtrip` mode = byte-identical check
- `gfx_fonts.py` — lists fonts and glyph code tables inside Scaleform GFx movies (DefineCompactedFont)
- `gfx_imports.py` — per-movie EditText/font usage summary
- `remind_map.py`, `text_counts.py`, `tag_inventory.py` — reports

Not used / forbidden: Steamless, AES Key Finder, any exe unpacking or patching. FModel/umodel/QuickBMS not needed (repak CLI worked).
AES key: see `KEY_SOURCE.txt` only.

- `apply_corrections.py` - applies review\corrections\*.tsv (id, old_AR, new_AR, reason) to translation\; refuses on mismatch; tests in `test_corrections.py`.
- `make_review.py` - writes review\md\ pages, review\INDEX.md, review\FLAGS.md (Markdown only).
- `gfx_edittext.py` - lists every DefineEditText of Scaleform movies: font class, size, letterSpacing, alignment, bounds.
- `build_arabictest2.py` - ARABIC-TEST-2 build: title screen locres + TresFont ($sougei, $KH2Menu) with join extension, paks F1/F2, verify.
- `preview_text.py` - offline PNG preview of shaped text with a (rebuilt) TresFont, Scaleform-style layout incl. letterSpacing.
- `update_map.py` - regenerates the (auto) sections of PROJECT_MAP.md; run by refresh.bat.
