"""SWAP-1/TEST50/BUILD-1/FULL-1/TRANS-4/BUILD-4: generate SWAP_TO_F1.bat, SWAP_TO_F2.bat, SWAP_TO_TEST50.bat, SWAP_TO_BUILD1.bat,
SWAP_TO_BUILD2.bat, SWAP_TO_BUILD3.bat, SWAP_TO_BUILD4.bat, SWAP_TO_BUILD5.bat, SWAP_TO_BUILD6.bat, SWAP_TO_BUILD7.bat, SWAP_TO_BUILD8.bat, SWAP_TO_BUILD9.bat, SWAP_TO_BUILD10.bat, SWAP_TO_BUILD11.bat, SWAP_TO_BUILD12.bat, SWAP_TO_BUILD13.bat, SWAP_TO_BUILD14.bat, SWAP_TO_BUILD15.bat, SWAP_TO_BUILD16.bat, SWAP_TO_BUILD17.bat, SWAP_TO_BUILD18.bat,
REMOVE_ARABIC.bat, SWAP_TO_IMAGES_PILOT.bat, REMOVE_IMAGES_PILOT.bat (FINAL-1: touch only pakchunk98-arabic-images_P.pak),
SWAP_TO_IMAGES_MASS.bat, SWAP_TO_IMAGES_MASS2.bat, SWAP_TO_IMAGES_MASS3.bat, SWAP_TO_IMAGES_MASS4.bat, SWAP_TO_IMAGES_MASS5.bat, SWAP_TO_IMAGES_MASS6.bat, SWAP_TO_IMAGES_MASS7.bat, SWAP_TO_IMAGES_MASS8.bat, SWAP_TO_IMAGES_MASS9.bat, SWAP_TO_IMAGES_MASS10.bat, SWAP_TO_IMAGES_MASS11.bat, REMOVE_IMAGES.bat (IMAGES-MASS, same rule) in the project root (CRLF)."""
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
    'done_BUILD7': 'تم: BUILD-7 مثبت الآن / Done: BUILD-7 installed',
    'done_BUILD8': 'تم: BUILD-8 مثبت الآن / Done: BUILD-8 installed',
    'done_BUILD9': 'تم: BUILD-9 مثبت الآن / Done: BUILD-9 installed',
    'done_BUILD10': 'تم: BUILD-10 مثبت الآن / Done: BUILD-10 installed',
    'done_BUILD11': 'تم: BUILD-11 مثبت الآن / Done: BUILD-11 installed',
    'done_BUILD12': 'تم: BUILD-12 مثبت الآن / Done: BUILD-12 installed',
    'done_BUILD13': 'تم: BUILD-13 مثبت الآن / Done: BUILD-13 installed',
    'done_BUILD14': 'تم: BUILD-14 مثبت الآن / Done: BUILD-14 installed',
    'done_BUILD15': 'تم: BUILD-15 مثبت الآن / Done: BUILD-15 installed',
    'done_BUILD16': 'تم: BUILD-16 مثبت الآن / Done: BUILD-16 installed',
    'done_BUILD17': 'تم: BUILD-17 مثبت الآن / Done: BUILD-17 installed',
    'done_BUILD18': 'تم: BUILD-18 مثبت الآن / Done: BUILD-18 installed',
    'done_IMAGES_PILOT': 'تم: تجربة الصور مثبتة الآن بجانب التعريب النصي / Done: image pilot installed next to the text pak',
    'done_REMOVE_IMAGES': 'تم: حُذفت حزمة الصور، والتعريب النصي باقٍ / Done: images pak removed, text pak kept',
    'done_IMAGES_MASS': 'تم: حزمة الصور مثبتة الآن بجانب التعريب النصي / Done: images pak installed next to the text pak',
    'done_IMAGES_MASS2': 'تم: حزمة الصور (الجولة 2) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 2) installed next to the text pak',
    'done_IMAGES_MASS3': 'تم: حزمة الصور (الجولة 3) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 3) installed next to the text pak',
    'done_IMAGES_MASS4': 'تم: حزمة الصور (الجولة 4) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 4) installed next to the text pak',
    'done_IMAGES_MASS5': 'تم: حزمة الصور (الجولة 5) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 5) installed next to the text pak',
    'done_IMAGES_MASS6': 'تم: حزمة الصور (الجولة 6) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 6) installed next to the text pak',
    'done_IMAGES_MASS7': 'تم: حزمة الصور (الجولة 7) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 7) installed next to the text pak',
    'done_IMAGES_MASS8': 'تم: حزمة الصور (الجولة 8) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 8) installed next to the text pak',
    'done_IMAGES_MASS9': 'تم: حزمة الصور (الجولة 9) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 9) installed next to the text pak',
    'done_IMAGES_MASS10': 'تم: حزمة الصور (الجولة 10) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 10) installed next to the text pak',
    'done_IMAGES_MASS11': 'تم: حزمة الصور (الجولة 11) مثبتة الآن بجانب التعريب النصي / Done: images pak (round 11) installed next to the text pak',
    'done_REMOVE':'تم: حُذف التعريب من اللعبة / Done: Arabic removed',
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
     'BUILD6': r'%~dp0out\builds\BUILD-6\pakchunk99-arabic_P.pak',
     'BUILD7': r'%~dp0out\builds\BUILD-7\pakchunk99-arabic_P.pak',
     'BUILD8': r'%~dp0out\builds\BUILD-8\pakchunk99-arabic_P.pak',
     'BUILD9': r'%~dp0out\builds\BUILD-9\pakchunk99-arabic_P.pak',
     'BUILD10': r'%~dp0out\builds\BUILD-10\pakchunk99-arabic_P.pak',
     'BUILD11': r'%~dp0out\builds\BUILD-11\pakchunk99-arabic_P.pak',
     'BUILD12': r'%~dp0out\builds\BUILD-12\pakchunk99-arabic_P.pak',
     'BUILD13': r'%~dp0out\builds\BUILD-13\pakchunk99-arabic_P.pak',
     'BUILD14': r'%~dp0out\builds\BUILD-14\pakchunk99-arabic_P.pak',
     'BUILD15': r'%~dp0out\builds\BUILD-15\pakchunk99-arabic_P.pak',
     'BUILD16': r'%~dp0out\builds\BUILD-16\pakchunk99-arabic_P.pak',
     'BUILD17': r'%~dp0out\builds\BUILD-17\pakchunk99-arabic_P.pak',
     'BUILD18': r'%~dp0out\builds\BUILD-18\pakchunk99-arabic_P.pak'}
