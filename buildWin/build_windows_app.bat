@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo Windows Application Build Script Starting
echo Current Directory: %cd%

:: Check system
if not "%OS%"=="Windows_NT" (
    echo ERROR: This script is only for Windows
    exit /b 1
)

:: Check Python environment
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found, please install Python 3.8+
    exit /b 1
)

echo Python Version:
python --version

:: Check required files
set REQUIRED_FILES=main_monitor_gui_app.py config_with_yolo.yaml fuzzy_matcher.py config_manager.py network_monitor.py

echo Checking required files...
for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo ERROR: Missing required file: %%f
        exit /b 1
    )
    echo   OK: %%f
)

:: Check icon files (prefer PNG, shared with macOS)
echo Checking icon files...
set ICON_FILE=
if exist "assets\icons\icon.png" (
    set ICON_FILE=assets\icons\icon.png
    echo   OK: Found PNG icon file: !ICON_FILE!
) else if exist "assets\icons\icon_256x256.png" (
    set ICON_FILE=assets\icons\icon_256x256.png
    echo   OK: Found PNG icon file: !ICON_FILE!
) else if exist "assets\icon.png" (
    set ICON_FILE=assets\icon.png
    echo   OK: Found PNG icon file: !ICON_FILE!
) else if exist "icons\icon.png" (
    set ICON_FILE=icons\icon.png
    echo   OK: Found PNG icon file: !ICON_FILE!
) else if exist "icon.png" (
    set ICON_FILE=icon.png
    echo   OK: Found PNG icon file: !ICON_FILE!
) else if exist "assets\icons\icon.ico" (
    set ICON_FILE=assets\icons\icon.ico
    echo   OK: Found ICO icon file: !ICON_FILE!
) else if exist "assets\icon.ico" (
    set ICON_FILE=assets\icon.ico
    echo   OK: Found ICO icon file: !ICON_FILE!
) else if exist "icon.ico" (
    set ICON_FILE=icon.ico
    echo   OK: Found ICO icon file: !ICON_FILE!
) else (
    echo   WARNING: No icon file found, will use default icon
    echo   TIP: Run on macOS: python create_png_icon.py
    echo   TIP: Then copy the entire directory to Windows
)

:: Build directories
set BUILD_DIR=build_windows_app
set RELEASE_DIR=release

echo Cleaning build directory...
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"

echo Creating build directory: %BUILD_DIR%
mkdir "%BUILD_DIR%"

:: Install PyInstaller
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

echo Building Windows application...

:: Create PyInstaller command
set PYINSTALLER_CMD=python -m PyInstaller --onedir --windowed --name=ChatMonitor --noconfirm --add-data=config_with_yolo.yaml;. --add-data=fuzzy_matcher.py;. --add-data=config_manager.py;. --add-data=network_monitor.py;. --hidden-import=cv2 --hidden-import=numpy --hidden-import=psutil --hidden-import=pyautogui --hidden-import=requests --hidden-import=urllib3 --hidden-import=charset_normalizer --hidden-import=idna --hidden-import=certifi --hidden-import=yaml --hidden-import=PIL --hidden-import=pytesseract --hidden-import=playsound --hidden-import=watchdog --hidden-import=ultralytics --hidden-import=cv2 --hidden-import=numpy --hidden-import=tkinter --exclude-module=PyQt5 --exclude-module=PyQt6 --exclude-module=IPython --exclude-module=jupyter --exclude-module=scikit-learn --exclude-module=tensorflow --exclude-module=transformers --debug=all

:: Add icon if found
if not "!ICON_FILE!"=="" (
    set PYINSTALLER_CMD=!PYINSTALLER_CMD! --icon=!ICON_FILE!
    echo   Using icon: !ICON_FILE!
)

:: Add main program
set PYINSTALLER_CMD=!PYINSTALLER_CMD! main_monitor_gui_app.py

echo Executing: !PYINSTALLER_CMD!
!PYINSTALLER_CMD!

