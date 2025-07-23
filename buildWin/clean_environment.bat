@echo off
chcp 65001 >nul
echo ========================================
echo Clean Environment Script
echo ========================================

echo Cleaning existing environment...

:: Remove existing .venv directory
if exist "..\.venv" (
    echo Removing existing .venv directory...
    rmdir /s /q "..\.venv"
    echo SUCCESS: .venv directory removed
) else (
    echo No .venv directory found
)

:: Remove existing uv directory
if exist "..\uv" (
    echo Removing existing uv directory...
    rmdir /s /q "..\uv"
    echo SUCCESS: uv directory removed
) else (
    echo No uv directory found
)

:: Clean UV cache
echo Cleaning UV cache...
uv cache clean

:: Remove temporary files
if exist "temp_requirements_*.txt" (
    del temp_requirements_*.txt
    echo SUCCESS: Temporary files removed
)

echo ========================================
echo SUCCESS: Environment cleaned!
echo ========================================
echo Now you can create a fresh environment
echo Run: setup_uv_offline.bat
echo ========================================

pause 