@echo off
chcp 65001 >nul
echo ========================================
echo Python Version Check Script
echo ========================================

echo Checking available Python versions...
echo.

:: Check Python 3.9
echo Checking Python 3.9...
python3.9 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Python 3.9 found
    python3.9 --version
) else (
    echo MISSING: Python 3.9
)

:: Check Python 3.10
echo.
echo Checking Python 3.10...
python3.10 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Python 3.10 found
    python3.10 --version
) else (
    echo MISSING: Python 3.10
)

:: Check Python 3.11
echo.
echo Checking Python 3.11...
python3.11 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Python 3.11 found
    python3.11 --version
) else (
    echo MISSING: Python 3.11
)

:: Check default Python
echo.
echo Checking default Python...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: Default Python found
    python --version
) else (
    echo MISSING: Default Python
)

:: Check py launcher
echo.
echo Checking py launcher...
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS: py launcher found
    py --version
    echo.
    echo Available Python versions via py launcher:
    py -0
) else (
    echo MISSING: py launcher
)

echo.
echo ========================================
echo Recommendation:
echo - For Python 3.9: Use 'python3.9' or 'py -3.9'
echo - For Python 3.10: Use 'python3.10' or 'py -3.10'
echo - For Python 3.11: Use 'python3.11' or 'py -3.11'
echo - For default: Use 'python'
echo ========================================

pause 