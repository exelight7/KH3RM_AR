"""Check cloud_repo/ (or any directory / file list) before every push to the private cloud repo. Fails on: forbidden
path/extension, the AES key (read from tools/KEY_SOURCE.txt in memory only, never printed), files over 25 MB, or any commit of the
private project's history inside the cloud repo's .git.
Usage: python -I tools/cloud_secret_check.py [dir]          (default: cloud_repo next to tools/)
       python -I tools/cloud_secret_check.py --list FILE    (paths one per line, e.g. git ls-tree -r origin/main --name-only)"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD_EXT = ('.pak', '.uasset', '.uexp', '.ubulk', '.ttf', '.otf', '.usm', '.locres', '.exe', '.dll', '.bin', '.umap')
BAD_PREFIX = ('extracted/', 'out/', 'tools/key_source.txt', 'tools/repak-', 'tools/gh-', 'tools/installer/bin/', 'tools/installer/obj/',
              'screenshots/', 'review/gpt/', '.codex/', '.serena/', 'public_repo/', 'cloud_repo/')
MAX = 25 * 1024 * 1024


def key_values(root=ROOT):
    p = os.path.join(root, 'tools', 'KEY_SOURCE.txt')
    if not os.path.exists(p):
        return []
    vals = re.findall(r'^key_\w+=\s*(\S+)', open(p, encoding='utf-8', errors='ignore').read(), re.M)
    return list(dict.fromkeys(vals + [v[:32] for v in vals if len(v) > 32]))


def bad_path(rel):
    low = rel.replace('\\', '/').lower()
    return low.endswith(BAD_EXT) or low.startswith(BAD_PREFIX) or '/.git/' in '/' + low


def scan_list(paths):
    """forbidden path/extension only (no file access): for git ls-tree output"""
    return [f'{p} forbidden path' for p in paths if p and bad_path(p)]


def scan(d, keys=()):
    bad = []
    for dp, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x != '.git']
        for f in fs:
            p = os.path.join(dp, f)
            r = os.path.relpath(p, d).replace(os.sep, '/')
            if bad_path(r):
                bad.append(f'{r} forbidden path')
            if os.path.getsize(p) > MAX:
                bad.append(f'{r} over 25 MB')
            if keys:
                data = open(p, 'rb').read()
                if any(k.encode() in data for k in keys):
                    bad.append(f'{r} AES key')
    return bad


def history(d, private_root=ROOT):
    """commits shared between the cloud repo's .git and the private project's .git"""
    git = lambda r, *a: subprocess.run(['git', '-C', r, *a], capture_output=True, text=True).stdout.split()
    if not os.path.isdir(os.path.join(d, '.git')) or not os.path.isdir(os.path.join(private_root, '.git')):
        return []
    if os.path.abspath(d) == os.path.abspath(private_root):
        return []
    shared = set(git(private_root, 'rev-list', '--all')) & set(git(d, 'rev-list', '--all'))
    return ['.git shares history with the private project'] if shared else []


def run(d, private_root=ROOT):
    return scan(d, key_values(private_root)) + history(d, private_root)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['--list']:
        bad = scan_list(open(a[1], encoding='utf-8').read().split('\n'))
    else:
        d = a[0] if a else os.path.join(ROOT, 'cloud_repo')
        bad = run(d)
    print('\n'.join('BAD: ' + b for b in bad) or 'cloud_secret_check PASS')
    sys.exit(1 if bad else 0)
