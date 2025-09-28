@echo off
title JobHunter Platform - Flask Application

echo.
echo 🎯 JobHunter Platform - 4-Module Flask Application
echo ================================================
echo.

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv\" (
    echo ⚠️ Virtual environment not found
    echo 🔧 Creating virtual environment...
    py -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist ".venv\Lib\site-packages\flask\" (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

REM Set environment variables
set FLASK_ENV=development
set FLASK_APP=app.py

echo.
echo 🚀 Starting JobHunter Platform...
echo.

REM Run the application
python run.py

REM Deactivate virtual environment on exit
deactivate

echo.
echo 👋 Thanks for using JobHunter Platform!
pause