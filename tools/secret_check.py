r"""Fail if the AES key or a game binary is tracked by git (or staged). Checks the index, not the working tree."""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAD_EXT = ('.pak', '.uasset', '.uexp', '.ubulk', '.ttf', '.otf', '.usm', '.locres', '.exe', '.dll', '.bin', '.umap')
BAD_PREFIX = ('extracted/', 'out/builds/', 'out/old/', 'tools/KEY_SOURCE.txt', 'tools/repak-')
git = lambda *a: subprocess.run(['git', '-C', ROOT, *a], capture_output=True, check=True).stdout


def key_values():
    p = os.path.join(ROOT, 'tools', 'KEY_SOURCE.txt')
    if not os.path.exists(p):
        return []
    vals = re.findall(r'^key_\w+=\s*(\S+)', open(p, encoding='utf-8', errors='ignore').read(), re.M)
    return list(dict.fromkeys(vals + [v[:32] for v in vals if len(v) > 32]))


if __name__ == '__main__':
    files = git('ls-files', '-z').decode('utf-8').split('\0')[:-1]
    bad = [f for f in files if f.lower().endswith(BAD_EXT) or f.startswith(BAD_PREFIX)]
    for k in key_values():
        for f in files:
            p = os.path.join(ROOT, f)
            if os.path.isfile(p) and k.encode() in open(p, 'rb').read():
                bad.append(f'{f} (contains the AES key)')
    print(f'secret_check: {len(files)} tracked files,', 'FAIL' if bad else 'PASS')
    for b in bad:
        print('  BAD:', b)
    sys.exit(1 if bad else 0)
