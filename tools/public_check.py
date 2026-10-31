r"""Check public_repo\ before every publish. Fails on: forbidden path/extension, EN column or a Latin sentence of 6+ words
in a translation file, a damaged text file (control characters, or most lines prefixed with a backtick), the AES key (read from tools\KEY_SOURCE.txt in memory, never printed), files over 25 MB, or any
commit of the private repo in public_repo's history. Usage: python -I tools\public_check.py [public_dir]"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import secret_check
ROOT = secret_check.ROOT
BAD_EXT = secret_check.BAD_EXT + ('.ubulk', '.umap', '.pak')
BAD_PREFIX = ('extracted/', 'out/', 'tools/repak-', 'tools/gh-', 'tools/installer/bin/', 'tools/installer/obj/', 'tools/KEY_SOURCE.txt', 'review/gpt/', 'review/script/', 'review/md/',
              'screenshots/', '.codex/', '.serena/', 'state/LAST_REPORT.md', 'public_repo/')
MAX = 25 * 1024 * 1024
TEXT_EXT = ('.md', '.py', '.tsv', '.bat', '.cs', '.axaml', '.xaml', '.csproj', '.yml', '.json', '.txt', '.svg', '.html')
CTRL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')

def damaged(data):
    """control characters (lost escapes such as tools\\b... -> backspace) or most lines prefixed with a backtick"""
    t = data.decode('utf-8', 'replace')
    lines = [l for l in t.split('\n') if l.strip()]
    return bool(CTRL.search(t)) or (len(lines) >= 10 and sum(l.startswith('`') for l in lines) * 2 > len(lines))

LATIN = re.compile(r"(?:[A-Za-z][A-Za-z'.,!?-]*\s+){5}[A-Za-z][A-Za-z'.,!?-]*")

def scan(pub, keys=()):
    bad = []
    for d, ds, fs in os.walk(pub):
        ds[:] = [x for x in ds if x != '.git']
        for f in fs:
            p = os.path.join(d, f); r = os.path.relpath(p, pub).replace(os.sep, '/')
            low = r.lower()
            if low.endswith(BAD_EXT) or low.startswith(tuple(x.lower() for x in BAD_PREFIX)): bad.append(f'{r} forbidden path')
            if r.startswith('review/') and r != 'review/RULES.md': bad.append(f'{r} review file')
            if os.path.getsize(p) > MAX: bad.append(f'{r} over 25 MB')
            data = open(p, 'rb').read()
            if any(k.encode() in data for k in keys): bad.append(f'{r} AES key')
            if low.endswith(TEXT_EXT) and damaged(data): bad.append(f'{r} damaged text')
            if r.startswith('translation/ar/') and low.endswith('.tsv'):
                lines = data.decode('utf-8').splitlines()
                if 'EN' in lines[0].split('\t'): bad.append(f'{r} EN column')
                i = lines[0].split('	').index('AR') if 'AR' in lines[0].split('	') else 0
                if any(LATIN.search((l.split('	') + [''] * (i + 1))[i]) for l in lines[1:]): bad.append(f'{r} Latin sentence')
    return bad

def history(pub):
    git = lambda d, *a: subprocess.run(['git', '-C', d, *a], capture_output=True, text=True).stdout.split()
    if not os.path.isdir(os.path.join(pub, '.git')): return []
    shared = set(git(ROOT, 'rev-list', '--all')) & set(git(pub, 'rev-list', '--all'))
    return ['.git shares history with the private repo'] if shared else []

if __name__ == '__main__':
    pub = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'public_repo')
    bad = scan(pub, secret_check.key_values()) + history(pub)
    print('\n'.join('BAD: ' + b for b in bad) or 'public_check PASS')
    sys.exit(1 if bad else 0)
