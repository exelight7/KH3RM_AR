"""Read-only: for each Scaleform SwfMovie .uexp, list fonts it imports (ImportAssets/ImportAssets2, tags 57/71)
and fonts it defines, plus EditText count. Usage: python -I gfx_imports.py <dir>"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir
from gfx_fonts import movie, tags


def cstr(t, p):
    z = t.index(b'\0', p)
    return t[p:z].decode('utf-8', 'replace'), z + 1


def scan(path):
    sig, ver, size, at, body = movie(open(path, 'rb').read())
    imports, defs, edit = [], [], 0
    for code, t in tags(body):
        if code in (57, 71):
            url, p = cstr(t, 0)
            if code == 71:
                p += 2
            n = struct.unpack_from('<H', t, p)[0]
            p += 2
            for _ in range(n):
                p += 2
                name, p = cstr(t, p)
                imports.append(f'{url}:{name}')
        elif code in (48, 75, 1005):
            defs.append(code)
        elif code == 37:
            edit += 1
    return imports, defs, edit


def main():
    for dp, _, fs in os.walk(sys.argv[1]):
        for f in sorted(fs):
            if f.endswith('.uexp'):
                p = os.path.join(dp, f)
                try:
                    imp, defs, edit = scan(p)
                except ValueError:
                    continue  # not a movie (texture etc.)
                rel = p.replace(os.sep, '/').split('/Scaleform/')[-1]
                print(f'{rel}\tedittext={edit}\tfontdefs={defs}\timports={sorted(set(imp))}')


if __name__ == '__main__':
    main()
