@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion
set "GAME=%ProgramFiles(x86)%\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III"
set "MODS=%GAME%\Content\Paks\~mods"
set "PAK=pakchunk99-arabic_P.pak"
set "SRC=%~dp0%PAK%"
set "MSG=%~dp0AR_MESSAGES.txt"
set "WANT={{SHA}}"
set "GOT=-"
tasklist /FI "IMAGENAME eq KINGDOM HEARTS III*" 2>nul | find /I "KINGDOM HEARTS III" >nul
if not errorlevel 1 call :say RUNNING & goto end
if not exist "%GAME%\Content\Paks" call :say NOGAME & goto end
if not exist "%SRC%" call :say NOPAK & goto end
if not exist "%MODS%" mkdir "%MODS%" 2>nul
del /q "%MODS%\%PAK%" 2>nul
copy /y "%SRC%" "%MODS%\" >nul 2>nul
if errorlevel 1 call :say PERM & goto end
for /f "skip=1 tokens=*" %%H in ('certutil -hashfile "%MODS%\%PAK%" SHA256') do if "!GOT!"=="-" set "GOT=%%H"
set "GOT=%GOT: =%"
if /I not "%GOT%"=="%WANT%" del /q "%MODS%\%PAK%" 2>nul & call :say BADHASH & goto end
call :say DONE
goto end

:say
for /f "usebackq tokens=1,* delims=|" %%A in ("%MSG%") do if "%%A"=="%~1" echo %%B
exit /b

:end
echo.
pause
endlocal
