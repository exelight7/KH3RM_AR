r"""UE4.17 cooked Texture2D (.uasset/.uexp[/.ubulk]) reader/writer + pixel codec (FINAL-1).

Layout (verified on KH3 culture textures, see technical\IMAGES_PLAN.md):
  .uasset  package summary + name map (unversioned, LegacyFileVersion -7); never changed here: every write keeps the
           uexp/ubulk sizes, so SerialSize / BulkDataStartOffset stay valid (asserted on read)
  .uexp    tagged properties ... None | i32 hasGuid | u8 u8 UTexture strip | u8 u8 UTexture2D strip | i32 bCooked
           per platform: FName PixelFormat, i32 SkipOffset (package-absolute) | i32 SizeX SizeY NumSlices |
           FString "PF_xxx" | i32 FirstMip | i32 NumMips | per mip: i32 bCooked, FByteBulkData{u32 flags, i32 count,
           i32 sizeOnDisk, i64 offset, payload if inline}, i32 SizeX SizeY | ... FName None | u32 package tag
  bulk     flags 0x40 = inline in the uexp (offset is package-absolute), 0x100 = in the .ubulk (offset + the summary's
           BulkDataStartOffset = position in the .ubulk)
Codec: decode with texture2ddecoder (BGRA out); encode with etcpak (RGBA in). An edit re-encodes only the 4x4 blocks
whose pixels changed, so an unedited texture is rebuilt byte for byte; untouched blocks keep the original bits.
Usage: python -I tools\texture_codec.py info <x.uasset>...
       python -I tools\texture_codec.py png <x.uasset> <out.png>          (mip 0, RGBA)
       python -I tools\texture_codec.py roundtrip <out.tsv> <x.uasset>...  (byte round trip + full re-encode pixel diff)"""
import hashlib, os, struct, sys
import numpy as np
from PIL import Image
import texture2ddecoder
import etcpak

TAG = b'\xc1\x83\x2a\x9e'
BLOCK = {'PF_DXT1': 8, 'PF_BC4': 8, 'PF_DXT5': 16, 'PF_BC5': 16, 'PF_BC7': 16}   # bytes per 4x4 block
RAW = {'PF_B8G8R8A8': 4, 'PF_G8': 1}                                              # bytes per pixel


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---- package -------------------------------------------------------------------------------------------
def names(ua):
    p = 0x1c
    p += 4 + struct.unpack_from('<i', ua, p)[0]                     # FolderName
    _, count, off = struct.unpack_from('<Iii', ua, p)
    out = []
    for _ in range(count):
        n = struct.unpack_from('<i', ua, off)[0]
        assert n > 0, 'UTF-16 names not expected'
        out.append(ua[off + 4:off + 3 + n].decode('ascii'))
        off += 4 + n + 4                                            # string + hash
    return out


def read(ua, ue, ub=b''):
    """-> dict with props, platform data and mips (each mip: fmt-sized payload as bytes)"""
    assert ua[:4] == TAG and ue[-4:] == TAG
    assert ua.count(struct.pack('<q', len(ue) - 4)) == 1, 'export SerialSize not found'
    nm = names(ua)
    fn = lambda p: (nm[struct.unpack_from('<i', ue, p)[0]], struct.unpack_from('<i', ue, p + 4)[0])
    props, p = [], 0
    while True:
        name, _ = fn(p)
        if name == 'None':
            p += 8
            break
        typ = fn(p + 8)[0]
        size = struct.unpack_from('<i', ue, p + 16)[0]
        q = p + 24
        if typ == 'StructProperty':
            q += 24
        elif typ == 'BoolProperty':
            q += 1
        elif typ in ('ByteProperty', 'EnumProperty', 'ArrayProperty', 'SetProperty'):
            q += 8
        elif typ == 'MapProperty':
            q += 16
        q += 1 + 16 * ue[q]
        props.append((name, typ, ue[q:q + size]))
        p = q + size
    has_guid, s1, s2, cooked = struct.unpack_from('<i2s2si', ue, p)
    assert has_guid == 0 and cooked == 1, (has_guid, cooked)
    p += 12
    t = dict(ua=ua, ue=ue, ub=ub, names=nm, props=props, platforms=[])
    base = len(ua)
    while True:
        pf = fn(p)[0]
        if pf == 'None':
            break
        skip = struct.unpack_from('<i', ue, p + 8)[0]
        sx, sy, slices = struct.unpack_from('<3i', ue, p + 12)
        n = struct.unpack_from('<i', ue, p + 24)[0]
        pfs = ue[p + 28:p + 27 + n].decode('ascii')
        q = p + 28 + n
        first, nmips = struct.unpack_from('<2i', ue, q)
        q += 8
        mips = []
        for _ in range(nmips):
            mc, flags, cnt, sod, off = struct.unpack_from('<iIiiq', ue, q)
            q += 24
            if flags & 0x40:
                assert off == base + q, 'inline offset'
                where, at = 'uexp', q
                q += sod
            elif flags & 0x100:
                where, at = 'ubulk', off + base + len(ue) - 4      # relative to BulkDataStartOffset
                assert 0 <= at and at + sod <= len(ub), 'ubulk offset'
            else:
                where, at = 'none', 0
            w, h = struct.unpack_from('<2i', ue, q)
            q += 8
            mips.append(dict(flags=flags, size=sod, where=where, at=at, w=w, h=h))
        assert base + q == skip, 'SkipOffset'
        t['platforms'].append(dict(pf=pf, pfs=pfs, sx=sx, sy=sy, slices=slices, first=first, mips=mips))
        p = q
    return t


