r"""Generate review\script\ (FULL-1 Part E): the reference script for translation and review, Markdown only.
Story script (script_NNN.md): every cutscene subtitle (kh3_event_*, Re Mind *_dlc included) in story order, then the
field/battle voice (kh3_fieldvoice_*: banter, NPC talk, battle lines) per world in story order. Story order = the
Theater scene table (UI/Data/TheaterSceneData, read-only copy in out\builds\FULL-1\ref\data, order kept in
technical\theater_order.tsv): its cutscene list gives the order of 264 events and their scene titles (kh3_menu.theater); events not in the Theater go after the Theater event of
the same world with the next lower number. Speaker = the speaker code inside the key (voice-file id, e.g. sr in
bt9070160sr0) or the character prefix of field-voice keys (sora_0330); no speaker-name table exists in the game data.
TIPS pages (tips_NN.md) hold every other row (loading posts, game-over hints, tutorials, journal, menus and settings,
items) in game order. 300 rows per page; INDEX.md = chapter -> scene -> page, row counts, translated %.
Usage: python -I tools/make_script.py   (run by tools\refresh.bat)"""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tsvlib import *
from make_review import esc, write, pct

PAGE = 300
OUT = os.path.join(ROOT, 'review', 'script')
THEATER = os.path.join(ROOT, 'out', 'builds', 'FULL-1', 'ref', 'data', 'KINGDOM HEARTS III', 'Content', 'UI', 'Data',
                       'TheaterSceneData.uexp')
ORDER = os.path.join(ROOT, 'technical', 'theater_order.tsv')
EVENT = re.compile(r'^([a-z]{2})(\d{3})')
SPEAKER = re.compile(r'^[a-z]{2}\d{7}([a-z]{2})\d')
TIPS = [('Loading screen posts', lambda r: r['stem'] == 'kh3_extraload'),
        ('Game-over hints', lambda r: r['namespace'] == 'kh3_system.gameoverhint'),
        ('Tutorials and Game Help', lambda r: r['stem'] in ('kh3_tutorial', 'kh3_gamehelp')),
        ('Journal (Gummiphone)', lambda r: r['stem'] == 'kh3_mobile'),
        ('Items, abilities and commands', lambda r: r['category'] == 'items_abilities'),
        ('Menus and settings', lambda r: True)]


def theater():
    r"""-> [(event id, scene key or '')] in Theater order, from technical\theater_order.tsv; written once from the
    game table (a row's cutscene list comes before its scene title key) if the TSV is missing"""
    if not os.path.exists(ORDER):
        u = open(THEATER, 'rb').read()
        out, pending, seen = [], [], set()
        for m in re.finditer(rb'TexturePump/cutscene_[a-z0-9]+_([a-z]{2}\d{3}[a-z0-9-]*)\.|kh3_menu\.theater\.(scene_\d+_\d+)', u):
            if m[1]:
                if m[1].decode() not in seen:
                    seen.add(m[1].decode())
                    pending.append(m[1].decode())
            else:
                out += [(e, m[2].decode()) for e in pending]
                pending = []
        write_tsv(ORDER, [['event', 'theater_scene_key']] + [list(x) for x in out + [(e, '') for e in pending]])
    return [tuple(r) for r in read_tsv(ORDER)[1:]]


def natural(s):
    return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', s)]


def story(rows):
    """-> ordered [(chapter, scene label, rows)] for cutscenes, then field voice per world"""
    th = theater()
    tid = {e: i for i, (e, _) in enumerate(th)}
    title = {r['key']: r['EN'] for r in rows if r['namespace'] == 'kh3_menu.theater'}
    world = {r['key'][6:]: r['EN'] for r in rows if r['namespace'] == 'kh3_map.wm' and r['key'].startswith('world_')}
    by_ns = {}
    for r in rows:
        if r['stem'].startswith(('kh3_event_', 'kh3_fieldvoice_')):
            by_ns.setdefault(r['namespace'], []).append(r)

    def place(ev):
        """sort key of an event namespace suffix (bt052a): Theater index, or after the same world's lower event"""
        hit = max((e for e in tid if ev.startswith(e)), key=len, default=None)
        if hit:
            return (tid[hit], 0, natural(ev)), hit
        m = EVENT.match(ev)
        if not m:
            return (len(th), ev[:2], natural(ev)), None
        same = [(int(EVENT.match(e)[2]), e) for e in tid if e[:2] == m[1] and EVENT.match(e)]
        lower = [x for x in same if x[0] <= int(m[2])]
        if lower:
            e = max(lower)[1]
            return (tid[e], 1, natural(ev)), e
        if same:
            e = min(same)[1]
            return (tid[e], -1, natural(ev)), e
        return (len(th), ev[:2], natural(ev)), None

    events = []
    for ns, rs in by_ns.items():
        if ns.startswith('kh3_event_'):
            ev = ns.split('.', 1)[1]
            key, anchor = place(ev)
            events.append((key, ev, anchor, sorted(rs, key=lambda r: natural(r['key']))))
    events.sort(key=lambda x: x[0])
    scene_of = dict(th)
    out, chapter = [], 'Prologue'
    for _, ev, anchor, rs in events:
        sk = scene_of.get(anchor, '') if anchor else ''
        if sk:
            chapter = title.get('chapter_' + sk.split('_')[1], chapter)
        label = f'{ev} — {title[sk]}' if sk and anchor and ev.startswith(anchor) and sk in title else ev
        out.append((chapter, label, rs))
    # field / battle voice: worlds in the order they first appear in the story
    order = []
    for _, ev, _, _ in events:
        if ev[:2] not in order:
            order.append(ev[:2])
    wcode = lambda ns: ns.split('.')[0].replace('kh3_fieldvoice_', '').replace('town_', '').replace('_dlc', '')
    fv = sorted((ns for ns in by_ns if ns.startswith('kh3_fieldvoice_')),
                key=lambda ns: (order.index(wcode(ns)) if wcode(ns) in order else 99, ns))
    for ns in fv:
        stem, grp = ns.split('.', 1)
        name = world.get(wcode(ns), wcode(ns))
        out.append((f'Field and battle voice — {name}' + (' (Re Mind)' if stem.endswith('_dlc') else ''),
                    f'{stem[4:]} {grp}', sorted(by_ns[ns], key=lambda r: natural(r['key']))))
    return out


