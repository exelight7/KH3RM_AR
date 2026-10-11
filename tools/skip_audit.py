"""FINISH-TRANS: skip audit (todo rows), suspects, AR==EN / empty-AR check. Read-only on translation TSVs."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
from collections import Counter
rows = load_translation()
allowed = {l.strip().lower() for l in open(os.path.join(ROOT, 'translation', 'allowed_latin.txt'), encoding='utf-8') if l.strip()}
TAG = re.compile(r'<[^>]*>|\{[^}]*\}|%[sd]|\[[^\]]*\]')
URL = re.compile(r'(https?://|www\.)\S+|\S+\.(com|net|org)\b', re.I)
LANGS = {'english', 'deutsch', 'français', 'francais', 'español', 'espanol', 'italiano', 'português', 'portugues',
         'nederlands', 'polski', 'türkçe', 'turkce', 'čeština', 'magyar', 'svenska', 'русский', '日本語', '한국어',
         '中文', '简体中文', '繁體中文', 'العربية', 'ไทย', 'tiếng việt', 'bahasa indonesia', '日本語 (japanese)', 'português (brasil)'}
def cls(en):
    if en == '': return 'blank'
    if not en.strip(): return 'whitespace-only'
    if URL.fullmatch(en.strip()): return 'URL-only'
    if en.strip().lower() in LANGS: return 'language-name-in-own-script'
    rest = TAG.sub('', en)
    if TAG.search(en) and not re.search(r'\w', rest): return 'placeholder-only'
    if not rest.strip(): return 'placeholder-only'
    if not re.search(r'[^\W\d_]', rest):
        return 'digits-only' if re.fullmatch(r'[\d\s.,:/%+\-]*\d[\d\s.,:/%+\-]*', rest) else 'symbols-only'
    return 'other'
def realword(en):
    rest = URL.sub('', TAG.sub('', en))
    return any(len(w) >= 2 for w in re.findall(r'[^\W\d_]+', rest))
done = ('translated', 'reviewed', 'verified')
skip = [r for r in rows if r['status'] not in done]
out = [['id', 'category', 'file', 'key', 'EN', 'class', 'note']]
sus = [['id', 'category', 'file', 'key', 'EN', 'class', 'note']]
cnt = Counter()
for r in skip:
    c = cls(r['EN']); cnt[c] += 1
    line = [r['id'], r['category'], r['stem'], r['key'], r['EN'], c, r['note']]
    out.append(line)
    if c == 'other' or realword(r['EN']): sus.append(line)
write_tsv(os.path.join(ROOT, 'review', 'SKIP_AUDIT.tsv'), out)
write_tsv(os.path.join(ROOT, 'review', 'SKIP_SUSPECTS.tsv'), sus)
same = [['id', 'category', 'file', 'key', 'EN', 'AR', 'status', 'why']]
for r in rows:
    if r['status'] not in done: continue
    en, ar = r['EN'], r['AR']
    if not ar.strip(): same.append([r['id'], r['category'], r['stem'], r['key'], en, ar, r['status'], 'empty AR'])
    elif ar == en and re.search(r'[A-Za-z]', en):
        ws = [w.lower() for w in re.findall(r'[A-Za-z]+', URL.sub('', TAG.sub('', en)))]
        if not ws or all(w in allowed or len(w) <= 2 for w in ws): continue   # Latin policy: acronyms/rank letters/URLs
        same.append([r['id'], r['category'], r['stem'], r['key'], en, ar, r['status'], 'AR == EN'])
write_tsv(os.path.join(ROOT, 'review', 'SAME_AS_EN.tsv'), same)
print(len(skip), dict(cnt)); print('suspects', len(sus) - 1, [x[0] for x in sus[1:41]]); print('same_as_en', len(same) - 1)
for x in sus[1:6]: print(x)
for x in same[1:6]: print(x)
