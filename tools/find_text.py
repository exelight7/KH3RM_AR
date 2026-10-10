r"""Find translation rows by Arabic (as shown in the game) or English text.
Usage: find_text.py <word or phrase> [--ids] [--around N]
Searches translation\*\*.tsv and translation\images_strings.tsv. Arabic matches with or without a leading ال, ignoring tags,
harakat and tatweel; pre-shaped (presentation-form) Arabic copied from a screenshot is brought back to logical text with
shaper.unshape (both directions tried). --around N prints N rows before/after (game order = id order)."""
import os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
import shaper

MARKS = re.compile('[ً-ْٰـ]')
PRES = re.compile('[ﭐ-﷿ﹰ-﻿]')


def norm(s):
    s = MARKS.sub('', TAG.sub('', s))
    return re.sub(r'\s+', ' ', s).strip().lower()


def candidates(q):
    """query -> set of normalised search strings (logical Arabic guesses for pre-shaped input)"""
    out = {q}
    if PRES.search(q):
        out.add(unicodedata.normalize('NFKC', q))
        for rev in (True, False):
            try:
                out.add(shaper.unshape(q, rev))
            except Exception:
                pass
        out |= {unicodedata.normalize('NFKC', c) for c in list(out)} | {c[::-1] for c in list(out)}
    res = set()
    for c in out:
        c = norm(c)
        if c:
            res.add(c)
            if c.startswith('ال') and len(c) > 3:
                res.add(c[2:])
    return res


def all_rows():
    return load_translation() + [dict(r, namespace='images', key=r['asset'], file='images_strings') for r in load_images_strings()]


def find(q, rows=None):
    rows = rows or all_rows()
    cs = candidates(q)
    return [r for r in rows if any(c in norm(r['AR']) or c in norm(r['EN']) for c in cs)]


def show(r):
    return '\t'.join([r['id'], r['category'], r.get('stem', r.get('file', '')), r.get('key', ''), r['EN'], r['AR'], r['status']])


def around(r, n, rows):
    order = [x for x in rows if x['category'] != 'images']
    i = next((k for k, x in enumerate(order) if x['id'] == r['id']), None)
    return [] if i is None else order[max(0, i - n):i + n + 1]


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    a = sys.argv[1:]
    n = int(a[a.index('--around') + 1]) if '--around' in a else 0
    q = ' '.join(x for i, x in enumerate(a) if not x.startswith('--') and not (i and a[i - 1] == '--around'))
    rows = all_rows()
    hits = find(q, rows)
    if '--ids' in a:
        print('\n'.join(r['id'] for r in hits))
    else:
        print('id\tcategory\tfile\tkey\tEN\tAR\tstatus')
        for r in hits:
            for x in (around(r, n, rows) if n else [r]):
                print(('> ' if n and x is r else '  ' if n else '') + show(x))
    print(f'{len(hits)} match(es)', file=sys.stderr)
