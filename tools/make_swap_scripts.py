"""SWAP-1/TEST50/BUILD-1/FULL-1/TRANS-4/BUILD-4: generate SWAP_TO_F1.bat, SWAP_TO_F2.bat, SWAP_TO_TEST50.bat, SWAP_TO_BUILD1.bat,
SWAP_TO_BUILD2.bat, SWAP_TO_BUILD3.bat, SWAP_TO_BUILD4.bat, SWAP_TO_BUILD5.bat, SWAP_TO_BUILD6.bat,
REMOVE_ARABIC.bat, SWAP_TO_IMAGES_PILOT.bat, REMOVE_IMAGES_PILOT.bat (FINAL-1: touch only pakchunk98-arabic-images_P.pak) in the project root (CRLF)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the .bat files stay pure ASCII (cmd mis-parses UTF-8 bytes after chcp 65001); Arabic lines live in tools\swap_msgs\*.txt and are shown with `type`
MSGS = {
    'done_F1': 'تم: F1 مثبت الآن / Done: F1 installed',
    'done_F2': 'تم: F2 مثبت الآن / Done: F2 installed',
    'done_TEST50': 'تم: TEST50 مثبت الآن / Done: TEST50 installed',
    'done_BUILD1': 'تم: BUILD-1 مثبت الآن / Done: BUILD-1 installed',
    'done_BUILD2': 'تم: BUILD-2 مثبت الآن / Done: BUILD-2 installed',
    'done_BUILD3': 'تم: BUILD-3 مثبت الآن / Done: BUILD-3 installed',
    'done_BUILD4': 'تم: BUILD-4 مثبت الآن / Done: BUILD-4 installed',
    'done_BUILD5': 'تم: BUILD-5 مثبت الآن / Done: BUILD-5 installed',
    'done_BUILD6': 'تم: BUILD-6 مثبت الآن / Done: BUILD-6 installed',
    'done_IMAGES_PILOT': 'تم: تجربة الصور مثبتة الآن بجانب التعريب النصي / Done: image pilot installed next to the text pak',
    'done_REMOVE_IMAGES': 'تم: حُذفت تجربة الصور، والتعريب النصي باقٍ / Done: image pilot removed, text pak kept',
    'done_REMOVE': 'تم: حُذف التعريب من اللعبة / Done: Arabic removed',
    'running': 'اللعبة تعمل الآن. أغلقها ثم شغّل هذا الملف من جديد. / The game is running. Close it, then run this file again.',
    'permfail': 'فشل: لا توجد صلاحية على مجلد اللعبة / FAILED: no permission on the game folder',
    'badhash': 'فشل: البصمة لا تطابق البناء، حُذف الملف / FAILED: SHA256 mismatch, copy removed',
}
os.makedirs(os.path.join(ROOT, 'tools', 'swap_msgs'), exist_ok=True)
for k, v in MSGS.items():
    with open(os.path.join(ROOT, 'tools', 'swap_msgs', k + '.txt'), 'w', encoding='utf-8', newline='') as f:
        f.write(v + '\r\n')
TAB = '\t'
MSG = '%~dp0tools' + chr(92) + 'swap_msgs' + chr(92)  # templates hold no backslash escapes (SWAP-1 lost two to control bytes)
HEAD = r'''@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
set "MODS=C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods"
set "LOG=%~dp0state\SWAP_LOG.tsv"
set "ACT=@ACT@"
set "SRC=@SRC@"
set "WANT=@WANT@"
set "GOT=-"
tasklist /FI "IMAGENAME eq KINGDOM HEARTS III*" 2>nul | find /I "KINGDOM HEARTS III" >nul
if not errorlevel 1 goto running
@CHECKSRC@
del /q "%MODS%\@DEL@" 2>nul
if exist "%MODS%\@DEL@" goto perm
'''
SWAP = r'''if not exist "%MODS%" mkdir "%MODS%" 2>nul
copy /y "%SRC%" "%MODS%\" >nul 2>nul
if errorlevel 1 goto perm
for %%F in ("%SRC%") do set "DST=%MODS%\%%~nxF"
for /f "skip=1 tokens=*" %%H in ('certutil -hashfile "%DST%" SHA256') do if "!GOT!"=="-" set "GOT=%%H"
set "GOT=%GOT: =%"
if /I not "%GOT%"=="%WANT%" goto badhash
call :log OK
echo.
type "@MSG@done_%ACT%.txt"
echo SHA256 %GOT%
goto end
'''
REMOVE = r'''dir /b "%MODS%" 2>nul | findstr "^" >nul
if errorlevel 1 rd "%MODS%" 2>nul
call :log OK
echo.
type "@MSG@done_%ACT%.txt"
goto end
'''
TAIL = r'''
:running
echo.
type "@MSG@running.txt"
call :log GAME_RUNNING
goto end

:perm
if /I "%~1"=="elev" goto permfail
echo Need admin rights, asking...
powershell -NoProfile -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList 'elev'"
exit /b

:permfail
echo.
type "@MSG@permfail.txt"
call :log PERM_FAIL
goto end

:badhash
echo.
type "@MSG@badhash.txt"
echo got  %GOT%
echo want %WANT%
del /q "%DST%" 2>nul
call :log HASH_MISMATCH
goto end

:log
if not exist "%LOG%" >"%LOG%" echo time@TAB@action@TAB@hash@TAB@result
>>"%LOG%" echo %DATE% %TIME%@TAB@%ACT%@TAB@%GOT%@TAB@%1
exit /b

:end
echo.
pause
endlocal
'''
CHECK = r'''if not exist "%SRC%" (echo Missing build: %SRC% & goto end)'''
B = {'F1': r'%~dp0out\builds\ARABIC-TEST-2\pakchunk99-arabictest2F1_P.pak',
     'F2': r'%~dp0out\builds\ARABIC-TEST-2\pakchunk99-arabictest2F2_P.pak',
     'TEST50': r'%~dp0out\builds\TEST50\pakchunk99-test50_P.pak',
     'BUILD1': r'%~dp0out\builds\BUILD-1\pakchunk99-arabic_P.pak',
     'BUILD2': r'%~dp0out\builds\BUILD-2\pakchunk99-arabic_P.pak',
     'BUILD3': r'%~dp0out\builds\BUILD-3\pakchunk99-arabic_P.pak',
     'BUILD4': r'%~dp0out\builds\BUILD-4\pakchunk99-arabic_P.pak',
     'BUILD5': r'%~dp0out\builds\BUILD-5\pakchunk99-arabic_P.pak',
     'BUILD6': r'%~dp0out\builds\BUILD-6\pakchunk99-arabic_P.pak'}
H = {'F1': '302d95d10a972622a2c9d805ff6bbeb5e4cdf47eb2f64e814a240b5accf1f2d0',
     'F2': '5e60bd3a94a573b8af2db8182baaeea4480bf5244f8113b1eebd77cbdb43cb99',
     'TEST50': 'a26a76917c005f8c1d26e7c42da030bf405075a9243f9bdb68191099ead14191',
     'BUILD1': '0f27502d8824fd517f5188fd285c6e704376ebb3a29a2c838da826fe703326ab',
     'BUILD2': '2ce95c73c7ba110ed0d42d7cabdfd2f755ac1c08d76374b7b2036bafb68db364',
     'BUILD3': '2834d65a94462fae60ac96c5cd22b92f3f69ddb784151d2070e34eb1d6fcad27',
     'BUILD4': 'ae9d609ae953032b1551854df559071ff284af50152ae54f231509ebb8bce243',
     'BUILD5': 'e43d8f9705588ba4cb7e8058e2f630d2d65734f7bf3068ab7a24c2dddcbe6602',
     'BUILD6': 'f6e8be85feae061c120674adccfcacd847727c51ef5952aa3b5594898a6e8ae3'}
def write(name, body):
    s = (body + TAIL).replace('@TAB@', TAB).replace('@MSG@', MSG)
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='') as f:
        f.write(s.replace('\n', '\r\n'))
TEXT = 'pakchunk99-*_P.pak'                  # text builds: any of our pakchunk99 paks
PILOT = 'pakchunk98-arabic-images_P.pak'      # FINAL-1 image pilot: only this one file, never the text pak
for v in B:
    h = HEAD.replace('@ACT@', v).replace('@SRC@', B[v]).replace('@WANT@', H[v]).replace('@CHECKSRC@', CHECK).replace('@DEL@', TEXT)
    write(f'SWAP_TO_{v}.bat', h + SWAP)
write('REMOVE_ARABIC.bat', HEAD.replace('@ACT@', 'REMOVE').replace('@SRC@', '-').replace('@WANT@', '-').replace('@CHECKSRC@', '').replace('@DEL@', TEXT) + REMOVE)
write('SWAP_TO_IMAGES_PILOT.bat', HEAD.replace('@ACT@', 'IMAGES_PILOT').replace('@SRC@', r'%~dp0out' + chr(92) + r'builds' + chr(92) + 'IMAGES-PILOT' + chr(92) + PILOT)
      .replace('@WANT@', '75a944612fab129687e15a7d77dadbd843a68ecde21810ae1cd0c35fea84853e').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
write('REMOVE_IMAGES_PILOT.bat', HEAD.replace('@ACT@', 'REMOVE_IMAGES').replace('@SRC@', '-').replace('@WANT@', '-').replace('@CHECKSRC@', '').replace('@DEL@', PILOT) + REMOVE)
