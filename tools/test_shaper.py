"""unit tests for shaper.py: SHAPER_SPEC §9a (U1-U12), §9b (the 20 TAGS.md examples T1-T20 + T21/T22),
30 real translated rows (exact round trip), the round trip over every translated row, and (BUILD-1) conv hoist,
icon clusters and line breaking (wrap) with fixed advances and with the real font on real long rows."""
import os, re, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shaper import shape, unshape, normalize, has_letters, wrap, meter, reflow, BREAK
from tsvlib import load_translation
import locres

cp = lambda s: ''.join(chr(int(x, 16)) for x in s.split())
R = shape  # one Arabic word: forms, reversed
ATOMS = re.compile(r'<icon\([^)]*\)>|\{\d+\}|<nbsp>|<[Bb]r>|<pb(?:\([^)]*\))?>|\|plural\(|<conv\([^)]*\)>')
REAL = ['11127', '11128', '13504', '13505', '00048', '10952', '15836', '15837', '00126', '10713', '12983', '12997',
        '14797', '15844', '12203', '12565', '00671', '10958', '00106', '00107', '00031', '00032', '00201', '10953',
        '00033', '00034', '00041', '12900', '00046', '00164']  # plural, bold, pb, conv, color+{n}, icon+color, red,
# digits+%, Greek, Roman numerals, icons, 3+ lines, brackets, Latin acronyms, digit/digit, '?'

TAGS = [  # (#, logical AR, expected visual) — SHAPER_SPEC §9b
    ('T1', '<i(on)>يمكنهم أخذ عالمك.<i(off)>', '<i(on)>.' + R('عالمك') + ' ' + R('أخذ') + ' ' + R('يمكنهم') + '<i(off)>'),
    ('T2', '<i(on)>هذه<I(off)> طبيعة القلب—<br>ألا يترك أبدا.',
     '—' + R('القلب') + ' ' + R('طبيعة') + ' <i(on)>' + R('هذه') + '<i(off)><br>.' + R('أبدا') + ' ' + R('يترك') + ' ' + R('ألا')),
    ('T3', '<i(on)>ليس لنا إلا بعضنا<i(off)><br>',
     '<i(on)>' + R('بعضنا') + ' ' + R('إلا') + ' ' + R('لنا') + ' ' + R('ليس') + '<i(off)><br>'),
    ('T4', 'نعم. معلمهم، المعلم إراكوس،<Br>كان احتمالا آخر،',
     '،' + R('إراكوس') + ' ' + R('المعلم') + ' ،' + R('معلمهم') + ' .' + R('نعم') + '<Br>،' + R('آخر') + ' ' + R('احتمالا') + ' ' + R('كان')),
    ('T5', '<pb(0.55)>انظر.', '<pb(0.55)>.' + R('انظر')),
    ('T6', 'القصر القديم؟ اعبر الممر،<br>ثم امش قليلا في الغابة.',
     '،' + R('الممر') + ' ' + R('اعبر') + ' ؟' + R('القديم') + ' ' + R('القصر') + '<br>.' + R('الغابة') + ' ' + R('في') + ' ' + R('قليلا') + ' ' + R('امش') + ' ' + R('ثم')),
    ('T7', 'يمكنك الآن الإبحار إلى منطقة جديدة!<pb>استخدم <icon(L2)> أو <icon(R2)> للتنقل.',
     '!' + R('جديدة') + ' ' + R('منطقة') + ' ' + R('إلى') + ' ' + R('الإبحار') + ' ' + R('الآن') + ' ' + R('يمكنك') +
     '<pb>.' + R('للتنقل') + ' <icon(R2)> ' + R('أو') + ' <icon(L2)> ' + R('استخدم')),
    ('T8', '<icon(Decide)> التالي  <icon(Cancel)> إغلاق', R('إغلاق') + ' <icon(Cancel)>  ' + R('التالي') + ' <icon(Decide)>'),
    ('T9', '<icon(KeyLeftRight)> تبديل  <icon(RstickLeft)>/<icon(RstickRight)> تدوير',
     R('تدوير') + ' <icon(RstickRight)>/<icon(RstickLeft)>  ' + R('تبديل') + ' <icon(KeyLeftRight)>'),
    ('T10', '<icon(Kb_Del)> تراجع', R('تراجع') + ' <icon(Kb_Del)>'),
    ('T11', '<conv(disable)><icon(Cross)><conv(off)>', '<conv(disable)><icon(Cross)><conv(off)>'),
    ('T12', 'استخدم <icon(Triangle)><color(strong)>الضربة المحمية<color> للتقدم!',
     '!' + R('للتقدم') + ' <color(strong)>' + R('المحمية') + ' ' + R('الضربة') + '<color><icon(Triangle)> ' + R('استخدم')),
    ('T13', 'هل نسيت التحكم؟<br>اختر <color(strong)>مساعدة اللعب<color> من القائمة الرئيسية.',
     '؟' + R('التحكم') + ' ' + R('نسيت') + ' ' + R('هل') + '<br>.' + R('الرئيسية') + ' ' + R('القائمة') + ' ' + R('من') +
     ' <color(strong)>' + R('اللعب') + ' ' + R('مساعدة') + '<color> ' + R('اختر')),
    ('T14', '<color(red)>تم فصل وحدة التحكم.<color>',
     '<color(red)>.' + R('التحكم') + ' ' + R('وحدة') + ' ' + R('فصل') + ' ' + R('تم') + '<color>'),
    ('T15', '<color(heading)>بسيط<color>', '<color(heading)>' + R('بسيط') + '<color>'),
    ('T16', '{0} / {1}', '{0} / {1}'),
    ('T17', '{0}′{1}″{2}', '{0}′{1}″{2}'),
    ('T18', 'صورت {0}|plural(one=أول شعار حظ,other={0} شعارات حظ)!<br>حصلت على <color(strong)>{1}<color>.',
     '!{0}|plural(one=' + R('حظ') + ' ' + R('شعار') + ' ' + R('أول') + ',other=' + R('حظ') + ' ' + R('شعارات') + ' {0}) ' +
     R('صورت') + '<br>.<color(strong)>{1}<color> ' + R('على') + ' ' + R('حصلت')),
    ('T19', '<b(on)>بوابة المعركة 1 - الصعوبة ★☆☆<b(off)><br><br>قوى عظيمة.',
     '<b(on)>☆☆★ ' + R('الصعوبة') + ' - 1 ' + R('المعركة') + ' ' + R('بوابة') + '<b(off)><br><br>.' + R('عظيمة') + ' ' + R('قوى')),
    ('T20', 'سأنقذك مهما حدث.<br><color(hashtag)>￠قسم<color>',
     '.' + R('حدث') + ' ' + R('مهما') + ' ' + R('سأنقذك') + '<br><color(hashtag)>' + R('قسم') + '￠<color>'),
    ('T21', 'العب Re<icon(Coda)>Mind.', '.Re<icon(Coda)>Mind ' + R('العب')),
    ('T22', '<nbsp><nbsp><nbsp>نص', R('نص') + '<nbsp><nbsp><nbsp>'),
]


