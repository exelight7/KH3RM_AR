r"""BATCH-234 / BATCH 2a: glyph coverage + suspicious letter combinations (report only, changes nothing).
1. every character of the shaped text actually built into a pak (locres entries of <build>\unpacked, one per translated
   row) is looked up in the four TresFont classes of that build ($jimakuNE 1, $JimakuJP 2, $sougei 3, $KH2Menu 4);
   a missing character = a box in game if the row is drawn in that class. Non-Arabic characters that the row's EN also
   uses are listed apart (the English game draws them the same way). Rows of translation\raw_logical_ids.tsv are drawn
   by Windows (not TresFont) and only counted.
2. image strings (images_strings.tsv + every rect source of technical\images_rects.tsv) are drawn by
   tools\texture_text.py with segoeui.ttf: their shaped characters are looked up in its cmap (and in the 4 classes).
3. suspicious combinations in the logical AR: Latin token not in EN, doubled article (ال ال / الال...), presentation
   forms in the source, a non-letter glued inside a word (tag, digit, punctuation, ZWNJ/ZWJ/LRM/RLM, NBSP),
   ta marbuta / alef maqsura followed by a letter (missing space), comma / full stop glued to the next word.
-> review\BATCH2_GLYPHS.md (+ review\BATCH2_GLYPHS.tsv)
Usage: python -I tools\batch2_glyphs.py [build-dir]   (default out\builds\BUILD-11)"""
import collections, csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locres, shaper, tresfont
import texture_text as tt
from build_arabictest1 import FONT
from build_test50 import FONT_IDS
from fontTools.ttLib import TTFont
from tsvlib import load_translation, read_tsv

AR = 'ء-يٱ-ۓ'
LETTER = re.compile(f'[{AR}]')
CHECKS = [
    ('DOUBLE_ARTICLE', re.compile(f'(?<![{AR}])[وفبكل]?(?:ال|لل)\\s*ال(?=[{AR}])')),
    ('PRESENTATION_FORM', re.compile('[ﭐ-﷿ﹰ-ﻼ]')),
    ('GLUED_INSIDE_WORD', re.compile(f'[{AR}](?:<[^<>]*>|[0-9A-Za-z‌‍‎‏ ­.,،:;!?])+(?=[{AR}])')),
    ('TA_MARBUTA_OR_MAQSURA_JOINED', re.compile(f'[ةى](?=[{AR}])')),
    ('PUNCT_NO_SPACE', re.compile(f'[{AR}][،.!?:](?=[{AR}])')),
]


def built_text(build):
    out = {}
    for d, _, fs in os.walk(os.path.join(build, 'unpacked')):
        for fn in fs:
            if fn.endswith('.locres'):
                for ns, _, es in locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                    out.update({(ns, k): t for k, _, _, t, _ in es})
    return out


def visible_chars(text):
    return {c for c in shaper.TOKEN.sub('', locres.unesc(text)) if c not in ' \r\n\t'}


def classes(build):
    fonts = tresfont.load(os.path.join(build, 'unpacked', FONT + '.uasset'))[2].values()
    return {f['id']: {chr(c) for c, _, _ in f['glyphs']} for f in fonts if f['id'] in FONT_IDS}


def image_strings(rows):
    strings = tt.load_strings()
    out = {f'img:{k}': v['AR'] for k, v in strings.items()}
    for asset, rs in tt.rows_by_asset().items():
        for r in rs:
            if r['source'] != 'blank':
                out.setdefault(r['source'], tt.arabic(r['source'], rows, strings))
    return out


