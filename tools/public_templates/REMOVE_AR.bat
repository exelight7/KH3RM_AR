@echo off
chcp 65001 >nul
setlocal EnableExtensions
set "MODS=%ProgramFiles(x86)%\Steam\steamapps\common\KINGDOM HEARTS III\KINGDOM HEARTS III\Content\Paks\~mods"
set "PAK=pakchunk99-arabic_P.pak"
set "MSG=%~dp0AR_MESSAGES.txt"
tasklist /FI "IMAGENAME eq KINGDOM HEARTS III*" 2>nul | find /I "KINGDOM HEARTS III" >nul
if not errorlevel 1 call :say RUNNING & goto end
del /q "%MODS%\%PAK%" 2>nul
if exist "%MODS%\%PAK%" call :say PERM & goto end
dir /b "%MODS%" 2>nul | findstr "^" >nul
if errorlevel 1 rd "%MODS%" 2>nul
call :say REMOVED
goto end

:say
for /f "usebackq tokens=1,* delims=|" %%A in ("%MSG%") do if "%%A"=="%~1" echo %%B
exit /b

:end
echo.
pause
endlocal
