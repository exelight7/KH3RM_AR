r"""Merge translation\<category>\*.tsv back into one pipeline TSV (namespace,key,source_hash,text,category,file) for `locres.py tsv-import`.
  merge_translation.py --check          merged EN must be byte-identical to translation\en_source.tsv (exit 1 otherwise)
  merge_translation.py -o out.tsv       text = AR where status != todo and AR is non-empty, else EN
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *


def merge(use_ar):
    lines = ['\t'.join(SRC_COLS)]
    for r in load_translation():
        text = r['AR'] if use_ar and r['status'] != 'todo' and r['AR'] else r['EN']
        lines.append('\t'.join([r['namespace'], r['key'], r['source_hash'], text, r['category'], PREFIX + r['stem'] + '.locres']))
    return ('\n'.join(lines) + '\n').encode('utf-8')


if __name__ == '__main__':
    if '--check' in sys.argv:
        ok = merge(False) == open(SRC, 'rb').read()
        print('merge check:', 'PASS (merged EN == en_source.tsv, byte-identical)' if ok else 'FAIL')
        sys.exit(0 if ok else 1)
    out = sys.argv[sys.argv.index('-o') + 1] if '-o' in sys.argv else os.path.join(ROOT, 'out', 'builds', 'ORG-1', 'merged.tsv')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'wb').write(merge(True))
    print('wrote', out)
