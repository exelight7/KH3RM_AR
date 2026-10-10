import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import COLS, read_tsv, write_tsv
from apply_corrections import apply, HEADER


class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.t = os.path.join(self.d, 'translation', 'c', 'f.tsv')
        write_tsv(self.t, [COLS, ['00001', 'n', 'k', 'h', 'a', 'قديم', 'reviewed', ''], ['00002', 'n', 'k2', 'h', 'b', '', 'todo', '']])
        self.c = os.path.join(self.d, 'review', 'corrections')

    def corr(self, *rows):
        write_tsv(os.path.join(self.c, 'x.tsv'), [HEADER, *rows])

    def test_apply(self):
        self.corr(['00001', 'قديم', 'جديد', 'typo'], ['00002', '', 'ب', 'new'])
        self.assertEqual(apply(self.d), 2)
        r = read_tsv(self.t)
        self.assertEqual((r[1][5], r[1][6], r[2][5], r[2][6]), ('جديد', 'reviewed', 'ب', 'translated'))
        self.assertTrue(os.path.exists(os.path.join(self.c, 'applied', 'x.tsv')))
        self.assertFalse(os.path.exists(os.path.join(self.c, 'x.tsv')))
        self.assertIn('00001', open(os.path.join(self.c, 'LOG.md'), encoding='utf-8').read())

    def test_refuse_mismatch(self):
        before = open(self.t, encoding='utf-8').read()
        self.corr(['00002', '', 'ب', 'ok'], ['00001', 'غلط', 'جديد', 'bad'])
        with self.assertRaises(SystemExit):
            apply(self.d)
        self.assertEqual(open(self.t, encoding='utf-8').read(), before)
        self.assertTrue(os.path.exists(os.path.join(self.c, 'x.tsv')))

    def test_unknown_and_duplicate(self):
        self.corr(['99999', '', 'ب', ''])
        with self.assertRaises(SystemExit):
            apply(self.d)
        self.corr(['00002', '', 'ب', ''], ['00002', '', 'ج', ''])
        with self.assertRaises(SystemExit):
            apply(self.d)

    def test_cloud_marks_checked(self):
        write_tsv(os.path.join(self.c, 'cloud', 'p1.tsv'), [HEADER, ['00001', 'قديم', 'جديد', 'x'], ['00002', '', '', '']])
        self.assertEqual(apply(self.d), 2)
        r = read_tsv(self.t)
        self.assertEqual((r[1][5], r[1][6], r[1][7]), ('جديد', 'reviewed', 'cloud review pass 2'))
        self.assertEqual((r[2][6], r[2][7]), ('todo', ''))  # empty AR row untouched
        self.assertTrue(os.path.exists(os.path.join(self.c, 'applied', 'cloud', 'p1.tsv')))
        self.assertFalse(os.path.exists(os.path.join(self.c, 'cloud', 'p1.tsv')))

    def test_no_files(self):
        self.assertEqual(apply(self.d), 0)


unittest.main()
