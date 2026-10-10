"""Read-only (BUILD-4): where a Scaleform movie places its characters. For every DefineSprite (tag 39) and the root
timeline: each PlaceObject2/3 (26/70) of the first frame that sets a character -> sprite, depth, character id,
instance name, translate x/y and scale x/y (px). Text-field neighbours of a field: the other characters placed in the
same sprite, with their edit-text bounds moved by the placement (scale and rotate ignored when 1/0).
Usage: python -I tools/gfx_layout.py <movie.uexp> <field id>"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx_fonts import movie, tags
from gfx_edittext import edittext, cstr


class Bits:
    def __init__(self, d, p):
        self.d, self.b = d, p * 8

    def u(self, n):
        v = 0
        for _ in range(n):
            v = v << 1 | (self.d[self.b >> 3] >> (7 - (self.b & 7))) & 1
            self.b += 1
        return v

    def s(self, n):
        v = self.u(n)
        return v - (1 << n) if n and v >> (n - 1) else v

    def end(self):
        return (self.b + 7) // 8


def matrix(d, p):
    """-> (sx, sy, tx px, ty px), next byte offset"""
    r = Bits(d, p)
    sx = sy = 1.0
    if r.u(1):
        n = r.u(5)
        sx, sy = r.s(n) / 65536, r.s(n) / 65536
    if r.u(1):
        n = r.u(5)
        r.s(n), r.s(n)
    n = r.u(5)
    tx, ty = r.s(n) / 20, r.s(n) / 20
    return (sx, sy, tx, ty), r.end()


def place(code, t):
    """PlaceObject2/3 -> dict(depth, char, name, m) or None (no character)"""
    f = t[0]
    if code == 26:
        depth, p = struct.unpack_from('<H', t, 1)[0], 3
        f2 = 0
    else:
        f2 = t[1]
        depth, p = struct.unpack_from('<H', t, 2)[0], 4
        if f2 & 0x08:  # class name (with HasImage alone GFx writes none, unlike the SWF spec)
            _, p = cstr(t, p)
    char = None
    if f & 0x02:
        char = struct.unpack_from('<H', t, p)[0]
        p += 2
    m = (1.0, 1.0, 0.0, 0.0)
    if f & 0x04:
        m, p = matrix(t, p)
    if f & 0x08:  # color transform: skip (bit-packed)
        r = Bits(t, p)
        ha, hm, n = r.u(1), r.u(1), r.u(4)
        for _ in range((4 if hm else 0) + (4 if ha else 0)):
            r.s(n)
        p = r.end()
    if f & 0x10:
        p += 2
    name = cstr(t, p)[0] if f & 0x20 else ''
    return dict(depth=depth, char=char, name=name, m=m) if char is not None else None


def layout(body):
    """-> {sprite id (0 = root): [placement]}, {char id: edittext record}"""
    sprites, fields = {}, {}

    def walk(sid, it):
        out = sprites.setdefault(sid, [])
        for code, t in it:
            if code in (26, 70):
                pl = place(code, t)
                if pl:
                    out.append(pl)
            elif code == 1:  # first frame only
                break
    for code, t in tags(body):
        if code == 37:
            r = edittext(t)
            fields[r['id']] = r
        elif code == 39:
            sid = struct.unpack_from('<H', t)[0]
            walk(sid, sub_tags(t[4:]))
    return sprites, fields


def sub_tags(t):
    p = 0
    while p + 2 <= len(t):
        h = struct.unpack_from('<H', t, p)[0]
        p += 2
        code, ln = h >> 6, h & 0x3F
        if ln == 0x3F:
            ln = struct.unpack_from('<I', t, p)[0]
            p += 4
        yield code, t[p:p + ln]
        p += ln
        if code == 0:
            break


def neighbours(body, fid):
    """-> [(sprite, placement, x0, x1, y0, y1 in sprite px, field record or None)] for the sprites that place fid"""
    sprites, fields = layout(body)
    out = []
    for sid, pls in sprites.items():
        if not any(p['char'] == fid for p in pls):
            continue
        for p in pls:
            f = fields.get(p['char'])
            sx, sy, tx, ty = p['m']
            box = (tx + sx * f['bounds'][0], tx + sx * f['bounds'][1], ty + sy * f['bounds'][2], ty + sy * f['bounds'][3]) if f else (tx, tx, ty, ty)
            out.append((sid, p, *box, f))
    return out


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    body = movie(open(sys.argv[1], 'rb').read())[4]
    for sid, p, x0, x1, y0, y1, f in neighbours(body, int(sys.argv[2])):
        txt = f and f['text'][:30].replace('\n', ' ').replace('\r', ' ')
        print(f'sprite {sid}\tdepth {p["depth"]}\tchar {p["char"]}\t{p["name"]}\tm {p["m"]}\t'
              f'x {x0:.2f}..{x1:.2f} y {y0:.2f}..{y1:.2f}\t{(f["height"], f["align"], txt) if f else ""}')
