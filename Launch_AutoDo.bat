@echo off
title Auto Do Desktop Launcher
cd /d "%~dp0\Auto do Application"

echo Launching DENM Auto-Do...
start "" pythonw main.py
if %errorlevel% neq 0 (
    python main.py
)
exit
