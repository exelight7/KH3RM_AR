r"""BUILD-2 (FULL-1): the full build of tools\build_build1.py (every translated row, line breaking) with the FULL-1
field table (help-text fields: max_lines 2, rows over it reflowed) -> out\builds\BUILD-2\pakchunk99-arabic_P.pak.
Usage (from the project root): python -I tools/build_build2.py   |   --installed (after SWAP_TO_BUILD2.bat)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_build1 as b

b.BUILD, b.OUT = 'BUILD-2', 'out/builds/BUILD-2'
b.PAK = os.path.join(b.OUT, 'pakchunk99-arabic_P.pak')

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    b.installed() if sys.argv[1:] == ['--installed'] else b.main()
