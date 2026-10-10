r"""One-time (BUILD-1): write review\corrections\build1_conv.tsv (the 12 tutorial control lists with <conv> groups,
translated now that the shaper keeps a whole-row conv pair) and build1_films.tsv (Frozen / Toy Story dub titles),
and add the three film titles to translation\glossary.tsv. Then run tools\apply_corrections.py. Do not re-run."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import load_translation, read_tsv, write_tsv, GLOSSARY, ROOT

A = '<icon(ArrowSpace)>'
K = lambda b: A + f'<icon({b})><icon({b}_S)>' + A  # keyboard rows: spacer, pad icon, key icon, spacer
N4 = '<nbsp>' * 4
PAD_A = ('<icon(Decide)> تأكيد<br><icon(Triangle)> استخدام أمر الموقف (عند ظهوره)<br><icon(Square)> صد / مراوغة '
         '(أثناء الحركة)<br><icon(Cancel)> إلغاء / قفز / إفلات (أثناء التعلق)<br><br><icon(Lstick)> تحريك الشخصية<br>'
         '<icon(Rstick)> ضبط الكاميرا<br><icon(R3)> إعادة الكاميرا خلف الشخصية<br>' + N4 +
         '(أو توسيطها على الهدف المثبت)')
PAD_B = ('<icon(L1)> اضغط مطولا لفتح الاختصارات<br>' + N4 + '(اضغط <icon(Decide)><icon(Triangle)><icon(Square)>'
         '<icon(Cancel)> لاستخدام الاختصارات)<br>@L2@ التنقل بين أوامر المواقف<br>' + N4 + '(عند ظهورها)<br><br>'
         '<icon(R1)> تبديل التثبيت / التصويب المثبت (اضغط مطولا)<br><icon(R2)> تغيير هدف التثبيت<br><br><icon(Option)> '
         'إيقاف مؤقت / فتح القائمة الرئيسية<br><icon(Pad)> دخول وضع الكاميرا')


def stick(s, label):
    return (K(s + 'Up') + f'<br><icon({s}Left)><icon({s}Left_S)><icon(4WayArrow)><icon({s}Right)><icon({s}Right_S)> '
            f'{label}<br>' + K(s + 'Down'))


KB_A = (K('Decide') + ' تأكيد<br>' + K('Cancel') + ' إلغاء / قفز / إفلات (أثناء التعلق)<br>' + K('Square') +
        ' صد / مراوغة (أثناء الحركة)<br>' + K('Triangle') + ' استخدام أمر الموقف<br>' + A * 3 + '  (عند ظهوره)<br><br>' +
        stick('Lstick', 'تحريك الشخصية') + '<br><br>' + K('LstickModify') + ' المشي (اضغط مطولا)<br><br>' +
        stick('Rstick', 'ضبط الكاميرا') + '<br><br>' + K('R3') + ' إعادة الكاميرا خلف الشخصية<br>' + A * 3 +
        ' (أو توسيطها على الهدف المثبت)')
KB_B = (K('L1') + ' اضغط مطولا لفتح الاختصارات<br>' + A * 3 + ' (اضغط <icon(Decide)><icon(Triangle)><icon(Square)>'
        '<icon(Cancel)> لاستخدام الاختصارات)<br><br>@L2@<br><br>' + K('R1') + ' تبديل التثبيت / التصويب المثبت '
        '(اضغط مطولا)<br>' + K('R2') + ' تغيير هدف التثبيت<br><br>' + K('Option') + ' إيقاف مؤقت / فتح القائمة '
        'الرئيسية<br>' + K('Pad') + ' دخول وضع الكاميرا')
GUMMI_A = ('<icon(Decide)>/<icon(R2)> الهجوم بغامي الأسلحة<br><icon(Square)> تدحرج للمراوغة<br><icon(Triangle)> '
           'استخدام السلاح الخاص<br><icon(Cancel)> تعزيز (يستهلك مقياس التعزيز)<br><br><icon(Lstick)> توجيه سفينة '
           'الغامي<br><icon(Rstick)> ضبط الكاميرا<br><icon(L1)>/<icon(R1)> التقدم للأمام / إيقاف التقدم<br>' +
           '<nbsp>' * 7 + 'الخروج من خط السديم / الخروج من لعبة كرة الكنز المصغرة<br><icon(L3)> التفاف<br>'
           '<icon(R3)> إعادة ضبط الكاميرا')
GUMMI_B = ('اضغط مطولا على <icon(L2)> أثناء الاستكشاف للدخول في <color(strong)>وضع التحرك الجانبي<color>.<br>'
           '(في وضع التحرك الجانبي: <icon(Lstick)> التحرك جانبيا)<br><br><icon(Option)> إيقاف مؤقت وفتح القائمة<br>'
           '<icon(Pad)> التقاط صورة بهاتف الغامي<br><br><icon(KeyLeftRight)> تغيير تشكيل السفن الصغيرة<br>'
           '<icon(KeyUpDown)> إعادة السفينة إلى الوضع الأفقي')
GUMMI_KB_A = (K('Decide') + ' الهجوم بغامي الأسلحة<br>' + K('R2') + '<br>' + K('Square') + ' تدحرج للمراوغة<br>' +
              K('Triangle') + ' استخدام السلاح الخاص<br>' + K('Cancel') + ' تعزيز (يستهلك مقياس التعزيز)<br><br>' +
              K('LstickUp') + '<br><icon(LstickLeft)><icon(LstickLeft_S)><icon(4WayArrow)><icon(LstickRight)>'
              '<icon(LstickRight_S)> توجيه سفينة الغامي<br>' + K('LstickDown') + ' التحرك جانبيا (في وضع التحرك '
              'الجانبي)<br><br>' + K('L2') + ' وضع التحرك الجانبي<br>' + A * 3 + '  <color(strong)>ادخل وضع التحرك '
              'الجانبي أثناء الاستكشاف<color><br><br>' + K('L1') + ' التقدم للأمام / إيقاف التقدم<br>' + K('R1') +
              ' الخروج من خط السديم<br>' + A * 3 + '  الخروج من لعبة كرة الكنز المصغرة')
GUMMI_KB_B = (stick('Rstick', 'ضبط الكاميرا') + '<br><br>' + K('R3') + ' إعادة ضبط الكاميرا<br><br>' + K('L3') +
              ' التفاف<br><br>' + K('Option') + ' إيقاف مؤقت وفتح القائمة<br>' + K('Pad') + ' التقاط صورة بهاتف الغامي'
              '<br><br>' + K('KeyLeft') + ' تغيير تشكيل السفن الصغيرة<br>' + K('KeyRight') + '<br><br>' + K('KeyUp') +
              ' إعادة السفينة إلى الوضع الأفقي<br>' + K('KeyDown'))
D, F, OFF = '<conv(disable)>', '<conv(force)>', '<conv(off)>'
CONV = {
    '10307': D + PAD_A + OFF, '10309': D + PAD_A + OFF,
    '10308': D + PAD_B.replace('@L2@', '<icon(L2)>') + OFF,
    '10310': D + PAD_B.replace('@L2@', '<icon(KeyUpDown)>') + OFF,
    '10317': F + KB_A + OFF, '10319': F + KB_A + OFF,
    '10318': F + KB_B.replace('@L2@', K('L2') + ' التنقل بين أوامر المواقف<br>' + A * 3 + ' (عند ظهورها)') + OFF,
    '10320': F + KB_B.replace('@L2@', K('KeyUp') + ' التنقل بين أوامر المواقف<br>' + K('KeyDown') + ' (عند ظهورها)') + OFF,
    '10510': D + GUMMI_A + OFF, '10511': D + GUMMI_B + OFF, '10530': F + GUMMI_KB_A + OFF, '10531': F + GUMMI_KB_B + OFF,
}
FILMS = {'المملكة المتجمدة': 'ملكة الثلج', 'قصة لعبة': 'حكاية لعبة'}  # supervisor BUILD-1: common Arabic dub titles
REASON = 'BUILD-1: conv hoist approved, control list translated'


def main():
    rows = {r['id']: r for r in load_translation()}
    tags = lambda s: sorted(re.findall(r'<[^>]*>', s))
    conv = [['id', 'old_AR', 'new_AR', 'reason']]
    for i, ar in CONV.items():
        assert tags(ar) == tags(rows[i]['EN']), i  # same tags as EN, conv pair at the row start / end
        conv.append([i, rows[i]['AR'], ar, REASON])
    films = [['id', 'old_AR', 'new_AR', 'reason']]
    for r in rows.values():
        new = r['AR']
        for a, b in FILMS.items():
            new = new.replace(a, b)
        if new != r['AR']:
            films.append([r['id'], r['AR'], new, 'BUILD-1: film dub title (supervisor)'])
    d = os.path.join(ROOT, 'review', 'corrections')
    write_tsv(os.path.join(d, 'build1_conv.tsv'), conv)
    write_tsv(os.path.join(d, 'build1_films.tsv'), films)
    g = read_tsv(GLOSSARY)
    have = {r[0] for r in g}
    for en, ar, st, note in [('Frozen', 'ملكة الثلج', 'approved', 'film title (common Arabic dub title); supervisor BUILD-1'),
                             ('Toy Story', 'حكاية لعبة', 'approved', 'film title (common Arabic dub title); supervisor BUILD-1'),
                             ('Tangled', 'متشابك', 'proposed', 'pending: supervisor to verify (film title, BUILD-1)')]:
        if en not in have:
            g.append([en, ar, 'other', 'KH3-new', st, '0', '', note])
    write_tsv(GLOSSARY, g)
    print(len(conv) - 1, 'conv rows,', len(films) - 1, 'film rows')


if __name__ == '__main__':
    main()
