REM @echo off
cd src/
color 0f
py -3.4 main.py REM > Logs/errors.log 2>&1
notepad Logs/errors.log