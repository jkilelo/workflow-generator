@echo off
REM 🚀 Workflow Generator Installation Script for Windows

echo.
echo =================================================
echo   🚀 WORKFLOW GENERATOR INSTALLATION
echo =================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo [SUCCESS] Python detected

REM Run autonomous setup
echo [STEP] Running autonomous setup...
python auto_setup.py

echo [SUCCESS] 🎉 Installation complete!
echo.
echo Next steps:
echo   1. Run the demo: run_demo.bat
echo   2. Access UI at: http://localhost:8003
echo.
pause
