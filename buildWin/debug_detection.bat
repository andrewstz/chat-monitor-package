@echo off
echo Checking model and config files... 

echo.
echo Checking model file...
if exist "..\models\best.pt" (
    echo Model file exists: ..\models\best.pt
) else (
    echo Model file missing: ..\models\best.pt
    echo Please download the YOLO model file.
)

echo.
echo Checking config file...
if exist "..\config_with_yolo.yaml" (
    echo Config file exists: ..\config_with_yolo.yaml
) else (
    echo Config file missing: ..\config_with_yolo.yaml
)

echo.
echo Testing Python imports...
python -c "import ultralytics; print('ultralytics OK')" 2>nul || echo "ultralytics missing"
python -c "import cv2; print('cv2 OK')" 2>nul || echo "cv2 missing"
python -c "import pyautogui; print('pyautogui OK')" 2>nul || echo "pyautogui missing"

echo.
echo Check completed!
pause 