r"""One-time/idempotent: split translation\en_source.tsv into translation\<category>\<file>.tsv.
Never overwrites a file that already holds AR/status work: refuses if the target exists (use --force-todo only on a fresh tree)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

rows = read_tsv(SRC)
assert rows[0] == SRC_COLS
groups = {}
for n, (ns, key, h, text, cat, f) in enumerate(rows[1:], 1):
    assert f.startswith(PREFIX) and f.endswith('.locres'), f
    groups.setdefault((cat, f[len(PREFIX):-7]), []).append([f'{n:05d}', ns, key, h, text, '', 'todo', ''])
for (cat, stem), rs in groups.items():
    p = os.path.join(ROOT, 'translation', cat, stem + '.tsv')
    if os.path.exists(p):
        sys.exit(f'exists, not overwriting: {p}')
for (cat, stem), rs in groups.items():
    write_tsv(os.path.join(ROOT, 'translation', cat, stem + '.tsv'), [COLS] + rs)
print(f'{len(groups)} files, {sum(map(len, groups.values()))} rows')