def mip_bytes(t, m):
    src = {'uexp': t['ue'], 'ubulk': t['ub']}.get(m['where'], b'')
    return src[m['at']:m['at'] + m['size']]


def write(t, new):
    """new = {mip index: payload bytes of the same size} for platform 0 -> (uasset, uexp, ubulk)"""
    ue, ub = bytearray(t['ue']), bytearray(t['ub'])
    for i, data in new.items():
        m = t['platforms'][0]['mips'][i]
        assert len(data) == m['size'], 'mip size must not change'
        buf = ue if m['where'] == 'uexp' else ub
        buf[m['at']:m['at'] + m['size']] = data
    return t['ua'], bytes(ue), bytes(ub)


def load(uasset_path):
    stem = uasset_path[:-len('.uasset')]
    rd = lambda e: open(stem + e, 'rb').read() if os.path.exists(stem + e) else b''
    return read(rd('.uasset'), rd('.uexp'), rd('.ubulk'))


# ---- pixels --------------------------------------------------------------------------------------------
def decode(pf, data, w, h):
    """-> RGBA uint8 array (h, w, 4)"""
    if pf in RAW:
        a = np.frombuffer(data, np.uint8)
        if pf == 'PF_G8':
            g = a.reshape(h, w)
            return np.dstack([g, g, g, np.full_like(g, 255)])
        return a.reshape(h, w, 4)[..., [2, 1, 0, 3]].copy()
    bw, bh = (w + 3) // 4 * 4, (h + 3) // 4 * 4
    fn = {'PF_DXT1': texture2ddecoder.decode_bc1, 'PF_DXT5': texture2ddecoder.decode_bc3, 'PF_BC4': texture2ddecoder.decode_bc4,
          'PF_BC5': texture2ddecoder.decode_bc5, 'PF_BC7': texture2ddecoder.decode_bc7}[pf]
    a = np.frombuffer(fn(data, bw, bh), np.uint8).reshape(bh, bw, 4)[..., [2, 1, 0, 3]]
    return a[:h, :w].copy()


def encode(pf, rgba):
    """full encode of an RGBA array (dimensions padded to 4)"""
    h, w = rgba.shape[:2]
    if pf in RAW:
        return rgba[..., 0].tobytes() if pf == 'PF_G8' else rgba[..., [2, 1, 0, 3]].tobytes()
    bh, bw = (h + 3) // 4 * 4, (w + 3) // 4 * 4
    pad = np.zeros((bh, bw, 4), np.uint8)
    pad[:h, :w] = rgba
    pad[h:, :w] = rgba[h - 1:h]
    pad[:, w:] = pad[:, w - 1:w]
    raw = np.ascontiguousarray(pad).tobytes()
    if pf == 'PF_BC7':
        p = etcpak.BC7CompressBlockParams()
        p.init_perceptual_weights()
        return etcpak.compress_bc7(raw, bw, bh, p)
    return {'PF_DXT1': etcpak.compress_bc1, 'PF_DXT5': etcpak.compress_bc3, 'PF_BC4': etcpak.compress_bc4,
            'PF_BC5': etcpak.compress_bc5}[pf](raw, bw, bh)


def patch(pf, data, w, h, rgba):
    """re-encode only the 4x4 blocks whose decoded pixels differ from rgba; other bytes stay as they are"""
    old = decode(pf, data, w, h)
    if pf in RAW:
        return encode(pf, rgba)
    bs, bw, bh = BLOCK[pf], (w + 3) // 4, (h + 3) // 4
    out = bytearray(data)
    for by in range(bh):
        for bx in range(bw):
            ys, xs = slice(by * 4, min(by * 4 + 4, h)), slice(bx * 4, min(bx * 4 + 4, w))
            if np.array_equal(old[ys, xs], rgba[ys, xs]):
                continue
            blk = rgba[ys, xs]
            blk = np.pad(blk, ((0, 4 - blk.shape[0]), (0, 4 - blk.shape[1]), (0, 0)), mode='edge')
            i = (by * bw + bx) * bs
            out[i:i + bs] = encode(pf, blk)
    return bytes(out)


