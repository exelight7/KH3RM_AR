@echo off
rem Every translation round must end with this.
cd /d "%~dp0.."
python tools\merge_translation.py --check || exit /b 1
python tools\test_validate.py || exit /b 1
python tools\test_corrections.py || exit /b 1
python tools\test_shaper.py || exit /b 1
python tools\test_cloud_secret_check.py || exit /b 1
python tools\apply_corrections.py || exit /b 1
python tools\make_glossary.py || exit /b 1
python tools\validate.py || exit /b 1
python tools\make_review.py || exit /b 1
python tools\make_script.py || exit /b 1
python tools\stats.py || exit /b 1
python tools\update_map.py || exit /b 1
python tools\secret_check.py || exit /b 1
