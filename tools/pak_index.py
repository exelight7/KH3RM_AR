"""Read-only: decrypt and parse UE4 pak v4 indexes -> TSV (pak, path, size, compressed_size, compression, encrypted).
Key is read from tools/KEY_SOURCE.txt (line key_hex_first32=...).
Usage: python -I pak_index.py <out.tsv> <pak> [<pak> ...]"""
import os, struct, sys
from Crypto.Cipher import AES

HERE = os.path.dirname(os.path.abspath(__file__))


def load_key():
    for line in open(os.path.join(HERE, 'KEY_SOURCE.txt'), encoding='utf-8'):
        if line.startswith('key_hex_first32='):
            return bytes.fromhex(line.split('=', 1)[1].strip())
    raise SystemExit('key not found in KEY_SOURCE.txt')


def fstring(d, p):
    n = struct.unpack_from('<i', d, p)[0]
    p += 4
    if n == 0:
        return '', p
    if n < 0:  # UTF-16
        s = d[p:p - n * 2].decode('utf-16-le')
        return s.rstrip('\0'), p - n * 2
    return d[p:p + n].decode('latin-1').rstrip('\0'), p + n


def entries(path, key):
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        f.seek(size - 45)
        t = f.read(45)
        enc = t[0]
        magic, ver, off, isz = struct.unpack_from('<IIQQ', t, 1)
        assert magic == 0x5A6F12E1 and ver == 4, (path, hex(magic), ver)
        f.seek(off)
        d = f.read(isz)
    if enc:
        d = AES.new(key, AES.MODE_ECB).decrypt(d)
    mount, p = fstring(d, 0)
    count = struct.unpack_from('<i', d, p)[0]
    p += 4
    for _ in range(count):
        name, p = fstring(d, p)
        _off, csize, usize, comp = struct.unpack_from('<qqqi', d, p)
        p += 28 + 20  # + sha1
        if comp:
            nb = struct.unpack_from('<i', d, p)[0]
            p += 4 + nb * 16
        encrypted = d[p]
        p += 5  # flag + block size
        yield mount, name, usize, csize, comp, encrypted


def main():
    key = load_key()
    out = open(sys.argv[1], 'w', encoding='utf-8', newline='\n')
    out.write('pak\tpath\tsize\tcompressed_size\tcompression\tencrypted\n')
    for pak in sys.argv[2:]:
        rel = pak.replace('\\', '/').split('/Content/', 1)[-1]  # Paks/x.pak or _DLC_/VOICE/en/Paks/x.pak
        n = 0
        for mount, name, usize, csize, comp, enc in entries(pak, key):
            full = (mount + name).replace('../../../', '', 1)
            out.write(f'{rel}\t{full}\t{usize}\t{csize}\t{comp}\t{enc}\n')
            n += 1
        print(os.path.basename(pak), n, file=sys.stderr)


if __name__ == '__main__':
    main()
