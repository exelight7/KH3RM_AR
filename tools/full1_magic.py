r"""One-time (FULL-1 Part B): magic names in Arabic (user decision FULL-1, KH3 only; KH2 glossary file unchanged).
Writes review\corrections\full1_magic.tsv (id old_AR new_AR reason) from the substitutions below and updates the
magic rows of translation\glossary.tsv. Each (old, new) pair must occur in the row's current AR. Run once, then
tools\refresh.bat applies the corrections. Usage: python -I tools/full1_magic.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *

NOTE = 'user decision FULL-1'
# spell -> Arabic (user table); definite forms for idafa compounds (تعزيز النار)
SPELL = {
    'Fire': 'نار', 'Fira': 'نار قوية', 'Firaga': 'نار كبرى', 'Firaza': 'نار قصوى',
    'Blizzard': 'جليد', 'Blizzara': 'جليد قوي', 'Blizzaga': 'جليد أكبر', 'Blizzaza': 'جليد أقصى',
    'Thunder': 'صاعقة', 'Thundara': 'صاعقة قوية', 'Thundaga': 'صاعقة كبرى', 'Thundaza': 'صاعقة قصوى',
    'Cure': 'شفاء', 'Cura': 'شفاء قوي', 'Curaga': 'شفاء أكبر', 'Curaza': 'شفاء أقصى',
    'Aero': 'ريح', 'Aerora': 'ريح قوية', 'Aeroga': 'ريح كبرى', 'Aeroza': 'ريح قصوى',
    'Water': 'ماء', 'Watera': 'ماء قوي', 'Waterga': 'ماء أكبر', 'Waterza': 'ماء أقصى',
    'Donald Fire': 'نار دونالد', 'Donald Blizzard': 'جليد دونالد', 'Donald Thunder': 'صاعقة دونالد',
    'Donald Cure': 'شفاء دونالد', 'Donald Aero': 'ريح دونالد', 'Dark Firaga': 'نار كبرى مظلمة',
    'Fire Boost': 'تعزيز النار',
}
OLD = {  # transliterated form -> spell
    'فاير': 'Fire', 'فايرا': 'Fira', 'فايراغا': 'Firaga', 'فايرازا': 'Firaza',
    'بليزارد': 'Blizzard', 'بليزارا': 'Blizzara', 'بليزاغا': 'Blizzaga', 'بليزازا': 'Blizzaza',
    'ثاندر': 'Thunder', 'ثاندارا': 'Thundara', 'ثانداغا': 'Thundaga', 'ثاندازا': 'Thundaza',
    'كيور': 'Cure', 'كيورا': 'Cura', 'كيوراغا': 'Curaga', 'كيورازا': 'Curaza',
    'إيرو': 'Aero', 'إيرورا': 'Aerora', 'إيروغا': 'Aeroga', 'إيروزا': 'Aeroza',
    'ووتر': 'Water', 'ووترا': 'Watera', 'ووترغا': 'Waterga', 'ووترزا': 'Waterza',
}


def ar(old):
    return SPELL[OLD[old]]


def defin(old):
    """definite form (genitive of an idafa / adjective-noun): نار كبرى -> النار الكبرى"""
    return ' '.join('ال' + w for w in ar(old).split())


S = {}  # id -> [(old, new)]
for i, o, suf in [(11415 + k, 'إيرو', f'/G-{k + 1:02d}') for k in range(12)] + [
        (11427, 'فاير', '/G'), (11428, 'فايرا', '/G'), (11429, 'فايراغا', '/G-01'), (11430, 'فايراغا', '/G-02'),
        (11431, 'بليزارد', '/G'), (11432, 'بليزارا', '/G'), (11433, 'بليزاغا', '/G-01'), (11434, 'بليزاغا', '/G-02'),
        (11439, 'ووتر', '/G'), (11440, 'ووترا', '/G'), (11441, 'ووترغا', '/G-01'), (11442, 'ووترغا', '/G-02'),
        (11445, 'ثاندر', '/G'), (11446, 'ثاندارا', '/G'), (11447, 'ثانداغا', '/G'),
        (11741, 'فاير', '/S'), (11742, 'بليزارد', '/S'), (11743, 'ووتر', '/S'), (11744, 'ثاندر', '/S')]:
    S[f'{i:05d}'] = [(o + suf, ar(o) + suf)]
# equipment: noun + definite spell
for i, noun, o in [(12344, 'سوار', 'فاير'), (12345, 'سوار', 'فايراغا'), (12346, 'سوار', 'فايرازا'),
                   (12347, 'سلسلة', 'فاير'), (12348, 'طوق', 'بليزارد'), (12349, 'طوق', 'بليزارا'),
                   (12350, 'طوق', 'بليزاغا'), (12351, 'سلسلة', 'بليزارد'), (12352, 'تميمة', 'ثاندر'),
                   (12353, 'تميمة', 'ثانداغا'), (12354, 'تميمة', 'ثاندازا'), (12355, 'سلسلة', 'ثاندر'),
                   (12365, 'سوار', 'إيرو'), (12371, 'سوار', 'فايرا'), (12372, 'طوق', 'بليزازا'),
                   (12373, 'تميمة', 'ثاندارا'), (12477, 'زر كم', 'ووتر'), (12478, 'زر كم', 'ثاندر'),
                   (12479, 'زر كم', 'فاير'), (12480, 'زر كم', 'إيرو'), (12481, 'زر كم', 'بليزارد'),
                   (16424, 'تعزيز', 'فاير'), (16425, 'تعزيز', 'بليزارد'), (16426, 'تعزيز', 'ثاندر'),
                   (16427, 'تعزيز', 'ووتر'), (16428, 'تعزيز', 'إيرو'), (16487, 'مص', 'فاير'),
                   (16488, 'مص', 'بليزارد'), (16489, 'مص', 'ثاندر'), (16490, 'مص', 'ووتر'), (16491, 'مص', 'إيرو'),
                   (16499, 'محول', 'كيور'), (16543, 'عاصفة', 'بليزارد'), (16247, 'نصال', 'بليزارد'),
                   (16251, 'مخالب', 'بليزارد')]:
    S[f'{i:05d}'] = [(f'{noun} {o}', f'{noun} {defin(o)}')]
# command names (16036-16059) and the situation command Thunder
for k, o in enumerate(['فاير', 'فايرا', 'فايراغا', 'فايرازا', 'بليزارد', 'بليزارا', 'بليزاغا', 'بليزازا',
                       'ثاندر', 'ثاندارا', 'ثانداغا', 'ثاندازا', 'ووتر', 'ووترا', 'ووترغا', 'ووترزا',
                       'إيرو', 'إيرورا', 'إيروغا', 'إيروزا', 'كيور', 'كيورا', 'كيوراغا', 'كيورازا']):
    S[f'{16036 + k:05d}'] = [(o, ar(o))]
S['16231'] = [('ثاندر', 'صاعقة')]
S['16480'] = [('كيورازا', 'شفاء أقصى')]
for i, o in [(16060, 'فاير'), (16061, 'بليزارد'), (16062, 'إيرو'), (16063, 'ثاندر')]:
    S[f'{i:05d}'] = [(f'{o} البحر', f'{ar(o)} البحر')]
for i, o in [(16297, 'فاير'), (16298, 'بليزارد'), (16299, 'ثاندر'), (16362, 'فاير'), (16363, 'بليزارد'),
             (16364, 'ثاندر')]:
    S[f'{i:05d}'] = [(f'{o} التناغم', f'{ar(o)} التناغم')]
for i, o in [(16367, 'فاير'), (16368, 'بليزارد'), (16369, 'ثاندر'), (16370, 'إيرو'), (16371, 'كيور')]:
    S[f'{i:05d}'] = [(f'دونالد {o}', f'{ar(o)} دونالد')]
S['16064'] = [('فايراغا المظلمة', SPELL['Dark Firaga'])]
S['16110'] = [('زئير فايراغا', 'زئير النار الكبرى')]
S['16111'] = [('قفزة فايراغا', 'قفزة النار الكبرى')]
S['10346'] = S['16110'] + S['16111']
S['12294'] = [('مخالب بليزارد', 'مخالب الجليد'), ('شفرات بليزارد', 'نصال الجليد')]
S['14803'] = [('بلا كيور', 'بلا شفاء')]
S['14816'] = [('سحر كيور', 'سحر الشفاء')]
for i in ('16663', '16702', '16752'):
    S[i] = [('سحر <color(strong)>كيور<color>', 'سحر <color(strong)>الشفاء<color>')]
S['16728'] = [('<color(strong)>كيورازا<color>', '<color(strong)>شفاء أقصى<color>')]
for i, o in [(16747, 'فايرازا'), (16748, 'بليزازا'), (16749, 'ثاندازا'), (16750, 'ووترزا'), (16751, 'إيروزا')]:
    S[f'{i:05d}'] = [(f'<color(strong)>{o}<color>', f'<color(strong)>{ar(o)}<color>')]
S['16756'] = [('مثل فايرازا', 'مثل نار قصوى')]
for i in ('16958', '16987'):
    S[i] = [('هجوم دارك فايراغا المنقسم', 'هجوم النار الكبرى المظلمة المنقسم')]
S['17033'] = [('سحر بليزارد', 'سحر الجليد')]
S['17063'] = [('سحر <color(strong)>بليزارد<color>', 'سحر <color(strong)>الجليد<color>')]
for i in ('17190', '17192'):
    S[i] = [('<color(strong)>فاير<color>', '<color(strong)>نار<color>')]
S['15480'] = [('تعويذة ماء أو بليزارد', 'تعويذة ماء أو جليد')]
S['15481'] = [('تعويذة فاير', 'تعويذة نار')]
S['15487'] = [('تعويذة بليزارد', 'تعويذة جليد')]
S['15492'] = [('سحر بليزارد', 'سحر الجليد')]
S['15512'] = [('بتعاويذ بليزارد', 'بتعاويذ الجليد')]
S['15514'] = [('فبليزارد بدلا منها', 'فالجليد بدلا منها'), ('شيء ما فاير', 'شيء ما نار')]

# glossary: (en, ar, type) rows replaced or added
GLOSS = [(en, a, 'magic') for en, a in SPELL.items() if ' ' not in en] + [
    (en, a, 'term') for en, a in SPELL.items() if ' ' in en]


def main():
    rows = {r['id']: r for r in load_translation()}
    out = [['id', 'old_AR', 'new_AR', 'reason']]
    for i, subs in sorted(S.items()):
        old = rows[i]['AR']
        new = old
        for a, b in subs:
            assert a in new, (i, a)
            new = new.replace(a, b)
        out.append([i, old, new, f'FULL-1 Part B magic names ({NOTE})'])
    write_tsv(os.path.join(ROOT, 'review', 'corrections', 'full1_magic.tsv'), out)

    g = read_tsv(GLOSSARY)
    have = {r[0]: r for r in g[1:]}
    for en, a, typ in GLOSS:
        if en in have:
            r = have[en]
            r[1], r[4] = a, 'approved'
            r[7] = f'{NOTE}: replaces the transliterated form' + ('' if not r[7] else f' (was: {r[7][:60]})')
        else:
            g.append([en, a, typ, 'FULL-1', 'approved', '0', '', f'{NOTE}: new row'])
    write_tsv(GLOSSARY, g)
    print(f'full1_magic.tsv: {len(out) - 1} rows; glossary: {len(GLOSS)} magic terms set')


if __name__ == '__main__':
    main()
