@echo off
setlocal enabledelayedexpansion
title Chatterbox AI Voice Generator

echo =======================================================
echo          Chatterbox AI Voice Generator Launcher
echo =======================================================
echo.

cd /d "%~dp0"

:: 1. Find Python executable
set "PY_CMD="

if exist ".venv\Scripts\python.exe" (
    set "PY_CMD=.venv\Scripts\python.exe"
    goto :START_APP
)

:: Check Python 3.11 pre-installed path
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "BASE_PY=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :CREATE_VENV
)

:: Check system python
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "BASE_PY=python"
    goto :CREATE_VENV
)

:: Check py launcher
where py >nul 2>nul
if %errorlevel% equ 0 (
    set "BASE_PY=py -3.11"
    goto :CREATE_VENV
)

echo [ERROR] Python 3.11 or Python 3 is not found on your system!
echo Please install Python 3.11 from https://www.python.org/downloads/
echo and make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:CREATE_VENV
echo Creating virtual environment (.venv)...
%BASE_PY% -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo Installing dependencies from requirements.txt...
echo This may take a few moments on the first run...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation encountered an issue.
    pause
    exit /b 1
)

set "PY_CMD=.venv\Scripts\python.exe"

:START_APP
echo.
echo Launching Chatterbox AI Voice Generator Web UI...
echo The app will open in your default browser at http://127.0.0.1:7860
echo.
%PY_CMD% app.py

if %errorlevel% neq 0 (
    echo.
    echo Application stopped with an error.
    pause
)
