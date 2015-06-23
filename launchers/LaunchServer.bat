REM @echo off
cd ../server/
color 0f
py -3.4 serveur.py > errors.log 2>&1
notepad errors.log