@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
set "MODS=C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods"
set "LOG=%~dp0state\SWAP_LOG.tsv"
set "ACT=BUILD7"
set "SRC=%~dp0out\builds\BUILD-7\pakchunk99-arabic_P.pak"
set "WANT=f9e23f373ce52a5e9c6690d264b7228d43d0e28aa55d9d76386514db511e82d7"
set "GOT=-"
tasklist /FI "IMAGENAME eq KINGDOM HEARTS III*" 2>nul | find /I "KINGDOM HEARTS III" >nul
if not errorlevel 1 goto running
if not exist "%SRC%" (echo Missing build: %SRC% & goto end)
del /q "%MODS%\pakchunk99-*_P.pak" 2>nul
if exist "%MODS%\pakchunk99-*_P.pak" goto perm
if not exist "%MODS%" mkdir "%MODS%" 2>nul
copy /y "%SRC%" "%MODS%\" >nul 2>nul
if errorlevel 1 goto perm
for %%F in ("%SRC%") do set "DST=%MODS%\%%~nxF"
for /f "skip=1 tokens=*" %%H in ('certutil -hashfile "%DST%" SHA256') do if "!GOT!"=="-" set "GOT=%%H"
set "GOT=%GOT: =%"
if /I not "%GOT%"=="%WANT%" goto badhash
call :log OK
echo.
type "%~dp0tools\swap_msgs\done_%ACT%.txt"
echo SHA256 %GOT%
goto end

:running
echo.
type "%~dp0tools\swap_msgs\running.txt"
call :log GAME_RUNNING
goto end

:perm
if /I "%~1"=="elev" goto permfail
echo Need admin rights, asking...
powershell -NoProfile -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList 'elev'"
exit /b

:permfail
echo.
type "%~dp0tools\swap_msgs\permfail.txt"
call :log PERM_FAIL
goto end

:badhash
echo.
type "%~dp0tools\swap_msgs\badhash.txt"
echo got  %GOT%
echo want %WANT%
del /q "%DST%" 2>nul
call :log HASH_MISMATCH
goto end

:log
if not exist "%LOG%" >"%LOG%" echo time	action	hash	result
>>"%LOG%" echo %DATE% %TIME%	%ACT%	%GOT%	%1
exit /b

:end
echo.
pause
endlocal
