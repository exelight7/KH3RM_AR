# SHAPER_SPEC — Arabic pre-shaper for KH3 Scaleform text

round: PIPE-1 (design) / TEST50 (built) / BUILD-1 (§7) · date: 2026-10-09 · status: **BUILT** §1-7 in `tools\shaper.py`, tests §9 in `tools\test_shaper.py` (U1-U12, T1-T22, 30 real rows, round trip over all translated rows, BUILD-1 wrap / conv / icon-cluster tests). §7 as built (BUILD-1): `wrap()` breaks every logical line wider than its field (also lines between EN `<br>`) at space runs outside tags, `{n}`, plural blocks and conv groups and never between two LTR characters; widths from `technical\FIELD_WIDTHS.tsv` (movie field per namespace prefix + key regex) and the glyph advances of the rebuilt TresFont, margin 0.97, icon = 1.25 em, `{n}` = width of `0000`; namespaces without a known field stay unbroken. A whole-row `<conv(X)>`…`<conv(off)>` pair is kept and its inside shaped (conv hoist); adjacent icons form one atom. Round trip: UAX #9 maps a number run followed by a Latin run and the reverse order to the same visual line, so unshape() returns one of them (7 of 5,744 rows); `<I(off)>` comes back as `<i(off)>`.

## 0. Why
- KH3 draws all game text with Scaleform GFx (`TresFont` `$sougei` / `$jimakuNE`, RECON §4). Scaleform lays glyphs **left to right, one code point = one glyph, no joining, no bidi** (same situation as KH2; UNVERIFIED in-game until ARABIC-TEST).
- So the `.locres` text must already be in **visual order** and use **presentation-form code points** (U+FB50–FDFF, U+FE70–FEFC), which the rebuilt TresFont will contain (Segoe UI Regular, RECON §4).
- Pipeline position: translator writes logical Arabic into the TSV (`text` column) → validator (TAGS.md §3) on the logical text → **shaper** → `tools\locres.py tsv-import` → pak.
- The TSV keeps the logical text. Shaped text exists only in build output; `unshape()` restores the logical text (round-trip check).

## 1. Input / output contract
`shape(text: str, profile) -> str`, `unshape(shaped: str) -> str`.
- Input: one locres entry in logical order, may contain the tags of TAGS.md §1.
- Output: same tags, Arabic letters replaced by presentation forms, each line in visual (left-to-right drawing) order.
- **Passthrough:** an entry with no Arabic letter (U+0621–064A, U+066E–06D3, U+FB50–FEFC) is returned **unchanged** (e.g. `{0} / {1}`, `{0}′{1}″{2}`, `<conv(disable)><icon(Cross)><conv(off)>`, language names).
- Deterministic, no randomness, no dictionary. Same input → same bytes.

## 2. Tokenizer
Split the entry into tokens, in this priority:

| Token | Pattern | Class for bidi | Joining |
|---|---|---|---|
| Line break | `<br>`, `<Br>` (case kept) | splits lines | — |
| Page break | `<pb>`, `<pb(N)>` | splits pages (each page = lines) | — |
| Style tag | `<color(X)>`, `<color>`, `<i(on)>`, `<i(off)>`, `<I(off)>`, `<b(on)>`, `<b(off)>` | removed → per-character style state (§5) | transparent |
| Conv group | `<conv(X)>` … up to and incl. the next `<conv(off)>` (or end of line) | one atom, ON | non-joining |
| Icon | `<icon(X)>` | atom, ON | non-joining |
| Non-break space | `<nbsp>` | atom, WS | non-joining |
| Plural | `{n}\|plural(k=…,k=…)` | atom, ON; each form text shaped recursively (§6) | non-joining |
| Argument | `{n}` | atom, ON | non-joining |
| Any other `<…>` | — | **error** (unknown tag) | — |
| Character | everything else | Unicode bidi class | Unicode joining type |

Atoms are never split, never reordered internally and never altered.

## 3. Letter forms (shaping)
Per line, per maximal run of Arabic letters (style tags are transparent, everything else breaks the run):
1. Joining type from Unicode `ArabicShaping.txt` (embedded table): **R** (ا أ إ آ ٱ د ذ ر ز و ؤ ة ى), **D** (all other letters incl. ئ), **U** (ء), **T** (marks — rejected, see 3.5).
2. Form: joins-right = previous letter is D and current is R/D; joins-left = current is D and next is R/D.
   isolated / final (joins-right only) / initial (joins-left only) / medial (both).
