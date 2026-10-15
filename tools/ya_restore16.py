r"""BUILD-16 TASK 1: the BUILD-15 TresFont with ONLY the 6 ya glyphs (U+064A, U+FEF1, U+FEF2 in $jimakuNE and $sougei)
restored from the BUILD-14 TresFont (out/fonts_gpt/TresFont, the BUILD-14 pin). Owner option B: dots back in their original
Plex position, no moving, no enlarging. -> out\builds\BUILD-16\TresFont\TresFont.{uasset,uexp}
Usage (from the project root): python -I tools/ya_restore16.py"""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import font_swap_adapter, font_swap_adapter15, tresfont

B14 = 'out/fonts_gpt/TresFont/TresFont.uasset'
B15 = 'out/builds/BUILD-15/TresFont/TresFont.uasset'
ORIG = 'extracted/assets/KINGDOM HEARTS III/Content/UI/Scaleform/91_font/TresFont.uasset'
OUT = 'out/builds/BUILD-16/TresFont'
YA = (0x064A, 0xFEF1, 0xFEF2)
PLEX = (1, 3)  # $jimakuNE, $sougei
sha = lambda d: hashlib.sha256(d).hexdigest()
glyphs = lambda f: {c: (a, f['shapes'][s]) for c, a, s in f['glyphs']}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(OUT, exist_ok=True)
    for src, pins in ((B14, font_swap_adapter.PINNED), (B15, font_swap_adapter15.PINNED15)):
        for n in pins:
            assert sha(open(os.path.join(os.path.dirname(src), n), 'rb').read()) == pins[n], (src, n)
    a, m, tags = tresfont.load(B15)
    _, _, t14 = tresfont.load(B14)
    old = {f['id']: glyphs(f) for f in t14.values()}
    fonts = {f['id']: f for f in tags.values()}
    n = 0
    for fid in PLEX:
        f = fonts[fid]
        for c, adv, s in f['glyphs']:
            if c in YA:
                assert old[fid][c][0] == adv, 'advance'
                f['shapes'][s] = old[fid][c][1]
                n += 1
    assert n == 6, n
    ua, ue = tresfont.save(a, m, tags)
    for name, data in (('TresFont.uasset', ua), ('TresFont.uexp', ue)):
        open(os.path.join(OUT, name), 'wb').write(data)
        print(f'{OUT}/{name}: {len(data)} B sha256 {sha(data)}')
    # ---- verify the saved copy, re-parsed
    _, _, t16 = tresfont.load(os.path.join(OUT, 'TresFont.uasset'))
    _, _, t15 = tresfont.load(B15)
    _, _, t0 = tresfont.load(ORIG)
    g16, g15, g0 = ({f['id']: glyphs(f) for f in t.values()} for t in (t16, t15, t0))
    diff15 = sorted((fid, c) for fid in g16 for c in g16[fid] if g16[fid][c] != g15[fid][c])
    diff14 = sorted((fid, c) for fid in g16 for c in g16[fid] if g16[fid][c] != old[fid][c])
    print(f'glyphs differing from BUILD-15: {[(f, hex(c)) for f, c in diff15]}')
    print(f'glyphs differing from BUILD-14: {diff14}')
    assert diff15 == sorted((f, c) for f in PLEX for c in YA) and not diff14
    for fid in g16:
        assert all(g16[fid][c] == v for c, v in g0[fid].items()), f'{fid}: original game glyph changed'
    print('counts per class (glyphs):', {fid: len(g) for fid, g in g16.items()})
    print('byte-identical to BUILD-14 pair:', all(open(os.path.join(OUT, n), 'rb').read() ==
          open(os.path.join(os.path.dirname(B14), n), 'rb').read() for n in ('TresFont.uasset', 'TresFont.uexp')))


if __name__ == '__main__':
    main()
