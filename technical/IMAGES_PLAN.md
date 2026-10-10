# IMAGES_PLAN — English text inside textures (FINAL-1 part 2)

Read-only inventory from the decrypted pak index (`extracted\pak_index.tsv`; newest copy = a `_P` patch pak over the base pak), decoded with `tools\texture_codec.py` and read by eye from the contact sheets (`out\builds\IMAGES\ref\sheet_*.png`, private, not published). Full list: `technical\IMAGES_INVENTORY.tsv` (private: it holds the English words); words and plan per asset: `technical\images_words.tsv`; generator: `tools\images_inventory.py`.

## 1. What exists

| group | textures | where in the game | format | plan |
|---|---|---|---|---|
| title: `UI/Icon/Mapname/Localization/en/mapName_*` | 26 | area name banner when entering an area | BC7 720×400, 1 mip, inline | repaint 25; keep 1 (Monsters, Inc. = world logo) |
| scaleform_loc: `UI/Scaleform/*/en/*_loc` | 89 | command menu headers (14 world styles), situation/attraction/formchange logos (45), minigame HUD words (14), shotlock MAX, chain, Data Greeting, Premium menu, credits, key labels | BC7 (11 with mips), inline | repaint 36 + 46 styled logos/titles later; keep 6; 1 to read full-size |
| tutorial: `UI/Icon/HelpItem/Localization/en[/ps4|windows|xboxone]/HelpItem*` | 150 (39 shared + 37 × 3 platform copies) | Game Help pictures (in-game screenshots with English HUD/menu labels) | BC7 / DXT5 768×432, inline | repaint labels; one rect list per image id, reused by the platform copies |
| menus: `UI/IconText/Localization/en/IconText*_km` | 2 | keyboard/mouse key prompts | B8G8R8A8 512×1024 | keep (key names) |
| logo: `UI/Icon/LsiLogo` (23) + `Cutscene/end_title/*/TitleLogo` (2) | 25 | Classic Kingdom game titles, ending title card | BC7 / DXT5 | keep English (brand wordmarks) |
| other: `LSI/Games/*/Localization/en` | 9 | Classic Kingdom LCD games (score words, FUEL, FARES) | B8G8R8A8 with mips | repaint (plain lettering) |
| scaleform_shared (non-culture textures with baked words) | 23 | autosave notice, battle HUD gauges (FOCUS/MAX/AIR/MP/CHARGE, HP/ARMOR), keyhole, Luxord gauge, battle report, camera SHARE, item filter ALL, MAX!, title logos, credits | BC7 / B8G8R8A8 | repaint 14 (most hold de/fr/it/es words beside the English cell; the game picks the cell per language) + 1 styled logo later; keep 8 (brands, credits, DLC, names) |
| **total** | **324** | | | **repaint 234 + 47 styled logos later, keep 42, read full-size first 1** — by priority: 1 = 48, 2 = 160, 3 = 75, 4 = 41 (keep) |

Formats found (all UI/LSI/end_title textures, 983 parsed): PF_BC7 837, PF_B8G8R8A8 98, PF_DXT5 48; with mips 58; all inline in the `.uexp`. Streamed `.ubulk` mips exist elsewhere in the game (effect textures) and are supported by the codec (tested on a BC4 texture), but none of the text textures uses them.

Other sources checked:
- **Movie bitmaps:** 561 Scaleform movies hold 2,107 `DefineExternalImage2` (tag 1009) and 344 `DefineSubImage` (1008) references: every bitmap is an external UE texture (the lists above). One `DefineBitsJPEG2` tag (in `MenuGigasGameTitle01`) is empty. No text is baked inside a movie.
- **TexturePump lists:** 287 `TresTexturePump` assets (`Cutscene/Localization/ja/TexturePump` + `Camera/TexturePump`): streaming lists of cutscene shot textures (names only, no pixels); the `ja` ones belong to the Japanese culture and are not loaded by the English game. Nothing to translate.
- Not covered: signage decals in 3D maps (shared, no culture path), the copyright video and world-title videos (TEXT_COVERAGE §5).

## 2. Keep English (not repainted)

