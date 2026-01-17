#!/usr/bin/env bash
# File: scripts/setup_dev.sh
# Clouseau Developer Setup for Linux/macOS

set -e

echo "🕵️  Clouseau Developer Setup"
echo "=============================="
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
    echo "✗ Python 3 not found"
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
        exit 1
    fi
else
    echo "✗ Node.js not found"
    echo "  Install from: https://nodejs.org/"
    exit 1
fi

# Install uv if not present
echo "Checking for uv..."
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✓ uv found"
fi

# Backend setup
echo ""
echo "Setting up Backend..."
cd backend

echo "Creating Python virtual environment with uv..."
uv venv
source .venv/bin/activate

echo "Installing backend dependencies..."
uv pip install -e ".[dev]"

echo "Initializing database..."
alembic upgrade head

cd ..

# Frontend setup
echo ""
echo "Setting up Frontend..."
cd frontend

echo "Installing frontend dependencies..."
npm install

cd ..

# CLI setup
echo ""
echo "Setting up CLI..."
cd cli

echo "Installing CLI dependencies..."
npm install

echo "Building CLI..."
npm run build

cd ..

# Create config files from examples
echo ""
echo "Creating configuration files..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env (please add your API keys)"
fi

if [ ! -f config.yaml ]; then
    cp config.example.yaml config.yaml
    echo "✓ Created config.yaml"
fi

if [ ! -f settings.yaml ]; then
    cp settings.example.yaml settings.yaml
    echo "✓ Created settings.yaml"
fi

# Set up pre-commit hooks
echo ""
echo "Setting up pre-commit hooks..."
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Backend checks
cd backend
source .venv/bin/activate
echo "  - Running black..."
black --check app/
echo "  - Running ruff..."
ruff check app/
echo "  - Running mypy..."
mypy app/
cd ..

# Frontend checks
cd frontend
echo "  - Running prettier..."
npm run format -- --check
echo "  - Running eslint..."
npm run lint
cd ..

# CLI checks
cd cli
echo "  - Running prettier..."
npm run format -- --check
echo "  - Running eslint..."
npm run lint
cd ..

echo "✓ All pre-commit checks passed!"
EOF

chmod +x .git/hooks/pre-commit
echo "✓ Pre-commit hooks installed"

# Run initial tests
echo ""
echo "Running initial test suite..."

# Backend tests
echo "  Backend tests..."
cd backend
source .venv/bin/activate
pytest
cd ..

# Frontend tests
echo "  Frontend tests..."
cd frontend
npm test -- --passWithNoTests
cd ..

# CLI tests
echo "  CLI tests..."
cd cli
npm test -- --passWithNoTests
cd ..

# Generate coverage report
echo ""
echo "Generating coverage report..."
cd backend
source .venv/bin/activate
pytest --cov=app --cov-report=html
echo "✓ Coverage report: backend/htmlcov/index.html"
cd ..

echo ""
echo "=============================="
echo "✓ Developer setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add your API keys to .env"
echo "  2. Review config.yaml for LLM providers"
echo "  3. Run 'cd backend && source .venv/bin/activate && uvicorn app.main:app --reload'"
echo "  4. In another terminal: 'cd frontend && npm run dev'"
echo "  5. Or use CLI: 'cd cli && npm run dev'"
echo ""
echo "Developer tools:"
echo "  - Backend tests: cd backend && pytest"
echo "  - Frontend tests: cd frontend && npm test"
echo "  - CLI tests: cd cli && npm test"
echo "  - Code formatting: Run pre-commit hook or format manually"
echo ""
