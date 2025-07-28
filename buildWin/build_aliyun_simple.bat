@echo off
echo ========================================
echo Simple Build for Windows
echo ========================================

:: Check main program
if not exist "..\main_monitor_gui_app.py" (
    echo ERROR: main_monitor_gui_app.py not found!
    pause
    exit /b 1
)

:: Clean builds
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: Build
echo.
echo Starting build...
echo This may take several minutes...

pyinstaller --onefile --windowed --name ChatMonitor --add-data "..\sounds;sounds" --add-data "..\models;models" --add-data "..\config_with_yolo.yaml;." "..\main_monitor_gui_app.py"

:: Check result
if exist "dist\ChatMonitor.exe" (
    echo.
    echo ========================================
    echo SUCCESS: Build completed!
    echo ========================================
    echo File: dist\ChatMonitor.exe
    dir dist\ChatMonitor.exe
    
    echo.
    echo Creating portable package...
    if not exist "dist\ChatMonitor_Portable" mkdir "dist\ChatMonitor_Portable"
    copy "dist\ChatMonitor.exe" "dist\ChatMonitor_Portable\"
    if exist "..\sounds" xcopy "..\sounds" "dist\ChatMonitor_Portable\sounds\" /E /I /Y
    if exist "..\models" xcopy "..\models" "dist\ChatMonitor_Portable\models\" /E /I /Y
    if exist "..\config_with_yolo.yaml" copy "..\config_with_yolo.yaml" "dist\ChatMonitor_Portable\"
    
    echo.
    echo Portable package: dist\ChatMonitor_Portable\
    echo.
    echo Test: dist\ChatMonitor_Portable\ChatMonitor.exe
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo.
    echo Troubleshooting:
    echo 1. Install pyinstaller: pip install pyinstaller
    echo 2. Check main_monitor_gui_app.py exists
    echo 3. Try: python ..\main_monitor_gui_app.py
)

echo.
echo Press any key to exit...
pause 