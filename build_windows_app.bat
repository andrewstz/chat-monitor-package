@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🪟 Windows 应用程序构建脚本启动
echo 📁 当前目录: %cd%

:: 检查系统
if not "%OS%"=="Windows_NT" (
    echo ❌ 此脚本仅适用于 Windows
    exit /b 1
)

:: 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 python，请先安装Python 3.8+
    exit /b 1
)

echo ✅ Python版本:
python --version

:: 检查必要文件
set REQUIRED_FILES=main_monitor_gui_app.py config_with_yolo.yaml fuzzy_matcher.py config_manager.py network_monitor.py

echo 🔍 检查必要文件...
for %%f in (%REQUIRED_FILES%) do (
    if not exist "%%f" (
        echo ❌ 缺少必要文件: %%f
        exit /b 1
    )
    echo   ✅ %%f
)

:: 检查图标文件（优先使用PNG，与macOS共用）
echo 🎨 检查图标文件...
set ICON_FILE=
if exist "assets\icons\icon.png" (
    set ICON_FILE=assets\icons\icon.png
    echo   ✅ 找到PNG图标文件: !ICON_FILE!
) else if exist "assets\icons\icon_256x256.png" (
    set ICON_FILE=assets\icons\icon_256x256.png
    echo   ✅ 找到PNG图标文件: !ICON_FILE!
) else if exist "assets\icon.png" (
    set ICON_FILE=assets\icon.png
    echo   ✅ 找到PNG图标文件: !ICON_FILE!
) else if exist "icons\icon.png" (
    set ICON_FILE=icons\icon.png
    echo   ✅ 找到PNG图标文件: !ICON_FILE!
) else if exist "icon.png" (
    set ICON_FILE=icon.png
    echo   ✅ 找到PNG图标文件: !ICON_FILE!
) else if exist "assets\icons\icon.ico" (
    set ICON_FILE=assets\icons\icon.ico
    echo   ✅ 找到ICO图标文件: !ICON_FILE!
) else if exist "assets\icon.ico" (
    set ICON_FILE=assets\icon.ico
    echo   ✅ 找到ICO图标文件: !ICON_FILE!
) else if exist "icon.ico" (
    set ICON_FILE=icon.ico
    echo   ✅ 找到ICO图标文件: !ICON_FILE!
) else (
    echo   ⚠️  未找到图标文件，将使用默认图标
    echo   💡 建议在macOS上运行: python create_png_icon.py
    echo   💡 然后将整个目录复制到Windows环境
)

:: 构建目录
set BUILD_DIR=build_windows_app
set RELEASE_DIR=release

echo 🧹 清理构建目录...
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"

echo 📁 创建构建目录: %BUILD_DIR%
mkdir "%BUILD_DIR%"

:: 安装PyInstaller
echo 📦 检查PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 📦 安装 PyInstaller...
    python -m pip install pyinstaller
)

echo 🔨 构建Windows应用程序...

:: 创建PyInstaller命令
set PYINSTALLER_CMD=python -m PyInstaller --onedir --windowed --name=ChatMonitor --noconfirm --add-data=config_with_yolo.yaml;. --add-data=fuzzy_matcher.py;. --add-data=config_manager.py;. --add-data=network_monitor.py;. --hidden-import=cv2 --hidden-import=numpy --hidden-import=psutil --hidden-import=pyautogui --hidden-import=requests --hidden-import=urllib3 --hidden-import=charset_normalizer --hidden-import=idna --hidden-import=certifi --hidden-import=yaml --hidden-import=PIL --hidden-import=pytesseract --hidden-import=playsound --hidden-import=watchdog --hidden-import=ultralytics --hidden-import=cv2 --hidden-import=numpy --hidden-import=tkinter --exclude-module=PyQt5 --exclude-module=PyQt6 --exclude-module=IPython --exclude-module=jupyter --exclude-module=scikit-learn --exclude-module=tensorflow --exclude-module=transformers --debug=all

:: 添加图标（如果找到）
if not "!ICON_FILE!"=="" (
    set PYINSTALLER_CMD=!PYINSTALLER_CMD! --icon=!ICON_FILE!
    echo   🎨 使用图标: !ICON_FILE!
)

:: 添加主程序
set PYINSTALLER_CMD=!PYINSTALLER_CMD! main_monitor_gui_app.py

echo 🚀 执行: !PYINSTALLER_CMD!
!PYINSTALLER_CMD!

