r"""Fix one translated row in place: python -I tools\setrow.py <id> <AR> [note]  (menus_ui only; TRANS-1 helper)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
d = os.path.join(ROOT, 'translation', 'menus_ui')
for fn in os.listdir(d):
    rows = read_tsv(os.path.join(d, fn))
    for r in rows[1:]:
        if r[0] == sys.argv[1]:
            r[5] = sys.argv[2]
            if len(sys.argv) > 3:
                r[7] = sys.argv[3]
            write_tsv(os.path.join(d, fn), rows)
            print('set', r[0], fn)
