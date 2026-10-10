r"""Read-only (TEST50): font classes of every text field in the game's Scaleform movies.
Extracts each UI/Scaleform/**/*.uexp (no culture subfolders except en/, <= 2 MB; bigger ones are bitmap holders) from
the copy the game loads (a *_P patch pak wins over the base pak) into out\builds\TEST50\ref\movies\, lists its
DefineEditText fields (tools\gfx_edittext.py) and writes out\builds\TEST50\ref\font_fields.tsv + a per-class summary
(stdout). The AES key comes from tools\KEY_SOURCE.txt (used read-only to read the pak index, never stored elsewhere).
Usage (from the project root): python -I tools/font_census.py"""
import collections, csv, os, re, subprocess, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx_fonts import movie, tags
from gfx_edittext import fonts, edittext, html_attr
from pak_index import load_key

GAME = r'C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content'
OUT = 'out/builds/TEST50/ref'
REPAK = os.path.abspath('tools/repak-0.2.3/repak.exe')
SF = 'KINGDOM HEARTS III/Content/UI/Scaleform/'
CULTURE = re.compile(r'/(ja|de|fr|it|es|ko|zh-Hant)/')


def movies():
    """path -> pak the game loads it from"""
    best = {}
    for r in csv.DictReader(open('extracted/pak_index.tsv', encoding='utf-8', newline=''), delimiter='\t', quoting=csv.QUOTE_NONE):
        p = r['path']
        if p.startswith(SF) and p.endswith('.uexp') and not CULTURE.search(p) and int(r['size']) <= 2 << 20:
            if p not in best or r['pak'].endswith('_P.pak') and not best[p].endswith('_P.pak'):
                best[p] = r['pak']
    return best


def extract(best):
    key = '0x' + load_key().hex()
    os.makedirs(os.path.join(OUT, 'movies'), exist_ok=True)  # repak does not create the output root
    by_pak = collections.defaultdict(list)
    for p, pak in best.items():
        if not os.path.exists(os.path.join(OUT, 'movies', p)):
            by_pak[pak].append(p)
    for pak, paths in by_pak.items():
        for i in range(0, len(paths), 50):
            subprocess.run([REPAK, '-a', key, 'unpack', '-q', '-f', '-o', os.path.join(OUT, 'movies'),
                            os.path.join(GAME, pak.replace('/', os.sep))] + [a for x in paths[i:i + 50] for a in ('-i', x)],
                           check=True, capture_output=True)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    best = movies()
    extract(best)
    rows = []
    for p, pak in sorted(best.items()):
        try:
            body = movie(open(os.path.join(OUT, 'movies', p), 'rb').read())[4]
        except (ValueError, FileNotFoundError, zlib.error):  # texture holders: no movie or a stray signature
            continue
        fmap = fonts(body)
        for code, t in tags(body):
            if code == 37:
                r = edittext(t)
                ls = ','.join(html_attr(r['text'], 'LETTERSPACING')) or '0'
                rows.append([p[len(SF):-5], os.path.basename(pak), r['id'], r['var'],
                             r['fontclass'] or fmap.get(r['font'], f'id{r["font"]}'), r['height'], ls,
                             re.sub(r'<[^>]*>', '', r['text']).replace('\r', ' ').replace('\n', ' ')[:40]])
    with open(os.path.join(OUT, 'font_fields.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('movie\tpak\tid\tvar\tfont\tsize_pt\tletterSpacing\ttext\n')
        f.writelines('\t'.join(map(str, r)) + '\n' for r in rows)
    print(len(best), 'movies,', len({r[0] for r in rows}), 'with text fields,', len(rows), 'fields')
    per = collections.defaultdict(list)
    for r in rows:
        per[r[4]].append(r)
    for font, rs in sorted(per.items(), key=lambda x: -len(x[1])):
        spaced = sorted({(float(r[6].split(',')[-1]), r[5]) for r in rs if r[6] != '0'})
        print(f'{font}\t{len(rs)} fields\t{len({r[0] for r in rs})} movies\tsizes {sorted({r[5] for r in rs})}\t'
              f'letterSpacing!=0 (ls, pt): {spaced}')


if __name__ == '__main__':
    main()
