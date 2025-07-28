@echo off
chcp 65001 >nul

echo ========================================
echo Conda Dependencies Installer (Fixed)
echo ========================================

:: Check conda
conda --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: conda not found!
    pause
    exit /b 1
)

echo Installing dependencies...

:: Install with conda
echo Installing with conda...
conda install -y -c conda-forge opencv
conda install -y -c conda-forge pillow
conda install -y -c conda-forge requests
conda install -y -c conda-forge pyyaml
conda install -y -c conda-forge psutil
conda install -y -c conda-forge pygame
conda install -y -c conda-forge pyinstaller

:: Install with pip
echo Installing with pip...
pip install ultralytics

:: Test
echo.
echo Testing main program...
python ..\main_monitor_gui_app.py

if errorlevel 1 (
    echo.
    echo ERROR: Test failed!
    echo.
    echo Manual commands:
    echo conda install -c conda-forge opencv pillow requests pyyaml psutil pygame pyinstaller
    echo pip install ultralytics
) else (
    echo.
    echo SUCCESS: All dependencies installed!
    echo.
    echo You can now run: buildWin\build_conda_simple.bat
)

pause 