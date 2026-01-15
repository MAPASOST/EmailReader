@echo off
echo Starting Email Reader...
echo.

REM Activate virtual environment and run the GUI
call venv\Scripts\activate.bat
python email_app.py

pause
