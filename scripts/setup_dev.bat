@echo off
echo Clouseau Developer Setup (Windows)
echo ===================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.10+
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js not found. Please install Node.js 18+
    exit /b 1
)

REM Install uv
uv --version >nul 2>&1
if errorlevel 1 (
    echo Installing uv...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
)

REM Backend setup
cd backend
call uv venv
call .venv\Scripts\activate
call uv pip install -e .[dev]
call alembic upgrade head
cd ..

REM Frontend setup
cd frontend
call npm install
cd ..

REM CLI setup
cd cli
call npm install
call npm run build
cd ..

REM Create configs
if not exist .env copy .env.example .env
if not exist config.yaml copy config.example.yaml config.yaml
if not exist settings.yaml copy settings.example.yaml settings.yaml

echo.
echo Setup complete!
echo Add your API keys to .env
echo.

