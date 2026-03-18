@echo off
REM MOA & Legal Opinion Tracking System - Startup Script
REM This script runs the application from Windows

echo Starting MOA & Legal Opinion Tracking System...
python main.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the application.
    echo.
    echo Make sure:
    echo 1. Python 3.8 or higher is installed
    echo 2. Dependencies are installed: pip install -r requirements.txt
    echo 3. You're running this script from the moa_system folder
    echo.
    pause
)
