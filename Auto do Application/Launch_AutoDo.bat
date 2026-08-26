@echo off
setlocal EnableDelayedExpansion
title Auto Do Desktop Launcher

echo ===================================================
echo             DENM Auto-Do Launcher
echo ===================================================
echo.

:: Resolve script location
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%Auto do Application\main.py" (
    cd /d "%SCRIPT_DIR%Auto do Application"
) else if exist "%SCRIPT_DIR%main.py" (
    cd /d "%SCRIPT_DIR%"
) else (
    echo [ERROR] Could not locate main.py. Please extract all files from the zip archive before launching.
    echo Current Directory: %CD%
    echo.
    pause
    exit /b 1
)

:: Find python executable
set "PY_CMD="
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_CMD=python"
) else (
    where py >nul 2>nul
    if !errorlevel! equ 0 (
        set "PY_CMD=py"
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python was not found in your system PATH.
    echo Please install Python 3.8+ from https://www.python.org and ensure "Add python.exe to PATH" is checked.
    echo.
    pause
    exit /b 1
)

echo [1/3] Python detected: %PY_CMD%
%PY_CMD% --version

:: Check dependencies
echo [2/3] Checking required libraries (customtkinter, pynput, Pillow)...
%PY_CMD% -c "import customtkinter, pynput, PIL, darkdetect" >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing missing dependencies...
    if exist "requirements.txt" (
        %PY_CMD% -m pip install -r requirements.txt
    ) else (
        %PY_CMD% -m pip install customtkinter pynput Pillow darkdetect
    )
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.
        echo.
        pause
        exit /b 1
    )
)

:: Launch the application
echo [3/3] Starting Auto Do Desktop Application...
echo.
%PY_CMD% main.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application closed unexpectedly (Exit Code: %errorlevel%).
    pause
)

