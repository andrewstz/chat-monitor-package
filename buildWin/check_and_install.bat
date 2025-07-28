@echo off
echo Checking and installing all dependencies...

echo Checking basic dependencies...
python -c "import psutil" 2>nul || pip install psutil
python -c "import cv2" 2>nul || pip install opencv-python-headless
python -c "import ultralytics" 2>nul || pip install ultralytics
python -c "import pygame" 2>nul || pip install pygame
python -c "import PIL" 2>nul || pip install pillow
python -c "import requests" 2>nul || pip install requests
python -c "import yaml" 2>nul || pip install pyyaml

echo Checking GUI dependencies...
python -c "import pyautogui" 2>nul || pip install pyautogui
python -c "import pytesseract" 2>nul || pip install pytesseract
python -c "import mouseinfo" 2>nul || pip install mouseinfo
python -c "import pymsgbox" 2>nul || pip install pymsgbox
python -c "import pytweening" 2>nul || pip install pytweening
python -c "import pyscreeze" 2>nul || pip install pyscreeze

echo Testing all dependencies...
python -c "import psutil; print('psutil OK')" 2>nul || echo "psutil missing"
python -c "import cv2; print('cv2 OK')" 2>nul || echo "cv2 missing"
python -c "import ultralytics; print('ultralytics OK')" 2>nul || echo "ultralytics missing"
python -c "import pygame; print('pygame OK')" 2>nul || echo "pygame missing"
python -c "import pyautogui; print('pyautogui OK')" 2>nul || echo "pyautogui missing"
python -c "import pytesseract; print('pytesseract OK')" 2>nul || echo "pytesseract missing"

echo Testing main program...
python ..\main_monitor_gui_app.py

echo Done!
pause 