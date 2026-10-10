import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import check, build_gloss

def c(en, ar, **k):
    return check(en, ar, **k)


class T(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(c('Use <icon(L2)> now<br>{0} HP', 'استخدم <icon(L2)> الآن<br>{0} HP'), [])
        self.assertEqual(c('Hello', '', status='todo'), [])
        self.assertEqual(c('Hello', '', status='translated'), ['EMPTY'])

    def test_tags(self):
        self.assertIn('TAGS', c('<icon(L2)> a', 'أ'))
        self.assertIn('TAGS', c('<color(strong)>a<color>', '<color(strong)>أ'))
        self.assertEqual(c('<icon(L2)> <icon(R2)>', '<icon(R2)> <icon(L2)>'), ['ARGORDER'])
        self.assertIn('TAGS', c('{0} and {1}', '{0}'))
        self.assertIn('TAGS', c('{0}|plural(one=a,other=b)', '{0}'))

    def test_br(self):
        self.assertEqual(c('a<br>b', 'أ ب'), ['TAGS', 'BR'])
        self.assertEqual(c('a<br>b', 'أ<Br>ب'), ['TAGS'])  # case differs; count equal

    def test_hashtag(self):
        en = 'Hi<br><color(hashtag)>￠sora ￠oath<color>'
        self.assertIn('HASHTAG', c(en, 'مرحبا<br><color(hashtag)>￠sora ￠عهد<color>'))
        self.assertNotIn('HASHTAG', c(en, 'مرحبا<br><color(hashtag)>￠سورا ￠عهد<color>'))
        self.assertNotIn('HASHTAG', c('Hi sora', 'مرحبا sora'))

    def test_latin(self):
        self.assertIn('LATIN', c('Sora', 'Riku'))  # not in this row's EN
        self.assertIn('LATIN', c('Hello', 'مرحبا HP'))
        self.assertEqual(c('Max HP', 'أقصى HP'), [])
        self.assertEqual(c('Second Form S', 'الشكل الثاني S'), [])
        self.assertIn('LATIN', c('Second Form S', 'الشكل الثاني A'))
        self.assertEqual(c('KINGDOM HEARTS Ⅲ', 'كينغدوم هارتس Ⅲ'), [])
        self.assertIn('LATIN', c('KINGDOM HEARTS Ⅲ', 'كينغدوم هارتس III'))
        self.assertEqual(c('Teeny Ship α', 'سفينة صغيرة α'), [])
        self.assertIn('LATIN', c('Teeny Ship α', 'سفينة صغيرة β'))
        self.assertEqual(c('Re<icon(CodaL)>Mind', 'Re<icon(CodaL)>Mind'), [])
        self.assertEqual(c('play<br>Re<icon(CodaL)>Mind', 'العب<br>Re<icon(CodaL)>Mind'), [])
        self.assertEqual(c('x{1}', '×{1}'), [])
        self.assertEqual(c('Visit www.x.com', 'زر www.x.com'), [])
        self.assertIn('LATIN', c('hp', 'HP'))  # verbatim: case matters
        self.assertNotIn('LATIN', c('<icon(L2)>', '<icon(L2)>'))
        self.assertNotIn('LATIN', c('{0}|plural(one=a,other=b)', '{0}|plural(one=أ,other=ب)'))

    def test_chars(self):
        self.assertIn('HARAKAT', c('a', 'سَلام'))
        self.assertIn('TATWEEL', c('a', 'سـلام'))
        self.assertIn('DSPACE', c('a b', 'س  ل'))
        self.assertNotIn('DSPACE', c('a  b', 'س  ل'))
        self.assertIn('LEAD', c('a', ' س'))
        self.assertIn('TRAIL', c('a', 'س '))
        self.assertNotIn('TRAIL', c('a ', 'س '))

    def test_brackets_ratio(self):
        self.assertIn('BRACKETS', c('(a)', '(س'))
        self.assertIn('RATIO', c('a long english sentence here', 'ن'))

    def test_plural_brackets(self):
        en = 'Find {0}|plural(one=a waypoint,other={0} waypoints) now'
        self.assertEqual(c(en, 'اعثر على {0}|plural(one=نقطة,other={0} من النقاط) الآن'), [])
        self.assertEqual(c(en, 'اعثر على {0}|plural(one=نقطة,other={0} من النقاط) (الآن'), ['BRACKETS'])

    def test_gloss(self):
        E = [dict(en='Sora', ar='سورا', status='approved', type='character'),
             dict(en='Kingdom Hearts', ar='كينغدوم هارتس', status='approved', type='term'),
             dict(en='Beast', ar='الوحش', status='approved', type='character'),
             dict(en='Will', ar='ويل', status='approved', type='character'),
             dict(en='Save', ar='حفظ', status='approved', type='menu'),
             dict(en='Munny', ar='موني', status='pending', type='item'),
             dict(en="Beast's Castle", ar='قلعة الوحش', status='approved', type='world')]
        g = build_gloss(E, common={'will'})
        self.assertEqual(c('Sora', 'سورا', gloss=g), [])
        self.assertEqual(c('Sora', 'ريكو', gloss=g), ['GLOSS'])
        self.assertEqual(c('Hi, Sora!', 'مرحبا يا سورا!', gloss=g), [])
        self.assertEqual(c('Sorado', 'ريكو', gloss=g), [])  # whole word only
        self.assertEqual(c('KINGDOM HEARTS', 'كينغدم هارتس', gloss=g), ['GLOSS'])  # all caps matches
        self.assertEqual(c('KINGDOM HEARTS', 'كينغدوم هارتس', gloss=g), [])
        self.assertEqual(c('kingdom hearts', 'شيء آخر هنا', gloss=g), [])  # lowercase is not the name
        g3 = build_gloss([dict(en='Scrooge McDuck', ar='سكروج ماكدك', type='character', status='approved'),
                          dict(en='Scrooge', ar='العم سكروج', type='character', status='approved')])
        self.assertEqual(c('Scrooge McDuck', 'سكروج ماكدك', gloss=g3), [])  # longer term covers the short one
        self.assertEqual(c('Scrooge', 'شيء', gloss=g3), ['GLOSS'])
        g2 = build_gloss([dict(en='Master', ar='الإتقان', type='ability', status='approved'),
                          dict(en='master', ar='السيد', type='term', status='approved')])
        self.assertEqual(c('Master Eraqus', 'السيد إيراكوس', gloss=g2), [])  # two approved forms: either passes
        self.assertEqual(c('Master Eraqus', 'شيء إيراكوس', gloss=g2), ['GLOSS'])
        self.assertEqual(c('The Beast', 'وحش', gloss=g), [])  # leading ال optional
        self.assertEqual(c('Will', 'سوف', gloss=g), [])  # ambiguous one-word term skipped
        self.assertEqual(c('Save', 'خزن', gloss=g), [])  # menu terms not checked
        self.assertEqual(c('Munny', 'مال', gloss=g), [])  # only approved terms
        self.assertEqual(c("Beast´s Castle", 'القلعة', gloss=g), ['GLOSS'])  # KH2 apostrophe normalized
        self.assertEqual(c('Sora', '', status='todo', gloss=g), [])

    def test_qmark_typo(self):
        self.assertIn('QMARK', c('Why?', 'لماذا؟'))
        self.assertEqual(c('Why?', 'لماذا?'), [])
        self.assertIn('TYPO', c('Go', 'اصل إلى الباب'))      # imperative wrong
        self.assertEqual(c('Go', 'واصل إلى الباب'), [])       # longer word, not a hit
        self.assertEqual(c('Go', 'صل إلى الباب'), [])
        self.assertIn('TYPO', c('Go', 'لقد اضغطت الزر'))
        self.assertIn('TYPO', c('Go', 'مرحبا. بلغ الجميع'))   # sentence-start imperative
        self.assertEqual(c('Go', 'لقد بلغ الجميع'), [])        # mid-sentence: not flagged
        self.assertIn('TYPO', c('Go', 'هذا لا أحدا'))
        self.assertEqual(c('Go', 'هذا من اللا أحد'), [])


unittest.main()
