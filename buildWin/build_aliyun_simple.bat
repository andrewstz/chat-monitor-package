@echo off
chcp 65001 >nul

echo ========================================
echo Simple Build for Aliyun Windows
echo ========================================

:: 检查主程序文件
if not exist "..\main_monitor_gui_app.py" (
    echo ERROR: main_monitor_gui_app.py not found!
    echo Please make sure you are in the correct directory.
    pause
    exit /b 1
)

:: 清理之前的构建
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: 测试主程序
echo Testing main program...
python ..\main_monitor_gui_app.py --test
if errorlevel 1 (
    echo ERROR: Main program test failed!
    echo Please check if all dependencies are installed correctly.
    pause
    exit /b 1
)

:: 开始构建
echo.
echo Starting build process...
echo This may take several minutes...

pyinstaller --onefile --windowed --name ChatMonitor --add-data "..\sounds;sounds" --add-data "..\models;models" --add-data "..\config_with_yolo.yaml;." "..\main_monitor_gui_app.py"

:: 检查构建结果
if exist "dist\ChatMonitor.exe" (
    echo.
    echo ========================================
    echo SUCCESS: Build completed!
    echo ========================================
    echo Generated file: dist\ChatMonitor.exe
    dir dist\ChatMonitor.exe
    
    echo.
    echo Creating portable package...
    if not exist "dist\ChatMonitor_Portable" mkdir "dist\ChatMonitor_Portable"
    copy "dist\ChatMonitor.exe" "dist\ChatMonitor_Portable\"
    if exist "..\sounds" xcopy "..\sounds" "dist\ChatMonitor_Portable\sounds\" /E /I /Y
    if exist "..\models" xcopy "..\models" "dist\ChatMonitor_Portable\models\" /E /I /Y
    if exist "..\config_with_yolo.yaml" copy "..\config_with_yolo.yaml" "dist\ChatMonitor_Portable\"
    
    echo.
    echo Portable package created: dist\ChatMonitor_Portable\
    echo.
    echo To test the application:
    echo dist\ChatMonitor_Portable\ChatMonitor.exe
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo.
    echo Troubleshooting:
    echo 1. Check if pyinstaller is installed: pip install pyinstaller
    echo 2. Check if main_monitor_gui_app.py exists
    echo 3. Try running: python ..\main_monitor_gui_app.py
)

echo.
echo Press any key to exit...
pause 