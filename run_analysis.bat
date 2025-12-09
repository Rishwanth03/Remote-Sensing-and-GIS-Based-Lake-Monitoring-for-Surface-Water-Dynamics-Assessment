@echo off
REM Quick run script for Live Lake Monitoring System

echo Starting Live Lake Monitoring Analysis...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Virtual environment not found. Please run setup.bat first
    pause
    exit /b 1
)

REM Run the analysis
python src\main.py %*

echo.
echo Analysis complete! Check outputs folder for results.
pause