H = {'F1': '302d95d10a972622a2c9d805ff6bbeb5e4cdf47eb2f64e814a240b5accf1f2d0',
     'F2': '5e60bd3a94a573b8af2db8182baaeea4480bf5244f8113b1eebd77cbdb43cb99',
     'TEST50': 'a26a76917c005f8c1d26e7c42da030bf405075a9243f9bdb68191099ead14191',
     'BUILD1': '0f27502d8824fd517f5188fd285c6e704376ebb3a29a2c838da826fe703326ab',
     'BUILD2': '2ce95c73c7ba110ed0d42d7cabdfd2f755ac1c08d76374b7b2036bafb68db364',
     'BUILD3': '2834d65a94462fae60ac96c5cd22b92f3f69ddb784151d2070e34eb1d6fcad27',
     'BUILD4': 'ae9d609ae953032b1551854df559071ff284af50152ae54f231509ebb8bce243',
     'BUILD5': 'e43d8f9705588ba4cb7e8058e2f630d2d65734f7bf3068ab7a24c2dddcbe6602',
     'BUILD6': 'f6e8be85feae061c120674adccfcacd847727c51ef5952aa3b5594898a6e8ae3',
     'BUILD7': 'f9e23f373ce52a5e9c6690d264b7228d43d0e28aa55d9d76386514db511e82d7',
     'BUILD8': '45f043de4a4832b1ace0c34f43f2d09e96123d9aaff72768e04524d9ee70e381',
     'BUILD9': '23ae437a117d5f77f1742d85b1f80a87e5dad0dc8755cf0950a79f99ca2a62f0',
     'BUILD10': '89e00ead0a83e5d1cb07d257d98530541da447a5849c42f84ba9759dd4c7beea',
     'BUILD11': '8aa9b0e816e61a303f8b1f36e03fa90caf5c2d0a4ed90e1b7bd0a812ffeb7f91',
     'BUILD12': '2cdb5b7b7ee79f5432f488aa86f1a2cf724eaf6983c0077f797dd831e62795cd',
     'BUILD13': '3675a16aefe35a70010e1c721de0701f7709b589b1987fb1a4860653bf78fd7c',
     'BUILD14': 'a7d2eacd7bf7f790d91b57568e184ab45b0266112baa98532380c661d6bf5f92',
     'BUILD15': '11c078410b74471d8a078707ac20035de6d3fa1910e5237a69992a068a17b79f',
     'BUILD16': '5ff72110e9ab7c8cca443ce6d7c9b5d27b209bde395a904d6cf81ba08ca1ec5f',
     'BUILD17': '58bad87725b3e1029cb7fb4a31258a0fda97eca5d3d4192d1562ed3bc4f9858c',
     'BUILD18': 'dde67ce67b7d93bf95835a0126e317e003e3a2a51370321da51ce48035afe527'}
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
MASS = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS.bat', HEAD.replace('@ACT@', 'IMAGES_MASS').replace('@SRC@', r'%~dp0out' + chr(92) + MASS)
      .replace('@WANT@', '233ef22839ba331896474f50ebb2761e87a234ac0411cc8cb683e4375bd155f1').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS2 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS2' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS2.bat', HEAD.replace('@ACT@', 'IMAGES_MASS2').replace('@SRC@', r'%~dp0out' + chr(92) + MASS2)
      .replace('@WANT@', 'bc546502a712675520b70d738b65be5835372fa2ec61fec04a04296e49a0dd29').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS3 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS3' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS3.bat', HEAD.replace('@ACT@', 'IMAGES_MASS3').replace('@SRC@', r'%~dp0out' + chr(92) + MASS3)
      .replace('@WANT@', 'd8d139481f4c4b794483a61ddb44c4862ffdafeb052bd44ab2bcac67ab2865c9').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS4 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS4' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS4.bat', HEAD.replace('@ACT@', 'IMAGES_MASS4').replace('@SRC@', r'%~dp0out' + chr(92) + MASS4)
      .replace('@WANT@', 'e8ebf70acab5612339cdbe20cb130f197199bc0d9b1776c96232f28bc541a403').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS5 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS5' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS5.bat', HEAD.replace('@ACT@', 'IMAGES_MASS5').replace('@SRC@', r'%~dp0out' + chr(92) + MASS5)
      .replace('@WANT@', 'd5b39c12c25f34108b97d9d8c6056374800bcd6a9727bb26f82a01941a0bff21').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS6 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS6' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS6.bat', HEAD.replace('@ACT@', 'IMAGES_MASS6').replace('@SRC@', r'%~dp0out' + chr(92) + MASS6)
      .replace('@WANT@', 'a6b6d55625de72f2948c581f445ab6298a44f5fb644f60bbf72743a83f19aa55').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS7 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS7' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS7.bat', HEAD.replace('@ACT@', 'IMAGES_MASS7').replace('@SRC@', r'%~dp0out' + chr(92) + MASS7)
      .replace('@WANT@', 'dabd8b855cb83d3aa0b529bcccbcb5a80fc04ac382ed57346b6ae25aa3b38bad').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS8 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS8' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS8.bat', HEAD.replace('@ACT@', 'IMAGES_MASS8').replace('@SRC@', r'%~dp0out' + chr(92) + MASS8)
      .replace('@WANT@', '917d92733f1e7808007bc089aa067e7b12973d3ddc6ae1045532908baea282e0').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS9 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS9' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS9.bat', HEAD.replace('@ACT@', 'IMAGES_MASS9').replace('@SRC@', r'%~dp0out' + chr(92) + MASS9)
      .replace('@WANT@', 'abe75ddd6ee0e1522ec8f217d88a4826cdc4ba89a88655c1c58906bbc9245573').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS10 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS10' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS10.bat', HEAD.replace('@ACT@', 'IMAGES_MASS10').replace('@SRC@', r'%~dp0out' + chr(92) + MASS10)
      .replace('@WANT@', '2dfb6baff273fc0320c687b3c0afac988703e83d5b9682a8ede61cb84f83ba34').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
MASS11 = 'b' + 'uilds' + chr(92) + 'IMAGES-MASS11' + chr(92) + PILOT
write('SWAP_TO_IMAGES_MASS11.bat', HEAD.replace('@ACT@', 'IMAGES_MASS11').replace('@SRC@', r'%~dp0out' + chr(92) + MASS11)
      .replace('@WANT@', '7b37f84b390db3d62fe837892a99bbe3fe4ae7cccf9bc67a119decb3d643c964').replace('@CHECKSRC@', CHECK).replace('@DEL@', PILOT) + SWAP)
# REMOVE_IMAGES.bat deletes the images pak by name (any build: IMAGES-MASS .. -MASS11), so it pins no hash
write('REMOVE_IMAGES.bat', HEAD.replace('@ACT@', 'REMOVE_IMAGES').replace('@SRC@', '-').replace('@WANT@', '-').replace('@CHECKSRC@', '').replace('@DEL@', PILOT) + REMOVE)
