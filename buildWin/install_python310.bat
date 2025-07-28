@echo off
chcp 65001 >nul
echo ========================================
echo Python 3.10.11 Installation Script
echo ========================================

:: 检查是否已安装Python 3.10
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set CURRENT_VERSION=%%i
    echo Current Python version: %CURRENT_VERSION%
    
    :: 检查是否为3.10.x
    echo %CURRENT_VERSION% | findstr "3.10" >nul
    if not errorlevel 1 (
        echo Python 3.10.x is already installed!
        echo You can now use: .\setup_uv_with_local_python.bat
        pause
        exit /b 0
    )
)

:: 设置下载URL和文件名
set PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
set INSTALLER_NAME=python-3.10.11-amd64.exe

echo Downloading Python 3.10.11...
echo URL: %PYTHON_URL%

:: 检查是否已存在安装包
if exist "%INSTALLER_NAME%" (
    echo Found existing installer: %INSTALLER_NAME%
    echo Do you want to use existing file? (Y/N)
    set /p use_existing=
    if /i "%use_existing%" equ "Y" (
        goto :install_python
    )
)

:: 下载Python安装包
echo Downloading Python 3.10.11 installer...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER_NAME%'}"

if errorlevel 1 (
    echo ERROR: Failed to download Python installer
    echo.
    echo Manual download instructions:
    echo 1. Visit: https://www.python.org/downloads/release/python-31011/
    echo 2. Download: Windows installer (64-bit)
    echo 3. Save as: %INSTALLER_NAME%
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

:install_python
:: 检查安装包是否存在
if not exist "%INSTALLER_NAME%" (
    echo ERROR: Installer not found: %INSTALLER_NAME%
    echo Please download the installer manually and place it in this directory
    pause
    exit /b 1
)

echo Installing Python 3.10.11...
echo This will install Python for all users with PATH option enabled

:: 静默安装Python 3.10.11
"%INSTALLER_NAME%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

if errorlevel 1 (
    echo ERROR: Python installation failed
    echo You can try manual installation:
    echo 1. Run: %INSTALLER_NAME%
    echo 2. Check "Add Python to PATH"
    echo 3. Choose "Install for all users"
    pause
    exit /b 1
)

:: 清理安装包
echo Cleaning up installer...
del "%INSTALLER_NAME%"

:: 刷新环境变量
echo Refreshing environment variables...
call refreshenv >nul 2>&1

:: 验证安装
echo Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python not found in PATH after installation
    echo Please restart your command prompt or computer
    echo Then run: python --version
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set NEW_VERSION=%%i
    echo SUCCESS: Python installed successfully!
    echo Version: %NEW_VERSION%
)

echo ========================================
echo Python 3.10.11 installation completed!
echo ========================================
echo.
echo Next steps:
echo 1. Restart your command prompt
echo 2. Run: python --version
echo 3. Run: .\setup_uv_with_local_python.bat
echo.
pause 