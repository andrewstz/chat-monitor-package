@echo off
echo Checking model file...

if exist "..\models\best.pt" (
    echo Model file exists: ..\models\best.pt
) else (
    echo Model file missing: ..\models\best.pt
    echo.
    echo Please download the YOLO model file.
    echo You can find it in the models directory or download from:
    echo https://github.com/your-repo/models/best.pt
)

echo.
echo Checking config file...
if exist "..\config_with_yolo.yaml" (
    echo Config file exists: ..\config_with_yolo.yaml
) else (
    echo Config file missing: ..\config_with_yolo.yaml
)

pause 