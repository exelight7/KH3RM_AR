"""Read-only: parse UE4 .pak footers (magic 0x5A6F12E1) and print version/encryption info.
Usage: python -I pak_footer.py <pak> [<pak> ...]  -> TSV on stdout."""
import struct, sys, os

MAGIC = 0x5A6F12E1

def footer(path):
    size = os.path.getsize(path)
    with open(path, 'rb') as f:
        n = min(size, 1024)
        f.seek(size - n)
        tail = f.read(n)
    # find the magic searching backwards; footer layouts differ by version
    for i in range(len(tail) - 4, -1, -1):
        if struct.unpack_from('<I', tail, i)[0] != MAGIC:
            continue
        ver, idx_off, idx_size = struct.unpack_from('<IQQ', tail, i + 4)
        if not (1 <= ver <= 12) or idx_off + idx_size > size:
            continue
        sha = tail[i + 24:i + 44].hex()
        guid = tail[i - 17:i - 1].hex() if i >= 17 else ''
        enc_idx = tail[i - 1] if i >= 1 else -1
        comp = []
        p = i + 44
        while p + 32 <= len(tail):
            name = tail[p:p + 32].split(b'\0')[0].decode('ascii', 'replace')
            if name:
                comp.append(name)
            p += 32
        return dict(size=size, ver=ver, idx_off=idx_off, idx_size=idx_size,
                    enc_idx=enc_idx, guid=guid, comp=','.join(comp),
                    footer_from_end=len(tail) - i + 17)
    return dict(size=size, ver='NOMAGIC')

if __name__ == '__main__':
    print('pak\tsize\tver\tenc_index\tkey_guid\tindex_off\tindex_size\tcompression')
    for p in sys.argv[1:]:
        d = footer(p)
        print('\t'.join(str(x) for x in [os.path.basename(p), d['size'], d['ver'], d.get('enc_idx'),
                                           d.get('guid'), d.get('idx_off'), d.get('idx_size'), d.get('comp')]))
