@echo off
echo Installing Tesseract for Windows...

echo.
echo Step 1: Installing pytesseract...
pip install pytesseract

echo.
echo Step 2: Downloading Tesseract installer...
echo Please download Tesseract from:
echo https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Step 3: Install Tesseract to default location
echo Default: C:\Program Files\Tesseract-OCR
echo.
echo Step 4: Add to PATH
echo Add: C:\Program Files\Tesseract-OCR to your PATH

echo.
echo Step 5: Testing installation...
python -c "
import pytesseract
try:
    pytesseract.get_tesseract_version()
    print('Tesseract installed successfully')
except Exception as e:
    print('Tesseract not found in PATH')
    print('Please install Tesseract and add to PATH')
"

echo.
echo Installation guide completed!
pause 