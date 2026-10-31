r"""Repair Markdown files damaged by an escaping slip (found 2026-10-31 in PROJECT_MAP.md and CHANGELOG.md since BATCH-234):
every line prefixed with a backtick, and Windows path escapes turned into control characters (tools\build -> backspace +
"uild", tools\font -> form feed + "ont", out\release -> carriage return + "elease", which a text-mode read turns into a line
break). Fixes what is unambiguous and lists the rest by line number for a manual fix. Idempotent; run before refresh.bat.
Usage: python -I tools\repair_docs.py [--check] [file ...]   (default PROJECT_MAP.md CHANGELOG.md; --check writes nothing)"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESC = {'\x08': '\\b', '\x0c': '\\f', '\x0b': '\\v', '\x07': '\\a'}   # control char -> the escape it came from
CTRL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def repair(text):
    """-> (fixed text, [(line no, reason)] left for a manual fix)"""
    text = re.sub(r'\r(?!\n)', r'\\r', text)                         # lone CR (out\release) back to the escape
    lines = text.split('\n')
    body = [l for l in lines if l.strip()]
    if len(body) >= 10 and sum(l.startswith('`') for l in body) * 2 > len(body):
        lines = [l[1:] if l.startswith('`') else l for l in lines]
    lines = [''.join(ESC.get(c, c) for c in l) for l in lines]
    left = [(n, 'control character %r' % CTRL.search(l).group()) for n, l in enumerate(lines, 1) if CTRL.search(l)]
    fence = False
    for n, l in enumerate(lines, 1):
        if l.startswith('```'): fence = not fence; continue
        if not fence and l.count('`') % 2 and not l.startswith(('|', '#')):
            left.append((n, 'odd number of backticks (line split by a lost \\r or \\f? join it with the next line)'))
    return '\n'.join(lines), left


if __name__ == '__main__':
    check = '--check' in sys.argv
    files = [a for a in sys.argv[1:] if a != '--check'] or ['PROJECT_MAP.md', 'CHANGELOG.md']
    for f in files:
        p = os.path.join(ROOT, f)
        old = open(p, encoding='utf-8', newline='').read()
        new, left = repair(old)
        if new != old and not check: open(p, 'w', encoding='utf-8', newline='').write(new)
        print(f'{f}: {"changed" if new != old else "unchanged"}{" (check only)" if check and new != old else ""}, {len(left)} line(s) to check')
        for n, why in left: print(f'  line {n}: {why}')
