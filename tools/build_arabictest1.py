"""ARABIC-TEST-1 build: NEW GAME (kh3_menu.title/menu_0002) in 3 variants + TresFont with Segoe UI Arabic in $sougei.
Writes out/builds/ARABIC-TEST-1/{A,B,C}/pakroot/ (kh3_menu.locres + TresFont.uasset/.uexp); packing is done by repak.
Usage (from the project root): python -I tools/build_arabictest1.py"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import locres, shaper, tresfont

SRC = 'extracted/locres'
MENU = 'KINGDOM HEARTS III/Content/Localization/Game/en/kh3_menu.locres'
FONT = 'KINGDOM HEARTS III/Content/UI/Scaleform/91_font/TresFont'
OUT = 'out/builds/ARABIC-TEST-1'
TEXT = 'لعبة جديدة'  # "New Game"
SEGOE = 'C:/Windows/Fonts/segoeui.ttf'
K, DY = 256 / 2048, -5  # Segoe em -> 256 units; baseline matches $sougei (Latin glyph bottoms at y = -5)
CODES = ([0x060C, 0x061B, 0x061F] + list(range(0x0621, 0x063B)) + list(range(0x0641, 0x064B))
         + list(range(0x0660, 0x066A)) + list(range(0xFE70, 0xFEFD)))
VARIANTS = {'A': shaper.shape(TEXT), 'B': TEXT, 'C': shaper.shape(TEXT, reverse=False)}


def font_bytes():
    a, m, fonts = tresfont.load(os.path.join('extracted/assets', FONT + '.uasset'))
    sougei = next(f for f in fonts.values() if f['id'] == 3)
    new = tresfont.ttf_glyphs(SEGOE, CODES, K, DY)
    tresfont.add_glyphs(sougei, new)
    return tresfont.save(a, m, fonts), new


def main():
    rows = [r for r in csv.DictReader(open('translation/en_source.tsv', encoding='utf-8', newline=''),
                                      delimiter='\t', quoting=csv.QUOTE_NONE) if r['file'] == MENU]
    (ua, ue), new = font_bytes()
    for name, text in VARIANTS.items():
        for r in rows:
            if (r['namespace'], r['key']) == ('kh3_menu.title', 'menu_0002'):
                r['text'] = text
        root = os.path.join(OUT, name, 'pakroot')
        for rel, data in ((MENU, locres.tsv_import(rows, open(os.path.join(SRC, MENU), 'rb').read())),
                          (FONT + '.uasset', ua), (FONT + '.uexp', ue)):
            os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
            open(os.path.join(root, rel), 'wb').write(data)
        print(name, shaper.cps(text))
    print('glyphs added to $sougei:', len(new), 'missing in Segoe UI:', [hex(c) for c in CODES if c not in new])


if __name__ == '__main__':
    main()
