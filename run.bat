@echo off
cls
echo.
echo ============================================================
echo     Prime Employee Enrollment Data Processing System
echo ============================================================
echo.
echo Available Commands:
echo.
echo   1. Install Dependencies
echo   2. Run Main Processing
echo   3. Run Analytics Report
echo   4. Run Data Validation
echo   5. Update Prime Output File
echo   6. Run Demo/Test Script
echo   7. Check Excel Columns
echo   8. Create Sample Data
echo   9. Exit
echo.
echo ============================================================
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto process
if "%choice%"=="3" goto analytics
if "%choice%"=="4" goto validate
if "%choice%"=="5" goto update
if "%choice%"=="6" goto demo
if "%choice%"=="7" goto check
if "%choice%"=="8" goto sample
if "%choice%"=="9" goto end

echo Invalid choice. Please run the script again.
pause
goto end

:install
echo.
echo Installing Python dependencies...
echo.
pip install -r requirements.txt
echo.
echo Installation complete!
pause
goto end

:process
echo.
echo Running enrollment automation with tier reconciliation (all fixes)...
echo.
python enrollment_automation_tier_reconciled.py
echo.
echo Processing complete! Check the output folder for results.
pause
goto end

:analytics
echo.
echo Generating analytics report...
echo.
python src\enrollment_analytics.py
echo.
echo Analytics report generated! Check output\analytics_report.xlsx
pause
goto end

:validate
echo.
echo Running data validation checks...
echo.
python src\enrollment_validator.py
echo.
echo Validation complete! Check output\validation_report.csv
pause
goto end

:update
echo.
echo Updating Prime output file (Column D)...
echo.
echo Running in DRY-RUN mode first...
python src\update_prime_output.py --source "data\input\Data_file_prime.xlsx" --target "data\input\Prime_output_file.xlsx" --dry-run
echo.
set /p confirm="Do you want to apply the changes? (y/n): "
if /i "%confirm%"=="y" (
    echo.
    echo Applying changes...
    python src\update_prime_output.py --source "data\input\Data_file_prime.xlsx" --target "data\input\Prime_output_file.xlsx"
    echo.
    echo Update complete!
) else (
    echo.
    echo Update cancelled.
)
pause
goto end

:demo
echo.
echo Running demo/test script...
echo.
cd tests
python enrollment_processing_demo.py
cd ..
echo.
echo Demo complete!
pause
goto end

:check
echo.
echo Checking Excel column structure...
echo.
python scripts\check_excel_columns.py
echo.
pause
goto end

:sample
echo.
echo Creating sample Excel data...
echo.
python scripts\create_sample_excel.py
echo.
echo Sample data created!
pause
goto end

:end
echo.
echo Thank you for using Prime EFR Data Processing System!
echo.