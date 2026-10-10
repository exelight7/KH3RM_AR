r"""Read-only (FINAL-1 part 2): inventory of the textures that show English text.
Sources (from the decrypted pak index extracted\pak_index.tsv, newest pak copy = a _P patch pak over the base pak):
  en culture Texture2D (UI/Icon HelpItem, Mapname, LsiLogo, IconText; LSI games; end_title), Scaleform en *_loc textures,
  Scaleform shared textures (non-culture, read to find baked English), Cutscene TexturePump lists, movie bitmap tags.
Missing assets are extracted read-only (repak + the key in tools\KEY_SOURCE.txt) into extracted\assets.
Writes technical\IMAGES_INVENTORY.tsv (English words, screen and priority from technical\images_words.tsv, written by eye),
out\builds\IMAGES\ref\png\<group>\*.png (mip 0) and one or more contact sheets per group in out\builds\IMAGES\ref\.
Usage: python -I tools\images_inventory.py"""
import collections, csv, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import texture_codec as tc
from pak_index import load_key
from gfx_fonts import movie, tags
from text_coverage import walk, GAME, REPAK

ROOTS = ['extracted/assets', 'out/builds/TEST50/ref/movies', 'out/builds/FULL-1/ref/movies']
REF = 'out/builds/IMAGES/ref'
SF = 'KINGDOM HEARTS III/Content/UI/Scaleform/'
GROUPS = [  # (group, regex on the pak path, default priority)
    ('menus', r'/UI/IconText/Localization/en/', 1),
    ('title', r'/UI/Icon/Mapname/Localization/en/', 1),
    ('tutorial', r'/UI/Icon/HelpItem/Localization/en/', 2),
    ('scaleform_loc', r'/UI/Scaleform/.*/en/[^/]*_loc\.', 1),
    ('logo', r'/UI/Icon/LsiLogo/Localization/en/|/end_title/.*/Localization/en/', 3),
    ('other', r'/LSI/Games/.*/Localization/en/', 3),
    ('scaleform_shared', r'/UI/Scaleform/(?!.*/(ja|en|de|fr|it|es|ko|zh-Hant)/)', 4),
]


def newest(rows):
    """path -> pak: a _P patch pak wins over the base pak (UE mount order), later chunk names win ties"""
    best = {}
    for pak, path in rows:
        k = (('_P.pak' in pak), pak)
        if path not in best or k > best[path][0]:
            best[path] = (k, pak)
    return {p: v[1] for p, v in best.items()}


def local(path):
    """the root holding both the .uasset and the .uexp of this asset (parts never mixed across roots)"""
    stem = path.rsplit('.', 1)[0]
    return next((os.path.join(r, path) for r in ROOTS
                 if all(os.path.exists(os.path.join(r, stem + e)) for e in ('.uasset', '.uexp'))), None)


def extract(missing, where):
    key = '0x' + load_key().hex()
    by = collections.defaultdict(list)
    for p in missing:
        by[where[p]].append(p)
    for pak, ps in by.items():
        for i in range(0, len(ps), 40):
            args = []
            for p in ps[i:i + 40]:
                args += ['-i', p]
            subprocess.run([REPAK, '-a', key, 'unpack', '-q', '-f', '-o', 'extracted/assets',
                            os.path.join(GAME, pak.replace('/', os.sep)), *args], check=True, capture_output=True)


def words_table():
    p = 'technical/images_words.tsv'
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as f:
        return {r['asset']: r for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)}


