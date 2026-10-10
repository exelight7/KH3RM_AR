"""Offline preview: draw a shaped string with the glyphs of a (rebuilt) TresFont, the way Scaleform lays it out
(left to right, advance * size / 256 + letterSpacing px after every glyph). Even-odd fill, 4x supersampled.
Not the game renderer: use it to spot gaps/overlaps before an in-game screenshot.
Usage: python -I preview_text.py <TresFont.uasset> <font id> <size px> <letterSpacing px> <out.png> <logical text>..."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageChops, ImageDraw
import shaper, tresfont

SS = 4


def contours(shape):
    """compacted shape -> list of point lists (font units, y down), curves flattened."""
    out = []
    for x, y, edges in shape[1]:
        pts = [(x, y)]
        for t, f in edges:
            if t < 2:
                x += f[0]
            elif t < 4:
                y += f[0]
            elif t < 8:
                x, y = x + f[0], y + f[1]
            else:
                cx, cy = x + f[0], y + f[1]
                ax, ay = cx + f[2], cy + f[3]
                for i in range(1, 9):
                    u = i / 8
                    pts.append(((1 - u) ** 2 * x + 2 * u * (1 - u) * cx + u * u * ax,
                                (1 - u) ** 2 * y + 2 * u * (1 - u) * cy + u * u * ay))
                x, y = ax, ay
                continue
            pts.append((x, y))
        out.append(pts)
    return out


def render(font, text, size, spacing):
    g = {c: (a, font['shapes'][s]) for c, a, s in font['glyphs']}
    k = size / 256 * SS
    w = int(sum(g[ord(c)][0] * size / 256 + spacing for c in text) * SS) + 40 * SS
    img = Image.new('L', (w, int(size * 1.6 * SS)), 0)
    pen, base = 20 * SS, size * 1.1 * SS
    for c in text:
        adv, shape = g[ord(c)]
        glyph = Image.new('1', img.size, 0)  # even-odd inside a glyph, union between glyphs
        for pts in contours(shape):
            if len(pts) > 2:
                m = Image.new('1', img.size, 0)
                ImageDraw.Draw(m).polygon([(pen + x * k, base + y * k) for x, y in pts], fill=1)
                glyph = ImageChops.logical_xor(glyph, m)
        img = ImageChops.lighter(img, glyph.convert('L'))
        pen += (adv * size / 256 + spacing) * SS
    return Image.eval(img.resize((img.width // SS, img.height // SS), Image.LANCZOS), lambda v: 255 - v)


if __name__ == '__main__':
    path, fid, size, spacing, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    font = next(f for f in tresfont.load(path)[2].values() if f['id'] == fid)
    lines = [render(font, shaper.shape(t), size, spacing) for t in sys.argv[6:]]
    sheet = Image.new('L', (max(i.width for i in lines), sum(i.height for i in lines)), 255)
    y = 0
    for i in lines:
        sheet.paste(i, (0, y))
        y += i.height
    sheet.save(out)
