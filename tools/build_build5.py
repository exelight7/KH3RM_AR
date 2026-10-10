r"""BUILD-5: the BUILD-4 pipeline unchanged (tools\build_build4.py: same movie patches, TresFont, line breaking, no <p align>)
run on the current translation\ TSVs (REVIEW-1 + REVIEW-2 corrections). Only the build name/output dir differ.
-> out\builds\BUILD-5\pakchunk99-arabic_P.pak + verify tables, diff_vs_build4.tsv.
Usage (from the project root): python -I tools/build_build5.py   |   --installed (after SWAP_TO_BUILD5.bat)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build4 as m4

b = m4.b
b.BUILD, b.OUT = 'BUILD-5', 'out/builds/BUILD-5'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')
m4.b.OUT = b.OUT

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1:] == ['--installed']:
        b.installed()
    else:
        os.makedirs(b.OUT, exist_ok=True)
        b.EXTRA = m4.movie_files()
        b.main()
        for d, _, fs in os.walk(os.path.join(b.OUT, 'unpacked')):
            for fn in fs:
                if fn.endswith('.locres'):
                    for ns, _, es in m4.locres.read(open(os.path.join(d, fn), 'rb').read())['namespaces']:
                        assert not any('<p align' in t.lower() for _, _, _, t, _ in es), (fn, ns)
        print('no <p align> in any built locres')
        m4.overflow()