- **Brand wordmarks:** KINGDOM HEARTS III / Re Mind title logos and the ending title cards, the 23 Classic Kingdom cartoon titles, CLASSIC KINGDOM, VERUM REX, Monsters, Inc. (world logo).
- Keyboard key names and language names, credits/staff names, single letters (E, A), DLC (LATIN policy), Le Grand Bistrot.

## 3. Tooling (done in FINAL-1)

- `tools\texture_codec.py`: reads/writes the cooked UE4.17 Texture2D (`.uasset` untouched, `.uexp` mip payloads, `.ubulk` streamed mips at BulkDataStartOffset + offset). Decode: texture2ddecoder 1.0.6; encode: etcpak 0.9.15 (BC1/BC3/BC4/BC5/BC7), raw BGRA/G8 directly. Edits re-encode only the 4×4 blocks whose pixels changed, so sizes never change and untouched blocks keep their original bits.
- **Round trip (proof):** 18 textures (BC7 with and without mips, DXT5, B8G8R8A8 with and without mips, BC4 with `.ubulk`): decode → unedited re-encode → rebuild = **byte-identical** uasset/uexp/ubulk, re-parse identical (`out\builds\IMAGES\roundtrip.tsv`). A full re-encode of every block (lossy formats) keeps the structure and size; pixel difference max 47–207, mean 0.04–2.03 per channel (BC7/DXT5), 0 for BGRA — which is why the block-patch method is used.
- `tools\texture_text.py`: per rectangle in `technical\images_rects.tsv` — fill the old text (clear / per-column gradient / quadratic surface fit / flat), sample fill, outline and glow colours from the original ink, draw the pre-shaped Arabic (`tools\shaper.py`, visual order, presentation forms) with Segoe UI outlines (BASIC layout, so no second bidi pass), centred or aligned like the English, small sizes hinted at 1×, large sizes 4× supersampled.

## 4. Pilot (FINAL-1, installed, not released)

`out\builds\IMAGES-PILOT\pakchunk98-arabic-images_P.pak` (3 textures, 16 text boxes), next to the BUILD-6 text pak:

| kind | texture | English → Arabic (source row) |
|---|---|---|
| menu / HUD | `HudCmdTextTT01_loc` (command menu header, Twilight Town style) | COMMANDS ×3 → 00231, SHORTCUTS → 00221, CONTROLS → 16121, SHOTLOCK → 10260 |
| world title | `mapName_tt01` (area banner, plain serif lettering, not a wordmark) | The Neighborhood → 13728 (glossary «الحي السكني»); underline kept |
| tutorial | `HelpItem01600` (Game Help › Synthesis) | 9 labels: 14397, 14416, 14400, 14401, 14319, 14402, 14404, 14406, 14396 (vertical WORKSHOP) |

In-game checks: `technical\IMAGES_PILOT_CHECKLIST.md`.

## 5. IMAGES-MASS (2026-10-10, installed, not released)

`out\builds\IMAGES-MASS\pakchunk98-arabic-images_P.pak` replaces the pilot: 194 textures, 1,240 boxes; 193 of the 234 planned = 82.5 % (+ SlideShowTx). Rules: 1 px stroke in the text colour from 24 px; screenshot labels healed stroke by stroke (`heal`), plates inpainted, cut-out plates refilled and the Arabic cut out (`knockout`); only the English cell in multi-language textures. Still English with reasons: `technical\IMAGES_STILL_ENGLISH.tsv`. Checks: `out\builds\IMAGES-MASS\checks.tsv` (all PASS). In-game checks: `technical\IMAGES_MASS_CHECKLIST.md`.
Next: user screenshots (verdict decides 0.9.0); 16 minigame HUD textures; 47 styled logos.

## 6. Next steps (FINAL-1, kept for history)

1. **User screenshots** of the 3 pilot places (checklist). Decide: font size/weight for banners (Segoe UI Regular looks lighter than the English display faces), glow strength, whether area banners may use a bolder look.
2. **IMAGES-MASS:** rect lists for priority 1 (area banners, command headers, battle HUD cells, autosave), then priority 2 (tutorial pictures; one list per image id), then 3 (minigames, styled logos); styled logos need a separate decision (plain Arabic vs. effect layers).
3. Release **0.9.0** with the image pak (optional second pak or merged), then user screenshots → **1.0.0**.
