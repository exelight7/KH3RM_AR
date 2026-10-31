import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'translation', 'images_strings.tsv')):
    sys.exit(print('%s SKIP: private translation workspace not present (public clone)' % os.path.basename(__file__)))
import find_text as ft, shaper
rows = ft.all_rows()
r = next(x for x in rows if x['category'] == 'menus_ui' and len(x['AR']) > 3 and x['AR'].startswith('ال') and '<' not in x['AR'])
core = r['AR'][2:]
assert r in ft.find(r['AR'], rows) and r in ft.find(core, rows)           # with / without ال
assert r in ft.find('َ' + r['AR'] + 'ـ', rows)                  # harakat / tatweel ignored
assert r in ft.find(shaper.shape(r['AR']), rows), 'pre-shaped input'      # screenshot text
assert r in ft.find(r['EN'].upper(), rows) and ft.find('zzqq no such text', rows) == []
assert any(x['category'] == 'images' for x in ft.find('time gauge', rows))
a = ft.around(r, 2, rows)
assert r in a and len(a) <= 5
print('test_find_text PASS')
