@echo off
REM Launch Streamlit dashboard

echo Starting Live Lake Monitoring Dashboard...
echo.
echo Dashboard will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Virtual environment not found. Please run setup.bat first
    pause
    exit /b 1
)

REM Launch dashboard
streamlit run src\dashboard.py

pause
