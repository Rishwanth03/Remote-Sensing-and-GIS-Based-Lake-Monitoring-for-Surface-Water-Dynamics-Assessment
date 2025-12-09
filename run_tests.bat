@echo off
REM Test Framework Setup and Execution Script

echo ============================================================
echo Live Lake Monitoring - Test Framework Setup
echo ============================================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    echo Run setup.bat first to create the environment
    pause
    exit /b 1
)

echo Installing test dependencies...
pip install -r requirements-dev.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install test dependencies
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Running Tests
echo ============================================================
echo.

REM Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=html --cov-report=term

echo.
echo ============================================================
echo Test Results
echo ============================================================
echo.
echo Coverage report generated at: htmlcov\index.html
echo.
echo To run specific test types:
echo   pytest tests/ -m unit          # Run only unit tests
echo   pytest tests/ -m integration   # Run only integration tests
echo   pytest tests/ -k test_ndwi     # Run tests matching pattern
echo.

pause
