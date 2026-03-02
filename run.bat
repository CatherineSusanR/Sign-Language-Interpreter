@echo off
echo ==========================================
echo      Sign Language Converter Setup
echo ==========================================

echo [Step 1] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies. Please ensure Python is installed and added to PATH.
    pause
    exit /b
)

echo.
echo [Step 2] Generating placeholder images (if needed)...
python create_placeholders.py

echo.
echo [Step 3] Starting Application...
python main.py

pause
