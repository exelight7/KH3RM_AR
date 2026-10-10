"""Arabic pre-shaper for KH3 Scaleform text (technical/SHAPER_SPEC.md §1-6; §8 checks in tools/test_shaper.py).

shape(text)                 logical Arabic -> presentation forms, each line in visual (left-to-right drawing) order
shape(text, reverse=False)  presentation forms, logical order (ARABIC-TEST-1 variant C)
unshape(visual)             inverse of shape(): logical base letters, style tags re-emitted in logical order
Tokens: <br>/<Br>/real line breaks and <pb>/<pb(N)> split lines (each line shaped and reordered on its own, line order
kept); <color(X)>..<color>, <i(on)>/<i(off)>/<I(off)>, <b(on)>/<b(off)> become per-character style state and are
re-emitted after reordering (tags tight around the styled characters, closed at each line end); <icon(..)>, {n},
<conv(..)>..<conv(off)> and {n}|plural(..) are neutral atoms (each plural form is shaped as its own line);
<nbsp> is a whitespace atom; adjacent icons form one atom (button diagrams keep their drawn order). A row wrapped in
one <conv(X)>..<conv(off)> pair (conv hoisted to the string start / end, BUILD-1) keeps the pair and shapes the inside.
Bidi = UAX #9 rules W1-W7, N1-N2, I1-I2, L1, L2, L4 with paragraph level 1 (RTL).
wrap(text, width, measure) (SHAPER_SPEC §7, BUILD-1) inserts <br> into the logical text at spaces (never inside
tags/args/plural/conv groups or between two LTR characters) so that no line is wider than the field; meter() builds
the measure function from a font's glyph advances.
Limits: unshape() re-runs the same bidi pass on the visual line; UAX #9 is not injective in general (a number run
followed by a Latin run gives the same visual string as the Latin run followed by the number), test_shaper.py checks
the round trip on the real rows.
Usage: python -I shaper.py "<logical text>"   -> prints the shaped string and its U+ code points
"""
import re, sys, unicodedata

# (base letter -> {form: code point}) and lam-alef ligatures, from the Unicode decompositions of the presentation forms
FORMS, LIGA, BASE = {}, {}, {}
for cp in list(range(0xFE70, 0xFEFD)) + list(range(0xFB50, 0xFBB0)):
    dec = unicodedata.decomposition(chr(cp)).split()
    if len(dec) < 2 or dec[0] not in ('<isolated>', '<final>', '<initial>', '<medial>'):
        continue
    form, letters = dec[0][1:-1], ''.join(chr(int(h, 16)) for h in dec[1:])
    if cp >= 0xFF00 or (cp < 0xFE70 and letters not in 'پچڤگ'):
        continue  # FB50-FBFF: only the optional letters for foreign names (SHAPER_SPEC §3.4)
    if len(letters) == 1 and unicodedata.category(letters) == 'Lo':
        FORMS.setdefault(letters, {})[form] = chr(cp)
    elif len(letters) == 2 and letters[0] == 'ل':
        LIGA.setdefault(letters[1], {})[form] = chr(cp)
    BASE[chr(cp)] = letters
DUAL = {c for c, f in FORMS.items() if 'initial' in f}  # joins on both sides; others join right only (or none)
MARKS = {chr(c) for c in range(0x064B, 0x0653)} | {'ٰ', 'ـ'}
MIRROR = dict(zip('()[]{}«»<>‹›', ')(][}{»«><›‹'))
NONE = (None, False, False)  # style state: (open color tag, italic, bold)
TOKEN = re.compile(r'<[Bb]r>|\r?\n|<pb(?:\([^)]*\))?>|<color(?:\([^)]*\))?>|<[iI]\((?:on|off)\)>|<b\((?:on|off)\)>'
                   r'|<conv\([^)]*\)>|<icon\([^)]*\)>|<nbsp>|\{\d+\}(?:\|plural\()?|<[^<>]*>')
PLURAL_KW = re.compile(r',(?=(?:zero|one|two|few|many|other)=)')
CONV = re.compile(r'(<conv\((?!off\))[^)]*\)>)((?:(?!<conv\().)*)(<conv\(off\)>)', re.S)  # whole-row conv pair
BREAK = re.compile(r'(<[Bb]r>|\r?\n|<pb(?:\([^)]*\))?>)')


