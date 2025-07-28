@echo off
echo Simple Tesseract Check

echo.
echo Step 1: Check pytesseract module
python -c "import pytesseract; print('pytesseract OK')"

echo.
echo Step 2: Check tesseract executable
tesseract --version

echo.
echo Step 3: Test pytesseract
python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
python check_tesseract.py
echo.
echo Check completed!
pause 