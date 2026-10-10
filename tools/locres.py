"""UE4 .locres reader/writer (legacy v0 and compact v1, as shipped by KH3 / UE 4.17).

Usage:
  python -I locres.py roundtrip <dir>          byte-identical check of every .locres under <dir>
  python -I locres.py export <out.tsv> <file>... -> TSV: file, namespace, key, hash, text (escaped)
  python -I locres.py tsv-export <root> <out.tsv> [<path-substring>]
      -> pipeline TSV: namespace, key, source_hash, text, category, file (file = path relative to <root>, '/')
  python -I locres.py tsv-import <tsv> <src_root> <out_root>
      rebuild every file named in <tsv>; the original under <src_root> is the template (entry/namespace order,
      empty namespaces, UTF-16 flags); namespace/key/source_hash must match it, text comes from the TSV.
Escapes in TSV text: \\ \n \r \t
"""
import csv, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir
from text_counts import category

TSV_COLS = ['namespace', 'key', 'source_hash', 'text', 'category', 'file']

MAGIC = bytes.fromhex('0e147475674a03fc4a15909dc3377f1b')


class Reader:
    def __init__(self, d, p=0):
        self.d, self.p = d, p

    def u8(self):
        self.p += 1
        return self.d[self.p - 1]

    def i32(self):
        self.p += 4
        return struct.unpack_from('<i', self.d, self.p - 4)[0]

    def u32(self):
        self.p += 4
        return struct.unpack_from('<I', self.d, self.p - 4)[0]

    def i64(self):
        self.p += 8
        return struct.unpack_from('<q', self.d, self.p - 8)[0]

    def fstr(self):
        """-> (text, wide) ; wide None means length 0 (empty, no terminator)."""
        n = self.i32()
        if n == 0:
            return '', None
        if n < 0:
            raw = self.d[self.p:self.p - 2 * n]
            self.p -= 2 * n
            assert raw[-2:] == b'\0\0'
            return raw[:-2].decode('utf-16-le', 'surrogatepass'), True
        raw = self.d[self.p:self.p + n]
        self.p += n
        assert raw[-1:] == b'\0'
        return raw[:-1].decode('latin-1'), False


