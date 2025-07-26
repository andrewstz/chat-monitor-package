@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Checking Dependencies
echo ========================================

:: Activate UV environment
call ..\.venv\Scripts\activate.bat

echo.
echo Checking installed packages:
uv pip list

echo.
echo Testing imports:
python -c "import psutil; print('psutil OK')"
python -c "import cv2; print('cv2 OK')"
python -c "import numpy; print('numpy OK')"
python -c "import ultralytics; print('ultralytics OK')"
python -c "import PIL; print('PIL OK')"
python -c "import requests; print('requests OK')"
python -c "import yaml; print('yaml OK')"
python -c "import tkinter; print('tkinter OK')"

echo.
echo Press any key to exit...
pause 