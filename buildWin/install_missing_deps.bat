@echo off
echo Installing pyautogui...

pip install pyautogui
pip install pillow
pip install mouseinfo

echo install Done!


echo Testing and installing dependencies...

echo Testing pyautogui...
python -c "import pyautogui; print('pyautogui OK')" 2>nul
if errorlevel 1 (
    echo pyautogui missing, installing...
    pip install pyautogui
    pip install pillow
    pip install mouseinfo
)

echo Testing main program...
python ..\main_monitor_gui_app.py

echo Done!
pause 