def w_fstr(text, wide):
    if wide is None and text == '':
        return struct.pack('<i', 0)
    if wide is None:
        wide = any(ord(c) > 127 for c in text)
    if wide:
        b = text.encode('utf-16-le', 'surrogatepass') + b'\0\0'
        return struct.pack('<i', -(len(b) // 2)) + b
    b = text.encode('latin-1') + b'\0'
    return struct.pack('<i', len(b)) + b


def read(data):
    """-> dict(version, namespaces=[(ns, ns_wide, [(key, key_wide, hash, text, text_wide)])], strings=[(text, wide)])"""
    r = Reader(data)
    if data[:16] != MAGIC:  # legacy v0: no header, strings inline
        ver = 0
        r.p = 0
    else:
        r.p = 16
        ver = r.u8()
        assert ver == 1, f'locres version {ver} not supported'
    strings = None
    if ver == 1:
        off = r.i64()
        save = r.p
        r.p = off
        strings = [r.fstr() for _ in range(r.i32())]
        assert r.p == len(data), 'trailing bytes after string array'
        r.p = save
    namespaces = []
    for _ in range(r.u32()):
        ns, nsw = r.fstr()
        keys = []
        for _ in range(r.u32()):
            key, kw = r.fstr()
            h = r.u32()
            if ver == 1:
                text, tw = strings[r.i32()]
            else:
                text, tw = r.fstr()
            keys.append((key, kw, h, text, tw))
        namespaces.append((ns, nsw, keys))
    if ver == 1:
        assert r.p == off
    else:
        assert r.p == len(data)
    return dict(version=ver, namespaces=namespaces, strings=strings)


def write(loc):
    """Rebuild bytes. v1: string array is rebuilt deduplicated in first-use order."""
    ver = loc['version']
    out = [MAGIC, bytes([1]), b'\0' * 8] if ver == 1 else []
    table, index = [], {}
    out.append(struct.pack('<I', len(loc['namespaces'])))
    for ns, nsw, keys in loc['namespaces']:
        out += [w_fstr(ns, nsw), struct.pack('<I', len(keys))]
        for key, kw, h, text, tw in keys:
            out += [w_fstr(key, kw), struct.pack('<I', h)]
            if ver == 1:
                if (text, tw) not in index:
                    index[(text, tw)] = len(table)
                    table.append((text, tw))
                out.append(struct.pack('<i', index[(text, tw)]))
            else:
                out.append(w_fstr(text, tw))
    if ver == 1:
        head = b''.join(out)
        out[2] = struct.pack('<q', len(head))
        out += [struct.pack('<i', len(table))] + [w_fstr(t, w) for t, w in table]
    return b''.join(out)


def esc(s):
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')


def unesc(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            out.append({'n': '\n', 'r': '\r', 't': '\t', '\\': '\\'}[s[i + 1]])
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def locres_files(root, sub=''):
    return sorted(r for r in (os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/')
                              for dp, _, fs in os.walk(root) for f in fs if f.endswith('.locres')) if sub in r)


def tsv_rows(root, rel):
    loc = read(open(os.path.join(root, rel), 'rb').read())
    name = os.path.basename(rel)
    for ns, _, keys in loc['namespaces']:
        for key, _, h, text, _ in keys:
            cat = category(name, ns, key) if '/Localization/Game/' in '/' + rel else 'engine'
            yield [esc(ns), esc(key), f'{h:08x}', esc(text), cat, rel]


def tsv_import(rows, template):
    """rows: dicts from a pipeline TSV for one file -> new locres bytes built on the template's structure."""
    loc = read(template)
    want = {}
    for r in rows:
        k = (unesc(r['namespace']), unesc(r['key']))
        assert k not in want, f'duplicate row {k}'
        want[k] = (int(r['source_hash'], 16), unesc(r['text']))
    n = 0
    for i, (ns, nsw, keys) in enumerate(loc['namespaces']):
        new = []
        for key, kw, h, text, tw in keys:
            wh, wt = want[(ns, key)]  # KeyError = row missing from TSV
            assert wh == h, f'source_hash changed for {ns}/{key}'
            if wt != text:
                if tw is None:
                    tw = None if wt == '' else any(ord(c) > 127 for c in wt)
                elif not tw and any(ord(c) > 127 for c in wt):
                    tw = True
            new.append((key, kw, h, wt, tw))
            n += 1
        loc['namespaces'][i] = (ns, nsw, new)
    assert n == len(want), f'{len(want) - n} TSV rows not in template'
    return write(loc)


def self_check():
    loc = dict(version=1, strings=None, namespaces=[
        ('', None, [('a', False, 1, 'Hi\n{0}', False), ('b', False, 2, 'Hi\n{0}', False)]),
        ('ns', False, [('c', False, 3, 'مرحبا', None), ('d', False, 4, '', None)])])
    again = read(write(loc))
    assert [k[3] for _, _, ks in again['namespaces'] for k in ks] == ['Hi\n{0}', 'Hi\n{0}', 'مرحبا', '']
    assert len(again['strings']) == 3  # dedup
    assert unesc(esc('a\\b\n\tc')) == 'a\\b\n\tc'
    rows = [dict(namespace='', key='a', source_hash='00000001', text='Hi\\n{0}'),
            dict(namespace='', key='b', source_hash='00000002', text='X'),
            dict(namespace='ns', key='c', source_hash='00000003', text='مرحبا'),
            dict(namespace='ns', key='d', source_hash='00000004', text='')]
    t = write(loc)
    assert tsv_import(rows[::-1], t) != t  # 'b' changed; order still comes from the template
    rows[1]['text'] = 'Hi\\n{0}'
    assert tsv_import(rows[::-1], t) == t


def main():
    self_check()
    cmd = sys.argv[1]
    if cmd == 'roundtrip':
        ok = bad = 0
        for root, _, files in os.walk(sys.argv[2]):
            for f in files:
                if not f.endswith('.locres'):
                    continue
                p = os.path.join(root, f)
                d = open(p, 'rb').read()
                if write(read(d)) == d:
                    ok += 1
                else:
                    bad += 1
                    print('DIFF', p)
        print(f'roundtrip identical={ok} different={bad}')
        sys.exit(1 if bad else 0)
    if cmd == 'export':
        with open(sys.argv[2], 'w', encoding='utf-8', newline='\n') as out:
            out.write('file\tnamespace\tkey\thash\ttext\n')
            for p in sys.argv[3:]:
                loc = read(open(p, 'rb').read())
                name = os.path.basename(p)
                for ns, _, keys in loc['namespaces']:
                    for key, _, h, text, _ in keys:
                        out.write(f'{name}\t{esc(ns)}\t{esc(key)}\t{h:08x}\t{esc(text)}\n')
    if cmd == 'tsv-export':
        root, sub = sys.argv[2], (sys.argv[4] if len(sys.argv) > 4 else '')
        rels = locres_files(root, sub)
        with open(sys.argv[3], 'w', encoding='utf-8', newline='\n') as out:
            out.write('\t'.join(TSV_COLS) + '\n')
            for rel in rels:
                for row in tsv_rows(root, rel):
                    out.write('\t'.join(row) + '\n')
        print(f'tsv-export files={len(rels)}')
    if cmd == 'tsv-import':
        src, dst, sub = sys.argv[3], sys.argv[4], (sys.argv[5] if len(sys.argv) > 5 else '')
        by_file = {}
        with open(sys.argv[2], encoding='utf-8', newline='') as f:
            rd = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
            assert rd.fieldnames == TSV_COLS, rd.fieldnames
            for r in rd:
                by_file.setdefault(r['file'], []).append(r)
        rels = locres_files(src, sub)  # files without entries have no TSV rows but are rebuilt too
        assert set(by_file) <= set(rels), sorted(set(by_file) - set(rels))[:5]
        for rel in rels:
            out = os.path.join(dst, rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'wb').write(tsv_import(by_file.get(rel, []), open(os.path.join(src, rel), 'rb').read()))
        print(f'tsv-import files={len(rels)} with_rows={len(by_file)}')


if __name__ == '__main__':
    main()
