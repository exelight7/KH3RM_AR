r"""TRANS-3: ASCII ',' used as Arabic punctuation -> '،' in translated AR rows. Usage: comma_fix.py [--apply]
Skipped: inside <tags>, {args}, plural keyword separators (,other=), digit,digit, and commas after Latin letters/digits (Latin run)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
sys.stdout.reconfigure(encoding='utf-8')
PROT = re.compile(r'<[^<>]*>|\{\d+\}|,(?:zero|one|two|few|many|other)=')
AR = re.compile(r'[؀-ۿﭐ-﻿]')

def fix(s):
    out, pos, n = [], 0, 0
    spans = [(m.start(), m.end()) for m in PROT.finditer(s)]
    def prot(i): return any(a <= i < b for a, b in spans)
    res = list(s)
    for i, ch in enumerate(s):
        if ch != ',' or prot(i): continue
        prev = s[i-1] if i else ''
        nxt = s[i+1] if i+1 < len(s) else ''
        if prev.isdigit() and nxt.isdigit(): continue
        # previous visible char (skip spaces/tags) must be Arabic
        j = i - 1
        while j >= 0 and (s[j] == ' ' or s[j] == '>'):
            j = s.rfind('<', 0, j) - 1 if s[j] == '>' else j - 1
        pv = s[j] if j >= 0 else ''
        k = i + 1
        while k < len(s) and (s[k] == ' ' or s[k] == '<'):
            k = s.find('>', k) + 1 if s[k] == '<' else k + 1
        nv = s[k] if k < len(s) else ''
        if not (AR.match(pv) or (pv in ')}' or pv.isascii() and pv.isalpha()) and AR.match(nv)): continue
        res[i] = '،'
    t = ''.join(res)
    t = re.sub(r' +،', '،', t)
    t = re.sub(r'،(?=[^\s<،.\d)])', '، ', t)   # one space after, unless tag/space/end/punct
    return t

if __name__ == '__main__':
    apply = '--apply' in sys.argv
    tot = rows = 0; ex = []
    for cat in CATEGORIES:
        d = os.path.join(ROOT, 'translation', cat)
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn); R = read_tsv(p); ch = False
            for r in R[1:]:
                if r[5] and r[6] != 'todo' and ',' in r[5]:
                    t = fix(r[5])
                    if t != r[5]:
                        rows += 1; tot += r[5].count(',') - t.count(','); ex.append((r[0], r[5], t)); 
                        if apply: r[5] = t; ch = True
            if apply and ch: write_tsv(p, R)
    print('rows changed', rows, 'commas changed', tot)
    for e in ex[:15]: print(e[0], e[1], '=>', e[2])
    left = 0
    for cat in CATEGORIES:
        for fn in os.listdir(os.path.join(ROOT, 'translation', cat)):
            for r in read_tsv(os.path.join(ROOT, 'translation', cat, fn))[1:]:
                if r[5] and r[6] != 'todo' and ',' in r[5]: left += 1
    print('rows still containing ASCII comma:', left)
    if '--left' in sys.argv:
        for cat in CATEGORIES:
            for fn in os.listdir(os.path.join(ROOT, 'translation', cat)):
                for r in read_tsv(os.path.join(ROOT, 'translation', cat, fn))[1:]:
                    if r[5] and r[6] != 'todo' and ',' in r[5]: print('LEFT', r[0], r[5][:100].encode('unicode_escape').decode() if False else r[5][:100])
