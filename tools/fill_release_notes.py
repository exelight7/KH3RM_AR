r"""Fill {{placeholders}} in a release-notes draft from state\STATS.md. Usage: fill_release_notes.py [draft.md] [--write]
Default is a dry run (prints the result and any unfilled placeholder); --write saves docs\RELEASE_NOTES_<name>.md.
Placeholders: rows_total rows_translated rows_translated_pct images_textures images_plan images_repainted images_pct."""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
draft = args[0] if args else os.path.join(ROOT, 'docs', 'RELEASE_DRAFT_0.9.0.md')
cells = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]
vals = {}
for l in open(os.path.join(ROOT, 'state', 'STATS.md'), encoding='utf-8'):
    c = cells(l) if l.startswith('|') else []
    if c[:1] == ['TOTAL']:
        vals.update(rows_total=c[1], rows_translated=c[2].split()[0], rows_translated_pct=c[2].split()[1].strip('()'))
    elif c[:1] == ['all groups']:
        vals.update(images_textures=c[1], images_plan=c[2], images_repainted=c[3], images_pct=c[4])
text = open(draft, encoding='utf-8').read()
out = re.sub(r'\{\{(\w+)\}\}', lambda m: vals.get(m.group(1), m.group(0)), text)
print(out)
miss = sorted(set(re.findall(r'\{\{(\w+)\}\}', out)))
print('unfilled:', miss or 'none', file=sys.stderr)
if '--write' in sys.argv:
    open(os.path.join(ROOT, 'docs', 'RELEASE_NOTES_' + os.path.basename(draft).split('_', 2)[-1]), 'w', encoding='utf-8', newline='\n').write(out)
