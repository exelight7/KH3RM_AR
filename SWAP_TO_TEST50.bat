@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
set "MODS=C:\Program Files (x86)\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods"
set "LOG=%~dp0state\SWAP_LOG.tsv"
set "ACT=TEST50"
set "SRC=%~dp0out\builds\TEST50\pakchunk99-test50_P.pak"
set "WANT=a26a76917c005f8c1d26e7c42da030bf405075a9243f9bdb68191099ead14191"
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