def sheet(group, items, n):
    """contact sheet(s): 6 columns, label = asset name, checkerboard behind alpha"""
    cw, ch, cols = 320, 200, 6
    font = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 14)
    per = cols * 6
    for s in range(0, len(items), per):
        part = items[s:s + per]
        rows = (len(part) + cols - 1) // cols
        im = Image.new('RGB', (cols * cw, rows * (ch + 20)), (40, 40, 48))
        for i, (name, png) in enumerate(part):
            t = Image.open(png).convert('RGBA')
            t.thumbnail((cw - 8, ch - 8))
            x, y = i % cols * cw + 4, i // cols * (ch + 20) + 4
            bg = Image.new('RGBA', t.size, (90, 90, 100, 255))
            for yy in range(0, t.size[1], 16):
                for xx in range((yy // 16) % 2 * 16, t.size[0], 32):
                    bg.paste((120, 120, 132, 255), (xx, yy, xx + 16, yy + 16))
            im.paste(Image.alpha_composite(bg, t).convert('RGB'), (x, y))
            ImageDraw.Draw(im).text((x, y + ch - 4), name, fill=(255, 230, 140), font=font)
        im.save(os.path.join(REF, f'sheet_{group}_{s // per + 1:02d}.png'))
        n[group] = n.get(group, 0) + 1


def main():
    with open('extracted/pak_index.tsv', encoding='utf-8') as f:
        rows = [(r['pak'], r['path']) for r in csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)]
    where = newest(rows)
    group = {}
    for p in where:
        if not p.endswith('.uasset'):
            continue
        g = next((g for g, rx, _ in GROUPS if re.search(rx, p)), None)
        if g:
            group[p] = g
    missing = [q for p in group if not local(p) for q in (p, p[:-7] + '.uexp', p[:-7] + '.ubulk') if q in where]
    if missing:
        extract(missing, where)
    words = words_table()
    out, pngs, skipped = [], collections.defaultdict(list), collections.Counter()
    for p in sorted(group):
        lp = local(p)
        try:
            t = tc.load(lp)
        except Exception:
            skipped[group[p]] += 1          # not a Texture2D (movie, DataTable, font)
            continue
        i = tc.info(t)
        name = p.split('/')[-1][:-7]
        sub = '/'.join(p.split('/')[-2:])[:-7] if '/HelpItem/' in p else name
        d = os.path.join(REF, 'png', group[p])
        os.makedirs(d, exist_ok=True)
        png = os.path.join(d, sub.replace('/', '_') + '.png')
        if not os.path.exists(png):
            Image.fromarray(tc.rgba0(t), 'RGBA').save(png)
        pngs[group[p]].append((sub, png))
        w = words.get(p, {})
        if group[p] == 'scaleform_shared' and not w:
            continue                         # shared textures enter the inventory only when read as text-bearing
        prio = w.get('priority') or str(next(pr for g, _, pr in GROUPS if g == group[p]))
        out.append([p, group[p], f"{i['w']}x{i['h']}", i['format'], str(i['mips']),
                    'ubulk (streamed)' if 'ubulk' in i['storage'] else 'inline (uexp)', where[p].split('/')[-1],
                    w.get('screen', ''), w.get('english', ''), w.get('plan', ''), prio])
    out.sort(key=lambda r: (r[-1], r[1], r[0]))
    with open('technical/IMAGES_INVENTORY.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('asset\tgroup\tsize\tformat\tmips\tstorage\tpak\tscreen\tenglish\tplan\tpriority\n')
        f.writelines('\t'.join(r) + '\n' for r in out)
    n = {}
    for g, items in pngs.items():
        sheet(g, items, n)
    # movies: bitmaps baked into SWF (DefineBits*/Lossless*) vs external images
    bm = collections.Counter()
    for r in ROOTS:
        for d, _, fs in os.walk(r):
            for fn in fs:
                if fn.endswith('.uexp') and 'Scaleform' in d:
                    try:
                        body = movie(open(os.path.join(d, fn), 'rb').read())[4]
                    except Exception:
                        continue
                    bm['movies'] += 1
                    for code, _ in walk(tags(body)):
                        if code in (6, 20, 21, 35, 36, 90, 1001, 1008, 1009):
                            bm[code] += 1
    tp = sum(1 for p in where if '/TexturePump/' in p and p.endswith('.uasset'))
    print('textures per group:', dict(collections.Counter(r[1] for r in out)), '| not Texture2D:', dict(skipped))
    print('contact sheets:', n, '| movie tags:', dict(bm), '| TexturePump lists:', tp)


if __name__ == '__main__':
    main()