:: 检查构建结果
if exist "dist\ChatMonitor\ChatMonitor.exe" (
    echo ✅ 可执行文件创建成功: dist\ChatMonitor\ChatMonitor.exe
    
    :: 创建发布目录
    if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
    
    :: 复制可执行文件到发布目录
    echo 📦 复制应用程序到发布目录...
    xcopy "dist\ChatMonitor" "%RELEASE_DIR%\ChatMonitor" /E /I /Y
    
    :: 复制资源文件（如果存在）
    if exist "sounds" (
        xcopy "sounds" "%RELEASE_DIR%\ChatMonitor\sounds" /E /I /Y
        echo   ✅ 复制 sounds\
    )
    
    if exist "test_img" (
        xcopy "test_img" "%RELEASE_DIR%\ChatMonitor\test_img" /E /I /Y
        echo   ✅ 复制 test_img\
    )
    
    if exist "models" (
        xcopy "models" "%RELEASE_DIR%\ChatMonitor\models" /E /I /Y
        echo   ✅ 复制 models\
    )
    
    :: 复制 assets 目录（如果存在）
    if exist "assets" (
        xcopy "assets" "%RELEASE_DIR%\ChatMonitor\assets" /E /I /Y
        echo   ✅ 复制 assets\
    )
    
    :: 复制配置文件到外部可访问位置
    copy "config_with_yolo.yaml" "%RELEASE_DIR%\ChatMonitor\"
    echo   ✅ 复制 config_with_yolo.yaml
    
    :: 复制图标文件到发布目录
    if not "!ICON_FILE!"=="" (
        copy "!ICON_FILE!" "%RELEASE_DIR%\ChatMonitor\icon.png"
        echo   ✅ 复制图标到发布目录: !ICON_FILE!
    )
    
    :: 创建启动脚本
    echo @echo off > "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo cd /d "%%~dp0" >> "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo ChatMonitor.exe >> "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo pause >> "%RELEASE_DIR%\ChatMonitor\start_chatmonitor.bat"
    echo   ✅ 创建启动脚本: start_chatmonitor.bat
    
    :: 创建README文件
    echo ChatMonitor - 聊天弹窗监控器 > "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo. >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 使用说明: >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 1. 双击 start_chatmonitor.bat 启动程序 >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 2. 或者直接双击 ChatMonitor.exe >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 3. 首次运行可能需要允许防火墙访问 >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo. >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo 功能特性: >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - YOLO弹出框检测 >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - Tesseract OCR文字识别 >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - 网络监控功能 >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo - 进程监控功能 >> "%RELEASE_DIR%\ChatMonitor\README.txt"
    echo   ✅ 创建说明文件: README.txt
    
    :: 计算大小
    for /f "tokens=1" %%a in ('dir "%RELEASE_DIR%\ChatMonitor" /s ^| find "个文件"') do set APP_SIZE=%%a
    echo 📦 应用程序大小: !APP_SIZE!
    
    :: 创建压缩包
    echo 📦 创建绿色版压缩包...
    set ZIP_NAME=ChatMonitor-Windows-v1.0.0.zip
    set ZIP_PATH=%RELEASE_DIR%\%ZIP_NAME%
    
    :: 使用PowerShell创建ZIP文件
    powershell -command "Compress-Archive -Path '%RELEASE_DIR%\ChatMonitor' -DestinationPath '%ZIP_PATH%' -Force"
    
    if exist "%ZIP_PATH%" (
        echo ✅ 绿色版压缩包创建成功: %ZIP_PATH%
    ) else (
        echo ❌ 压缩包创建失败
    )
    
    echo.
    echo 🎉 构建完成！
    echo 📁 应用程序: %RELEASE_DIR%\ChatMonitor\
    echo 📦 绿色版压缩包: %ZIP_PATH%
    echo.
    echo 🚀 使用方法:
    echo   1. 解压 %ZIP_NAME% 到任意目录
    echo   2. 双击 start_chatmonitor.bat 启动程序
    echo   3. 或者直接双击 ChatMonitor.exe
    echo.
    echo ⚠️  注意: 首次运行可能需要在Windows防火墙中允许访问
    echo 🔧 构建特性:
    echo   - 使用 PyInstaller 创建独立的 exe 文件
    echo   - 自动处理图标和资源文件
    echo   - 绿色版免安装，可直接运行
    echo   - 包含启动脚本和说明文件
    
) else (
    echo ❌ 构建失败，未找到可执行文件
    exit /b 1
)

pause 