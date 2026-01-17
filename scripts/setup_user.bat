@echo off
REM File: scripts/setup_user.bat
REM Clouseau User Setup for Windows

echo.
echo ========================================
echo   Clouseau User Setup (Windows)
echo ========================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PY_VERSION=%%i
echo [OK] Python %PY_VERSION% found

REM Check if Python version is >= 3.10
for /f "tokens=1,2 delims=." %%a in ("%PY_VERSION%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)

if %PY_MAJOR% LSS 3 (
    echo [ERROR] Python 3.10+ required, found %PY_VERSION%
    pause
    exit /b 1
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% LSS 10 (
    echo [ERROR] Python 3.10+ required, found %PY_VERSION%
    pause
    exit /b 1
)

REM Check Node.js version
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 18 or higher.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

REM Get Node version
for /f "tokens=1 delims=v" %%i in ('node --version 2^>^&1') do set NODE_VERSION=%%i
echo [OK] Node.js v%NODE_VERSION% found

REM Check if Node version is >= 18
for /f "tokens=1 delims=." %%a in ("%NODE_VERSION%") do set NODE_MAJOR=%%a
if %NODE_MAJOR% LSS 18 (
    echo [ERROR] Node.js 18+ required, found v%NODE_VERSION%
    pause
    exit /b 1
)

REM Install uv if not present
echo.
echo Checking for uv package manager...
uv --version >nul 2>&1
if errorlevel 1 (
    echo Installing uv...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    if errorlevel 1 (
        echo [ERROR] Failed to install uv
        pause
        exit /b 1
    )
    REM Refresh environment
    call refreshenv >nul 2>&1
    echo [OK] uv installed
) else (
    echo [OK] uv found
)

REM Backend setup
echo.
echo ========================================
echo   Setting up Backend...
echo ========================================
cd backend

echo Creating Python virtual environment...
call uv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    cd ..
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing backend dependencies...
call uv pip install -e .
if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies
    cd ..
    pause
    exit /b 1
)

echo Initializing database...
call alembic upgrade head
if errorlevel 1 (
    echo [WARNING] Database initialization failed (this is OK if tables don't exist yet)
)

call deactivate
cd ..
echo [OK] Backend setup complete

REM Frontend setup
echo.
echo ========================================
echo   Setting up Frontend...
echo ========================================
cd frontend

echo Installing frontend dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
)

echo Building frontend...
call npm run build
if errorlevel 1 (
    echo [ERROR] Failed to build frontend
    cd ..
    pause
    exit /b 1
)

cd ..
echo [OK] Frontend setup complete

REM CLI setup
echo.
echo ========================================
echo   Setting up CLI...
echo ========================================
cd cli

echo Installing CLI dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install CLI dependencies
    cd ..
    pause
    exit /b 1
)

echo Building CLI...
call npm run build
if errorlevel 1 (
    echo [ERROR] Failed to build CLI
    cd ..
    pause
    exit /b 1
)

cd ..
echo [OK] CLI setup complete

REM Create configuration files from examples
echo.
echo ========================================
echo   Creating configuration files...
echo ========================================

if not exist .env (
    copy .env.example .env >nul
    echo [OK] Created .env
    echo [ACTION REQUIRED] Please edit .env and add your API keys
) else (
    echo [SKIP] .env already exists
)

if not exist config.yaml (
    copy config.example.yaml config.yaml >nul
    echo [OK] Created config.yaml
) else (
    echo [SKIP] config.yaml already exists
)

if not exist settings.yaml (
    copy settings.example.yaml settings.yaml >nul
    echo [OK] Created settings.yaml
) else (
    echo [SKIP] settings.yaml already exists
)

REM Create data directory
if not exist "%USERPROFILE%\.clouseau\data" (
    mkdir "%USERPROFILE%\.clouseau\data"
    echo [OK] Created data directory at %USERPROFILE%\.clouseau\data
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env and add your API keys for LLM providers
echo   2. Review config.yaml for LLM provider configuration
echo   3. Review settings.yaml for application settings
echo.
echo To start Clouseau:
echo   - Web Interface:
echo       cd backend
echo       .venv\Scripts\activate
echo       uvicorn app.main:app --reload
echo     Then in another terminal:
echo       cd frontend
echo       npm run dev
echo.
echo   - CLI Interface:
echo       cd cli
echo       npm start
echo     Or use the built executable:
echo       .\cli\dist\clou.exe
echo.
echo For help:
echo   - README.md for user documentation
echo   - DEVELOPER.md for development guide
echo.
pause