def is_arabic(c):
    return '؀' <= c <= 'ۿ' or 'ﭐ' <= c <= '﷿' or 'ﹰ' <= c <= 'ﻼ'


def has_letters(text):
    return any('ء' <= c <= 'ي' or 'ٮ' <= c <= 'ۓ' or 'ﭐ' <= c <= 'ﻼ' for c in text)


def close_paren(text, p):
    """index of the ')' that closes the '(' just before p"""
    depth = 1
    for i in range(p, len(text)):
        depth += {'(': 1, ')': -1}.get(text[i], 0)
        if depth == 0:
            return i
    raise ValueError('unclosed plural: ' + text)


def tokenize(text):
    """-> list of (kind, value); kind: br (line/page break), style, atom, ws (<nbsp>), char.
    Plural blocks come back as ('plural', (head, [(keyword, form text)])) ."""
    out, p = [], 0
    while p < len(text):
        m = TOKEN.match(text, p)
        if not m:
            out.append(('char', text[p]))
            p += 1
            continue
        s, p = m.group(), m.end()
        if s.endswith('|plural('):
            end = close_paren(text, p)
            forms_ = [f.split('=', 1) for f in PLURAL_KW.split(text[p:end])]
            assert all(len(f) == 2 for f in forms_), 'bad plural: ' + text
            out.append(('plural', (s, forms_)))
            p = end + 1
        elif s.startswith('<conv(') and s != '<conv(off)>':
            stop = [q for q in (text.find('<conv(off)>', p),) if q >= 0]
            br = TOKEN.search(text, p)
            while br and not re.fullmatch(r'<[Bb]r>|\r?\n|<pb(?:\([^)]*\))?>', br.group()):
                br = TOKEN.search(text, br.end())
            end = min(stop[0] + 11 if stop else len(text), br.start() if br else len(text))
            if has_letters(text[p:end]):
                raise ValueError('Arabic inside a <conv> group is not supported: ' + text)
            out.append(('atom', s + text[p:end]))
            p = end
        elif re.fullmatch(r'<[Bb]r>|\r?\n|<pb(?:\([^)]*\))?>', s):
            out.append(('br', s))
        elif re.fullmatch(r'<color(?:\([^)]*\))?>|<[iI]\((?:on|off)\)>|<b\((?:on|off)\)>', s):
            out.append(('style', s))
        elif s == '<nbsp>':
            out.append(('ws', s))
        elif s.startswith(('<icon(', '{', '<conv(')):
            out.append(('atom', s))
        else:
            raise ValueError(f'unknown tag {s}: {text}')
    return out


def styled(tokens, fn):
    """tokens -> lines of [(token, state)] and their separators; plural forms rewritten by fn(form text)."""
    lines, seps, cur, st = [[]], [], [], NONE
    for kind, v in tokens:
        if kind == 'br':
            seps.append(v)
            lines.append([])
        elif kind == 'style':
            c, i, b = st
            if v.startswith('<color('):
                c = v
            elif v == '<color>':
                c = None
            elif v[1] in 'iI':
                i = v.endswith('(on)>')
            else:
                b = v.endswith('(on)>')
            st = (c, i, b)
        elif kind == 'plural':
            head, fs = v
            lines[-1].append((head + ','.join(k + '=' + fn(f) for k, f in fs) + ')', st))
        elif kind == 'ws':
            lines[-1].append((' ' + v, st))  # leading space marks the whitespace atom (bidi WS), stripped on emit
        elif v.startswith('<icon(') and lines[-1] and lines[-1][-1][0].startswith('<icon(') and lines[-1][-1][1] == st:
            lines[-1][-1] = (lines[-1][-1][0] + v, st)  # icon cluster = one atom
        else:
            lines[-1].append((v, st))
    return lines, seps


