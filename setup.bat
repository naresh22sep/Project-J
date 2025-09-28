@echo off
REM Setup script for Flask application (Windows)

echo Setting up Flask Application...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Copy environment file
echo Setting up environment configuration...
copy config\.env.example .env

echo Setup complete!
echo.
echo To activate the virtual environment, run:
echo venv\Scripts\activate.bat
echo.
echo To start the application, run:
echo python app.py
echo.
echo Don't forget to:
echo 1. Update database credentials in .env file
echo 2. Create MySQL database
echo 3. Run 'flask db init' and 'flask db migrate' for migrations