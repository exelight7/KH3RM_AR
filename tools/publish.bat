@echo off
rem Every round ends with this (after refresh.bat and secret_check). Publishes to github.com/exelight7/KH3RM_AR, branch main, never forced.
cd /d "%~dp0.."
python -I tools\make_public.py || exit /b 1
python -I tools\public_check.py || exit /b 1
python -I tools\test_public_check.py || exit /b 1
for /f "delims=" %%R in ('python -I tools\make_public.py --last-round') do set "ROUND=%%R"
git -C public_repo add -A
git -C public_repo diff --cached --quiet && (echo Nothing to publish. & exit /b 0)
git -C public_repo commit -q -m "sync: %ROUND%" || exit /b 1
git -C public_repo push origin main || exit /b 1
