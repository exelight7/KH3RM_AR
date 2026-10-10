r"""Prepare out\release\ for a GitHub Release: the installed BUILD pak, SHA256.txt, INSTALL_AR.bat, REMOVE_AR.bat, AR_MESSAGES.txt.
Usage: python -I tools\make_release.py [BUILD-5]   (refuses if the build pak differs from the installed copy)"""
import hashlib, os, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAK = 'pakchunk99-arabic_P.pak'
MODS = r'C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods'
MSGS = """DONE|تم: التعريب مثبّت. شغّل اللعبة. / Done: Arabic installed. Start the game.
REMOVED|تم: حُذف التعريب من اللعبة. / Done: Arabic removed.
RUNNING|اللعبة تعمل الآن. أغلقها ثم شغّل هذا الملف من جديد. / The game is running. Close it and run this file again.
NOGAME|لم أجد اللعبة في مكتبة ستيم الافتراضية. انسخ الملف يدويا (انظر README). / Game not found in the default Steam library. Copy the pak by hand (see README).
NOPAK|ملف pakchunk99-arabic_P.pak يجب أن يكون بجانب هذا الملف. / pakchunk99-arabic_P.pak must be next to this file.
PERM|تعذر النسخ أو الحذف. شغّل الملف كمسؤول. / Copy or delete failed. Run this file as administrator.
BADHASH|الملف تالف (SHA256 لا يطابق). نزّله من جديد. / Corrupt file (SHA256 mismatch). Download it again.
"""
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
if __name__ == '__main__':
    build = sys.argv[1] if len(sys.argv) > 1 else 'BUILD-5'
    src = os.path.join(ROOT, 'out', 'builds', build, PAK)
    h = sha(src)
    inst = os.path.join(MODS, PAK)
    if os.path.exists(inst) and sha(inst) != h:
        sys.exit(f'FAIL: installed pak differs from {build}')
    out = os.path.join(ROOT, 'out', 'release'); os.makedirs(out, exist_ok=True)
    shutil.copy(src, os.path.join(out, PAK))
    open(os.path.join(out, 'SHA256.txt'), 'w', newline='\n').write(f'{h}  {PAK}\n')
    open(os.path.join(out, 'AR_MESSAGES.txt'), 'w', encoding='utf-8', newline='\r\n').write(MSGS)
    t = os.path.join(ROOT, 'tools', 'public_templates')
    for n in ('INSTALL_AR.bat', 'REMOVE_AR.bat'):
        open(os.path.join(out, n), 'w', newline='\r\n').write(open(os.path.join(t, n)).read().replace('{{SHA}}', h))
    print('PASS', build, h)
