@echo off
REM Migration management script for Windows

REM Set Flask app
set FLASK_APP=app.py

if "%1"=="init" (
    echo Initializing migrations...
    flask db init
) else if "%1"=="migrate" (
    echo Creating migration...
    if "%2"=="" (
        flask db migrate
    ) else (
        flask db migrate -m "%2"
    )
) else if "%1"=="upgrade" (
    echo Applying migrations...
    flask db upgrade
) else if "%1"=="downgrade" (
    echo Rolling back migration...
    flask db downgrade
) else if "%1"=="history" (
    echo Migration history...
    flask db history
) else if "%1"=="current" (
    echo Current migration...
    flask db current
) else if "%1"=="reset" (
    echo Resetting database...
    flask reset-db
) else (
    echo Usage: %0 {init^|migrate^|upgrade^|downgrade^|history^|current^|reset}
    echo.
    echo Commands:
    echo   init      - Initialize migration repository
    echo   migrate   - Create a new migration
    echo   upgrade   - Apply migrations to database
    echo   downgrade - Roll back migrations
    echo   history   - Show migration history
    echo   current   - Show current migration
    echo   reset     - Reset database (drop and recreate^)
)