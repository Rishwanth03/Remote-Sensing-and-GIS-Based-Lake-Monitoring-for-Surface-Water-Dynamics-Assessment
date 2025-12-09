#!/bin/bash
# Live Lake Monitoring - Quick Start Script
# Run live monitoring with Google Earth Engine

@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  LIVE LAKE MONITORING - GOOGLE EARTH ENGINE
echo ============================================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo ✗ Virtual environment not found
    echo Installing dependencies...
    python -m venv venv
    call .\venv\Scripts\activate.bat
    pip install -r requirements.txt
)

REM Activate venv
call .\venv\Scripts\activate.bat

REM Check GEE setup
echo.
echo [1/4] Checking Google Earth Engine setup...
python check_gee_setup.py

if errorlevel 1 (
    echo.
    echo ⚠  GEE setup incomplete. Please fix permissions:
    echo    → Read GEE_PERMISSION_FIX.md
    echo    → Grant access to: rishwanthuk20@gmail.com
    echo    → Visit: https://console.cloud.google.com/iam-admin/iam
    echo.
    pause
    exit /b 1
)

REM Run monitoring
echo.
echo [2/4] Running live lake monitoring...
python src/main.py --quick --months 1

if errorlevel 1 (
    echo.
    echo ✗ Monitoring failed
    pause
    exit /b 1
)

REM Show results
echo.
echo [3/4] Results saved to:
echo    ✓ Maps: outputs\maps\
echo    ✓ Data: outputs\timeseries\
echo    ✓ Report: outputs\reports\
echo.

REM Ask to view results
echo [4/4] View results?
set /p view="Open dashboard now? (y/n): "
if /i "!view!"=="y" (
    echo Launching Streamlit dashboard...
    streamlit run src/dashboard.py
) else (
    echo.
    echo To view results later:
    echo    Dashboard: streamlit run src/dashboard.py
    echo    Maps: outputs\maps\latest_water_extent.html
    echo    Data: outputs\timeseries\lake_timeseries.csv
)

echo.
echo ============================================================
echo ✅ Live monitoring complete!
echo ============================================================
pause
