@echo off
echo Installing Tesseract OCR...

echo.
echo Method 1: Installing via conda...
conda install -c conda-forge tesseract

echo.
echo Method 2: Installing via pip...
pip install pytesseract

echo.
echo Method 3: Manual installation instructions...
echo.
echo If the above methods fail, please:
echo 1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
echo 2. Install to: C:\Program Files\Tesseract-OCR
echo 3. Add to PATH: C:\Program Files\Tesseract-OCR

echo.
echo Testing Tesseract installation...
python -c "import pytesseract; print('pytesseract OK')" 2>nul || echo "pytesseract missing"

echo.
echo Installation completed!
pause 