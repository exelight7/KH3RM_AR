r"""Validate translated rows against EN. Writes review\VALIDATION.md; flags are reused by make_review.py.
ERR codes: TAGS (tag/arg/icon sequence differs) BR (<br> count) LATIN (Latin/Greek/Roman token in AR not in the row's EN) HARAKAT TATWEEL BRACKETS EMPTY
  QMARK (Arabic question mark U+061F; ASCII ? until a screenshot proves it, REVIEW-1)
WARN codes: ARGORDER (same tags, different order) DSPACE LEAD TRAIL (only if EN lacks them) RATIO
  HASHTAG (hashtag token in Latin letters while EN is a hashtag row)
  TYPO (a pattern of translation	ypo_patterns.tsv, whole-word regex, matches AR)
  GLOSS (an approved glossary term is in EN but its approved Arabic is missing from AR; see build_gloss)
Rows with empty AR and status todo are skipped."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

ERR = {'TAGS', 'BR', 'LATIN', 'HARAKAT', 'TATWEEL', 'BRACKETS', 'EMPTY', 'QMARK'}
HARAKAT = re.compile('[ً-ٰٟ]')
PLURAL_KW = re.compile(r'\b(zero|one|two|few|many|other)=')
PAIRS = {')': '(', ']': '[', '}': '{', '»': '«', '」': '「'}
WORD = re.compile(r'\w+')
TYPO_FILE = os.path.join(ROOT, 'translation', 'typo_patterns.tsv')
AR_LETTER = 'ء-ي'


def load_typos(path=TYPO_FILE):
    """-> [(compiled whole-word regex, correct, note)]; pattern column is a regex, wrapped so it never matches inside a longer Arabic word"""
    if not os.path.exists(path):
        return []
    return [(re.compile(f'(?<![{AR_LETTER}])(?:{r[0]})(?![{AR_LETTER}])'), r[1], r[2]) for r in read_tsv(path)[1:]]


TYPOS = load_typos()


# LATIN policy (TRANS-2): the game font renders every Latin letter, digit, Roman numeral and Greek letter of the EN text,
# so a Latin/Greek/Roman token in AR is fine iff it also appears verbatim in the EN of the same row.
HASHTAG_LATIN = re.compile(r'￠[^\s<]*[A-Za-z]')  # HASHTAG (TRANS-6): hashtag token left in Latin in a hashtag row
LATIN_TOKEN = re.compile(r'[A-Za-zÀ-ÖØ-öø-ɏ]+|[Ͱ-Ͽ]+|[Ⅰ-ↈ]+')


def latin_tokens(s):
    """tags/args count as word breaks (Re<icon>Mind -> Re, Mind)"""
    return set(LATIN_TOKEN.findall(visible(TAG.sub(' ', s))))


def sorted_tokens(s):
    """tags and {n} args in text order, plus plural markers"""
    return [m.group(0) for m in re.finditer(r'<[^<>]*>|\{\d+\}|\|plural\(', s)]


def visible(s):
    s = TAG.sub('', s)
    s = ARG.sub('', s)
    return PLURAL_KW.sub('', re.sub(r'\|plural\(([^)]*)\)', lambda m: m.group(1), s))


def balanced(s):
    st = []
    for c in s:
        if c in '([{«「':
            st.append(c)
        elif c in PAIRS:
            if not st or st.pop() != PAIRS[c]:
                return False
    return not st


def build_gloss(entries, common=frozenset()):
    """approved non-menu glossary entries -> {first EN word (lower): [(regex, Arabic core)]}.
    EN matches as written or ALL CAPS (so 'will' never matches Will); one-word terms that KH3 EN also uses as
    lowercase words (common = lowercase words of the corpus, e.g. will, even, pain) are skipped as ambiguous.
    Arabic core drops a leading ال so و/ب/ل prefixes and indefinite use still count."""
    out = {}
    for d in entries:
        en = norm_en(d['en'])
        words = WORD.findall(en.lower())
        if d['status'] != 'approved' or d['type'] == 'menu' or not words or (len(words) == 1 and words[0] in common):
            continue
        rx = re.compile(r'(?<!\w)(?:' + re.escape(en) + '|' + re.escape(en.upper()) + r')(?!\w)')
        ar = d['ar']
        out.setdefault(words[0], {}).setdefault(en.lower(), (rx, []))[1].append(ar[2:] if ar.startswith('ال') and len(ar) > 4 else ar)
    return {w: list(v.values()) for w, v in out.items()}


def corpus_lowercase_words(rows):
    return {w for r in rows for w in WORD.findall(norm_en(r['EN'])) if w.islower()}


def check(en, ar, status='translated', gloss=None):
    f = []
    if not ar:
        return ['EMPTY'] if status != 'todo' else []
    te, ta = sorted_tokens(en), sorted_tokens(ar)
    if te != ta:
        f.append('ARGORDER' if sorted(te) == sorted(ta) else 'TAGS')
    if en.lower().count('<br>') != ar.lower().count('<br>'):
        f.append('BR')
    if not latin_tokens(ar) <= latin_tokens(en):
        f.append('LATIN')
    if HARAKAT.search(ar):
        f.append('HARAKAT')
    if 'ـ' in ar:
        f.append('TATWEEL')
    if '  ' in ar and '  ' not in en:
        f.append('DSPACE')
    if ar != ar.lstrip() and en == en.lstrip():
        f.append('LEAD')
    if ar != ar.rstrip() and en == en.rstrip():
        f.append('TRAIL')
    if '؟' in ar:
        f.append('QMARK')
    if '￠' in en and HASHTAG_LATIN.search(ar):
        f.append('HASHTAG')
    if any(rx.search(ar) for rx, _, _ in TYPOS):
        f.append('TYPO')
    if not balanced(visible(ar)):
        f.append('BRACKETS')
    ne, na = len(visible(en).strip()), len(visible(ar).strip())
    if ne >= 12 and not 0.4 <= na / ne <= 1.8:
        f.append('RATIO')
    if gloss:
        n = norm_en(en)
        hits = [(m.span(), any(c in ar for c in cores)) for w in set(WORD.findall(n.lower()))
                for rx, cores in gloss.get(w, ()) for m in [rx.search(n)] if m]
        # a missing short term is excused when a longer term covering it is present (Scrooge inside Scrooge McDuck)
        if any(not ok and not any(o and a <= x and y <= b for (a, b), o in hits) for (x, y), ok in hits):
            f.append('GLOSS')
    return f


def validate_all(rows=None):
    """-> {id: [flags]} for rows that have any flag"""
    rows = rows or load_translation()
    gloss = build_gloss(load_glossary(), corpus_lowercase_words(rows))
    return {r['id']: fl for r in rows
            if (fl := check(r['EN'], r['AR'], r['status'], gloss))}


if __name__ == '__main__':
    rows = load_translation()
    flags = validate_all(rows)
    by = {r['id']: r for r in rows}
    n_checked = sum(1 for r in rows if r['AR'] or r['status'] != 'todo')
    cnt = {}
    for fl in flags.values():
        for c in fl:
            cnt[c] = cnt.get(c, 0) + 1
    L = ['# VALIDATION', '', f'Rows checked: {n_checked} of {len(rows)} (rows with AR or status != todo). Rows with flags: {len(flags)}.', '',
         'ERR = must fix; WARN = look at it. See tools/validate.py for rules.', '']
    L += ['| code | level | count |', '|---|---|---|'] + [f'| {c} | {"ERR" if c in ERR else "WARN"} | {n} |' for c, n in sorted(cnt.items())]
    if not cnt:
        L.append('| (none) | | 0 |')
    L += ['', '## Flagged rows (first 500)', '', '| id | category/file | flags |', '|---|---|---|']
    for i, fl in list(flags.items())[:500]:
        L.append(f'| {i} | {by[i]["category"]}/{by[i]["stem"]} | {" ".join(fl)} |')
    open(os.path.join(ROOT, 'review', 'VALIDATION.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
    print(f'validate: checked={n_checked} flagged={len(flags)} errors={sum(1 for f in flags.values() if ERR & set(f))}')
