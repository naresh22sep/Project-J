@echo off
echo 🧪 Route Testing Options
echo ========================

echo.
echo 1. Run automated route tests
echo 2. Run manual route tests (requires server running)
echo 3. Generate cURL commands
echo 4. Test with authentication examples
echo 5. Start Flask app and test
echo.

set /p choice="Choose option (1-5): "

if "%choice%"=="1" (
    echo Running automated route tests...
    python tests/test_routes.py
) else if "%choice%"=="2" (
    echo Running manual route tests...
    echo Make sure your Flask app is running on http://localhost:5051
    pause
    python test_routes_manual.py
) else if "%choice%"=="3" (
    echo Generating cURL commands...
    python test_routes_manual.py curl
) else if "%choice%"=="4" (
    echo Testing authentication examples...
    python test_routes_manual.py auth
) else if "%choice%"=="5" (
    echo Starting Flask app...
    start "Flask App" python run.py
    timeout /t 5
    echo Testing routes...
    python test_routes_manual.py
) else (
    echo Invalid choice. Please choose 1-5.
)

echo.
pause