r"""BUILD-3 (TRANS-4): the BUILD-2 full build plus
- CampMenu (party status) field #335 (instance articleLv, the LV label, right-aligned) widened to the LEFT so مستوى
  fits at 16 pt: xMin 96.1 -> 86.95 px (only those RECT bits change; user decision TRANS-4, LV label stays مستوى);
  base = the newest copy of the movie (pakchunk0_s7-WindowsNoEditor_0_P.pak), extracted read-only to
  out\builds\BUILD-3\ref; uasset shipped unchanged;
- (alignment test cancelled in REVIEW-1: <p align> drops the line; hook b.ALIGN_RIGHT kept, unused)
-> out\builds\BUILD-3\pakchunk99-arabic_P.pak (+ the BUILD-1 verify tables, movie_verify.tsv).
Usage (from the project root): python -I tools/build_build3.py   |   --installed (after SWAP_TO_BUILD3.bat)"""
import os, struct, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build1 as b
from build_test50 import REPAK, sha
from font_census import GAME
from gfx_fonts import movie
from gfx_edittext import edittext
from pak_index import load_key

b.BUILD, b.OUT = 'BUILD-3', 'out/builds/BUILD-3'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
MOVIE = 'KINGDOM HEARTS III/Content/UI/Scaleform/15_campmenu/CampMenu'
SRC_PAK = 'Paks/pakchunk0_s7-WindowsNoEditor_0_P.pak'  # the patch pak: newest copy of CampMenu (base pak has an older one)
FIELD, OLD_XMIN = 335, 1922  # twips (96.1 px)
# right edge 139.1 px - (مستوى 770 font units x 16 pt / 256 + 4 px gutter) = 86.975 px -> 86.95 px (twip floor)
NEW_XMIN = 1739


def tag_offsets(body):
    """(code, start of the tag data in body, length) for the top-level tags"""
    p = (5 + 4 * (body[0] >> 3) + 7) // 8 + 4
    while p + 2 <= len(body):
        h = struct.unpack_from('<H', body, p)[0]
        p += 2
        code, ln = h >> 6, h & 0x3F
        if ln == 0x3F:
            ln = struct.unpack_from('<I', body, p)[0]
            p += 4
        yield code, p, ln
        p += ln
        if code == 0:
            break


def fields(d):
    sig, ver, size, at, body = movie(d)
    return {r['id']: r for r in (edittext(body[p:p + n]) for c, p, n in tag_offsets(body) if c == 37)}


def patch(d):
    """the movie with field FIELD's xMin set to NEW_XMIN (same RECT bit width: file size unchanged)"""
    sig, ver, size, at, body = movie(d)
    assert sig == b'GFX', 'compressed movie: offsets would not map'
    p = next(p for c, p, n in tag_offsets(body) if c == 37 and struct.unpack_from('<H', body, p)[0] == FIELD)
    q = at + 8 + p + 2  # RECT in the file
    nb = d[q] >> 3
    nbytes = (5 + 4 * nb + 7) // 8
    bits = int.from_bytes(d[q:q + nbytes], 'big')
    shift = nbytes * 8 - 5 - nb
    mask = (1 << nb) - 1
    assert (bits >> shift) & mask == OLD_XMIN and NEW_XMIN < 1 << (nb - 1)
    bits = bits & ~(mask << shift) | NEW_XMIN << shift
    return d[:q] + bits.to_bytes(nbytes, 'big') + d[q + nbytes:]


def verify(old, new):
    """re-parse: only field FIELD's bounds differ; -> table rows"""
    assert len(old) == len(new)
    diff = [i for i in range(len(old)) if old[i] != new[i]]
    fo, fn = fields(old), fields(new)
    changed = [i for i in fo if fo[i] != fn[i]]
    assert changed == [FIELD] and {k for k in fo[FIELD] if fo[FIELD][k] != fn[FIELD][k]} == {'bounds'}
    assert fn[FIELD]['bounds'] == [NEW_XMIN / 20] + fo[FIELD]['bounds'][1:]
    so, sn = movie(old), movie(new)
    assert [(c, n) for c, p, n in tag_offsets(so[4])] == [(c, n) for c, p, n in tag_offsets(sn[4])]
    return [['check', 'result'],
            ['size', f'{len(old)} = {len(new)} B'],
            ['bytes differing', f'{len(diff)} (file offsets {diff[0]}..{diff[-1]}, inside the #{FIELD} RECT)'],
            ['edit fields', f'{len(fo)}; changed: {changed}'],
            [f'#{FIELD} bounds', f'{fo[FIELD]["bounds"]} -> {fn[FIELD]["bounds"]}'],
            ['tags', f'{sum(1 for _ in tag_offsets(sn[4]))} top-level tags, same codes and lengths'],
            ['sha256 base', sha(old)], ['sha256 patched', sha(new)]]


def movie_files():
    ref = os.path.join(b.OUT, 'ref')
    if not all(os.path.exists(os.path.join(ref, MOVIE + e)) for e in ('.uasset', '.uexp')):
        os.makedirs(ref, exist_ok=True)
        subprocess.run([REPAK, '-a', '0x' + load_key().hex(), 'unpack', '-q', '-f', '-o', ref,
                        os.path.join(GAME, SRC_PAK.replace('/', os.sep)), '-i', MOVIE + '.uasset', '-i', MOVIE + '.uexp'],
                       check=True, capture_output=True)
    ua, ue = (open(os.path.join(ref, MOVIE + e), 'rb').read() for e in ('.uasset', '.uexp'))
    for e, data in (('.uasset', ua), ('.uexp', ue)):  # the build's verify table compares with extracted\assets
        assert data == open(os.path.join('extracted/assets', MOVIE + e), 'rb').read(), 'extracted\\assets is not the _0_P copy'
    new = patch(ue)
    table = verify(ue, new)
    with open(os.path.join(b.OUT, 'movie_verify.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.writelines('\t'.join(r) + '\n' for r in table)
    return {MOVIE + '.uasset': ua, MOVIE + '.uexp': new}


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1:] == ['--installed']:
        b.installed()
    else:
        os.makedirs(b.OUT, exist_ok=True)
        b.EXTRA = movie_files()
        b.main()