def forms(units):
    """[(token, state)] -> same with Arabic letters in presentation forms (lam-alef = one glyph)."""
    out, i = [], 0
    while i < len(units):
        c, st = units[i]
        if c not in FORMS:
            out.append(units[i])
            i += 1
            continue
        right = i > 0 and units[i - 1][0] in DUAL  # previous letter connects to this one
        if c == 'ل' and i + 1 < len(units) and units[i + 1][0] in LIGA:
            out.append((LIGA[units[i + 1][0]]['final' if right else 'isolated'], st))
            i += 2
            continue
        left = c in DUAL and i + 1 < len(units) and units[i + 1][0] in FORMS
        form = {(0, 0): 'isolated', (1, 0): 'final', (0, 1): 'initial', (1, 1): 'medial'}[(right, left)]
        out.append((FORMS[c].get(form, FORMS[c]['isolated']), st))
        i += 1
    return out


def bidi_type(t):
    if t.startswith(' <'):
        return 'WS'
    if len(t) > 1:
        return 'ON'  # atoms are neutral
    return unicodedata.bidirectional(t) or 'ON'


def levels(types):
    """UAX #9 for one line, paragraph level 1, no explicit embeddings: bidi types -> embedding levels 1/2."""
    t, n = list(types), len(types)
    for i in range(n):  # W1
        if t[i] == 'NSM':
            t[i] = t[i - 1] if i else 'R'
    last = 'R'
    for i in range(n):  # W2
        if t[i] in ('L', 'R', 'AL'):
            last = t[i]
        elif t[i] == 'EN' and last == 'AL':
            t[i] = 'AN'
    t = ['R' if x == 'AL' else x for x in t]  # W3
    for i in range(1, n - 1):  # W4
        if t[i] == 'ES' and t[i - 1] == t[i + 1] == 'EN' or t[i] == 'CS' and t[i - 1] == t[i + 1] in ('EN', 'AN'):
            t[i] = t[i - 1]
    i = 0
    while i < n:  # W5
        j = i
        while j < n and t[j] == 'ET':
            j += 1
        if j > i and (i and t[i - 1] == 'EN' or j < n and t[j] == 'EN'):
            t[i:j] = ['EN'] * (j - i)
        i = max(j, i + 1)
    t = ['ON' if x in ('ES', 'ET', 'CS') else x for x in t]  # W6
    last = 'R'
    for i in range(n):  # W7
        if t[i] in ('L', 'R'):
            last = t[i]
        elif t[i] == 'EN' and last == 'L':
            t[i] = 'L'
    strong = lambda x: 'R' if x in ('R', 'EN', 'AN') else 'L'
    i = 0
    while i < n:  # N1/N2: neutrals between same-direction strongs take it, else the paragraph direction (R)
        if t[i] in ('L', 'R', 'EN', 'AN'):
            i += 1
            continue
        j = i
        while j < n and t[j] not in ('L', 'R', 'EN', 'AN'):
            j += 1
        a, b = (strong(t[i - 1]) if i else 'R'), (strong(t[j]) if j < n else 'R')
        t[i:j] = [a if a == b else 'R'] * (j - i)
        i = j
    lv = [1 if x == 'R' else 2 for x in t]  # I1/I2 at level 1
    for k in range(n - 1, -1, -1):  # L1: trailing whitespace back to the paragraph level
        if types[k] not in ('WS', 'S', 'B', 'BN'):
            break
        lv[k] = 1
    return lv


def reorder(units, lv=None):
    """L2 + L4: visual order of one line; with the same levels it is its own inverse."""
    lv = (lv or levels([bidi_type(t) for t, _ in units]))[::-1]
    out, i = units[::-1], 0
    while i < len(out):
        if lv[i] == 2:
            j = i
            while j < len(out) and lv[j] == 2:
                j += 1
            out[i:j] = out[i:j][::-1]
            i = j
        else:
            out[i] = (MIRROR.get(out[i][0], out[i][0]), out[i][1])
            i += 1
    return out


def emit(units):
    """[(token, state)] (state None = line separator) -> text; tags sit tight around the styled tokens."""
    out, cur, pend = [], NONE, []
    for tok, st in units + [('', NONE)]:
        if st is None:
            pend.append(tok)
            continue
        if st != cur:
            (c0, i0, b0), (c1, i1, b1) = cur, st
            out += (['<b(off)>'] if b0 and not b1 else []) + (['<i(off)>'] if i0 and not i1 else []) + \
                   (['<color>'] if c0 and c0 != c1 else [])
            out += pend
            out += ([c1] if c1 and c0 != c1 else []) + (['<i(on)>'] if i1 and not i0 else []) + \
                   (['<b(on)>'] if b1 and not b0 else [])
            cur = st
        else:
            out += pend
        pend = []
        out.append(tok.lstrip(' ') if tok.startswith(' <') else tok)
    return ''.join(out)