def main(build='out/builds/BUILD-11'):
    sys.stdout.reconfigure(encoding='utf-8')
    rows = load_translation()
    tr = [r for r in rows if r['status'] != 'todo' and r['AR']]
    raw = {r[0] for r in read_tsv('translation/raw_logical_ids.tsv')[1:]}
    built, cls = built_text(build), classes(build)
    miss = collections.defaultdict(lambda: collections.defaultdict(list))   # (fid, char) -> kind -> ids
    for r in tr:
        if r['id'] in raw:
            continue
        en = locres.unesc(r['EN'])
        for c in visible_chars(built[(r['namespace'], r['key'])]):
            for fid, have in cls.items():
                if c not in have:
                    kind = 'ARABIC' if shaper.is_arabic(c) else 'IN_EN' if c in en else 'NOT_IN_EN'
                    miss[(fid, c)][kind].append(r['id'])
    by_id = {r['id']: r for r in rows}
    imgs = image_strings(by_id)
    cmap = set(map(chr, TTFont(tt.FONT).getBestCmap()))
    img_miss = collections.defaultdict(list)
    img_cls = collections.defaultdict(list)
    for src, ar in imgs.items():
        for c in visible_chars(shaper.shape(ar)):
            if c not in cmap:
                img_miss[c].append(src)
            for fid, have in cls.items():
                if c not in have and shaper.is_arabic(c):
                    img_cls[(fid, c)].append(src)
    hits = collections.defaultdict(list)
    lat = []
    from validate import latin_tokens
    strings = tt.load_strings()
    for key, en, ar in [(r['id'], r['EN'], r['AR']) for r in tr] + [(k, v['EN'], v['AR']) for k, v in strings.items()]:
        if not latin_tokens(ar) <= latin_tokens(en):
            lat.append((key, sorted(latin_tokens(ar) - latin_tokens(en))))
        for name, rx in CHECKS:
            for m in rx.finditer(ar):
                hits[name].append((key, ar[max(0, m.start() - 12):m.end() + 12].replace('\t', ' ')))

    L = ['# BATCH 2a: glyph coverage and suspicious combinations', '',
         f'Build checked: `{build}` (pak locres = the shaped text that is really shipped). Generated by `tools/batch2_glyphs.py`.', '',
         f'- translated rows: {len(tr)}; drawn by TresFont: {len(tr) - len(raw & {r["id"] for r in tr})}; '
         f'raw logical (drawn by Windows, not checked against TresFont): {len(raw)} ({", ".join(sorted(raw))})',
         '- font classes: ' + ', '.join(f'{FONT_IDS[f]} {len(c)} glyphs' for f, c in sorted(cls.items())),
         f'- image sources: {len(imgs)} (images_strings {sum(s.startswith("img:") for s in imgs)}, rect sources '
         f'{sum(not s.startswith("img:") for s in imgs)}); renderer font segoeui.ttf, {len(cmap)} code points', '',
         '## 1. Characters missing from a TresFont class (text rows)', '',
         '| class | char | U+ | kind | rows | ids (first 12) |', '|---|---|---|---|---|---|']
    tsv = [['section', 'class', 'char', 'cp', 'kind', 'count', 'ids']]
    for (fid, c), kinds in sorted(miss.items(), key=lambda x: (x[0][0], ord(x[0][1]))):
        for kind, ids in sorted(kinds.items()):
            L.append(f'| {FONT_IDS[fid]} | `{c}` | {ord(c):04X} | {kind} | {len(ids)} | {", ".join(ids[:12])} |')
            tsv.append(['font', FONT_IDS[fid], c, f'{ord(c):04X}', kind, str(len(ids)), ' '.join(ids)])
    if not miss:
        L.append('| - | - | - | none | 0 | - |')
    n_ar = sum(len(ids) for k in miss.values() for kind, ids in k.items() if kind == 'ARABIC')
    n_new = sum(len(ids) for k in miss.values() for kind, ids in k.items() if kind == 'NOT_IN_EN')
    L += ['', f'Arabic characters missing (= boxes): {n_ar} row hits; non-Arabic characters missing and not in the '
          f'row\'s EN: {n_new} row hits; IN_EN = same glyph the English text needs in that class (unchanged game behaviour).', '',
          '## 2. Image strings (renderer segoeui.ttf)', '']
    L += [f'- missing in segoeui.ttf: {len(img_miss)} characters' + (': ' + ', '.join(f'U+{ord(c):04X} ({len(s)})' for c, s in img_miss.items()) if img_miss else '')]
    L += [f'- Arabic characters of the image strings missing in a TresFont class (only matters if one is ever drawn as '
          f'text): {len(img_cls)}' + (': ' + ', '.join(f'{FONT_IDS[f]} U+{ord(c):04X}' for (f, c) in img_cls) if img_cls else '')]
    for c, s in img_miss.items():
        tsv.append(['image', 'segoeui', c, f'{ord(c):04X}', 'MISSING', str(len(s)), ' '.join(s)])
    L += ['', '## 3. Suspicious combinations (logical AR)', '',
          f'- LATIN token not in EN: {len(lat)}' + (': ' + '; '.join(f'{k} {v}' for k, v in lat) if lat else '')]
    for name, _ in CHECKS:
        L.append(f'- {name}: {len(hits[name])}')
    for name, _ in CHECKS:
        if hits[name]:
            L += ['', f'### {name}', '', '| id | context |', '|---|---|']
            L += [f'| {k} | {ctx} |' for k, ctx in hits[name]]
            tsv += [['combo', name, '', '', '', '1', f'{k} {ctx}'] for k, ctx in hits[name]]
    open('review/BATCH2_GLYPHS.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    with open('review/BATCH2_GLYPHS.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in tsv)
    print(f'rows {len(tr)}; font misses {dict(collections.Counter(k for v in miss.values() for k in v))}; '
          f'arabic hits {n_ar}; image segoeui misses {len(img_miss)}; latin {len(lat)}; '
          + ', '.join(f'{n} {len(hits[n])}' for n, _ in CHECKS))


if __name__ == '__main__':
    main(*sys.argv[1:])
