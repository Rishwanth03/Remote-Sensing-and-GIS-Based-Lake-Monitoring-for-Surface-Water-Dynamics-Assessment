@echo off
REM Quick Analysis Script - Runs 6 months of data for Lake Victoria

echo ============================================================
echo Live Lake Monitoring - Quick Analysis
echo ============================================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Checking GEE authentication...
python src\gee_auth.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: GEE authentication failed!
    echo Please update your GEE_PROJECT_ID in the .env file
    echo Visit: https://console.cloud.google.com/
    pause
    exit /b 1
)

echo.
echo Starting quick analysis (6 months)...
echo This will:
echo   - Fetch Sentinel-2 data from Google Earth Engine
echo   - Calculate NDWI (water index)
echo   - Extract water surface area over time
echo   - Generate visualizations and statistics
echo.

python src\main.py --quick

echo.
echo ============================================================
echo Analysis complete!
echo.
echo Outputs saved to:
echo   - Maps: outputs\maps\
echo   - Time series data: outputs\timeseries\
echo   - Reports: outputs\reports\
echo.
echo To view the interactive dashboard:
echo   streamlit run src\dashboard.py
echo.
pause
