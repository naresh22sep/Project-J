@echo off
REM Test Runner Script for Windows

echo 🧪 Flask Application Test Runner
echo =================================

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Load environment variables (Windows doesn't have a direct equivalent to export $(cat .env | xargs))
if exist ".env" (
    echo Loading environment variables from .env...
    for /f "delims=" %%x in (.env) do set %%x
) else (
    echo ⚠️  .env file not found. Copy config\.env.example to .env
)

echo.

REM Check which test to run
if "%1"=="quick" (
    echo 🚀 Running quick connection test...
    python tests\test_connection.py
) else if "%1"=="database" (
    echo 🗄️  Running database tests...
    python tests\test_database.py
) else if "%1"=="app" (
    echo 🌐 Running application tests...
    python tests\test_app.py
) else if "%1"=="all" (
    echo 🎯 Running all tests...
    echo.
    echo 1. Quick connection test:
    python tests\test_connection.py
    echo.
    echo 2. Database tests:
    python tests\test_database.py
    echo.
    echo 3. Application tests:
    python tests\test_app.py
) else (
    echo Usage: %0 {quick^|database^|app^|all}
    echo.
    echo Test options:
    echo   quick    - Quick database connection test
    echo   database - Comprehensive database tests
    echo   app      - Flask application tests
    echo   all      - Run all tests
    echo.
    echo Examples:
    echo   run_tests.bat quick      # Quick test
    echo   run_tests.bat all        # All tests
    goto :eof
)

echo.
echo 🏁 Test run completed!