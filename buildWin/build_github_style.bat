@echo off
echo ========================================
echo GitHub Actions Style Build for Aliyun
echo ========================================

:: Check Python version
echo Checking Python version...
python --version

:: Install dependencies (GitHub Actions style)
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install opencv-python>=4.8.0
pip install numpy>=1.24.0
pip install psutil>=5.9.0
pip install pyautogui>=0.9.54
pip install requests>=2.31.0
pip install PyYAML>=6.0
pip install Pillow>=10.0.0
pip install pytesseract>=0.3.10
pip install watchdog>=3.0.0
pip install ultralytics>=8.0.0
pip install pyinstaller

:: Clean builds
echo.
echo Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

:: Build executable (GitHub Actions style)
echo.
echo Building executable...
pyinstaller --onefile --windowed --name ChatMonitor --add-data "..\sounds;sounds" --add-data "..\models;models" --add-data "..\config_with_yolo.yaml;." --hidden-import=requests --hidden-import=urllib3 --hidden-import=charset_normalizer --hidden-import=idna --hidden-import=certifi --hidden-import=tkinter --hidden-import=PIL --hidden-import=PIL.Image --hidden-import=PIL.ImageTk "..\main_monitor_gui_app.py"

:: Create package (GitHub Actions style)
echo.
echo Creating package...
if exist "dist\ChatMonitor.exe" (
    mkdir -p dist\ChatMonitor_Portable
    copy "dist\ChatMonitor.exe" "dist\ChatMonitor_Portable\"
    if exist "..\sounds" xcopy "..\sounds" "dist\ChatMonitor_Portable\sounds\" /E /I /Y
    if exist "..\models" xcopy "..\models" "dist\ChatMonitor_Portable\models\" /E /I /Y
    if exist "..\config_with_yolo.yaml" copy "..\config_with_yolo.yaml" "dist\ChatMonitor_Portable\"
    if exist "..\start_monitor.bat" copy "..\start_monitor.bat" "dist\ChatMonitor_Portable\"
    if exist "..\README.md" copy "..\README.md" "dist\ChatMonitor_Portable\"
    
    echo.
    echo ========================================
    echo SUCCESS: Build completed!
    echo ========================================
    echo Package: dist\ChatMonitor_Portable\
    echo Test: dist\ChatMonitor_Portable\ChatMonitor.exe
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
)

echo.
echo Press any key to exit...
pause 