@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Fixing ultralytics Installation
echo ========================================

:: Activate UV environment
call ..\.venv\Scripts\activate.bat

echo.
echo Current Python version:
python --version

echo.
echo Current pip version:
python -m pip --version

echo.
echo Installing ultralytics with different methods...

:: Method 1: Try direct install
echo Method 1: Direct install...
uv pip install ultralytics==8.0.196

:: Method 2: Try with mirror
echo.
echo Method 2: Install with mirror...
uv pip install ultralytics==8.0.196 -i https://mirrors.aliyun.com/pypi/simple/

:: Method 3: Try without version constraint
echo.
echo Method 3: Install latest version...
uv pip install ultralytics

:: Method 4: Try with pip directly
echo.
echo Method 4: Using pip directly...
python -m pip install ultralytics==8.0.196

:: Test installation
echo.
echo Testing ultralytics installation...
python -c "import ultralytics; print('ultralytics version:', ultralytics.__version__)"

echo.
echo Press any key to exit...
pause 