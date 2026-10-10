@echo off
rem Cloud sync: pull merged cloud review work into the private project, then regenerate and push cloud_repo (private KH3RM_AR_work, main, never forced).
rem Close nothing else needed; run from anywhere. Use --no-push to stop before the push.
cd /d "%~dp0.."
python -I tools\sync_cloud.py %*
