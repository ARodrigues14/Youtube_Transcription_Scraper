@echo off
rem Double-click launcher for ask_claude.py.
rem You can also drag a .txt file onto this file (or its shortcut) to load it.
title Ask Claude about a YouTube video
chcp 65001 >nul
set PYTHONUTF8=1

rem Run from the project folder so imports and transcription.txt resolve here.
cd /d "%~dp0"
".venv\Scripts\python.exe" ask_claude.py %*

echo.
pause
