@echo off
echo ====================================
echo Email Reader - Installation
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo Python found! Continuing with installation...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing required packages...
echo This may take a minute...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

REM Copy .env.example to .env if it doesn't exist
if not exist .env (
    echo.
    echo Creating configuration file...
    copy .env.example .env >nul
)

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo Next step: Double-click START.bat to run the application!
echo.
pause
