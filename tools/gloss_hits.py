r"""TRANS-2 helper: glossary terms (approved, not type menu unless exact row match) that occur in a dump file.
Usage: python -I tools\gloss_hits.py dumpfile > out.txt"""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from tsvlib import *
sys.stdout.reconfigure(encoding='utf-8')
text = '\n'.join(l for l in open(sys.argv[1], encoding='utf-8') if not l.startswith('#'))
text = norm_en(text)
seen = set()
for d in load_glossary():
    if d['status'] != 'approved':
        continue
    en = norm_en(d['en'])
    if en in seen or len(en) < 2:
        continue
    if term_re(en, 0).search(text):
        seen.add(en)
        print(f"{d['en']} = {d['ar']}  [{d['type']}]")
