# Tools (official sources only)

| Tool | Version | Source URL | File | SHA256 |
|---|---|---|---|---|
| repak (CLI) | 0.2.3 (2026-01-02) | https://github.com/trumank/repak/releases/download/v0.2.3/repak_cli-x86_64-pc-windows-msvc.zip | `repak-0.2.3/repak_cli-x86_64-pc-windows-msvc.zip` | 6720d602144d75df477a99d5bedb6ea780997546afc335901d4937cafeaa73fa (matches GitHub release digest) |
| | | | `repak-0.2.3/repak.exe` | fcd538e5994b9bb833622d425ae346f4e0692f02d4b0025114a559f9b6286022 |
| Python | 3.12.10 + pycryptodome 3.23.0, fontTools 4.65.0 | already installed | — | — |
| etcpak (BC1/BC3/BC4/BC5/BC7 encoder) | 0.9.15 | pip registry https://pypi.org/project/etcpak/0.9.15/ (installed; wheel re-downloaded with `pip download` to hash it) | `etcpak-0.9.15-cp37-abi3-win_amd64.whl` | 669d902eeb774bc6d4df226183c09c3d03c9fc0f47b4c0c20030fc2b39eec2f2 |
| texture2ddecoder (BCn decoder) | 1.0.6 | pip registry https://pypi.org/project/texture2ddecoder/1.0.6/ | `texture2ddecoder-1.0.6-cp311-abi3-win_amd64.whl` | 1bad8209d9dfbfc7daf13ea2e545236ea2bbc1e423b2992b6e7563909975a47b |
| Pillow | 12.3.0 (no raqm: text drawn with the BASIC layout) | pip registry https://pypi.org/project/pillow/12.3.0/ | `pillow-12.3.0-cp312-cp312-win_amd64.whl` | a2b55dd6b2a4c4b7d87ffa56bdb33fdc5fdb9a462173861a7bc097f17d91cb09 |
| numpy | 2.5.3 | pip registry https://pypi.org/project/numpy/2.5.3/ | `numpy-2.5.3-cp312-cp312-win_amd64.whl` | 0a59a421a32580a009e8a1751345bf829631b990dc1794b80514ab722b435def |

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
- `texture_codec.py` - UE4.17 Texture2D uasset/uexp/ubulk reader/writer + BCn/BGRA decode (texture2ddecoder) and block-patch encode (etcpak); `roundtrip` = byte-identical check (FINAL-1).
- `images_inventory.py` - read-only inventory of textures with English text → technical\IMAGES_INVENTORY.tsv, PNGs and contact sheets in out\builds\IMAGES\ref\ (FINAL-1).
- `texture_text.py` - repaints a text rectangle of a texture with pre-shaped Arabic drawn from Segoe UI outlines (technical\images_rects.tsv) (FINAL-1).
