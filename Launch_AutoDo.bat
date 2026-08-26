@echo off
title Auto Do Desktop Launcher

:: Determine directory location
if exist "%~dp0Auto do Application\main.py" (
    cd /d "%~dp0Auto do Application"
) else if exist "%~dp0main.py" (
    cd /d "%~dp0"
)

echo ===================================================
echo             DENM Auto-Do Launcher
echo ===================================================
echo.

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found in your system PATH.
    echo Please install Python 3.8+ from https://www.python.org and check "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

:: Ensure dependencies are installed
if exist "requirements.txt" (
    python -c "import customtkinter, pynput, PIL, darkdetect" >nul 2>nul
    if %errorlevel% neq 0 (
        echo Installing required dependencies...
        python -m pip install -r requirements.txt
    )
)

echo Starting Auto Do Application...
start "" pythonw main.py 2>nul
if %errorlevel% neq 0 (
    python main.py
)

exit