def check(text):
    if MARKS & set(text):
        raise ValueError('harakat/tatweel are not allowed: ' + text)


def shape(text, reverse=True):
    if not has_letters(text):
        return text  # SHAPER_SPEC §1 passthrough
    m = CONV.fullmatch(text)
    if m:
        return m[1] + shape(m[2], reverse) + m[3]
    check(text)
    lines, seps = styled(tokenize(text), lambda f: shape_line(f, reverse))
    out = [emit((reorder if reverse else list)(forms(l))) for l in lines]
    return ''.join(x for pair in zip(out, seps + ['']) for x in pair)


def shape_line(text, reverse=True):
    """one plural form: always processed (even without Arabic) so forms read the same way as their line"""
    check(text)
    lines, _ = styled(tokenize(text), lambda f: shape_line(f, reverse))
    assert len(lines) == 1, 'line break inside a plural form: ' + text
    return emit((reorder if reverse else list)(forms(lines[0])))


def base(units):
    return [(c, st) for t, st in units for c in (BASE[t] if t in BASE else (t,))]  # lam-alef -> 2 letters


def logical(vis, reversed_=True):
    """visual units of one line -> logical base units. The bidi levels are recomputed on the visual line, or, if that
    does not shape back to the same line, on the reversed visual line (W2/W7 search backwards: digits after Arabic)."""
    if not reversed_:
        return base(vis)
    first = None
    for src in (vis, vis[::-1]):
        lv = levels([bidi_type(t) for t, _ in src])
        cand = base(reorder(vis, lv if src is vis else lv[::-1]))
        if reorder(forms(cand)) == vis:
            return cand
        first = first or cand
    return first


def unshape(text, reversed_=True):
    if not has_letters(text):
        return text
    m = CONV.fullmatch(text)
    if m:
        return m[1] + unshape(m[2], reversed_) + m[3]
    lines, seps = styled(tokenize(text), lambda f: unshape_line(f, reversed_))
    units = []
    for i, l in enumerate(lines):
        units += logical(l, reversed_) + ([(seps[i], None)] if i < len(seps) else [])
    return emit(units)


def unshape_line(text, reversed_=True):
    lines, _ = styled(tokenize(text), lambda f: unshape_line(f, reversed_))
    return emit(logical(lines[0], reversed_))


def normalize(text):
    """logical text with style tags in the canonical places shape()/unshape() use (SHAPER_SPEC §8.1)"""
    return unshape(shape(text, reverse=False), reversed_=False)


def meter(adv, icon=320, arg=None, missing=None):
    """-> measure(logical text): width in font units (256 = 1 em = size in px) of its widest line after shaping:
    glyph advances from adv {code: advance}, icon = width of one <icon(..)>, arg = width of one {n} (default '0000'),
    a plural block counts its widest form. ponytail: icon/arg widths are estimates (calibration knobs)."""
    arg = 4 * adv.get(0x30, 128) if arg is None else arg
    miss = adv.get(0x3F, 128) if missing is None else missing

    def atom(v):
        return icon * v.count('<icon(') + arg * len(re.findall(r'\{\d+\}', v))

    def line(tokens):
        w = 0
        for kind, v in tokens:
            if kind == 'char':
                w += adv.get(ord(v), miss)
            elif kind == 'ws':
                w += adv.get(0xA0, adv.get(0x20, miss))
            elif kind == 'atom':
                w += atom(v)
            elif kind == 'plural':
                w += max(measure(f) for _, f in v[1])
        return w

    def measure(text):
        m = CONV.fullmatch(text)
        v = shape(m[2] if m else text)
        out, cur = [], []
        for t in tokenize(v):
            if t[0] == 'br':
                out.append(cur)
                cur = []
            else:
                cur.append(t)
        return max(line(t) for t in out + [cur])
    return measure


