"""Shared helpers for the translation TSVs (ORG-1). Plain TSV, no quoting; text is already escaped like en_source.tsv."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'translation', 'en_source.tsv')
SRC_COLS = ['namespace', 'key', 'source_hash', 'text', 'category', 'file']
COLS = ['id', 'namespace', 'key', 'source_hash', 'EN', 'AR', 'status', 'note']
STATUSES = ['todo', 'translated', 'reviewed', 'verified']
PREFIX = 'KINGDOM HEARTS III/Content/Localization/Game/en/'
CATEGORIES = ['dialogue', 'items_abilities', 'journal', 'menus_ui', 'remind', 'subtitles_cutscenes', 'tutorials']


def read_tsv(path):
    with open(path, encoding='utf-8', newline='') as f:
        lines = f.read().split('\n')
    assert lines[-1] == '', path
    return [l.split('\t') for l in lines[:-1]]


def write_tsv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write('\t'.join(r) + '\n')


def load_translation():
    r"""-> list of dicts (COLS + category + stem), all translation\<cat>\*.tsv, sorted by id (= game order)."""
    out = []
    base = os.path.join(ROOT, 'translation')
    for cat in sorted(os.listdir(base)):
        d = os.path.join(base, cat)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.tsv'):
                continue
            rows = read_tsv(os.path.join(d, fn))
            assert rows[0] == COLS, (cat, fn, rows[0])
            for r in rows[1:]:
                assert len(r) == len(COLS), (cat, fn, r[:3])
                out.append(dict(zip(COLS, r), category=cat, stem=fn[:-4]))
    out.sort(key=lambda r: r['id'])
    return out


TAG = re.compile(r'<[^<>]*>')
ARG = re.compile(r'\{\d+\}')

GLOSSARY = os.path.join(ROOT, 'translation', 'glossary.tsv')
GCOLS = ['en', 'ar', 'type', 'source', 'status', 'kh3_count', 'example_ids', 'note']


def load_glossary():
    """-> list of dicts (GCOLS) from translation\\glossary.tsv ([] if missing)"""
    if not os.path.exists(GLOSSARY):
        return []
    rows = read_tsv(GLOSSARY)
    assert rows[0] == GCOLS, rows[0]
    return [dict(zip(GCOLS, r)) for r in rows[1:]]


def norm_en(s):
    """apostrophes/nbsp unified so KH2 spellings (´) match KH3 text (')"""
    return s.replace('´', "'").replace('’', "'").replace('\xa0', ' ')


def term_re(term, flags=re.I):
    """whole-word match for an EN term (term may start/end with punctuation)"""
    return re.compile(r'(?<!\w)' + re.escape(norm_en(term)) + r'(?!\w)', flags)
