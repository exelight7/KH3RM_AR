"""Read-only: list every DefineEditText (tag 37) in Scaleform SwfMovie .uexp files: id, variable name, font
(id -> imported alias), size in pt, letterSpacing, alignment, bounds, flags, initial HTML text.
letterSpacing/align come from the field's initial HTML (<TEXTFORMAT LETTERSPACING=..>, <P ALIGN=..>);
the layout record's align is the fallback. Usage: python -I gfx_edittext.py <movie.uexp>... > out.tsv"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx_fonts import movie, tags

ALIGN = ['left', 'right', 'center', 'justify']


def cstr(t, p):
    z = t.index(b'\0', p)
    return t[p:z].decode('utf-8', 'replace'), z + 1


def rect(t):
    nb = t[0] >> 3
    bits = int.from_bytes(t[:(5 + 4 * nb + 7) // 8], 'big')
    total = (5 + 4 * nb + 7) // 8 * 8
    vals = []
    for i in range(4):
        v = (bits >> (total - 5 - nb * (i + 1))) & ((1 << nb) - 1)
        vals.append((v - (1 << nb) if v >> (nb - 1) else v) / 20)
    return vals, (5 + 4 * nb + 7) // 8


def fonts(body):
    """font id -> alias, from ImportAssets (57/71) and DefineFont/Compacted names."""
    out = {}
    for code, t in tags(body):
        if code in (57, 71):
            url, p = cstr(t, 0)
            p += 2 if code == 71 else 0
            n = struct.unpack_from('<H', t, p)[0]
            p += 2
            for _ in range(n):
                cid = struct.unpack_from('<H', t, p)[0]
                name, p = cstr(t, p + 2)
                out[cid] = name
        elif code == 1005:
            out.setdefault(struct.unpack_from('<H', t)[0], 'local:' + cstr(t, 2)[0])
    return out


def edittext(t):
    cid = struct.unpack_from('<H', t)[0]
    bounds, n = rect(t[2:])
    p = 2 + n
    f1, f2 = t[p], t[p + 1]
    p += 2
    r = dict(id=cid, bounds=bounds, wordwrap=bool(f1 & 0x40), multiline=bool(f1 & 0x20), html=bool(f2 & 0x02),
             autosize=bool(f2 & 0x40), font=None, fontclass='', height=None, align='', text='')
    if f1 & 0x01:
        r['font'] = struct.unpack_from('<H', t, p)[0]
        p += 2
    if f2 & 0x80:
        r['fontclass'], p = cstr(t, p)
    if f1 & 0x01 or f2 & 0x80:
        r['height'] = struct.unpack_from('<H', t, p)[0] / 20
        p += 2
    if f1 & 0x04:
        p += 4
    if f1 & 0x02:
        p += 2
    if f2 & 0x20:
        r['align'] = ALIGN[t[p]] if t[p] < 4 else str(t[p])
        p += 9
    r['var'], p = cstr(t, p)
    if f1 & 0x80:
        r['text'], p = cstr(t, p)
    return r


def html_attr(text, name):
    return sorted(set(m.upper() if name == 'ALIGN' else m for m in re.findall(name + r'="([^"]*)"', text, re.I)))


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    print('movie\tid\tvar\tfont\tsize_pt\tletterSpacing\talign\tbounds_px_x0..x1,y0..y1\tflags\ttext')
    for path in sys.argv[1:]:
        try:
            body = movie(open(path, 'rb').read())[4]
        except ValueError:
            continue  # not a movie (texture etc.)
        fmap = fonts(body)
        for code, t in tags(body):
            if code != 37:
                continue
            r = edittext(t)
            font = r['fontclass'] or fmap.get(r['font'], f'id{r["font"]}')
            ls = ','.join(html_attr(r['text'], 'LETTERSPACING')) or '0'
            al = ','.join(a.lower() for a in html_attr(r['text'], 'ALIGN')) or r['align']
            fl = ' '.join(k for k in ('html', 'multiline', 'wordwrap', 'autosize') if r[k])
            txt = re.sub(r'<[^>]*>', '', r['text']).replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
            print(f'{os.path.basename(path)[:-5]}\t{r["id"]}\t{r["var"]}\t{font}\t{r["height"]}\t{ls}\t{al}\t'
                  f'{"{:g}..{:g},{:g}..{:g}".format(*r["bounds"])}\t{fl}\t{txt[:60]}')


if __name__ == '__main__':
    main()
