"""unit tests for cloud_secret_check.py"""
import os, subprocess, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloud_secret_check as c

KEY = 'k' * 40


def put(d, rel, data=b'x'):
    p = os.path.join(d, *rel.split('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'wb').write(data)


class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def test_clean(self):
        put(self.d, 'translation/dialogue/a.tsv')
        put(self.d, 'tools/validate.py')
        self.assertEqual(c.scan(self.d), [])

    def test_forbidden_ext_and_prefix(self):
        for rel in ['a.pak', 'x/Font.TTF', 'a/b.uasset', 'a.uexp', 'a.ubulk', 'a.otf', 'a.usm', 'x/en.locres', 'tools/gh.exe',
                    'extracted/text.tsv', 'out/builds/B/x.txt', 'tools/KEY_SOURCE.txt', 'tools/repak-0.2.3/r.txt',
                    'tools/gh-2.102.0/x.txt', 'tools/installer/bin/x.txt', 'tools/installer/obj/x.txt', 'screenshots/a.txt',
                    'review/gpt/a.md', '.codex/a', '.serena/a', 'public_repo/a.md']:
            put(self.d, rel)
        bad = c.scan(self.d)
        self.assertEqual(len(bad), 21, bad)

    def test_list(self):
        self.assertEqual(c.scan_list(['a/b.md', 'extracted/x', 'tools/KEY_SOURCE.txt', '']), ['extracted/x forbidden path', 'tools/KEY_SOURCE.txt forbidden path'])

    def test_key_and_size(self):
        put(self.d, 'docs/a.md', b'text ' + KEY.encode() + b' text')
        put(self.d, 'docs/b.md', b'ok')
        self.assertEqual(c.scan(self.d, [KEY]), ['docs/a.md AES key'])
        big = os.path.join(self.d, 'big.txt')
        with open(big, 'wb') as f:
            f.truncate(c.MAX + 1)
        self.assertIn('big.txt over 25 MB', c.scan(self.d))

    def test_key_values_not_printed(self):
        root = tempfile.mkdtemp()
        put(root, 'tools/KEY_SOURCE.txt', f'key_ascii={KEY}\n'.encode())
        self.assertEqual(c.key_values(root)[0], KEY)
        put(self.d, 'a.md', KEY.encode())
        out = '\n'.join(c.run(self.d, root))
        self.assertIn('AES key', out)
        self.assertNotIn(KEY, out)

    def test_history(self):
        git = lambda r, *a: subprocess.run(['git', '-C', r, '-c', 'user.name=t', '-c', 'user.email=t@t', *a], check=True, capture_output=True)
        priv, cloud = tempfile.mkdtemp(), tempfile.mkdtemp()
        for r in (priv, cloud):
            git(r, 'init', '-q')
        put(priv, 'a.txt')
        git(priv, 'add', '.'); git(priv, 'commit', '-qm', 'one')
        put(cloud, 'b.txt')
        git(cloud, 'add', '.'); git(cloud, 'commit', '-qm', 'one')
        self.assertEqual(c.history(cloud, priv), [])
        git(cloud, 'pull', '-q', priv, 'HEAD', '--allow-unrelated-histories', '--no-rebase', '--no-edit')
        self.assertEqual(c.history(cloud, priv), ['.git shares history with the private project'])


unittest.main()