def mip_chain(t, rgba0):
    """payloads for every stored mip of platform 0 from an edited mip 0 (lower mips: box-filtered from mip 0,
    then block-patched against the original mip, so unchanged areas keep their bits)"""
    pl = t['platforms'][0]
    out = {}
    for i, m in enumerate(pl['mips']):
        if m['where'] == 'none':
            continue
        if i == 0:
            img = rgba0
        else:
            img = np.asarray(Image.fromarray(rgba0, 'RGBA').resize((m['w'], m['h']), Image.BOX))
            orig = decode(pl['pf'], mip_bytes(t, m), m['w'], m['h'])
            # keep the original pixels where the downscaled source did not change
            src0 = decode(pl['pf'], mip_bytes(t, pl['mips'][0]), pl['mips'][0]['w'], pl['mips'][0]['h'])
            same = np.asarray(Image.fromarray(src0, 'RGBA').resize((m['w'], m['h']), Image.BOX))
            img = np.where((img == same).all(-1, keepdims=True), orig, img)
        out[i] = patch(pl['pf'], mip_bytes(t, m), m['w'], m['h'], img)
    return out


def rgba0(t):
    pl = t['platforms'][0]
    m = pl['mips'][0]
    return decode(pl['pf'], mip_bytes(t, m), m['w'], m['h'])


# ---- CLI -----------------------------------------------------------------------------------------------
def info(t):
    pl = t['platforms'][0]
    return dict(format=pl['pf'], w=pl['sx'], h=pl['sy'], mips=len(pl['mips']),
                storage='+'.join(sorted({m['where'] for m in pl['mips']})), platforms=len(t['platforms']),
                props=','.join(p[0] for p in t['props']))


def roundtrip(out_tsv, paths):
    """1) parse -> decode -> patch with the unedited pixels -> write: must be byte-identical (uasset, uexp, ubulk);
    2) full re-encode of mip 0 (every block): same structure/size, pixel difference reported (lossy formats)"""
    rows, bad = [['asset', 'format', 'size', 'mips', 'storage', 'byte_identical', 'reparse_same',
                  'full_reencode_size_same', 'full_reencode_max_diff', 'full_reencode_mean_diff', 'sha256_uexp']], 0
    for up in paths:
        t = load(up)
        pl = t['platforms'][0]
        new = mip_chain(t, rgba0(t))
        ua, ue, ub = write(t, new)
        same = (ua, ue, ub) == (t['ua'], t['ue'], t['ub'])
        t2 = read(ua, ue, ub)
        reparse = info(t2) == info(t)
        m = pl['mips'][0]
        full = encode(pl['pf'], rgba0(t))
        ua3, ue3, ub3 = write(t, {0: full})
        d = np.abs(decode(pl['pf'], full, m['w'], m['h']).astype(int) - rgba0(t).astype(int))
        ok = same and reparse and len(ue3) == len(t['ue'])
        bad += not ok
        rows.append([os.path.basename(up)[:-7], pl['pf'], f"{pl['sx']}x{pl['sy']}", str(len(pl['mips'])), info(t)['storage'],
                     'PASS' if same else 'FAIL', 'PASS' if reparse else 'FAIL', 'PASS' if len(ue3) == len(t['ue']) else 'FAIL',
                     str(d.max()), f'{d.mean():.3f}', sha(t['ue'])])
    with open(out_tsv, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in rows)
    print(f'roundtrip: {len(paths)} textures, {bad} fail -> {out_tsv}')
    return bad


def self_check():
    """synthetic: patch() leaves untouched blocks byte-identical and changes only the edited ones"""
    rng = np.random.default_rng(1)
    img = rng.integers(0, 255, (16, 16, 4), np.uint8)
    for pf in ('PF_DXT1', 'PF_DXT5', 'PF_BC7', 'PF_B8G8R8A8'):
        data = encode(pf, img)
        dec = decode(pf, data, 16, 16)
        assert patch(pf, data, 16, 16, dec) == data, pf
        ed = dec.copy()
        ed[0:4, 0:4] = 255
        out = patch(pf, data, 16, 16, ed)
        if pf in BLOCK:
            bs = BLOCK[pf]
            assert out[bs:] == data[bs:] and out[:bs] != data[:bs], pf
    print('texture_codec self check: PASS')


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        self_check()
    elif a[0] == 'info':
        for p in a[1:]:
            print(os.path.basename(p), info(load(p)))
    elif a[0] == 'png':
        Image.fromarray(rgba0(load(a[1])), 'RGBA').save(a[2])
    elif a[0] == 'roundtrip':
        sys.exit(1 if roundtrip(a[1], a[2:]) else 0)
