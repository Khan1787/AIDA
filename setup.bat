@echo off
echo 🚀 Starting AIDA Demo Setup (Flask Only)...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nu este instalat!
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
cd aida-backend
pip install -r requirements.txt

echo ✅ Setup complet!
echo.
echo 🎯 Pentru a rula demo-ul:
echo 1. python app.py
echo 2. Deschide index.html în browser

pause