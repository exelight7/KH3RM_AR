"""Read-only: entry/word counts per category for the English locres export (extracted/text_en.tsv).
Words = whitespace tokens with a letter/digit after removing <tags> and {args}.
Usage: python -I text_counts.py <text_en.tsv> <out.tsv>"""
import collections, csv, re, sys

TAG = re.compile(r'<[^>]*>|\{[^}]*\}')
WORD = re.compile(r'\w')

REMIND_NS = {'kh3_gamehelp.remind', 'kh3_extraload.dlc', 'kh3_menu.slideshow', 'kh3_menu.hologram'}
ITEM_NS = {'kh3_system.ability', 'kh3_system.command', 'kh3_gumiship.item'}
TUT_NS = {'kh3_system.gameoverhint'}


def category(f, ns, key):
    if f.endswith('_dlc.locres') or ns in REMIND_NS or 'dlc' in key.lower():
        return 'remind'
    if f.startswith('kh3_event_'):
        return 'subtitles_cutscenes'
    if f.startswith('kh3_fieldvoice_'):
        return 'dialogue'
    if f in ('kh3_tutorial.locres', 'kh3_gamehelp.locres') or ns in TUT_NS:
        return 'tutorials'
    if f == 'kh3_item.locres' or ns in ITEM_NS:
        return 'items_abilities'
    if f in ('kh3_mobile.locres', 'kh3_extraload.locres'):
        return 'journal'
    return 'menus_ui'


def words(t):
    t = TAG.sub(' ', t.replace('\\n', ' '))
    return sum(1 for w in t.split() if WORD.search(w))


def main():
    rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
    agg = collections.defaultdict(lambda: [0, 0, set(), 0, 0])  # entries, empty, uniq, words, chars
    for r in rows:
        cat = category(r['file'], r['namespace'], r['key'])
        for k in (('category', cat, cat), ('file', r['file'], cat)):
            a = agg[k]
            a[0] += 1
            a[1] += r['text'] == ''
            a[2].add(r['text'])
            a[3] += words(r['text'])
            a[4] += len(r['text'])
    tot = [len(rows), sum(r['text'] == '' for r in rows), len({r['text'] for r in rows}),
           sum(words(r['text']) for r in rows), sum(len(r['text']) for r in rows)]
    with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as out:
        out.write('level\tname\tcategory\tentries\tempty\tunique_texts\twords\tchars\n')
        for (lvl, name, cat), a in sorted(agg.items(), key=lambda kv: (kv[0][0] != 'category', kv[0][2], kv[0][1])):
            out.write(f'{lvl}\t{name}\t{cat}\t{a[0]}\t{a[1]}\t{len(a[2])}\t{a[3]}\t{a[4]}\n')
        out.write(f'total\tall en Game locres\t-\t' + '\t'.join(map(str, tot)) + '\n')


if __name__ == '__main__':
    assert words('<icon(Decide)> Next  <icon(Cancel)> Close') == 2
    assert words('{0} / {1}') == 0
    main()
