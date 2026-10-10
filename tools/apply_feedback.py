r"""Read a filled state\FEEDBACK.tsv (date, build, where, id_or_words, type, note) and write review\FEEDBACK_REPORT.md:
each report with its matched rows (id, EN, AR, status) and 2 neighbours, so one later round can fix them in a batch.
id_or_words = a 5-digit row id or the words seen in game (see find_text.py). Usage: apply_feedback.py [feedback.tsv] [report.md]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
import find_text as ft

COLS_FB = ['date', 'build', 'where', 'id_or_words', 'type', 'note']


def report(fb_rows, rows):
    L = ['# Feedback report', '', f'{len(fb_rows)} reports.', '']
    for n, f in enumerate(fb_rows, 1):
        q = f['id_or_words'].strip()
        hits = [r for r in rows if r['id'] == q] if re.fullmatch(r'\d{5}|I\d{4}', q) else ft.find(q, rows)
        L += [f'## {n}. {q} - {f["type"]}', '', f'date {f["date"]} · build {f["build"]} · where: {f["where"]} · note: {f["note"] or "-"}', '']
        if not hits:
            L += ['No matching row (check spelling, or the text is not in the translation: image, video or font).', '']
        for r in hits[:5]:
            L += [f'- **{r["id"]}** ({r["category"]}, {r.get("key", "")}, {r["status"]})', f'  - EN: {r["EN"]}', f'  - AR: {r["AR"]}']
            for x in ft.around(r, 2, rows):
                if x is not r:
                    L.append(f'  - near {x["id"]}: {x["AR"]}')
        if len(hits) > 5:
            L.append(f'- ... {len(hits) - 5} more matches')
        L.append('')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'state', 'FEEDBACK.tsv')
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'review', 'FEEDBACK_REPORT.md')
    if not os.path.exists(src):
        sys.exit(rf'no {src} (copy state\FEEDBACK_TEMPLATE.tsv to state\FEEDBACK.tsv and fill it)')
    t = read_tsv(src)
    assert t[0] == COLS_FB, t[0]
    fb = [dict(zip(COLS_FB, (r + [''] * 6)[:6])) for r in t[1:] if any(r)]
    open(dst, 'w', encoding='utf-8', newline='\n').write(report(fb, ft.all_rows()))
    print(f'apply_feedback: {len(fb)} reports -> {dst}')
