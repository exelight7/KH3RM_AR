"""Read-only: count plaintext signatures inside pak files (uasset, locres, zlib, ttf/otf).
Usage: python -I scan_magic.py <pak> [...]"""
import mmap, sys, os

SIGS = {
    'uasset': bytes.fromhex('c1832a9e'),
    'locres': bytes.fromhex('0e147475674a03fc4a15909dc3377f1b'),
    'locmeta': bytes.fromhex('4fee4ca1686d4fa0a2c1ef14fd2bc6e5'),  # unverified guid, counted anyway
    'zlib78da': b'\x78\xda',
    'zlib789c': b'\x78\x9c',
    'ttf': bytes.fromhex('0001000000'),
    'otf': b'OTTO\x00',
    'fontface_ext': b'.ufont',
}

for p in sys.argv[1:]:
    with open(p, 'rb') as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
        out = []
        for k, s in SIGS.items():
            if k.startswith('zlib') or k == 'ttf':
                # only count a cheap sample: first 64 MB
                out.append(f'{k}(64MB)={m[:64 << 20].count(s)}')
            else:
                c, i = 0, m.find(s)
                first = i
                while i != -1 and c < 100000:
                    c += 1
                    i = m.find(s, i + 1)
                out.append(f'{k}={c}@{first}')
        print(os.path.basename(p), os.path.getsize(p), ' '.join(out))