3. **Lam-alef (mandatory):** ل followed by ا أ إ آ → one glyph: لا FEFB/FEFC, لأ FEF7/FEF8, لإ FEF9/FEFA, لآ FEF5/FEF6 (isolated / final, final if ل joins right). The ligature never joins left.
4. Map (letter, form) → presentation form: U+FE80–FEF4 for the 36 base letters + hamza forms; U+FB50–FBFF for the optional extra letters **پ چ ڤ گ** (foreign names, e.g. "V"). Letters without a form for the requested position fall back to isolated (and are reported).
5. Rejected by the validator before shaping: harakat U+064B–0652, U+0670, tatweel U+0640 (Scaleform has no mark positioning; KH2 rule). Allowed punctuation: ، ؛ ؟ (U+060C/061B/061F, in Segoe UI and in the new glyph set), ASCII `. ! : - ( ) " '`, `—`, `…`.
6. Digits: **Western 0–9** in static text (runtime numbers from `{n}` are Western too; consistent look). ٠–٩ allowed but not recommended.

## 4. Visual order (per line)
Unicode Bidirectional Algorithm (UAX #9) with **paragraph level 1 (RTL)**, rules W1–W7, N1–N2, I1–I2, L2, L4, on the token sequence (atoms = one character of the class in §2):
- Arabic letters/forms = AL→R, Latin letters = L, digits = EN, `/ , . :` between digits = CS (keeps `3/10`, `1.5`), ￠ = ET, spaces/punctuation = neutral.
- **English runs** (names, `HP`, `MP`, `KINGDOM HEARTS`, `Re<icon(Coda)>Mind`) and **number runs** stay left-to-right inside the line, as whole runs placed by RTL order.
- `{n}`/icons are neutral: between Arabic words they follow RTL order; `{0} / {1}` inside an Arabic sentence comes out as `{1} / {0}` (reads "..." right-to-left).
- **L4 mirroring:** `( ) [ ] « »` inside RTL resolve get their mirrored code point (the engine draws LTR, so `(` must be stored as `)`).
- L2: reverse every run with odd level → final left-to-right glyph sequence.
- Lines are processed **independently**; line order (top → bottom) and page order stay logical. Empty lines (`<br><br>`) and a trailing `<br>` are kept.

## 5. Style tags after reordering
Style tags are not characters, so they are converted to a per-character state (color X | none, italic on/off, bold on/off) before reordering and re-emitted after it:
- Walk the visual sequence; whenever the state changes, emit closing tags for what turned off (`<color>`, `<i(off)>`, `<b(off)>`) then opening tags for what turned on (`<color(X)>`, `<i(on)>`, `<b(on)>`), in a fixed order (color outermost).
- State is closed at the end of each line and reopened at the start of the next (a span crossing `<br>` becomes one span per line).
- Consequence (documented, accepted): the shaped output can differ from the EN tag multiset where EN is unbalanced (837 `<i(on)>` vs 833 closers, `<I(off)>` typo) — the EN-vs-AR validator runs on the **logical** text; the shaped text is checked by §8 rule 2 instead.

## 6. Plurals and arguments
- `{0}|plural(one=…,two=…,few=…,many=…,other=…)`: UE 4.17 picks one form at runtime and inserts it. Each form's text is shaped as its own one-line string (it may contain `{0}` and style tags); the whole plural block is then one atom in the line. Arabic categories zero/one/two/few/many/other are allowed (ICU); which ones UE 4.17 evaluates for culture `en` is **UNVERIFIED** (we overwrite `en`, so English rules apply: only one/other may ever be selected → translator writes forms that read correctly with `one` and `other` only).
- Separators inside plural: ASCII `,` and `)` are syntax; inside Arabic text use **،** (U+060C) instead of `,`.
- `{n}` values arrive at runtime already finished: numbers (LTR) or other locres strings (item/character names) that are themselves shaped → inserted as a block. No joining across `{n}`.

## 7. Line breaking (Scaleform word-wrap problem)
If a text field word-wraps, Scaleform breaks the **visual** string from its left end — the logical end of the sentence would come out on line 1. Rules:
1. The shaper never relies on engine wrapping: it breaks lines itself **before** reordering, at spaces in logical order, and inserts `<br>`.
2. Width = Σ advance of the glyphs (from the rebuilt TresFont code table, `tools\tresfont.py`) × pt size / 256. Per-category profile: font alias, pt size, max width in px (from the movie's DefineEditText bounds, e.g. Subtitle 38 pt `$jimakuNE`, Dialog 21 pt, GameHelp `$sougei`). Widths are a calibration knob, filled at ARABIC-TEST.
3. Keep the EN line count when it fits (KH2 rule); subtitles/menus never get extra lines silently — rows that do not fit go to `translation\long_rows.md`. Paragraph categories (journal, tutorials, loading posts) may re-flow to more lines.
4. Alignment: left-aligned fields will show Arabic flush-left. Whether Scaleform `<p align="right">` survives the game's tag conversion is UNVERIFIED (ARABIC-TEST item); centred fields (subtitles, titles) are unaffected. FULL-1: the exe's tag converter knows only b, br, color (`<font color='%s'>`), icon (`<img src='img://icontext:%s'>`), conv, i, pb, nbsp — no align tag (see `state\LAST_REPORT.md` FULL-1 A3 for the options).

### 7b. Reflow for fields that show fewer lines (FULL-1, built)
`technical\FIELD_WIDTHS.tsv` column `max_lines`: when a row has more logical lines than that, `shaper.reflow()` joins the body lines (all lines except a last whole-line `<color(..)>..<color>` footer) with one space, then `wrap()` re-breaks them at the field width — the fewest lines that fit. Used for the help-text fields (`MainLibrary#68` / `CodeMenu#26`: ability, customize and premium-menu descriptions, max 2 lines after the FULL-1 screenshot). The AR text in `translation\` keeps the EN `<br>` count (validator BR rule); only the built text changes.

## 8. Validation (run on every built row)
1. `unshape(shape(x)) == normalize(x)` (normalize = style tags in canonical form/positions).
2. Per character, style state in output == state in logical input; atom multiset (icons, `{n}`, plural, conv, nbsp, br, pb) identical and line/page counts identical.
3. Every output code point exists in the target font's code table (`$sougei`, `$jimakuNE` after the TresFont rebuild).
4. No code point in U+0600–06FF letter range left in output (all became presentation forms), except digits/punctuation ، ؛ ؟.
5. Width per line ≤ profile width (§7).

## 9. Unit tests
`R(w)` = shaped + reversed Arabic word; code points written as `uXXXX`.

### 9a. Core
| # | Input (logical) | Expected |
|---|---|---|
| U1 | `باب` | `uFE8F uFE8E uFE91` (ب iso, ا fin, ب ini, reversed) |
| U2 | `في` | `uFEF2 uFED3` |
| U3 | `لا` | `uFEFB` |
| U4 | `سلام` | `uFEE1 uFEFC uFEB3` (lam-alef final; م isolated after alef) |
| U5 | `مستوى 25` | `25 ` + R(مستوى) — digits keep LTR |
| U6 | `HP 120` alone | unchanged (passthrough, no Arabic) |
| U7 | `اسم (جديد)` | `(`R(جديد)`) `R(اسم) — order reversed, then L4 mirrors both brackets so they still open towards the word |
| U8 | `كلمة ، كلمة ؟` | Arabic punctuation kept, moves with RTL order |
| U9 | `ء` alone, `ة` after D letter | U isolated `uFE80`; ة final `uFE94` |
| U10 | `شَمس` | **rejected** (haraka) |
| U11 | `unshape(shape(x)) == x` | for U1–U9 |
| U12 | `ڤينتوس` | ڤ initial `uFB6C` (optional letter set) |

### 9b. The 20 TAGS.md examples (AR text here is a test sentence, not the final translation)
| # | Source (TAGS.md §2) | Test input (logical AR) | Expected structure |
|---|---|---|---|
| T1 | bt001a op0010010sr0_1 | `<i(on)>يمكنهم أخذ عالمك.<i(off)>` | `<i(on)>.` R(عالمك) ` ` R(أخذ) ` ` R(يمكنهم)`<i(off)>` — period at visual left |
| T2 | ts2700210sr1_1 | `<i(on)>هذه<I(off)> طبيعة القلب—<br>ألا يترك أبداً.` | 2 lines, each reversed alone; italic only on R(هذه) at the right end of line 1; output `<i(off)>` canonical (§5) |
| T3 | fz4620010af0_4 | `<i(on)>ليس لنا إلا بعضنا<i(off)><br>` | 1 line + trailing `<br>` kept |
| T4 | yt1540520ie0 | `نعم. معلمهم، المعلم إراكوس،<Br>كان احتمالاً آخر،` | `<Br>` kept with its case; line 1 then line 2 |
| T5 | rapunzel_0380 | `<pb(0.55)>انظر.` | `<pb(0.55)>` first (page split), then `.`R(انظر) |
| T6 | man01_0010 | `القصر القديم؟ اعبر الممر،<br>ثم امشِ قليلاً في الغابة.` | rejected (ِ haraka) → fixed text without marks passes; 2 lines |
| T7 | top_0460 | `يمكنك الآن الإبحار إلى منطقة جديدة!<pb>استخدم <icon(L2)> أو <icon(R2)> للتنقل.` | 2 pages; page 2 visual: `.`R(للتنقل) ` <icon(R2)> ` R(أو) ` <icon(L2)> ` R(استخدم) |
| T8 | button_002 | `<icon(Decide)> التالي  <icon(Cancel)> إغلاق` | R(إغلاق) ` <icon(Cancel)>  ` R(التالي) ` <icon(Decide)>` — icon/label pairs mirror as units |
| T9 | button_0010 | `<icon(KeyLeftRight)> تبديل  <icon(RstickLeft)>/<icon(RstickRight)> تدوير` | `<icon(RstickLeft)>/<icon(RstickRight)>` order between the two icons follows RTL (ON) → becomes `<icon(RstickRight)>/<icon(RstickLeft)>`; flagged for screenshot review |
| T10 | button_0020 | `<icon(Kb_Del)> تراجع` | R(تراجع) ` <icon(Kb_Del)>` |
| T11 | choice_0100 | `<conv(disable)><icon(Cross)><conv(off)>` | unchanged (passthrough) |
| T12 | bx information_0030 | `استخدم <icon(Triangle)><color(strong)>الضربة المحمية<color> للتقدم!` | `!`R(للتقدم)` <color(strong)>`R(المحمية)` `R(الضربة)`<color><icon(Triangle)> `R(استخدم) |
| T13 | general_0060 | 2 lines with `<color(strong)>مساعدة اللعب<color>` on line 2 | colour span stays on line 2, tags re-emitted around the reversed words |
| T14 | detail_0350 | `<color(red)>تم فصل وحدة التحكم.<color>` | `<color(red)>.`R(…)`<color>` — whole line one span |
| T15 | title_0050 | `<color(heading)>بسيط<color>` | `<color(heading)>`R(بسيط)`<color>` |
| T16 | window_0020 | `{0} / {1}` | unchanged (passthrough) |
| T17 | result_1010 | `{0}′{1}″{2}` | unchanged (passthrough) |
| T18 | dialog_0030 | `صوّرت {0}\|plural(one=أول شعار حظ,other={0} شعارات حظ)!<br>حصلت على <color(strong)>{1}<color>.` | `ّ` rejected; without it: plural forms shaped inside, block = atom; line 2 `.<color(strong)>{1}<color> `R(على)` `R(حصلت) |
| T19 | battleportal_01 | `<b(on)>بوابة المعركة 1 - الصعوبة ★☆☆<b(off)><br><br>…` | `1` stays an LTR run; `★☆☆` is neutral → reversed to `☆☆★` (filled star on the right = read first; screenshot check); empty line kept; bold span per line |
| T20 | detail_30500_00 | `سأنقذك مهما حدث.<br><color(hashtag)>￠قسم<color>` | line 2: `<color(hashtag)>`R(قسم)`￠<color>` — ￠ at the right (read first) |
| T21 | group_0060 | `Re<icon(Coda)>Mind` inside Arabic | stays one LTR run `Re<icon(Coda)>Mind` |
| T22 | detail_40101_01 | `<nbsp><nbsp><nbsp>نص` | nbsp atoms move to the visual right end (indent side for RTL) |

Expected values marked R(…) are generated by U-tests' table; the test file stores the full code-point strings once the shaper exists.
