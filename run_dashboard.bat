@echo off
echo 🚀 Starting Smart Contract AI Analyzer Dashboard...
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH!
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "dashboard\dashboard.py" (
    echo ❌ Error: dashboard\dashboard.py not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Run the dashboard
echo 🌐 Starting dashboard server...
echo 📱 Dashboard will be available at: http://localhost:8501
echo 🛑 Press Ctrl+C to stop the server
echo ------------------------------------------------------------

python -m streamlit run dashboard\dashboard.py --server.address localhost --server.port 8501 --browser.gatherUsageStats false

echo.
echo 🛑 Dashboard stopped
pause