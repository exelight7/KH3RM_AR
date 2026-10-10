import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_feedback as af, find_text as ft
rows = ft.all_rows()
r = next(x for x in rows if x['category'] == 'menus_ui' and x['AR'] and '<' not in x['AR'])
fb = [dict(zip(af.COLS_FB, ['2026-10-10', 'BUILD-7', 'menu', r['id'], 'cut', ''])),
      dict(zip(af.COLS_FB, ['2026-10-10', 'BUILD-7', 'menu', r['AR'], 'wrong', 'x'])),
      dict(zip(af.COLS_FB, ['2026-10-10', 'BUILD-7', 'menu', 'zzqq nothing', 'crash', '']))]
out = af.report(fb, rows)
assert out.count('**' + r['id'] + '**') >= 2 and 'No matching row' in out and 'near' in out
tpl = open(os.path.join(af.ROOT, 'state', 'FEEDBACK_TEMPLATE.tsv'), encoding='utf-8', newline='').read()
with tempfile.TemporaryDirectory() as d:
    p, q = os.path.join(d, 'f.tsv'), os.path.join(d, 'r.md')
    open(p, 'w', encoding='utf-8', newline='\n').write(tpl + 'a\tb\tc\t' + r['id'] + '\tcut\t\n')
    subprocess.run([sys.executable, '-I', af.__file__, p, q], check=True)
    assert os.path.exists(q)
print('test_apply_feedback PASS')
