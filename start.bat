@echo off
REM ============================================
REM  Carousel Generator - Auto Startup Script
REM  Installs deps, activates env, launches app
REM ============================================

echo 🚀 Starting Carousel Generator with all skills enabled...
echo.

REM Activate virtual environment
call D:\Generator\env\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Check if dependencies are installed
echo 📦 Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ⚙️  Installing dependencies...
    pip install -r requirements.txt
    playwright install chromium
) else (
    echo ✅ Dependencies already installed
)

echo.
echo 🎨 Available skills:
echo    - docs-audit-and-refresh
echo    - docs-update-from-diff
echo    - pr-review
echo    - qwen-code-claw
echo    - terminal-capture
echo.
echo 🛠️  Available commands:
echo    - qc/code-review
echo    - qc/commit
echo    - qc/create-issue
echo    - qc/create-pr
echo.
echo 🌐 Starting Flask app at http://localhost:5000
echo.

REM Start the Flask app
python app.py
