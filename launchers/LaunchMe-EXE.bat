@echo off
cd ../dist
main.exe 2>&1 Logs/errors.log
notepad Logs/errors.log