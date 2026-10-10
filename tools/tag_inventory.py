"""Read-only: inventory of markup in the English locres export.
Usage: python -I tag_inventory.py <text_en.tsv>  -> prints sections to stdout (UTF-8)."""
import collections, csv, re, sys, unicodedata

TAG = re.compile(r'<([^>]*)>')
ARG = re.compile(r'\{([^}]*)\}')
PLURAL = re.compile(r'\|(plural|gender|ordinal|hpp)\(')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
    kinds, icons, colors, args, mods, chars = (collections.Counter() for _ in range(6))
    example = {}
    for r in rows:
        t = r['text']
        ref = f"{r['file']}|{r['namespace']}|{r['key']}"
        for m in TAG.findall(t):
            k = re.sub(r'\(.*', '(…)', m)
            kinds[k] += 1
            example.setdefault('<' + k + '>', ref)
            if m.startswith('icon('):
                icons[m[5:-1]] += 1
            if m.startswith('color('):
                colors[m[6:-1]] += 1
        for a in ARG.findall(t):
            args['{' + a + '}'] += 1
            example.setdefault('{arg}', ref)
        for m in PLURAL.findall(t):
            mods['|' + m + '(…)'] += 1
            example.setdefault('|' + m, ref)
        if '\\n' in t:
            kinds['\\n (raw newline)'] += 1
            example.setdefault('\\n', ref)
        for c in t:
            if ord(c) > 0x7E:
                chars[c] += 1
    print('## tags'); [print(f'{n}\t<{k}>') for k, n in kinds.most_common()]
    print('## icons'); [print(f'{n}\t{k}') for k, n in icons.most_common()]
    print('## colors'); [print(f'{n}\t{k}') for k, n in colors.most_common()]
    print('## args'); [print(f'{n}\t{k}') for k, n in args.most_common()]
    print('## modifiers'); [print(f'{n}\t{k}') for k, n in mods.most_common()]
    print('## non-ascii chars')
    for c, n in chars.most_common():
        print(f'{n}\tU+{ord(c):04X}\t{c}\t{unicodedata.name(c, "?")}')
    print('## first example per feature'); [print(f'{k}\t{v}') for k, v in example.items()]


if __name__ == '__main__':
    main()