def ltr(c):
    return bool(c) and unicodedata.bidirectional(c) in ('L', 'EN')


def gaps(line):
    """(start, end) of the space runs where one logical line may break: outside tags, {n}, plural blocks and conv
    groups, and not inside an LTR run (Latin/digits on both sides, e.g. 'KINGDOM HEARTS', 'HP 80')"""
    out, p = [], 0
    while p < len(line):
        m = TOKEN.match(line, p)
        if m:
            s, p = m.group(), m.end()
            if s.endswith('|plural('):
                p = close_paren(line, p) + 1
            elif s.startswith('<conv(') and s != '<conv(off)>':
                q = line.find('<conv(off)>', p)
                p = len(line) if q < 0 else q + 11
            continue
        if line[p] != ' ':
            p += 1
            continue
        q = p
        while q < len(line) and line[q] == ' ':
            q += 1
        if 0 < p and q < len(line) and not (ltr(line[p - 1]) and ltr(line[q])):
            out.append((p, q))
        p = q
    return out


def wrap(text, width, measure):
    """SHAPER_SPEC §7: logical text -> same text with <br> in place of the space runs where a line gets wider than
    width (greedy, first fit). Existing <br>/<pb> are kept; a single word wider than width stays whole."""
    m = CONV.fullmatch(text)
    if m:
        return m[1] + wrap(m[2], width, measure) + m[3]
    if not has_letters(text):
        return text
    parts = BREAK.split(text)
    for i in range(0, len(parts), 2):
        line = parts[i]
        if measure(line) <= width:
            continue
        out, start, cut = [], 0, None  # cut = last gap that still fits
        for a, b in gaps(line):
            if measure(line[start:a]) <= width:
                cut = (a, b)
                continue
            if cut:
                out.append(line[start:cut[0]])
                start = cut[1]
                cut = (a, b) if measure(line[start:a]) <= width else None
            if not cut:  # word wider than the line: break after it
                out.append(line[start:a])
                start = b
        if cut and measure(line[start:]) > width:
            out.append(line[start:cut[0]])
            start = cut[1]
        parts[i] = '<br>'.join(out + [line[start:]])
    return ''.join(parts)


FOOTER = re.compile(r'\s*<color\([^)]*\)>[^<]*<color>\s*')


def reflow(text):
    """SHAPER_SPEC §7b (FULL-1): for fields that show fewer lines than the row has, join the body lines (every line
    but a last whole-line <color(..)>..<color> footer) with one space, so wrap() re-breaks them with the fewest lines."""
    lines = text.split('<br>')
    foot = [lines.pop()] if len(lines) > 1 and FOOTER.fullmatch(lines[-1]) else []
    return '<br>'.join([' '.join(l.strip() for l in lines if l.strip())] + foot)


def cps(s):
    return ' '.join(f'U+{ord(c):04X}' for c in s)


def self_check():
    t = lambda s: ''.join(chr(int(x, 16)) for x in s.split())
    cases = [
        ('باب', t('FE8F FE8E FE91')),                                          # plain word
        ('سلام', t('FEE1 FEFC FEB3')),                                         # lam-alef ligature (final)
        ('لعبة جديدة', t('FE93 FEAA FEF3 FEAA FE9F 0020 FE94 FE92 FECC FEDF')),  # ARABIC-TEST-1 string
        ('مستوى 25', '25 ' + t('FEEF FEEE FE98 FEB4 FEE3')),                     # digits stay LTR
        ('<icon(Decide)> التالي', t('FEF2 FEDF FE8E FE98 FEDF FE8D') + ' <icon(Decide)>'),       # atom
    ]
    for logical, want in cases:
        got = shape(logical)
        assert got == want, (logical, cps(got), cps(want))
        assert unshape(got) == logical, (logical, unshape(got))
    assert shape('HP 120') == 'HP 120'                                         # no Arabic: passthrough
    assert shape('لعبة جديدة', reverse=False) == t('FEDF FECC FE92 FE94 0020 FE9F FEAA FEF3 FEAA FE93')


self_check()
if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    s = shape(sys.argv[1])
    print(s)
    print(cps(s))