:: Check build result
if exist "dist\ChatMonitor\ChatMonitor.exe" (
    echo OK: Executable file created successfully: dist\ChatMonitor\ChatMonitor.exe
    
    :: Create release directory
    if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
    
    :: Copy executable to release directory
    echo Copying application to release directory...
    xcopy "dist\ChatMonitor" "%RELEASE_DIR%\ChatMonitor" /E /I /Y
    
    :: Copy resource files if exist
    if exist "sounds" (
        xcopy "sounds" "%RELEASE_DIR%\ChatMonitor\sounds" /E /I /Y
        echo   OK: Copied sounds\
    )
    
    if exist "test_img" (
        xcopy "test_img" "%RELEASE_DIR%\ChatMonitor\test_img" /E /I /Y
        echo   OK: Copied test_img\
    )
    
    if exist "models" (
        xcopy "models" "%RELEASE_DIR%\ChatMonitor\models" /E /I /Y
        echo   OK: Copied models\
    )
    
    :: Copy assets directory if exist
    if exist "assets" (
        xcopy "assets" "%RELEASE_DIR%\ChatMonitor\assets" /E /I /Y
        echo   OK: Copied assets\
    )
    
    :: Copy config file to accessible location
    copy "config_with_yolo.yaml" "%RELEASE_DIR%\ChatMonitor\"
    echo   OK: Copied config_with_yolo.yaml
    
    :: Copy icon file to release directory
    if not "!ICON_FILE!"=="" (
        copy "!ICON_FILE!" "%RELEASE_DIR%\ChatMonitor\icon.png"
        echo   OK: Copied icon to release directory: !ICON_FILE!
    )
    
    :: Create startup script
    echo @echo off > "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo cd /d "%%~dp0" >> "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo ChatMonitor.exe >> "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo pause >> "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo   OK: Created startup script: start_chatmonitor.bat
    
    :: Create README file
    echo ChatMonitor - Chat Popup Monitor > "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo. >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo Usage Instructions: >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 1. Double-click start_chatmonitor.bat to start >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 2. Or double-click ChatMonitor.exe directly >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 3. First run may need firewall access >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo. >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo Features: >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - YOLO popup detection >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - Tesseract OCR text recognition >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - Network monitoring >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - Process monitoring >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo   OK: Created README file: README.txt
    
    :: Calculate size
    for /f "tokens=1" %%a in ('dir "%RELEASE_DIR%\ChatMonitor" /s ^| find "File(s)"') do set APP_SIZE=%%a
    echo Application size: !APP_SIZE!
    
    :: Create zip package
    echo Creating portable zip package...
    set ZIP_NAME=ChatMonitor-Windows-v1.0.0.zip
    set ZIP_PATH=%RELEASE_DIR%\%ZIP_NAME%
    
    :: Use PowerShell to create ZIP file
    powershell -command "Compress-Archive -Path '%RELEASE_DIR%\ChatMonitor' -DestinationPath '%ZIP_PATH%' -Force"
    
    if exist "%ZIP_PATH%" (
        echo OK: Portable zip package created successfully: %ZIP_PATH%
    ) else (
        echo ERROR: Failed to create zip package
    )
    
    echo.
    echo Build completed!
    echo Application: %RELEASE_DIR%\ChatMonitor\
    echo Portable zip: %ZIP_PATH%
    echo.
    echo Usage:
    echo   1. Extract %ZIP_NAME% to any directory
    echo   2. Double-click start_chatmonitor.bat to start
    echo   3. Or double-click ChatMonitor.exe directly
    echo.
    echo NOTE: First run may need Windows firewall access
    echo Build features:
    echo   - Uses PyInstaller to create standalone exe
    echo   - Auto-handles icons and resource files
    echo   - Portable version, no installation needed
    echo   - Includes startup script and documentation
    
) else (
    echo ERROR: Build failed, executable not found
    exit /b 1
)

pause 