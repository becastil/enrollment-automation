@echo off
echo ========================================
echo ENROLLMENT AUTOMATION - TIER RECONCILIATION
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
python -c "import pandas, openpyxl, numpy" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install pandas openpyxl numpy
)

REM Run the main script
echo.
echo Running enrollment automation...
echo.
python enrollment_automation_tier_reconciled.py

echo.
echo ========================================
echo PROCESS COMPLETE
echo ========================================
echo.
echo Output files:
echo   - Prime Enrollment Funding by Facility for August_updated.xlsx
echo   - output\write_log.csv
echo   - output\tier_reconciliation_report.csv
echo.
pause