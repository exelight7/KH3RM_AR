import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import public_check as pc

def put(root, rel, data=b'x'):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'wb').write(data)

KEY = ['SECRETKEY']
CASES = [
    ('a.uasset', b'x', 'forbidden path'), ('x.ttf', b'x', 'forbidden path'), ('out/builds/a.txt', b'x', 'forbidden path'),
    ('review/gpt/a.md', b'x', 'forbidden path'), ('review/a.tsv', b'x', 'review file'),
    ('tools/KEY_SOURCE.txt', b'x', 'forbidden path'), ('notes.md', b'has SECRETKEY here', 'AES key'),
    ('translation/ar/a/c.tsv', b'id\tEN\tAR\n', 'EN column'),
    ('translation/ar/a/d.tsv', b'id\tAR\n1\tThe quick brown fox jumps over\n', 'Latin sentence'),
    ('docs/a.md', b'path tools\x08uild_build1.py\n', 'damaged text'), ('docs/b.md', b'`# T\n' + b'`line\n' * 12, 'damaged text'),
]
with tempfile.TemporaryDirectory() as d:
    put(d, 'README.md')
    put(d, 'translation/ar/a/b.tsv', 'id\tAR\n1\tمرحبا Sora\n'.encode())
    put(d, 'review/RULES.md')
    put(d, 'tools/x.py', b'print(1)')
    assert pc.scan(d, KEY) == [], 'clean tree must pass'
    for rel, data, why in CASES:
        put(d, rel, data)
        r = pc.scan(d, KEY)
        assert any(rel in x and why in x for x in r), (rel, r)
        os.remove(os.path.join(d, rel))
    pc.MAX = 0
    assert any('over 25 MB' in x for x in pc.scan(d))
print('test_public_check PASS')
