# TAGS — markup in KH3 English text (VERIFIED from `extracted\text_en.tsv`, 17,222 entries)

Source: all 67 `Localization/Game/en/*.locres`. Counts are occurrences. Tool: `tools\tag_inventory.py`.
Rule for translation: **every tag, argument and icon must survive unchanged**; only the text between them is translated.

## 1. Inventory

| Markup | Count | Meaning (inferred from use) | Arabic note |
|---|---|---|---|
| `<br>` | 6,252 | line break (Scaleform HTML) | keep; line order matters for RTL wrap |
| `<Br>` | 1 | same, odd case (yt154a) | keep as-is |
| `<i(on)>` … `<i(off)>` | 837 / 832 | italics on/off (whispers, inner voice, flashbacks) | Segoe UI Regular has no italic in the same file → renderer may fake-slant or ignore; screenshot test |
| `<I(off)>` | 1 | typo variant of `<i(off)>` (ts270a) | keep |
| `<b(on)>` … `<b(off)>` | 35 / 35 | bold (battle gate titles) | — |
| `<color(X)>` … `<color>` | 1,092 / 1,092 | colour span; X = strong 849, heading 194, hashtag 37, red 10, yellow 1, situation 1 | keep pair balanced |
| `<icon(X)>` | 1,410 | inline button/key/status icon, 130 distinct names (Triangle 157, Decide 152, ArrowSpace 133, Square 113, Cancel 63, R2 57 …, `Kb_*` keyboard, `*_S` small, `*Sub`, `dlc`, `Coda`) | icon is a glyph in the text run → its position flips with bidi; check |
| `<pb>` / `<pb(N)>` | 90 / 147 | page break / timed page break (N seconds, 0.4–3.7) — field voice bubbles, gummi tips | keep values |
| `<nbsp>` | 62 | non-breaking space (indent in help) | keep |
| `<conv(off\|disable\|force)>` | 36 | icon conversion control (gamepad ↔ keyboard icons) | keep |
| `{0}`…`{4}` | 245 / 47 / 9 / 2 / 1 | FText ordered arguments | may be reordered within the sentence |
| `{0}\|plural(one=…,other=…)` | 37 | ICU plural form | Arabic needs zero/one/two/few/many/other; UE 4.17 supports those keywords — test |
| `\n` (raw) | 0 | none — breaks are always `<br>` | — |
| Special chars | — | — 284, ￠ U+FFE0 164 (hashtag sign), ★ 92 / ☆ 68, χ 35, ①–④, ′ ″ | ￠ is the "#" of in-game posts; keep |

Language names in `kh3_settings.language` (日本語, 한국어, 繁體中文 …) are native-script on purpose.

## 2. Twenty real examples (file | namespace | key → text)

1. `kh3_event_bt | bt001a | op0010010sr0_1` → `<i(on)>They can take your world.<i(off)>`
2. `kh3_event_ts | ts270a | ts2700210sr1_1` → `<i(on)>That's<I(off)> the heart's true nature—<br>to never, ever let go.`
3. `kh3_event_fz | fz462a | fz4620010af0_4` → `<i(on)>We only have each other<i(off)><br>`
4. `kh3_event_yt | yt154a | yt1540520ie0` → `Yes. Their teacher, Master Eraqus,<Br>would have been another possibility,`
5. `kh3_fieldvoice_ra | chat | rapunzel_0380` → `<pb(0.55)>Look.`
6. `kh3_fieldvoice_town_tt | talk | man01_0010` → `The old mansion? Just head through the conduit,<br>and then it's a short walk through the woods.`
7. `kh3_gumiship | menu | top_0460` → `You can now voyage into a new zone!<pb>Use <icon(L2)> or <icon(R2)> to switch between zones.`
8. `kh3_gamehelp | general | button_002` → `<icon(Decide)> Next  <icon(Cancel)> Close`
9. `kh3_mobile | character | button_0010` → `<icon(KeyLeftRight)> Switch Models  <icon(RstickLeft)>/<icon(RstickRight)> Rotate Model  <icon(L2)> Previous  <icon(R2)> Next`
10. `kh3_settings | gamepad | button_0020` → `<icon(Kb_Del)> Undo`
11. `kh3_settings | gamepad | choice_0100` → `<conv(disable)><icon(Cross)><conv(off)>`
12. `kh3_level | bx | information_0030` → `Use <icon(Triangle)><color(strong)>Cover Shot<color> to push your way forward!`
13. `kh3_system | gameoverhint | general_0060` → `Hazy about the controls? Forgot how a feature works?<br>Select <color(strong)>Game Help<color> from the Main Menu to refresh your memory.`
14. `kh3_settings | gamepad | detail_0350` → `<color(red)>Gamepad has been disconnected.<color>`
15. `kh3_menu | slideshow | title_0050` → `<color(heading)>SIMPLE<color>`
16. `kh3_mobile | treasure | window_0020` → `{0} / {1}`
17. `kh3_level | ts | result_1010` → `{0}′{1}″{2}`
18. `kh3_mobile | camera | dialog_0030` → `You have photographed {0}|plural(one=your first lucky emblem,other={0} lucky emblems)!<br>Obtained <color(strong)>{1}<color>.`
19. `kh3_level | ex | battleportal_01` → `<b(on)>Battlegate 1 - Difficulty ★☆☆<b(off)><br><br>Powerful adversaries lie beyond this gate.<br>Enter and meet them in battle?`
20. `kh3_extraload | dlc | detail_30500_00` → `I'll save you, no matter what.<br><color(hashtag)>￠oath<color>`

Extra: `kh3_camp | gamehelp | group_0060` → `Re<icon(Coda)>Mind` (Re Mind logo is an icon inside the word); `kh3_gamehelp | minigame | detail_40101_01` uses `<nbsp><nbsp><nbsp>` for indent; `kh3_camp | gamehelp | detail_0020` → `Go to Game Help.<br><color(strong)>(<icon(dlc)> Downloadable Content)<color>`.

## 3. Validator rule for PIPE / translation rounds
Per entry, the multiset of `<…>` tags, `{n}` args, `|plural(` count and `<icon(X)>` names must be identical in EN and AR; `<color(..)>`/`<color>` and `<i(on)>`/`<i(off)>` must stay balanced (the EN source itself has oddities: one `<Br>`, one `<I(off)>`, and 837 `<i(on)>` vs 833 closers — compare AR against EN per entry, not against an ideal).
