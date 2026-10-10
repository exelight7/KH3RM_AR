"""Read-only: summarise extracted/pak_index.tsv per pak and flag Re Mind (DLC) content.
Re Mind marker = path segment/name containing 'DLC' (any case), 'Rebellis' (Re Mind flag set), or 'remind'.
Usage: python -I remind_map.py <pak_index.tsv> <out.tsv>"""
import collections, csv, re, sys

MARK = re.compile(r'dlc|rebellis|remind', re.I)


def main():
    per = collections.defaultdict(lambda: [0, 0, 0, collections.Counter()])
    for row in csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
        s = per[row['pak']]
        s[0] += 1
        s[1] += int(row['size'])
        if MARK.search(row['path']):
            s[2] += 1
            parts = row['path'].split('/')
            s[3]['/'.join(parts[2:5]) if parts[0] == 'KINGDOM HEARTS III' else '/'.join(parts[:3])] += 1
    with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as out:
        out.write('pak\tentries\tbytes\tremind_entries\tremind_share\ttop_remind_dirs\n')
        for pak in sorted(per):
            n, b, r, dirs = per[pak]
            top = '; '.join(f'{d}={c}' for d, c in dirs.most_common(4))
            out.write(f'{pak}\t{n}\t{b}\t{r}\t{r / n:.2f}\t{top}\n')


if __name__ == '__main__':
    main()
