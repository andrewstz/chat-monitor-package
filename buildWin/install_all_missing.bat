@echo off
echo Installing all missing dependencies...

echo Installing pyautogui...
pip install pyautogui

echo Installing pytesseract...
pip install pytesseract

echo Installing other dependencies...
pip install pillow
pip install mouseinfo
pip install pymsgbox
pip install pytweening
pip install pyscreeze

echo Testing installations...
python -c "import pyautogui; print('pyautogui OK')" 2>nul || echo "pyautogui missing"
python -c "import pytesseract; print('pytesseract OK')" 2>nul || echo "pytesseract missing"

echo Testing main program...
python ..\main_monitor_gui_app.py

echo Done!
pause 