@echo off
title Auto Do Launcher
cd /d "%~dp0"

echo ===================================================
echo             Launching DENM Auto-Do
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found on your system PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

:: Run the application
start "" pythonw main.py
if %errorlevel% neq 0 (
    echo Starting in console mode...
    python main.py
)

exit
