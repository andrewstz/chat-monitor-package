@echo off
echo Fixing startup issues...

echo Installing watchdog...
pip install watchdog

echo Creating debug log directory...
if not exist "C:\tmp" mkdir "C:\tmp"

echo Creating latest.py file...
(
echo import sys
echo import os
echo sys.path.append('..')
echo from main_monitor_gui_app import main
echo if __name__ == "__main__":
echo     main()
) > "latest.py"

echo Testing the fix...
python latest.py

echo Fix completed!
pause 