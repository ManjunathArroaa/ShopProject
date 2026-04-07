@echo off
echo ========================================
echo  Payment Reminder Tool - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/Update dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Copy .env.example to .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo NOTE: Please update the SECRET_KEY in .env file for production!
    echo.
)

REM Start the server
echo ========================================
echo  Starting the server...
echo ========================================
echo.
echo Access the application at:
echo   - Local: http://localhost:8000
echo   - Network: http://YOUR_PC_IP:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
