# RECON_KH3 — Kingdom Hearts III + Re Mind (Steam), read-only recon

round: ARABIC-TEST-2 · date: 2026-10-08 · status: **RECON complete (§1–8); PIPE-1 (§9); LOAD-TEST (§10) PASS; ARABIC-TEST-1 (§11) PASS/FAIL; ARABIC-TEST-2 (§12) F1 installed, checklist for the user**

Evidence levels: **VERIFIED** = read from the files on this PC (decrypted copies in `extracted\`) · **DOC** = public community docs (link) · **UNVERIFIED** = needs a screenshot / in-game test.

**Font decision (final, user 2026-10-08):** project font = **Segoe UI Regular** (`C:\Windows\Fonts\segoeui.ttf`, weight 400, not bold), same as KH2 "font G"..."Segoe UI" Version 5.71, SHA256 `8134dbcd09e7b123c9a7f229d49cffbcb01352cc72ea5e1076b65d0dca9f73cd` — VERIFIED
- Arabic coverage: U+0600–06FF 256 cps, presentation forms A U+FB50–FDFF 178, B U+FE70–FEFF 141; has GSUB/GPOS; TrueType outlines (`glyf`) — VERIFIED (fontTools 4.65.0)

## 1. Install

| Item | Value | Evidence |
|---|---|---|
| Path | `C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III` | VERIFIED |
| Steam app | 2552450 "...", buildid **14790811**, depots 2552452 + 2552453, language english | VERIFIED (appmanifest_2552450.acf) |
| Size on disk | 67 GiB (71,769,963,004 B per manifest): Paks 34 GB, CriMovie 32 GB, _DLC_ 1.3 GB, Movies 8.9 MB | VERIFIED |
| Exe | `KINGDOM HEARTS III\Binaries\Win64\KINGDOM HEARTS III.exe`, 150,713,896 B, FileVersion 1.0.0.0, has a `.bind` section (SteamStub DRM) — not touched | VERIFIED |
| Paks | 140 in `KINGDOM HEARTS III\Content\Paks` under the install path, i.e. `C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks` (70 base + 70 `_0_P`) + 2 voice paks `Content\_DLC_\VOICE\{en,ja}\Paks\voice_7_P.pak` | VERIFIED — `extracted\install_filelist.tsv`, `extracted\pak_footers.tsv` |
| Pak index | **555,921 entries in 142 paks** (137 non-empty; the five 61-B `_0_P` paks have no entries) | VERIFIED — `extracted\pak_index.tsv` (pak, path, size, compressed size, compression, encrypted); counts match `repak list` |
| Re Mind installed? | Yes, part of the combined app. Map of Re Mind content per pak: see §1a | VERIFIED |
| `~mods` folder | Does not exist | VERIFIED |
| Movies | CriWare `.usm` (180 files). Subtitles inside USM: not opened this round → UNVERIFIED | VERIFIED (list) |

### 1a. Re Mind (DLC) mapping — VERIFIED (`extracted\remind_map.tsv`, marker = path contains `DLC`/`Rebellis`/`remind`)
- **Text:** all inside `Paks/pakchunk0-WindowsNoEditor.pak` → 11 dedicated files per culture: `kh3_event_{bt,dp,dw,ew,he,kg,rg,ss}_dlc.locres`, `kh3_fieldvoice_{bt,kg,rg}_dlc.locres`, plus Re Mind namespaces inside shared files (`kh3_gamehelp.remind`, `kh3_extraload.dlc`, `kh3_menu.slideshow`, `kh3_menu.hologram`, keys with `dlc`). Total Re Mind text = 1,163 entries / 6,985 words (§3c).
- **Data:** mostly-DLC paks: `pakchunk1_s48` (100 %: `Maps/rg_DLC`, `ss_DLC`), `1_s11` (88 %), `1_s46` (71 %: `Effects/dlc02`), `1_s51` (54 %), `1_s20` (44 %: `Maps/bt_DLC`), `1_s19` (39 %), `1_s54` (35 %), `1_s49` (29 %: `Maps/ss_DLC`); DLC voice in `_DLC_/VOICE/{en,ja}/Paks/voice_7_P.pak` (35,894 entries each). Re Mind game flags: `game_data/flags/Rebellis/*` in pakchunk0. Many `_0_P` paks patch `Levels/*_DLC` and `Maps/*_DLC`.
- Title screen Re Mind art: `UI/Scaleform/11_title/TitleLogoReMind`, `TitleBg_ReMind*` (pakchunk0_s6).

## 2. Engine, pak format, encryption

| Item | Value | Evidence |
|---|---|---|
| Unreal Engine | **4.17** custom SE build | VERIFIED + DOC ([dennisstanistan.com](https://dennisstanistan.com/blog/848/using-unreal-engine-4-to-mod-kingdom-hearts-3/)) |
| Pak version | **v4** on all 142 paks, Zlib. Mount points (`repak info`, PIPE-1): `../../../` ×34 (incl. **pakchunk0**, which holds all `.locres` and `TresFont`, paths `KINGDOM HEARTS III/Content/…` and `Engine/…`), `../../../KINGDOM HEARTS III/Content/` ×96, 7 deeper sub-folders, `/` ×5 (the empty 61-B `_0_P` paks). Table: `out\builds\PIPE-1\game_pak_mounts.tsv` | VERIFIED |
| Compression | Zlib on 507,965 entries, stored on 47,956 | VERIFIED |
| Tooling | repak 0.2.3 CLI (official GitHub release, hashes in `tools\TOOLS.md`) reads and unpacks everything; no GUI tool needed. Steamless / AES Key Finder / exe patching: **not used** | VERIFIED |

## 3. Text — VERIFIED

### 3a. Where the text is
- **Game text = `.locres` only**, target `Game`, path `KINGDOM HEARTS III/Content/Localization/Game/<culture>/kh3_*.locres`, all inside `Paks/pakchunk0-WindowsNoEditor.pak`. **No `.locres` in any `_0_P` patch pak** → one mod pak overrides text cleanly.
- **English is many files, not one: 67 `.locres`** (2,291,841 B total), locres **format v1** (compact, dedup string table, UTF-16 for non-ASCII). Namespaces are `<file>.<group>` (e.g. `kh3_menu.title`), keys are ids (`menu_0001`, cutscene line ids like `bt9050210sr0`).
- File groups (en): `kh3_event_*` 31 files (cutscene subtitles, per world, 8 `_dlc`); `kh3_fieldvoice_*` 26 (field/NPC voiced lines and chat bubbles); `kh3_menu`, `kh3_camp`, `kh3_system`, `kh3_settings`, `kh3_map`, `kh3_level`, `kh3_epic` (UI); `kh3_gamehelp`, `kh3_tutorial` (help/tutorials); `kh3_item`, `kh3_char_name`; `kh3_mobile` (Gummiphone: Secret Reports, glossary, records = journal), `kh3_extraload` (loading-screen posts), `kh3_gumiship`, `kh3_minigame`.
- Also exported: Engine target (`Engine/Content/Localization/Engine/{de,en,es,fr,ja,ko,zh}`, 634 KB en) and 12 Online/HTTP plugin targets (tiny, platform messages). Not game-visible text in normal play.
- **StringTables: none** (no StringTable asset; the string "StringTable"..."memory" scenes); `Cutscene/Localization/ja/*` (≈ 1,000 files) are Japanese-only cutscene variants (lip-sync/edits). CriWare USM subtitle tracks: UNVERIFIED.
- Export: all 627 `.locres` + 13 `.locmeta` copied to `extracted\locres\` with original mount paths (sizes match the index, 640/640). English as TSV: `extracted\text_en.tsv`.

### 3b. Cultures
| Culture | Game locres files | Entries | Bytes |
|---|---|---|---|
| ja (native, `DefaultCulture=ja`) | 67 | 17,059 | 1,482,155 |
| en | 67 | 17,222 | 2,291,841 |
| fr / it / de / es | 67 each | 17,222 each | 2.45 / 2.41 / 2.58 / 2.36 MB |
| ko | 67 | 17,179 | 1,527,485 |
| zh-Hant | 67 | 17,179 | 1,320,511 |

- `DefaultGame.ini`: `CulturesToStage = ja en fr it de es ko zh-Hant` (exactly 8). The in-game Text-language menu (`kh3_settings.language choice_0100…0170`) lists the same 8. **No unused culture slot exists** (no `ar`, no empty folder). Adding a 9th culture would need cooked config + the hardcoded language menu → not a pak-only change. **Decision basis: Arabic replaces `en`.** VERIFIED
- Voice cultures: en, ja (`Sound/VOICE/Localization/{en,ja}`).

### 3c. Counts (English) — full table `technical\TEXT_COUNTS.tsv` (per category and per file)
| Category | Entries | Unique texts | Words |
|---|---|---|---|
| Menus / UI | 3,849 | 3,211 | 17,744 |
| Subtitles / cutscenes (`kh3_event_*`, non-DLC) | 6,336 | 5,605 | 38,846 |
| Dialogue (field voice / NPC chat, non-DLC) | 2,298 | 2,173 | 16,172 |
| Tutorials (gamehelp + tutorial + game-over hints) | 614 | 576 | 14,297 |
| Items / abilities / commands | 2,334 | 2,032 | 10,485 |
| Journal (Gummiphone `kh3_mobile` + loading posts) | 628 | 555 | 21,009 |
| Re Mind (all `_dlc` files + DLC namespaces/keys) | 1,163 | 1,074 | 6,985 |
| **Total** | **17,222** | **14,854** | **125,538** (781,876 chars) |
Words exclude `<tags>` and `{args}`. Empty entries: 0.

## 4. Fonts — VERIFIED

**The game UI and subtitles are Scaleform GFx (Flash), not UMG/Slate.** UE composite fonts / UFontFace do **not** drive game text.

| Asset | Where | What |
|---|---|---|
| `UI/Scaleform/91_font/TresFont` (SwfMovie; .uexp 4,352,744 B) | pakchunk0 | GFx v21 font library built from `TresGame/Flash/91_font/TresFont.swf` (2018-11-15). Used for ja/en/fr/it/de/es |
| `UI/Scaleform/91_font/ko/TresFont` (930,739 B), `…/zh-Hant/TresFont` (7,943,198 B) | pakchunk0_s7 | Culture variants; exe strings `TresFont`, `ko`, `zh`, `/%s/TresFont`, `/TresFont` sit together → ko/zh load their folder, others the root file (inferred from strings, UNVERIFIED in-game) |
| `Font/TresTestDebugFontLarge` | pakchunk1_s26 | debug font only |
| Engine `EngineFonts/Roboto*` (6 .ufont), `Slate/Fonts/*.ttf` incl. **`NotoNaskhArabicUI-Regular.ttf`** (146,548 B), DroidSansFallback, NanumGothic | pakchunk0 | stock UE Slate/engine fonts (debug, error dialogs); not used by Scaleform UI |

Fonts inside base `TresFont` (DefineCompactedFont, nominal size 256; alias = Scaleform export name used by every movie):

| id | Alias | Font name | Glyphs | Used by (sample) | Arabic |
|---|---|---|---|---|---|
| 3 | `$sougei` | ＤＦＰ綜藝体W5G_EURO_021 (DynaFont Sougei, EURO set) | 7,904 | all menus, camp menu, game help, messages, loading (14–60 pt, outlined, HTML text fields) | **0** |
| 1 | `$jimakuNE` | KH_TBシネマ丸ゴシック Std M2 (TB Cinema Maru Gothic; "NE" = non-Japanese subtitles) | 270 (Latin-1 + a few symbols) | Subtitle 38 pt, CutsceneText 38 pt, Dialog 21 pt | **0** |
| 2 | `$JimakuJP` | KH_映画字幕書体_TTF_ver.1.01 (movie-subtitle face) | 7,932 | Japanese subtitles 40 pt | **0** |
| 4 | `$KH2Menu` | KH2 ALL MENU ver1.22 | 219 | button/menu symbols (GameHelp 20 pt) | **0** |
ko variant: FOTK-YDHope L, FOTK-YDGothic 130, KH2 ALL MENU; zh-Hant: 文鼎隸書_D, 華康新綜藝體W5(P), KH2 ALL MENU — all with **0 Arabic glyphs**. (Tool: `tools\gfx_fonts.py`, `tools\gfx_imports.py`; code tables parsed, ascending check passed.)

**Arabic glyphs exist only in the engine's Slate fallback `NotoNaskhArabicUI-Regular.ttf`, which Scaleform text never uses → no Arabic in any game font.**

How Segoe UI Regular can be added (through a pak only, no game-file edits):
1. **Primary route — rebuild `TresFont`:** add Segoe UI Regular glyphs for U+0600–06FF + U+FB50–FDFF + U+FE70–FEFF into the `$sougei` (id 3) and `$jimakuNE` (id 1) **DefineCompactedFont** tags, keep ids/aliases/DoABC/SymbolClass unchanged, re-emit GFx, wrap back into the SwfMovie `.uexp`, pack at `KINGDOM HEARTS III/Content/UI/Scaleform/91_font/TresFont.{uasset,uexp}`. **PIPE-1 decoded the compacted format completely and `tools\tresfont.py` rebuilds all 3 TresFont files byte-identically, its edge encoder reproduces SE's compactor on 4.3 M edges** → no DefineFont3 detour needed; exact structure in §9 T4.
2. Scaleform GFx (no HarfBuzz) does **no Arabic shaping or bidi** → strings must be **pre-shaped to presentation forms and visually reversed** (KH2 approach), and multi-line `<br>` text must be split/reversed per line. UNVERIFIED in-game; ARABIC-TEST decides.
3. Not applicable here: UE composite-font sub-font range (only Slate/UMG would honour it). The exe contains `fontlib`/`FontMap` strings (Scaleform font-map support), but no config uses them → a system-font fallback route is UNVERIFIED and not planned.
4. Licensing note: Segoe UI is a Windows system font (personal-use project, same as KH2); not bundled until the user decides distribution.

## 5. Text features — VERIFIED
Full inventory and 20 real examples: `technical\TAGS.md`. Summary: `<br>` 6,252 · `<i(on)>/<i(off)>` ~1,670 · `<icon(X)>` 1,410 (130 icon names) · `<color(strong|heading|hashtag|red|…)>…<color>` 1,092 pairs · `<pb>`/`<pb(sec)>` 237 · `<b(on/off)>` 70 · `<nbsp>` 62 · `<conv(…)>` 36 · `{0}`–`{4}` 304 · ICU `|plural(one=…,other=…)` 37. No raw `\n`. Special characters: — ★☆ ￠(hashtag) ①–④ χ ′ ″.

## 6. Images with English text — VERIFIED
- **`Localization/en/TexturePump` does not exist in any pak.** The exe string is a path template; the only TexturePump-under-Localization folder is `Cutscene/Localization/ja/TexturePump` (270 `TresTexturePump` assets = texture-streaming lists for Japanese cutscenes, **no images**). Other TexturePump assets (`Camera/TexturePump/*`, 16) are also streaming lists.
- English-text images are culture-pathed `Texture2D` under `…/Localization/en/` (each culture has a twin): **212 textures** (+2 DataTables).

| Type | Count | Assets |
|---|---|---|
| Logo | 25 | `UI/Icon/LsiLogo/Localization/en/LsiLogo01–23` (Classic Kingdom game logos); `Cutscene/end_title/gm/…/gm155_TitleLogo`, `end_title/kg_DLC/…/kg951_TitleLogo` (ending title logo; kg951 = Re Mind) |
| Title (location banners) | 26 | `UI/Icon/Mapname/Localization/en/mapName_<world><nn>` |
| Menus | 2 | `UI/IconText/Localization/en/IconText_km`, `IconTextSub_km` (2048² text/icon atlases, keyboard+mouse labels) |
| Tutorial | 150 | `UI/Icon/HelpItem/Localization/en/` 39 shared + 37 each for `ps4`, `windows`, `xboxone` |
| Other (minigames) | 9 | `LSI/Games/*/Texture/Localization/en/` (golf score words ×4, BarnyardSports, Baseball "game set"..."chance", TrafficTroubles ×2) |
- Not counted (UNVERIFIED, no Localization path): bitmaps baked inside Scaleform movies (e.g. `11_title/TitleLogo`, `TitleLogoReMind`, `TitleMenu01`, `14_theater/ConcertCredit_NEA`) and map textures with signage (`Maps/mi/... Font*` decals). They are shared by all cultures.

## 7. Mod loading (DOC — nothing installed)
- Folder: `KINGDOM HEARTS III\Content\Paks\~mods\` (create it), pak name ends in `_P.pak`. Sources: [ScreenRant guide](https://screenrant.com/install-mods-kingdom-hearts-3-pc/), [KH3 Randomizer guide](https://kh3-randomizer-2ivd7.ondigitalocean.app/guide), [Dmgvol TranslationMod](https://github.com/Dmgvol/UE_Modding/blob/main/IntermediateModding/TranslationMod.md).
- Minimal test pak: `.locres` at `KINGDOM HEARTS III/Content/Localization/Game/en/kh3_*.locres`, mount point `../../../` (same as pakchunk0), pak v4, Zlib, unencrypted index (mods need no key — DOC, UNVERIFIED on this build). Built in PIPE-1: `out\builds\PIPE-1\pakchunk99-artest_P.pak` (§9).
- **CONFLICT / RISK:** after a recent Steam patch mods reportedly crash unless all `_0_P` files are moved ([Steam thread](https://steamcommunity.com/app/2552450/discussions/0/4408543518582770744/), [Nexus 938](https://www.nexusmods.com/kingdomhearts3/mods/938?tab=posts), [Nexus 2201](https://www.nexusmods.com/kingdomhearts3/mods/2201)). Not done (game files are read-only for us). Good news from this round: `_0_P` paks contain **no `.locres`**; `TresFont` itself is not patched either (only `92_message/Message`, `16_game_help/GameHelp` etc. are).

## 8. Pipeline
1. Extract (done): repak + community key → `extracted\` (read-only copies).
2. `.locres` ⇄ TSV with `tools\locres.py tsv-export / tsv-import` — **DONE (PIPE-1)**: `translation\en_source.tsv`, TSV → locres 627/627 byte-identical.
3. Translate in TSV (glossary from KH2), tag validator per `TAGS.md` §3 (on the logical text).
4. Arabic shaping: `tools\shaper.py` per `technical\SHAPER_SPEC.md` (designed, not built) — unless ARABIC-TEST proves Scaleform shapes it.
5. Rebuild `en/*.locres` → pak (repak v4, Zlib, mount `../../../`) → `out\`, name `pakchunk99-ar_P.pak`, installed to `~mods` only after approval. Pipeline proven with `pakchunk99-artest_P.pak` (PIPE-1).
6. Font: rebuilt `TresFont` with Segoe UI Regular glyphs (§4, §9 T4: format decoded, writer ready) in the same pak.
7. Images: 212 culture textures (§6), later round.

## Risks
1. `_0_P` mod-crash reports on the current build (§7) — LOAD-TEST first.
2. Scaleform has no Arabic shaping/bidi → pre-shaped reversed text; line-wrapping of reversed text needs our own line breaking (fixed `<br>` positions).
3. Overwriting `en` affects every English string; the `en` voice track still plays (independent).
4. `TresFont` rebuild: container + glyph format solved in PIPE-1 (byte-identical round-trip); remaining risk = in-game look (scale/baseline of Segoe UI vs DynaFont metrics) → ARABIC-TEST.
5. Italic `<i(on)>` (1,670 uses) has no Segoe UI Regular italic → Scaleform faux-italic or none; cosmetic.
6. CriWare USM subtitles UNVERIFIED.
7. Steam updates can change paks; re-run `tools\pak_index.py` and diff after each update.

## 9. PIPE-1 results (2026-10-08, no game interaction) — VERIFIED
Outputs in `out\builds\PIPE-1\`; SHA256 tables there and in `state\LAST_REPORT.md`.

**T1 TSV pipeline — PASS.** `tools\locres.py tsv-export <root> <tsv> [filter]` / `tsv-import <tsv> <src_root> <out_root> [filter]`.
- TSV columns: `namespace, key, source_hash, text, category, file` (escapes `\\ \n \r \t`; `file` = path under `extracted\locres\`; category = §3c categories, `engine` for non-Game targets).
- `translation\en_source.tsv`: 67 en files, 17,222 rows. Full set `tsv\all_627.tsv`: 157,456 rows from 549 files (78 files have no entries).
- Import uses the original `.locres` as template: entry order, namespace order, **1,175 empty namespaces**, per-string UTF-16 flag (all KH3 Game strings are stored UTF-16, even ASCII) come from it; TSV supplies the text; `source_hash` must equal the template's (checked, never rewritten). Changed text keeps UTF-16. String table is re-deduplicated in first-use order (identical to SE's).
- TSV → locres for all **627/627 files byte-identical** (+ the 67 en from `en_source.tsv`) → `rebuild_sha256.tsv`.

**T2 edited-string test — PASS.** Variant `artest\en_artest.tsv` → `artest\pakroot\`; re-parse of all 67 en files: exactly 3 entries differ, keys/hashes/order/flags unchanged.

| Marker | File | Namespace | Key | EN text | Where to see it |
|---|---|---|---|---|---|
| `[AR-TEST-1]` | kh3_menu.locres | kh3_menu.title | menu_0002 | NEW GAME | title screen menu |
| `[AR-TEST-2]` | kh3_tutorial.locres | kh3_tutorial.tut | title_0010 | TUTORIALS | header of the Tutorials screen |
| `[AR-TEST-3]` | kh3_event_bt.locres | kh3_event_bt.bt001a | op0010010sr0_1 | `<i(on)>They can take your world.<i(off)>` | first subtitle of the opening (`op001`) after NEW GAME (inferred from key, UNVERIFIED) |

**T3 test pak — PASS (not installed).** `pakchunk99-artest_P.pak` 881,923 B, SHA256 `0b5dd910030329191705dbd207384af44bb14160b43184b95233e99d9caf0868`; repak 0.2.3 `pack --version V4 --compression Zlib --mount-point ../../../`; 67 entries `KINGDOM HEARTS III/Content/Localization/Game/en/*.locres` (same mount and v4/Zlib as pakchunk0; index unencrypted). `repak list` 67, `hash-list` and `unpack` SHA256 = inputs 67/67 (`artest\pak_verify_sha256.tsv`).

**T4 TresFont — round-trip PASS; format documented.** `tools\tresfont.py roundtrip` parses uasset → uexp → GFX → every DefineCompactedFont down to glyph edges and re-encodes: base, ko, zh-Hant `.uasset` + `.uexp` all byte-identical (6/6).
- **Wrapper:** `.uasset` export `SerialSize` (= uexp − 4) and summary `BulkDataStartOffset` (= uasset + uexp − 4) must be patched; `.uexp` `RawData` ArrayProperty<Byte> tag size (= n + 4) and count n = GFX length; GFX header u32 file length; tag 1005 long-form length.
- **DefineCompactedFont (1005):** u16 id; then name UTF-8 NUL, u16 flags (0x6000), u16 nominal 256, s16 ascent/descent/leading, u32 numGlyphs, u32 glyphBytes, shapes, info table `{u16 code, s16 advance, u32 pos}` × n (**codes ascending — binary-searched, new codes must be inserted in order**; pos relative to byte after the id), UInt30 kerning count (0 in all fonts) + `{u16, u16, s16}` pairs.
- **Glyph shape:** SInt15 bbox[4] (y down), UInt15 contours; contour = SInt15 moveX, SInt15 moveY, UInt30 (edges ≪ 1 | shared-ref flag, never set), edges. Edge = 4-bit type + signed relative fields: H12/H20, V12/V20, L6/L10/L14/L18 (dx,dy), C5–C15 quadratic (control, anchor); 2–8 bytes. Units: 256 per em; contours closed implicitly. Validated: 4.3 M edges, all points inside their bbox, 100 % match with our smallest-encoding rule.
- **Adding Segoe UI Regular:** TrueType quadratic outlines map 1:1 to C/L edges; scale 256/2048 = 1/8, flip y; advance = round(advanceWidth/8). Append new shapes after existing glyph data, insert info rows by code; no DoABC/SymbolClass change. Measured by `tresfont.py estimate` (nothing written): U+0600–06FF 256 glyphs 35.1 KB, U+FB50–FDFF 178 / 31.5 KB, U+FE70–FEFF 141 / 19.9 KB, digits 10 / 1.1 KB → **≈ 88 KB per font, ≈ 175 KB for `$sougei` + `$jimakuNE`** (only U+FE70–FEFC + 060C/061B/061F + optional پ چ ڤ گ are needed by the shaper: ≈ 150 glyphs ≈ 22 KB per font). TresFont ≈ 4.35 → ≤ 4.53 MB: fits a `~mods` pak (no size limit; pakchunk0 is 455 MB). Calibration knob: Segoe UI's ascent 2210/desc 514 (= 276/64 at 256) is larger than `$jimakuNE` 204/38 → glyph scale/baseline offset is a parameter decided at ARABIC-TEST.
- Root `TresFont` serves en (and ja/fr/it/de/es); ko/zh-Hant have their own files and are untouched.

**T5 shaper design — `technical\SHAPER_SPEC.md`** (letter forms + lam-alef, UAX #9 RTL per line, atoms for `{n}`/icons/plural, style tags re-emitted, own line breaking with TresFont advances, 34 unit tests). Not built.

## 10. LOAD-TEST checklist (for the user — first time the game is touched)
Goal: does the game load an unencrypted `_P` pak from `~mods` on build 14790811, and does our rebuilt locres show? Nothing in the game is changed except one new folder with one file.
1. Close KINGDOM HEARTS III completely (also check the tray / Task Manager).
2. Open File Explorer and paste in the address bar:
   `C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks`
   You should see `pakchunk0-WindowsNoEditor.pak` etc.
3. Right-click → New → Folder → name it exactly `~mods` (tilde, lower-case). Allow the admin prompt if Windows asks.
4. Copy `C:\filessss\mewo\kh3fm-arabic\out\builds\PIPE-1\pakchunk99-artest_P.pak` into that `~mods` folder. Right-click → Properties: size must be **881,923 bytes**.
5. Start the game from Steam. Text language must be English (it is, per Steam manifest). Make sure Subtitles are On in Config if you changed them before.
6. Screenshots (Steam F12, or Win+PrtScn → `Pictures\Screenshots`):
   - **S1 title screen menu:** expected `[AR-TEST-1]` where NEW GAME was; CONTINUE/LOAD etc. still English.
   - **S2 Tutorials:** open TUTORIALS from the title menu (if there is no such entry, skip and say so): expected header `[AR-TEST-2]`.
   - **S3 opening subtitle:** select `[AR-TEST-1]` (New Game), pick any difficulty, watch the opening: expected the first subtitle line `[AR-TEST-3]` instead of "..." (no italics). Do not save; you can quit after it appears (or after ~3 minutes if it never appears — say so).
   - **S4** if anything goes wrong: the error dialog / the last screen before a crash, and the time it happened (logos, title, loading).
7. Answer: game started? (yes/no) · S1/S2/S3 shown as expected? · any crash?
8. Remove: quit the game, delete `pakchunk99-artest_P.pak` from `~mods`, then delete the empty `~mods` folder. Start the game once more → NEW GAME should be English again (optional S5). No Steam "verify files" needed (no game file was changed).
If the game crashes with the pak present but not without it: that is the known `_0_P` conflict (§7) — do **not** move `_0_P` files; report it and we decide next round.

## Next (after LOAD-TEST)
- ARABIC-TEST build: TresFont with Segoe UI Arabic glyphs + 3–5 strings in pre-shaped visual order next to logical order (tests SHAPER_SPEC §0/§7 open points: shaping/bidi in engine, word-wrap direction, alignment, plural keywords).
- Build `tools\shaper.py` + its unit tests from SHAPER_SPEC §9.

## 11. ARABIC-TEST-1 (2026-10-08) — built + variant A installed
LOAD-TEST result (user): **PASS**. An unencrypted v4 `_P` pak in `Content\Paks\~mods\` loads on build 14790811, and `[AR-TEST-1]` replaced NEW GAME. No `_0_P` move was needed.

**Single variable:** only `kh3_menu.title/menu_0002` (NEW GAME) plus TresFont `$sougei` (id 3) glyphs change. Title-menu text fields (`11_title/Title`, patched copy in `pakchunk0_s5_0_P`) use font class `$sougei` 23–30 pt, `letterSpacing` 0 or 2. Their only own DefineCompactedFont is a 1-glyph stub, so the glyphs come from TresFont.
- Font: 189 Segoe UI Regular glyphs added to `$sougei`, 7,904 → 8,093: U+060C/061B/061F, 0621–063A, 0641–064A, 0660–0669, FE70–FEFC (FE75 does not exist). Scale 256/2048, baseline shift −5 so the baseline matches the `$sougei` Latin glyphs, advance = Segoe advance / 8. Existing glyphs and all other fonts and tags are unchanged (verified by re-parse). TresFont.uexp 4,352,744 → 4,378,959 B.
- Shaper: `tools\shaper.py` (minimal subset of SHAPER_SPEC: forms + lam-alef, RTL per line, LTR Latin/digit runs, atoms, mirroring; self-tests for a plain word, lam-alef, digits and mixed English).
- Text `لعبة جديدة` in 3 paks, each holding `kh3_menu.locres` + `TresFont.uasset/.uexp` (`out\builds\ARABIC-TEST-1\`):

| Pak | Variant | NEW GAME stored as | If Scaleform has no shaping/bidi, you see |
|---|---|---|---|
| `pakchunk99-arabictest1_P.pak` (**installed**) | A: pre-shaped, visual order | `FE93 FEAA FEF3 FEAA FE9F 0020 FE94 FE92 FECC FEDF` | correct `لعبة جديدة`: joined, لعبة on the right |
| `pakchunk99-arabictest1B_P.pak` | B: logical, unshaped | `0644 0639 0628 0629 0020 062C 062F 064A 062F 0629` | separate letters, left-to-right: `ل ع ب ة  ج د ي د ة` (if it looks correct, the engine shapes by itself) |
| `pakchunk99-arabictest1C_P.pak` | C: shaped, logical order (not reversed) | `FEDF FECC FE92 FE94 0020 FE9F FEAA FEF3 FEAA FE93` | joined pieces in mirrored order: جديدة on the right, letters backwards (if C looks correct, the engine does bidi but not shaping) |

### ARABIC-TEST-1 screenshot checklist (for the user)
Now in `…\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods\`: only `pakchunk99-arabictest1_P.pak` (3,673,493 B). The empty `mods` folder next to it (no tilde, not ours) was left as it was.
1. Start the game from Steam and wait for the title menu. Do not load or start anything.
2. **A1:** full screen of the title menu with the cursor on the **second item** (where NEW GAME was). Steam F12 or Win+PrtScn.
3. **A2:** move the cursor to another item (e.g. CONTINUE/LOAD) and take a full screenshot again (highlight colour and size change).
4. **A3:** close-up. Win+Shift+S, crop around the Arabic item, then paste into Paint and save.
5. Check and write down (yes/no) for A:
   - a. Is any Arabic visible at all, or is the item empty, made of boxes (□), or `?`?
   - b. Are the letters **joined**: لـعـبـة with no breaks between ل ع ب ة, and جـديـدة with breaks only after د (that is normal)?
   - c. **Direction:** is `لعبة` on the right and `جديدة` on the left?
   - d. Spacing: thin gaps inside joined letters (the movie uses `letterSpacing="2"` on some fields, so a gap may come from the field, not the font), and the space between the two words?
   - e. Size and baseline next to the English items: too big or small, too high or low, dots under ب/ج cut off at the bottom?
   - f. Is the item aligned like the English items (left edge), or shifted?
   - g. Do CONTINUE / LOAD / CONFIG etc. still look normal (font change did not break English)?
6. **Switch to B:** quit the game fully. In `~mods`, delete `pakchunk99-arabictest1_P.pak` (the original stays in `C:\filessss\mewo\kh3fm-arabic\out\builds\ARABIC-TEST-1\`). Copy `out\builds\ARABIC-TEST-1\pakchunk99-arabictest1B_P.pak` into `~mods` (3,673,492 B). Start the game, take **B1** (cursor on the item) and **B3** (close-up), then answer a–c.
7. **Switch to C:** same as step 6 with `pakchunk99-arabictest1C_P.pak` (3,673,493 B): take **C1** and **C3**, then answer a–c. **Keep exactly one pak in `~mods` at a time.**
8. **Remove:** quit the game, delete the pak from `~mods`, then delete the empty `~mods` folder. Start the game once more: NEW GAME should be English again (optional screenshot). You don't need to verify game files in Steam.
9. Send A1–A3, B1, B3, C1, C3 + the yes/no answers.

## 12. ARABIC-TEST-2 (2026-10-08) — join fix, title screen in Arabic, F1 installed
ARABIC-TEST-1 result (user screenshot `20261008_ARABIC-TEST-1_01.png`, variant A): **PASS** joined letters, right-to-left order, no boxes → Scaleform does no shaping/bidi and our pre-shaping works. **FAIL** small gaps inside joined words; Arabic smaller than the English caps.

### 12a. Title-screen text fields — VERIFIED (read from the live movies)
Tool `tools\gfx_edittext.py`; full table (all fields of the 3 movies) `out\builds\ARABIC-TEST-2\ref\edittext_fields.tsv`. Movies used: `11_title/Title` from `pakchunk0_s5_0_P` (the patched copy the game loads), `16_game_help/GameHelp` from `pakchunk0_s7_0_P`, `85_settingmenu/SettingMenu` from `pakchunk1_s58_0_P`. letterSpacing and alignment come from each field's initial HTML (`<font size=".." letterSpacing=".." kerning="1">`); **no ActionScript in these movies sets letterSpacing** (every `letterSpacing` string sits inside an EditText tag).

| movie / field | font class | size pt | letterSpacing | align | holds (inferred from size/initial text) |
|---|---|---|---|---|---|
| Title 61 | `$sougei` | 30 | **2.00** | left | **menu items** (initial text `CONTINUE`) |
| Title 148, 151 | `$sougei` | 26 | 0 | right | help/detail lines |
| Title 79 | `$sougei` | 26 | 0 | center | wide one-line text |
| Title 18, 35, 37, 39, 43 | `$sougei` | 23 | 0 | left | dialog/window bodies (multiline) |
| Title 27, 245 | `$sougei` | 23 | 0 | center | difficulty names, window text |
| Title 232, 235 | `$sougei` | 20 | 0 | right | small labels (version etc.) |
| Title 273 | `$sougei` | 22 | 0 | center | small centred label |
| Title 71 | local 1-glyph stub | 60 | 0 | right | (not text) |
| GameHelp 10, 15 | `$sougei` | 23 | 0 | right / left | button-guide text |
| GameHelp 13, 18 | **`$KH2Menu`** | 20 | 0 | right / left | button-guide symbols |
| GameHelp 4, 8, 35, 38 | `$sougei` | 26 / 40 / 26 / 23 | 0 | — | help window body/title/page |
| SettingMenu 218 | **`$KH2Menu`** | 30 | 0 | left | **GAME SETTINGS header** (initial text `GAME SETTINGxx`) |
| SettingMenu (other 41) | `$sougei` | 20–42 | 0 | mixed | settings rows, buttons, dialogs |

**Hypothesis confirmed:** only the menu-item field has letterSpacing ≠ 0. Flash letterSpacing is in px of the field's 30 pt em: 2 / 30 em = **17.07 units** of the 256-unit TresFont em (= 136.5 Segoe UI units). Segoe UI's join tip reaches only 70 Segoe units (8.75 TresFont units) past the glyph origin and tapers to a point, so each join opened by ≈ 8–17 units ≈ 1–2 px at 30 pt — the gaps in the screenshot. Help lines (letterSpacing 0) were not affected.

### 12b. Fix (font only, movies untouched)
- All 46 Arabic initial/medial presentation forms in Segoe UI end in the same left join tip (stroke y −14…153 Segoe units, tip at x −70). Before the tip a straight piece of stroke is inserted, **GAP = ceil(17.07) = 18 TresFont units** long, same thickness and baseline (exact horizontal lines at the original stroke edges). With letterSpacing 2 the join closes (0.9 unit overlap); with letterSpacing 0 it just overlaps the neighbour's stroke. Lam-alef ligatures never join to the next letter → unchanged. Offline check (`tools\preview_text.py`, PNGs in `out\builds\ARABIC-TEST-2\preview\`): at the same ratio rendered large, TEST-1 had 17 pinched stroke columns in `لعبة`, F1 only the 2 word-end columns.
- Arabic glyphs are now in **`$sougei` (id 3) and `$KH2Menu` (id 4)** (`$KH2Menu` draws the GAME SETTINGS header and the GameHelp button symbols). 189 glyphs each: U+060C/061B/061F, 0621–063A, 0641–064A, 0660–0669, FE70–FEFC. `$KH2Menu` is caps-only with baseline 0 and cap height 204 (vs `$sougei` −5 / 174), so its Arabic is scaled ×204/174 to keep the same Arabic-to-caps ratio.
- Two paks, identical text, only the Arabic glyph scale differs (baseline kept): **F1** = ARABIC-TEST-1 scale (k = 1/8), **F2** = ×1.15.

| pak | bytes | SHA256 | status |
|---|---|---|---|
| `out\builds\ARABIC-TEST-2\pakchunk99-arabictest2F1_P.pak` | 3,694,281 | `302d95d10a972622a2c9d805ff6bbeb5e4cdf47eb2f64e814a240b5accf1f2d0` | **installed** in `~mods` |
| `out\builds\ARABIC-TEST-2\pakchunk99-arabictest2F2_P.pak` | 3,694,678 | `5e60bd3a94a573b8af2db8182baaeea4480bf5244f8113b1eebd77cbdb43cb99` | not installed |

Each pak: `kh3_menu.locres` (30 entries changed), `kh3_settings.locres` (4 changed), `TresFont.uasset/.uexp`. ARABIC-TEST-1 pak moved to `out\builds\old\` (SHA256 `c776c2f9…515f` before and after).

### 12c. ARABIC-TEST-2 screenshot checklist (for the user)
Now in `…\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods\`: only `pakchunk99-arabictest2F1_P.pak` (3,694,281 B).
What should be Arabic now: all title menu items except the Re Mind ones (they stay English with their icon), all their help lines, and the GAME SETTINGS / Confirm / Cancel strings. Everything else is still English.

**F1**
1. Start the game from Steam and wait for the title menu. Do not load or start anything.
2. **F1-1:** full screenshot with the cursor on `لعبة جديدة` (NEW GAME). Steam F12 or Win+PrtScn.
3. Check and write yes/no:
   - a. **Joins:** inside `لعبة جديدة`, `الخيارات`, `المحتوى الإضافي`, `أرشيف الذكريات` — is the line between joined letters closed (no light gaps)? Breaks are normal only after ا د ذ ر ز و ة ى.
   - b. **Size vs English:** compare the tall Arabic letters (ا ل) with the caps of an English item that is still English (a Re Mind item, or the version text). Arabic too small / OK / too big?
   - c. **Direction:** each item reads right-to-left (`لعبة` on the right of `جديدة`).
   - d. **Help line:** the description line shows `ابدأ اللعبة من البداية.` with the full stop at its **left** end; letters joined; no dark blobs where letters overlap.
   - e. Alignment: Arabic items start at the same left edge as English items did (expected: flush left).
4. **F1-2:** move the cursor down item by item (متابعة, تحميل, الخيارات, …). For 3 items take a screenshot each: does the help line change and stay Arabic? Note any item or help line still in English.
5. **F1-3 top-right buttons:** screenshot (or crop) the button guide in the top-right corner. Expected: each icon stays exactly as before, with its Arabic word `تأكيد` / `إلغاء` on the **left** of its icon (icon read first, right-to-left). If `إعدادات اللعبة` (GAME SETTINGS) appears there: visible, no boxes, size OK? Write down which words you see there in English, if any.
6. **F1-4 (optional):** if the top-right guide offers GAME SETTINGS, open it once: screenshot the header (expected `إعدادات اللعبة`, drawn with the `$KH2Menu` font). Change nothing; press Cancel/back.
7. **F1-5 close-up:** Win+Shift+S, crop around `لعبة جديدة` and around the help line, paste into Paint, save.

**Swap to F2**
8. Quit the game fully. In `~mods`, delete `pakchunk99-arabictest2F1_P.pak` (the original stays in `C:\filessss\mewo\kh3fm-arabic\out\builds\ARABIC-TEST-2\`). Copy `out\builds\ARABIC-TEST-2\pakchunk99-arabictest2F2_P.pak` into `~mods` (Properties: **3,694,678 bytes**). Keep exactly one of our paks in `~mods`.
9. Start the game; take **F2-1** (= step 2), **F2-3** (= step 5) and **F2-5** (= step 7); answer a–e again.
10. Compare F1 and F2: which size fits the English caps better? In F2, are low letters (ج ع ي, the dots under ب) cut at the bottom, or do items touch the highlight bar or each other?

**Remove**
11. Quit the game, delete the pak from `~mods`, then delete the empty `~mods` folder (leave the other empty `mods` folder alone, it is not ours). Start once more: the title menu is English again. No Steam file verification needed. (If you prefer to keep one installed, say which.)
12. Send: screenshots saved as `20261008_ARABIC-TEST-2_01.png`, `_02.png`, … in `C:\filessss\mewo\kh3fm-arabic\screenshots\` (please also put `20261008_ARABIC-TEST-1_01.png` there) + the yes/no answers per step, + F1 or F2.

## 13. TEST50 (2026-10-09) — fonts of all text fields, full shaper, 50-row test pack, installed
Title screenshot of ARABIC-TEST-2 F1 (chat): **PASS** (joins closed, RTL, help line full stop at the left, GAME SETTINGS + `button_0020` icon+Confirm/Cancel). F1 scale locked (PROJECT_MAP §4).

### 13a. Font classes of the movie text fields — VERIFIED (`tools\font_census.py`, full table `out\builds\TEST50\ref\font_fields.tsv`)
1,089 Scaleform movies (copy the game loads, `_P` wins), 1,165 DefineEditText fields.

| class (TresFont id) | where (groups) | letterSpacing != 0 in menu/help/subtitle movies | Arabic before → after TEST50 |
|---|---|---|---|
| `$sougei` (3) | all menus, camp menu, game help, HUD commands, messages (868 fields) | Title 61: 2 px \ 30 pt = 17.07 units → +18 | yes (F1) → yes |
| `$KH2Menu` (4) | pause, settings header, HUD, game help symbols (114) | none (gummi: 2 \ 34, −1) | yes (F1) → yes |
| `$jimakuNE` (1) | Subtitle 38 pt, CutsceneText 38 pt, Dialog 21 pt, Theater, Gummiphone (57) | none (Gummiphone −3/−4) | no → **yes** |
| `$JimakuJP` (2) | Japanese twins of the same fields (115) | none (Gummiphone 2 \ 23–35) | no → **yes** |
| local `KH2 WI CLASSIC Normal` | 42_mobilePortal/MobileLsi only (Classic Kingdom scores, digits/caps) | — | not touched |

Join extension: needed units = ceil(ls × 256 / pt) over the relevant fields → 18 for `$sougei`, 0 elsewhere; every class keeps +18 (the F1 value seen closed in-game at ls 2 and harmless overlap at ls 0). Glyph scale per class = F1 Arabic-to-cap-height ratio (K/DY in PROJECT_MAP §4). Re-parse: all original glyphs and non-font tags byte-equal; each class gained exactly the 189 codes.

### 13b. TEST50 pak
`out\builds\TEST50\pakchunk99-test50_P.pak` 3,881,308 B, SHA256 `a26a76917c005f8c1d26e7c42da030bf405075a9243f9bdb68191099ead14191`: 7 locres (kh3_camp 20, kh3_event_bt 6, kh3_gamehelp 3, kh3_item 11, kh3_menu 31, kh3_settings 4, kh3_system 9 entries changed = 50 test + 34 title rows) + TresFont. list / hash-list / unpack SHA256 9/9 PASS. Installed with `SWAP_TO_TEST50.bat` (F1 pak 302d95d1… removed; `state\SWAP_LOG.tsv`). Checklist: `technical\TEST50_CHECKLIST.md`.

