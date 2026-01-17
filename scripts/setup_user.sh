#!/usr/bin/env bash
# File: scripts/setup_user.sh
# Clouseau User Setup for Linux/macOS

set -e

echo ""
echo "========================================="
echo "  🕵️  Clouseau User Setup"
echo "========================================="
echo ""

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✓ OS: $OSTYPE detected"
else
    echo "⚠️  Warning: This script is designed for Linux/macOS"
fi

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✓ Python $PY_VERSION found"
    
    # Check if version is >= 3.10
    PY_MAJOR=$(echo $PY_VERSION | cut -d'.' -f1)
    PY_MINOR=$(echo $PY_VERSION | cut -d'.' -f2)
    if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
        echo "✗ Python 3.10+ required, found $PY_VERSION"
        exit 1
    fi
else
    echo "✗ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# Check Node.js version
echo "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2)
    echo "✓ Node.js $NODE_VERSION found"
    
    # Check if version is >= 18
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
    if [ "$NODE_MAJOR" -lt 18 ]; then
        echo "✗ Node.js 18+ required, found $NODE_VERSION"
        echo "  Install from: https://nodejs.org/"
        exit 1
    fi
else
    echo "✗ Node.js not found"
    echo "  Install from: https://nodejs.org/"
    exit 1
fi

# Install uv if not present
echo ""
echo "Checking for uv..."
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "✓ uv installed"
else
    echo "✓ uv found"
fi

# Backend setup
echo ""
echo "========================================="
echo "  Setting up Backend..."
echo "========================================="
cd backend

echo "Creating Python virtual environment..."
uv venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing backend dependencies..."
uv pip install -e .

echo "Initializing database..."
alembic upgrade head || echo "⚠️  Database initialization skipped (tables may not exist yet)"

deactivate
cd ..
echo "✓ Backend setup complete"

# Frontend setup
echo ""
echo "========================================="
echo "  Setting up Frontend..."
echo "========================================="
cd frontend

echo "Installing frontend dependencies..."
npm install

echo "Building frontend..."
npm run build

cd ..
echo "✓ Frontend setup complete"

# CLI setup
echo ""
echo "========================================="
echo "  Setting up CLI..."
echo "========================================="
cd cli

echo "Installing CLI dependencies..."
npm install

echo "Building CLI..."
npm run build

cd ..
echo "✓ CLI setup complete"

# Create config files from examples
echo ""
echo "========================================="
echo "  Creating configuration files..."
echo "========================================="

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env"
    echo "⚠️  ACTION REQUIRED: Please edit .env and add your API keys"
else
    echo "⊘ .env already exists (skipped)"
fi

if [ ! -f config.yaml ]; then
    cp config.example.yaml config.yaml
    echo "✓ Created config.yaml"
else
    echo "⊘ config.yaml already exists (skipped)"
fi

if [ ! -f settings.yaml ]; then
    cp settings.example.yaml settings.yaml
    echo "✓ Created settings.yaml"
else
    echo "⊘ settings.yaml already exists (skipped)"
fi

# Create data directory
mkdir -p ~/.clouseau/data
echo "✓ Created data directory at ~/.clouseau/data"

echo ""
echo "========================================="
echo "  ✓ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API keys for LLM providers"
echo "  2. Review config.yaml for LLM provider configuration"
echo "  3. Review settings.yaml for application settings"
echo ""
echo "To start Clouseau:"
echo "  - Web Interface:"
echo "      cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo "    Then in another terminal:"
echo "      cd frontend && npm run dev"
echo ""
echo "  - CLI Interface:"
echo "      cd cli && npm start"
echo "    Or use the built executable:"
echo "      ./cli/dist/clou"
echo ""
echo "For help:"
echo "  - README.md for user documentation"
echo "  - DEVELOPER.md for development guide"
echo ""
# EOF
