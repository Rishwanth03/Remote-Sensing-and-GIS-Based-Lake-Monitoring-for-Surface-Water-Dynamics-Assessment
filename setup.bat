@echo off
REM Setup script for Live Lake Monitoring System
REM This script automates the initial setup process

echo ============================================================
echo Live Lake Monitoring System - Setup Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Python found
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo [2/5] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
echo This may take 5-10 minutes depending on your internet speed...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [5/5] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [IMPORTANT] Please edit .env file and add your GEE project ID
    echo Open .env in a text editor and replace 'your-gee-project-id' with your actual project ID
    notepad .env
) else (
    echo [5/5] .env file already exists
)
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Make sure you have registered for Google Earth Engine
echo    Visit: https://earthengine.google.com/signup/
echo.
echo 2. Authenticate with Google Earth Engine:
echo    python src\gee_auth.py
echo.
echo 3. Edit config\config.yaml with your lake coordinates
echo.
echo 4. Run your first analysis:
echo    python src\main.py --quick
echo.
echo 5. Launch the dashboard:
echo    streamlit run src\dashboard.py
echo.
echo For detailed instructions, see docs\SETUP_GUIDE.md
echo.
pause
