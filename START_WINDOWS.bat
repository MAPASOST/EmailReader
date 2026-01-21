@echo off
echo ================================================
echo Email Reader - Starting Application
echo ================================================
echo.
echo The app will automatically install any missing
echo dependencies. This may take a moment on first run.
echo.

REM Activate virtual environment and run the GUI
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

python email_app.py

pause
