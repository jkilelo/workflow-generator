@echo off
REM 🚀 Workflow Generator Demo Launcher for Windows
REM Autonomous FastAPI + React workflow generation system

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_DIR=%~dp0
set VENV_DIR=%PROJECT_DIR%venv
set BACKEND_PORT=8003
set LOG_DIR=%PROJECT_DIR%logs

REM Create logs directory
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo.
echo ================================= 
echo   🚀 WORKFLOW GENERATOR DEMO    
echo =================================
echo.

REM Function to check if Python is installed
:check_python
echo [STEP] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)
echo [SUCCESS] Python detected

REM Function to setup virtual environment
:setup_venv
echo [STEP] Setting up Python virtual environment...
cd /d "%PROJECT_DIR%"

if not exist "%VENV_DIR%" (
    echo [STEP] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

REM Install requirements
echo [STEP] Installing Python dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt >nul 2>&1
) else (
    echo [WARNING] requirements.txt not found, installing core dependencies...
    pip install fastapi uvicorn pydantic jinja2 requests aiofiles python-multipart >nul 2>&1
)
echo [SUCCESS] Virtual environment ready

REM Function to run autonomous setup if needed
:run_setup
echo [STEP] Checking system setup...
if not exist "apps" goto need_setup
if not exist "backend" goto need_setup
if not exist "frontend" goto need_setup
goto setup_done

:need_setup
echo [STEP] Running autonomous setup (first-time setup)...
python auto_setup.py
echo [SUCCESS] Auto-setup completed

:setup_done
echo [SUCCESS] System already configured

REM Function to start FastAPI backend
:start_backend
echo [STEP] Starting FastAPI backend server...

REM Kill any existing processes on our port
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%BACKEND_PORT%') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Start the server
echo [STEP] Launching live server on port %BACKEND_PORT%...
start /b python live_server.py > "%LOG_DIR%\backend.log" 2>&1

REM Wait for server to start
echo [STEP] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul
echo [SUCCESS] Backend server is running

REM Function to open browser
:open_browser
echo [STEP] Opening demo in browser...
timeout /t 2 /nobreak >nul
start http://localhost:%BACKEND_PORT%
echo [SUCCESS] Demo interface should open in your browser

REM Show status
:show_status
echo.
echo =================================
echo [SUCCESS] 🎉 Workflow Generator Demo is now running!
echo.
echo 📊 Service Status:
echo   🔹 Backend Server: http://localhost:%BACKEND_PORT%
echo   🔹 Interactive UI: http://localhost:%BACKEND_PORT%
echo   🔹 API Health: http://localhost:%BACKEND_PORT%/api/health
echo.
echo 🎯 What to try:
echo   🔹 Click any workflow card to execute it
echo   🔹 Fill out dynamic forms and watch real-time execution
echo   🔹 View step-by-step progress tracking
echo   🔹 Test responsive design on different screen sizes
echo.
echo 📝 Logs:
echo   🔹 Backend: %LOG_DIR%\backend.log
echo.
echo 🛑 To stop the demo:
echo   🔹 Press Ctrl+C or close this window
echo.
echo =================================
echo.

REM Main execution
if "%1"=="--stop" goto stop_services
if "%1"=="--help" goto show_help
if "%1"=="-h" goto show_help

REM Default: start the demo
goto check_python

:stop_services
echo [STEP] Stopping all demo services...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%BACKEND_PORT%') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo [SUCCESS] All services stopped
exit /b 0

:show_help
echo 🚀 Workflow Generator Demo Launcher for Windows
echo.
echo Usage: %0 [OPTION]
echo.
echo Options:
echo   --start     Start the demo (default)
echo   --stop      Stop all demo services  
echo   --help      Show this help message
echo.
echo Examples:
echo   %0                  # Start the demo
echo   %0 --stop           # Stop all services
echo.
exit /b 0

REM Keep the window open
echo Press any key to stop the demo...
pause >nul

REM Cleanup on exit
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%BACKEND_PORT%') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo Demo stopped.