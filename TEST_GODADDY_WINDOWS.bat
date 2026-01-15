@echo off
echo ================================================
echo GoDaddy Email Connection Test
echo ================================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found.
    echo Installing required package...
    pip install python-dotenv
)

echo.
echo Starting test...
echo.

python test_godaddy.py

echo.
pause
