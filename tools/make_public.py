r"""Regenerate public_repo\ (a clone of github.com/exelight7/KH3RM_AR) from the private project. Never copies game files,
the AES key, English game text (translation files keep Arabic-only columns) or review pages. Run tools\public_check.py after.
Usage: python -I tools\make_public.py          (rebuild public_repo\ content)
       python -I tools\make_public.py --last-round   (print the last round name from state\PROGRESS.md)"""
import glob, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import secret_check

ROOT = secret_check.ROOT
PUB = os.path.join(ROOT, 'public_repo')
KEEP = {'.git', 'LICENSE'}                         # remote content we never touch
TECH = ['RECON_KH3.md', 'SHAPER_SPEC.md', 'FIELD_WIDTHS.tsv', 'TAGS.md', 'IMAGES_PLAN.md']   # + *CHECKLIST.md
COLS = ['id', 'namespace', 'key', 'source_hash', 'AR', 'status', 'note']
NOTE_ID = 'state/PROGRESS.md'
RELEASE = '0.8.3'                                  # README download link (tag)
SETUP = 'KH3RM_AR_Setup_v0.8.2.exe'                # installer attached to that release
IMG_VER = '0.8.2'                                  # out\release\v<IMG_VER>\ui_ar.png screenshot
# double-quoted English phrase of 3+ words (likely game text) -> "..."
QUOTE = re.compile(r'"(?=[^"\n]*[A-Za-z])(?:[^"\n؀-ۿ]*\s){2}[^"\n؀-ۿ]*"')

def last_round():
    lines = [l for l in open(os.path.join(ROOT, NOTE_ID), encoding='utf-8').read().splitlines() if re.match(r'\d{4}-\d\d-\d\d ', l)]
    return lines[-1].split()[1] if lines else 'unknown'

def scrub(text, keys):
    out = [l for l in text.splitlines() if 'KEY_SOURCE' not in l and not any(k in l for k in keys)]
    return QUOTE.sub('"..."', '\n'.join(out)) + '\n'

def put(rel, text):
    p = os.path.join(PUB, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(text)

def doc(rel, keys, src=None):
    put(rel, scrub(open(os.path.join(ROOT, src or rel), encoding='utf-8').read(), keys))

def tools_copy(rel):
    if os.path.isdir(os.path.join(ROOT, rel)):
        for f in sorted(os.listdir(os.path.join(ROOT, rel))):
            if f.startswith(('repak-', 'gh-')) or f in ('__pycache__', 'KEY_SOURCE.txt', 'bin', 'obj'): continue
            tools_copy(rel + '/' + f)
    else:
        os.makedirs(os.path.dirname(os.path.join(PUB, rel)), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, rel), os.path.join(PUB, rel))

def translation(keys):
    n = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'translation', '*', '*.tsv'))):
        cat, name = os.path.basename(os.path.dirname(p)), os.path.basename(p)
        lines = open(p, encoding='utf-8').read().splitlines()
        h = lines[0].split('\t')
        out = ['\t'.join(COLS)]
        for l in lines[1:]:
            c = (l.split('\t') + [''] * len(h))[:len(h)]
            r = dict(zip(h, c))
            if '"' in r.get('note', ''): r['note'] = ''
            out.append('\t'.join(r.get(k, '') for k in COLS))
            n += 1
        put(f'translation/ar/{cat}/{name}', '\n'.join(out) + '\n')
    for g in ('glossary.md', 'glossary.tsv'):
        doc('translation/' + g, keys)
    return n

def readme():
    stats = open(os.path.join(ROOT, 'state', 'STATS.md'), encoding='utf-8').read()
    t = [c.strip() for c in next(l for l in stats.splitlines() if l.startswith('| TOTAL')).strip('|').split('|')]
    pct = lambda s: s.split('(')[1].rstrip(')') if '(' in s else s
    cov = re.search(r'= (\d+) / (\d+) \(([\d.]+%)\)', stats)
    v = {'VER': RELEASE, 'SETUP': SETUP, 'TRANSLATABLE': f'{int(cov.group(1)):,}', 'TRANSLATABLE_PCT': cov.group(3),
         'VERIFIED': pct(t[5]), 'VERROWS': f"{int(t[5].split()[0]):,}"}
    s = open(os.path.join(ROOT, 'tools', 'public_templates', 'README.md'), encoding='utf-8').read()
    return re.sub(r'\{\{(\w+)\}\}', lambda m: v[m.group(1)], s)

def main():
    keys = secret_check.key_values()
    for f in os.listdir(PUB):
        if f in KEEP: continue
        p = os.path.join(PUB, f)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    put('README.md', readme())
    for f in ('PROJECT_MAP.md', 'CHANGELOG.md', 'FAQ.md', '.github/ISSUE_TEMPLATE/bug_report.yml', 'docs/TESTER_GUIDE.md'): doc(f, keys)
    put('LICENSE_TODO.md', '# الترخيص — لم يُحسم بعد\n\nلم يختر صاحب المشروع ترخيصا بعد. إلى ذلك الحين: كل الحقوق محفوظة لنصنا العربي؛ '
        'ترجمة غير رسمية من المعجبين، لا علاقة لها بـ Square Enix أو Disney. ملف `LICENSE` في هذا المستودع هو الملف الافتراضي '
        '(GPL v2) الذي أنشأه GitHub مع المستودع، وليس قرارا بشأن نص الترجمة.\n')
    for f in ('docs/INDEX.md', 'docs/SUPERVISOR.md', 'state/STATS.md', 'state/PROGRESS.md', 'review/RULES.md'): doc(f, keys)
    for f in sorted(glob.glob(os.path.join(ROOT, 'docs', 'rounds', '*.md'))): doc('docs/rounds/' + os.path.basename(f), keys)
    tech = TECH + sorted(os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'technical', '*CHECKLIST.md')))
    for f in tech: doc('technical/' + f, keys)
    n = translation(keys)
    img = os.path.join(ROOT, 'out', 'release', 'v' + IMG_VER, 'ui_ar.png')
    if os.path.exists(img):
        os.makedirs(os.path.join(PUB, 'docs', 'img'), exist_ok=True)
        shutil.copyfile(img, os.path.join(PUB, 'docs', 'img', 'ui_ar.png'))
    for f in sorted(os.listdir(os.path.join(ROOT, 'tools'))):
        if f.startswith(('repak-', 'gh-')) or f in ('__pycache__', 'KEY_SOURCE.txt', 'bin', 'obj'): continue
        tools_copy('tools/' + f)
    for f in sorted(glob.glob(os.path.join(ROOT, '*.bat'))): tools_copy(os.path.basename(f))
    print(f'make_public: {n} translation rows written to {PUB}')

if __name__ == '__main__':
    if '--last-round' in sys.argv: print(last_round())
    else: main()
