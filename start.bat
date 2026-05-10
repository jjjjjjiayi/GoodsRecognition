@echo off
cd /d "%~dp0"
call conda activate env_rec
python UI/pyqt_detect.py
pause
