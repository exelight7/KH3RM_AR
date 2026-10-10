r"""One-time (TRANS-1 part 1): apply supervisor decisions on the pending glossary conflicts. Do not re-run."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

g = load_glossary()
DROP = {('100 Acre Wood', 'الهبوط في غابة المئة فدان'), ('Jump to World Map?', 'الانتقال إلى خريطة العالم؟'),
        ('Postern', 'الباب الخلفي'), ('Whirli-Goof', 'دور غوفي'), ('Release', 'تحرير'), ('Hang On', 'لا تفلت'),
        ('Jump', 'القفز'), ('Auto', 'آلي')}
SET_AR = {('Postern', 'الباب الخلفي'): None}  # dropped; lowercase 'postern' row already البوابة الخلفية
APPROVE_EN = {'100 Acre Wood', 'Abilities', 'Jump to World Map?', 'postern', 'Master', 'master', 'Whirli-Goof', 'Release',
              'Hang On', 'Jump', 'Question', 'QUESTION', 'Auto', 'Materials', 'Limit', 'Lucky Lucky', 'Full Bloom'}
out, log = [], []
for d in g:
    k = (d['en'], d['ar'])
    if k in DROP:
        log.append(f'dropped {k}')
        continue
    if d['en'] == 'Journal':
        d['ar'] = 'اليوميات'; d['status'] = 'approved'
    elif d['en'] in ('Destiny Islands', 'Destiny Island'):
        d['ar'] = 'جزر المصير'; d['status'] = 'approved'
    elif d['en'] == 'Hollow Bastion':
        d['ar'] = 'حصن هولو'; d['status'] = 'approved'
    elif d['en'] == 'Postern':
        pass
    elif d['en'] in APPROVE_EN and d['status'] == 'pending':
        d['status'] = 'approved'
    elif d['status'] == 'pending' and d['source'] == 'KH2':
        if int(d['kh3_count'] or 0) == 0:
            d['status'] = 'kh2-only'
        else:
            log.append(f'STILL PENDING (kh3_count>0): {d["en"]} = {d["ar"]} ({d["kh3_count"]})')
            continue
    else:
        out.append(d); continue
    d['note'] = (d['note'] + '; ' if d['note'] else '') + 'supervisor decision TRANS-1'
    out.append(d)
# Postern (capital) -> same Arabic as postern
for d in out:
    if d['en'] == 'Postern':
        d['ar'] = 'البوابة الخلفية'; d['status'] = 'approved'; d['note'] += '; supervisor decision TRANS-1'
write_tsv(GLOSSARY, [GCOLS] + [[d[c] for c in GCOLS] for d in out])
print('\n'.join(log))
