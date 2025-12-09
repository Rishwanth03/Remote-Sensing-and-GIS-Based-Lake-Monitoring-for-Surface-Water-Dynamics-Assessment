@echo off
REM Lake Monitoring Quick Start Script
REM This script helps set up and run the automated monitoring system

echo.
echo ================================
echo Lake Monitoring - Quick Start
echo ================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment activated
echo.

REM Show menu
:menu
echo ================================
echo SELECT AN OPTION:
echo ================================
echo.
echo 1. Test monitoring (run once)
echo 2. Start automatic scheduler
echo 3. Check scheduler status
echo 4. View logs
echo 5. Launch dashboard
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto test
if "%choice%"=="2" goto start_scheduler
if "%choice%"=="3" goto status
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto dashboard
if "%choice%"=="6" goto exit

echo [ERROR] Invalid choice
goto menu

:test
echo.
echo Running test monitoring (daily mode)...
echo.
python src/scheduler.py --run-once daily
if %errorlevel% equ 0 (
    echo.
    echo [OK] Test completed successfully!
    echo Check outputs/maps/ for generated maps
) else (
    echo [ERROR] Test failed
)
pause
goto menu

:start_scheduler
echo.
echo Starting automatic scheduler...
echo.
echo Schedule:
echo  - Daily at 8:00 AM
echo  - Weekly on Monday at 6:00 AM
echo.
echo Press Ctrl+C to stop
echo.
python src/scheduler.py --start
pause
goto menu

:status
echo.
python src/scheduler.py --status
pause
goto menu

:logs
echo.
echo Recent logs:
echo.
if exist "outputs\scheduler.log" (
    powershell Get-Content outputs\scheduler.log -Tail 20
) else (
    echo No scheduler logs found yet
)
pause
goto menu

:dashboard
echo.
echo Launching dashboard at http://localhost:8501
echo Press Ctrl+C to stop
echo.
streamlit run src/dashboard.py
pause
goto menu

:exit
echo.
echo Goodbye!
pause
exit /b 0