def speaker(r):
    m = SPEAKER.match(r['key'])
    if m:
        return m[1]
    m = re.match(r'^([a-z]+(?:_[a-z]+)?)_\d', r['key'])
    return m[1] if m and r['stem'].startswith('kh3_fieldvoice_') else '—'


def pages(prefix, units, cols):
    """units = [(section, scene, rows)] -> page files; returns [(section, scene, n, translated, page names)]"""
    flat = [(sec, sc, r) for sec, sc, rs in units for r in rs]
    n = (len(flat) + PAGE - 1) // PAGE
    where = {}
    for p in range(n):
        chunk = flat[p * PAGE:(p + 1) * PAGE]
        fn = f'{prefix}_{p + 1:03d}.md'
        L = [f'# {"Script" if prefix == "script" else "Tips, menus and texts"} — page {p + 1}/{n}', '',
             f'[Index]({"INDEX.md" if prefix == "script" else "TIPS.md"}) · rows {p * PAGE + 1}–{p * PAGE + len(chunk)}', '']
        last = None
        for sec, sc, r in chunk:
            if (sec, sc) != last:
                L += ['', f'### {esc(sec)} · {esc(sc)}', '', '| ' + ' | '.join(cols) + ' |', '|' + '---|' * len(cols)]
                last = (sec, sc)
                where.setdefault((sec, sc), []).append(fn)
            cells = [r['id'], esc(sc)] + ([speaker(r)] if 'speaker' in cols else []) + [esc(r['EN']), esc(r['AR'])]
            L.append('| ' + ' | '.join(cells) + ' |')
        write(os.path.join(OUT, fn), L)
    return [(sec, sc, len(rs), sum(r['status'] != 'todo' for r in rs), where.get((sec, sc), [])) for sec, sc, rs in units]


def index(path, title, intro, summary):
    L = [f'# {title}', '', intro, '', '| section | scene | rows | translated | pages |', '|---|---|---|---|---|']
    tot = [0, 0]
    for sec, sc, n, t, pg in summary:
        L.append(f'| {esc(sec)} | {esc(sc)} | {n} | {pct(t, n)} | {" ".join(f"[{p[:-3]}]({p})" for p in pg)} |')
        tot[0] += n
        tot[1] += t
    L.insert(4, f'**Total: {tot[0]:,} rows, translated {pct(tot[1], tot[0])}.**')
    L.insert(5, '')
    write(path, L)
    return tot


def main():
    rows = load_translation()
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    st = story(rows)
    used = {r['id'] for _, _, rs in st for r in rs}
    s1 = pages('script', st, ['id', 'scene', 'speaker', 'EN', 'AR'])
    rest = [r for r in rows if r['id'] not in used]
    tips = []
    for name, test in TIPS:
        take = [r for r in rest if test(r)]
        rest = [r for r in rest if not test(r)]
        groups = {}
        for r in take:
            groups.setdefault(r['namespace'], []).append(r)
        tips += [(name, ns, rs) for ns, rs in groups.items()]
    s2 = pages('tips', tips, ['id', 'scene', 'EN', 'AR'])
    a = index(os.path.join(OUT, 'INDEX.md'), 'Master script — story order',
              'Reference script for translation and review (generated by `tools\\make_script.py`, refreshed by `tools\\refresh.bat`; '
              'do not edit by hand, fix rows through `review\\corrections\\`). Story order = the game\'s Theater scene table; '
              'speaker = voice code from the key (e.g. `sr`, `do`, `go`) or the field-voice prefix (`sora`); the game has no '
              'speaker-name table. Menus, tips, tutorials, journal and items: [TIPS.md](TIPS.md).', s1)
    b = index(os.path.join(OUT, 'TIPS.md'), 'Tips, tutorials, journal, menus and settings',
              'Every row that is not a cutscene or voice line, in game order (id order) per section. Back to the story: '
              '[INDEX.md](INDEX.md).', s2)
    assert a[0] + b[0] == len(rows), (a, b, len(rows))
    print(f'make_script: story {a[0]} rows ({len(s1)} scenes), tips {b[0]} rows, pages {len(os.listdir(OUT)) - 2}')


if __name__ == '__main__':
    main()