class T(unittest.TestCase):
    def test_core(self):  # §9a
        self.assertEqual(shape('باب'), cp('FE8F FE8E FE91'))                       # U1
        self.assertEqual(shape('في'), cp('FEF2 FED3'))                             # U2
        self.assertEqual(shape('لا'), cp('FEFB'))                                  # U3
        self.assertEqual(shape('سلام'), cp('FEE1 FEFC FEB3'))                      # U4
        self.assertEqual(shape('مستوى 25'), '25 ' + R('مستوى'))                    # U5
        self.assertEqual(shape('HP 120'), 'HP 120')                                # U6
        self.assertEqual(shape('اسم (جديد)'), '(' + R('جديد') + ') ' + R('اسم'))   # U7 mirrored brackets
        self.assertEqual(shape('كلمة ، كلمة ؟'), '؟ ' + R('كلمة') + ' ، ' + R('كلمة'))  # U8
        self.assertEqual(shape('ء'), cp('FE80'))                                   # U9
        self.assertEqual(shape('لعبة')[0], cp('FE94'))
        for bad in ('شَمس', 'امشِ', 'صوّرت', 'نص<foo>', 'عين <conv(disable)>نص<conv(off)>'):  # U10 + unknown tag
            self.assertRaises(ValueError, shape, bad)
        self.assertEqual(shape('ڤينتوس')[-1], cp('FB6C'))                         # U12
        for x in ('باب', 'في', 'لا', 'سلام', 'مستوى 25', 'اسم (جديد)', 'كلمة ، كلمة ؟', 'ء', 'لعبة', 'ڤينتوس'):
            self.assertEqual(unshape(shape(x)), x)                                 # U11

    def test_tags_examples(self):  # §9b
        for n, x, want in TAGS:
            got = shape(x)
            self.assertEqual(got, want, n)
            self.assertEqual(unshape(got), normalize(x), n)
            self.assertEqual(unshape(got), x if n != 'T2' else x.replace('<I(off)>', '<i(off)>'), n)  # T2: typo tag

    def test_real_rows(self):
        rows = {r['id']: r for r in load_translation()}
        if not rows: self.skipTest('private translation workspace not present (public clone)')
        for i in REAL:
            x = rows[i]['AR']
            v = shape(x)
            self.assertEqual(unshape(v), x, i)
            self.assertEqual(sorted(ATOMS.findall(v)), sorted(ATOMS.findall(x)), i)
            self.assertFalse(re.search('[ء-ي]', v), i)  # every letter became a presentation form

    def test_all_translated(self):
        """every translated row shapes; the round trip is exact or, where UAX #9 maps two logical orders to the same
        visual line (number run then Latin run), at least shapes back to the same visual line"""
        exact = ambiguous = 0
        for r in load_translation():
            x = r['AR']
            if r['status'] == 'todo' or not has_letters(x):
                continue
            v = shape(x)
            u = unshape(v)
            if u == x:
                exact += 1
            else:
                self.assertEqual(shape(u), v, r['id'])
                ambiguous += 1
        # TRANS-4: italic subtitle lines split by a pause (<i(off)><pb(..)><i(on)>) also come back in another tag order
        self.assertLess(ambiguous, max(20, exact // 100))
        print(f'\n  round trip: {exact} exact, {ambiguous} ambiguous (same visual line)', file=sys.stderr)


FONTS = ['out/builds/BUILD-1/pakroot/KINGDOM HEARTS III/Content/UI/Scaleform/91_font/TresFont.uasset',
         'out/builds/TEST50/unpacked/KINGDOM HEARTS III/Content/UI/Scaleform/91_font/TresFont.uasset']
LONG = ['10269', '10294', '15411', '15082', '15477', '15202', '15159', '07834', '15160']  # help, journal, item
words = lambda t: [w for w in re.split(r'\s+|<[Bb]r>', t) if w]


class Wrap(unittest.TestCase):
    def test_conv_hoist(self):  # BUILD-1: a row wrapped in one conv pair keeps it, the inside is shaped
        x = '<conv(disable)><icon(Decide)> تأكيد<br><icon(Lstick)> تحريك الشخصية<conv(off)>'
        v = shape(x)
        self.assertEqual(v, '<conv(disable)>' + R('تأكيد') + ' <icon(Decide)><br>' + R('الشخصية') + ' ' + R('تحريك') +
                         ' <icon(Lstick)><conv(off)>')
        self.assertEqual(unshape(v), x)
        self.assertRaises(ValueError, shape, 'عين <conv(disable)>نص<conv(off)>')  # conv in mid-row stays an error

    def test_conv_rows(self):  # the 12 tutorial control lists translated in BUILD-1
        rows = {r['id']: r for r in load_translation()}
        if not rows: self.skipTest('private translation workspace not present (public clone)')
        for i in ('10307', '10308', '10309', '10310', '10317', '10318', '10319', '10320', '10510', '10511', '10530', '10531'):
            x = rows[i]['AR']
            self.assertNotEqual(rows[i]['status'], 'todo', i)
            v = shape(x)
            self.assertEqual(v[:v.index('>') + 1], x[:x.index('>') + 1], i)          # conv pair stays at the ends
            self.assertTrue(v.endswith('<conv(off)>'), i)
            self.assertEqual(unshape(v), x, i)
            self.assertEqual(sorted(ATOMS.findall(v)), sorted(ATOMS.findall(x)), i)
            self.assertFalse(re.search('[ء-ي]', v), i)
            for cluster in re.findall(r'(?:<icon\([^)]*\)>){2,}', x):
                self.assertIn(cluster, v, i)                                          # icon diagrams keep their order

    def test_icon_cluster(self):  # adjacent icons keep their drawn order (stick diagrams, button rows)
        x = '<icon(LstickLeft)><icon(4WayArrow)><icon(LstickRight)> تحريك'
        self.assertEqual(shape(x), R('تحريك') + ' <icon(LstickLeft)><icon(4WayArrow)><icon(LstickRight)>')
        self.assertEqual(unshape(shape(x)), x)
        self.assertEqual(shape('<icon(L2)>/<icon(R2)> ك'), R('ك') + ' <icon(R2)>/<icon(L2)>')  # '/' between: RTL

    def test_wrap_fixed(self):  # every glyph 100 units, icon 300
        m = meter({}, icon=300, missing=100)
        self.assertEqual(wrap('كلمة كلمة كلمة', 1000, m), 'كلمة كلمة<br>كلمة')      # 4+1+4 = 900 fits, 1400 not
        self.assertEqual(wrap('كلمة كلمة', 1000, m), 'كلمة كلمة')                   # fits: unchanged
        self.assertEqual(wrap('سطر<br>كلمة كلمة كلمة', 1000, m), 'سطر<br>كلمة كلمة<br>كلمة')  # EN <br> kept
        self.assertEqual(wrap('كلماتكلماتكلمات قصير', 1000, m), 'كلماتكلماتكلمات<br>قصير')  # long word kept whole
        self.assertEqual(wrap('ا KINGDOM HEARTS ب', 1000, m), 'ا<br>KINGDOM HEARTS<br>ب')   # no break in LTR run
        self.assertEqual(wrap('اا <color(strong)>بب جج<color> دد', 600, m),
                         'اا <color(strong)>بب<br>جج<color> دد')                          # tags stay whole, style spans
        self.assertEqual(shape('اا <color(strong)>بب<br>جج<color> دد'),
                         '<color(strong)>' + R('بب') + '<color> ' + R('اا') + '<br>' + R('دد') + ' <color(strong)>' +
                         R('جج') + '<color>')                                              # each line shaped alone
        self.assertEqual(wrap('{0}|plural(one=ا ا ا ا,other=ب ب ب ب) ج', 500, m),
                         '{0}|plural(one=ا ا ا ا,other=ب ب ب ب)<br>ج')                    # no break inside plural
        self.assertEqual(wrap('<icon(Decide)> ككك ككك', 700, m), '<icon(Decide)> ككك<br>ككك')  # icon counts 300
        self.assertEqual(wrap('HP 80', 100, m), 'HP 80')                                # no Arabic: untouched
        x = '<conv(force)><icon(A)> كلمة كلمة كلمة<conv(off)>'
        self.assertEqual(wrap(x, 1300, m), '<conv(force)><icon(A)> كلمة كلمة<br>كلمة<conv(off)>')

    def test_reflow(self):  # FULL-1: body lines joined, last whole-line colour footer kept, then wrap re-breaks
        m = meter({}, icon=300, missing=100)
        x = 'اا بب<br>جج<br><color(strong)>(دد)<color>'
        self.assertEqual(reflow(x), 'اا بب جج<br><color(strong)>(دد)<color>')
        self.assertEqual(reflow('اا <br>بب<br>جج'), 'اا بب جج')                            # no footer: one body line
        self.assertEqual(reflow('<color(red)>اا<color>، بب<br>جج'), '<color(red)>اا<color>، بب جج')
        self.assertEqual(wrap(reflow('ااا ببب<br>ججج ددد<br><color(strong)>ه<color>'), 800, m),
                         'ااا ببب<br>ججج ددد<br><color(strong)>ه<color>')                   # 1500 > 800: two lines
        self.assertEqual(wrap(reflow('ااا<br>ببب<br>ججج<br><color(strong)>ه<color>'), 1200, m),
                         'ااا ببب ججج<br><color(strong)>ه<color>')                           # 4 lines -> 2

    def test_wrap_real_rows(self):  # real long rows, real glyph advances and field widths (technical/FIELD_WIDTHS.tsv)
        path = next((f for f in FONTS if os.path.exists(f)), None)
        if not path:
            self.skipTest('no rebuilt TresFont in out/builds (run tools/build_build1.py)')
        from build_build1 import profiles, profile, meters
        ms, profs = meters(path), profiles()
        rows = {r['id']: r for r in load_translation()}
        for i in LONG:
            r = rows[i]
            _, fid, cap, _, _ = profile(r['namespace'], r['key'], profs)
            x = locres.unesc(r['AR'])
            w = wrap(x, cap, ms[fid])
            lines = BREAK.split(w)[::2]
            self.assertGreater(len(lines), len(BREAK.split(x)[::2]), i)                  # the row needed breaking
            for l in lines:
                self.assertTrue(ms[fid](l) <= cap or len(words(l)) == 1, (i, l))           # every line fits
            self.assertEqual(words(w), words(x), i)                                        # same words, same order
            self.assertEqual(sorted(ATOMS.findall(w.replace('<br>', ''))), sorted(ATOMS.findall(x.replace('<br>', ''))), i)
            v = shape(w)
            self.assertEqual(unshape(v), w, i)
            self.assertEqual(len(BREAK.split(v)), len(BREAK.split(w)), i)                  # one visual line per line


if __name__ == '__main__':
    unittest.main()
