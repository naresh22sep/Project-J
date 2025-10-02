@echo off
title JobHunter Platform

echo Starting JobHunter Platform...
echo.

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run the Flask application
python run.py

echo.
echo Application stopped.
pause