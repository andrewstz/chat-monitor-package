@echo off
echo Fixing detection configuration...

echo Creating models directory...
if not exist "..\models" mkdir "..\models"

echo Creating backup of current config...
if exist "..\config_with_yolo.yaml" (
    copy "..\config_with_yolo.yaml" "..\config_with_yolo_backup.yaml"
    echo Backup created: config_with_yolo_backup.yaml
)

echo Creating improved config...
(
echo # 改进的配置文件 - 提高检测率
echo chat_app:
echo   name: "Mango"
echo   target_contacts:
echo     - js_wbmalia-研发部助理
echo     - 人事小姐姐
echo   fuzzy_match:
echo     enabled: true
echo     similarity_threshold: 0.5
echo     min_length: 2
echo.
echo monitor:
echo   check_interval: 1
echo   reply_wait: 3
echo.
echo yolo:
echo   enabled: true
echo   model_path: "models/best.pt"
echo   confidence: 0.3
echo   use_fallback: true
echo.
echo ocr:
echo   tesseract:
echo     lang: "chi_sim+eng"
echo     config: "--psm 6"
echo     use_preprocessing: true
echo.
echo debug:
echo   save_processed_images: true
echo   save_detection_images: true
echo   verbose: true
) > "..\config_with_yolo.yaml"

echo ✓ Created improved config with lower confidence threshold
echo.
echo Next steps:
echo 1. Download the YOLO model file to ..\models\best.pt
echo 2. Restart the monitoring program
echo 3. Test detection with the new settings

pause 