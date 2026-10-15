r"""Read-only adapter for BUILD-15. This file does not build or install anything.
BUILD-15: a copy of tools\font_swap_adapter.py; the TresFont now comes from out/builds/BUILD-15/TresFont (tools\ya_dots15.py:
the BUILD-14 Plex font with the ya dot contours of U+064A / FEF1 / FEF2 moved into the bowl in $jimakuNE and $sougei, nothing
else changed), pinned by PINNED15. Baseline / K / join info still come from out/fonts_gpt/analysis.json (advances unchanged),
whose own hashes must still be the BUILD-14 pair this font was derived from."""
from pathlib import Path
import hashlib, json, math
import font_swap_adapter as f14

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/fonts_gpt'
FONT15 = ROOT / 'out/builds/BUILD-15/TresFont'
IDS = f14.IDS
PINNED = f14.PINNED  # BUILD-14 pair (the source of the BUILD-15 font)
PINNED15 = {'TresFont.uasset': 'ae5911ef79fae0c8f075a05aff0df30a442a515b5f004dd75279d4c102ac087d',
            'TresFont.uexp': '3f0602200e07fb6ef455c0806f80aa337a427d86b3877b92aae2c1902254777a'}

def analysis():
    return json.loads((OUT/'analysis.json').read_text(encoding='utf-8'))

def font_bytes(_g=None):
    """Drop-in replacement for build_build1.font_bytes; keep its return contract."""
    m=analysis()
    contents=[]
    for name in ['TresFont.uasset','TresFont.uexp']:
        assert m['asset_sha256'][name]==PINNED[name], name
        data=(FONT15/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==PINNED15[name], name
        contents.append(data)
    info={IDS[c['class']]:(c['baseline'],c['original_H_cap'],c['K']) for c in m['classes']}
    return tuple(contents), info

def gaps():
    """Keep build logging consistent with the prepared extension, not old +18."""
    return {IDS[c['class']]:(c['join_extension'],math.ceil(c['max_gap_before'])) for c in analysis()['classes']}
