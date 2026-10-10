"""Read-only: list fonts inside a Scaleform GFx movie embedded in a SwfMovie .uexp.
Prints tag histogram, then per font: id, name, glyph count, code range summary, Arabic coverage.
Handles DefineFont2/3 (tags 48/75) and GFx DefineCompactedFont (1005) header/code table.
Usage: python -I gfx_fonts.py <TresFont.uexp> [...]"""
import collections, struct, sys, zlib

ARABIC = [(0x0600, 0x06FF), (0x0750, 0x077F), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF)]


def movie(d):
    i = min(x for x in (d.find(b'GFX'), d.find(b'CFX'), d.find(b'FWS'), d.find(b'CWS')) if x >= 0)
    sig, ver, size = d[i:i + 3], d[i + 3], struct.unpack_from('<I', d, i + 4)[0]
    body = d[i + 8:i + size] if sig in (b'GFX', b'FWS') else zlib.decompress(d[i + 8:])
    return sig, ver, size, i, body


def tags(body):
    nbits = body[0] >> 3
    p = (5 + 4 * nbits + 7) // 8 + 4  # RECT + framerate + framecount
    while p + 2 <= len(body):
        h = struct.unpack_from('<H', body, p)[0]
        p += 2
        code, ln = h >> 6, h & 0x3F
        if ln == 0x3F:
            ln = struct.unpack_from('<I', body, p)[0]
            p += 4
        yield code, body[p:p + ln]
        p += ln
        if code == 0:
            break


def ranges(codes):
    out, codes = [], sorted(set(codes))
    for c in codes:
        if out and c == out[-1][1] + 1:
            out[-1][1] = c
        else:
            out.append([c, c])
    return out


def define_font23(t):
    fid, flags, lang, nlen = struct.unpack_from('<HBBB', t, 0)
    name = t[5:5 + nlen].decode('latin-1').rstrip('\0')
    p = 5 + nlen
    n = struct.unpack_from('<H', t, p)[0]
    p += 2
    wide_off, wide_codes = flags & 0x08, flags & 0x04
    if n == 0:
        return fid, name, 0, []
    osz = 4 if wide_off else 2
    offs = struct.unpack_from('<%d%s' % (n, 'I' if wide_off else 'H'), t, p)
    code_off = struct.unpack_from('<I' if wide_off else '<H', t, p + n * osz)[0]
    ct = p + code_off
    codes = struct.unpack_from('<%d%s' % (n, 'H' if wide_codes else 'B'), t, ct)
    return fid, name, n, list(codes)


def compacted(t):
    """GFx DefineCompactedFont (1005): u16 id, then the FontCompactor container:
    name (NUL-terminated UTF-8), u16 flags, u16 nominalSize, s16 ascent, s16 descent, s16 leading,
    u32 numGlyphs, u32 glyphBytes, glyph shapes, then numGlyphs x {u16 code, s16 advance, u32 offset}.
    Returns (id, name, n, codes, extra)."""
    fid = struct.unpack_from('<H', t, 0)[0]
    z = t.index(b'\0', 2)
    name = t[2:z].decode('utf-8', 'replace')
    flags, nominal, asc, desc, lead, n, gbytes = struct.unpack_from('<HHhhhII', t, z + 1)
    p = z + 1 + 18 + gbytes
    codes = [struct.unpack_from('<H', t, p + 8 * i)[0] for i in range(n)]
    assert codes == sorted(codes), 'code table not ascending: layout guess wrong'
    return fid, name, n, codes, dict(flags=hex(flags), nominal=nominal, ascent=asc, descent=desc, leading=lead)


def main():
    for path in sys.argv[1:]:
        d = open(path, 'rb').read()
        sig, ver, size, at, body = movie(d)
        print(f'== {path}\n  {sig.decode()} v{ver} size={size} at={at}')
        hist = collections.Counter()
        for code, t in tags(body):
            hist[code] += 1
            extra = ''
            if code in (48, 75):
                fid, name, n, codes = define_font23(t)
            elif code == 1005:
                fid, name, n, codes, extra = compacted(t)
            elif code == 88:  # DefineFontName
                fid = struct.unpack_from('<H', t)[0]
                print(f'  DefineFontName id={fid} {t[2:].split(b"\0")[0].decode("latin-1")!r}')
                continue
            else:
                continue
            ar = sum(1 for c in codes if any(a <= c <= b for a, b in ARABIC))
            rs = ranges(codes)
            print(f'  tag{code} font id={fid} name={name!r} glyphs={n} arabic={ar} {extra} '
                  f'ranges={len(rs)} first={[(hex(a), hex(b)) for a, b in rs[:8]]} last={[(hex(a), hex(b)) for a, b in rs[-3:]]}')
        print('  tags', dict(sorted(hist.items())))


if __name__ == '__main__':
    main()
