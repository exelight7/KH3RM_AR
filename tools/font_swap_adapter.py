"""Read-only adapter for a FUTURE separately authorized build. This file does not build or install anything.
BUILD-14-FONTS: copied from out/fonts_gpt/work/font_swap_adapter.py; only ROOT (tools/ is one level below the project
root, the original sat three levels below) and the PINNED hashes (independent of analysis.json) were added."""
from pathlib import Path
import hashlib, json, math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/fonts_gpt'
IDS = {'jimakuNE':1, 'JimakuJP':2, 'sougei':3, 'KH2Menu':4}
PINNED = {'TresFont.uasset': '450b6b0493ec702eed50dc49b082784ce70f994480a4ab3c59bbf6480b871e58',
          'TresFont.uexp': '172aa8cc858f9966dc54edb027013ba212cfa042129b61f1d625cdbdccfcc5c7'}

def analysis():
    return json.loads((OUT/'analysis.json').read_text(encoding='utf-8'))

def font_bytes(_g=None):
    """Drop-in replacement for build_build1.font_bytes; keep its return contract."""
    m=analysis()
    contents=[]
    for name in ['TresFont.uasset','TresFont.uexp']:
        data=(OUT/'TresFont'/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==m['asset_sha256'][name]==PINNED[name], name
        contents.append(data)
    info={IDS[c['class']]:(c['baseline'],c['original_H_cap'],c['K']) for c in m['classes']}
    return tuple(contents), info

def gaps():
    """Keep future build logging consistent with the prepared extension, not old +18."""
    return {IDS[c['class']]:(c['join_extension'],math.ceil(c['max_gap_before'])) for c in analysis()['classes']}
