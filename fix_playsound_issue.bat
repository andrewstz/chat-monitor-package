@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

echo Fixing playsound installation issue...

:: Try different approaches to install playsound
echo Attempting to install playsound with different methods...

:: Method 1: Try with --frozen flag
echo Method 1: Using --frozen flag...
uv add playsound --frozen 2>nul
if not errorlevel 1 (
    echo SUCCESS: playsound installed with --frozen flag
    goto :success
)

:: Method 2: Try specific version
echo Method 2: Installing specific version...
uv add "playsound==1.2.2" 2>nul
if not errorlevel 1 (
    echo SUCCESS: playsound 1.2.2 installed
    goto :success
)

:: Method 3: Try older version
echo Method 3: Installing older version...
uv add "playsound==1.2.0" 2>nul
if not errorlevel 1 (
    echo SUCCESS: playsound 1.2.0 installed
    goto :success
)

:: Method 4: Use pip as fallback
echo Method 4: Using pip as fallback...
uv run pip install "playsound==1.2.2" 2>nul
if not errorlevel 1 (
    echo SUCCESS: playsound installed via pip
    goto :success
)

:: All methods failed
echo WARNING: All playsound installation methods failed
echo Using alternative audio solution...
goto :alternative

:success
echo.
echo Audio dependency installed successfully!
echo You can now use playsound for audio features.
goto :end

:alternative
echo.
echo Setting up alternative audio solution...
echo The application will use system commands for audio playback.
echo This works on Windows, macOS, and Linux without additional dependencies.

:: Test alternative audio
echo Testing alternative audio system...
uv run python audio_alternative.py

:end
echo.
echo Audio setup completed!
echo You can now run: build_windows_uv_simple.bat
pause 