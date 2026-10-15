r"""Read-only adapter for BUILD-16. This file does not build or install anything.
BUILD-16: a copy of tools\font_swap_adapter.py; the TresFont now comes from out/builds/BUILD-16/TresFont (tools\ya_restore16.py:
the BUILD-15 font with the 6 ya glyphs restored from BUILD-14, i.e. byte-identical to the BUILD-14 pair), pinned by PINNED16. Baseline / K / join info still come from out/fonts_gpt/analysis.json (advances unchanged),
whose own hashes must still be the BUILD-14 pair this font equals."""
from pathlib import Path
import hashlib, json, math
import font_swap_adapter as f14

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/fonts_gpt'
FONT16 = ROOT / 'out/builds/BUILD-16/TresFont'
IDS = f14.IDS
PINNED = f14.PINNED  # BUILD-14 pair (the source of the BUILD-16 font)
PINNED16 = {'TresFont.uasset': '450b6b0493ec702eed50dc49b082784ce70f994480a4ab3c59bbf6480b871e58',
            'TresFont.uexp': '172aa8cc858f9966dc54edb027013ba212cfa042129b61f1d625cdbdccfcc5c7'}

def analysis():
    return json.loads((OUT/'analysis.json').read_text(encoding='utf-8'))

def font_bytes(_g=None):
    """Drop-in replacement for build_build1.font_bytes; keep its return contract."""
    m=analysis()
    contents=[]
    for name in ['TresFont.uasset','TresFont.uexp']:
        assert m['asset_sha256'][name]==PINNED[name], name
        data=(FONT16/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==PINNED16[name], name
        contents.append(data)
    info={IDS[c['class']]:(c['baseline'],c['original_H_cap'],c['K']) for c in m['classes']}
    return tuple(contents), info

def gaps():
    """Keep build logging consistent with the prepared extension, not old +18."""
    return {IDS[c['class']]:(c['join_extension'],math.ceil(c['max_gap_before'])) for c in analysis()['classes']}
