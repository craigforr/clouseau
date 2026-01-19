# Clouseau

An inspector for LLM interactions written in Python, TypeScript, and React.

## Overview

Clouseau is a comprehensive observability tool for tracking, analyzing, and managing conversations with Large Language Models. It provides:

- Session and conversation management
- Real-time context window tracking
- Multi-provider LLM support
- Full-text search across conversations
- Web UI and CLI interfaces

## Prerequisites

- Python 3.10+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- make (for using Makefile commands)

## Quick Start

### Setup

```bash
# Clone the repository
git clone https://github.com/craigforr/clouseau.git
cd clouseau

# Set up all components (recommended)
make setup

# Or set up individually:
make setup-backend   # Python backend only
make setup-frontend  # React frontend only
make setup-cli       # CLI only
```

### Running

```bash
# Start the backend server
cd backend
uv run uvicorn app.main:app --reload

# Start the web frontend (in another terminal)
cd frontend
npm run dev

# Or use the CLI
cd cli
npm run build
clou chat
```

## Testing

### Using Make (Recommended)

```bash
# Run all tests
make test

# Run backend tests only
make test-backend
```

### Using Test Scripts

```bash
# Backend tests
cd backend
./run_tests.sh

# With pytest options
./run_tests.sh -v                    # Verbose
./run_tests.sh -k "test_health"      # Filter by name
./run_tests.sh --cov-report=html     # HTML coverage report
```

### Manual Commands

```bash
# Backend (from backend/ directory)
uv run pytest tests -v --cov=app --cov-report=term-missing

# Frontend (from frontend/ directory, after npm install)
npm test

# CLI (from cli/ directory, after npm install)
npm test
```

## Project Structure

```
clouseau/
├── backend/          # Python FastAPI backend
│   ├── app/          # Application code
│   ├── tests/        # Test suite
│   └── run_tests.sh  # Test runner
├── frontend/         # React web interface
├── cli/              # React Ink CLI
├── docs/             # Documentation
├── scripts/          # Setup scripts
└── Makefile          # Development commands
```

## Documentation

- [API Documentation](docs/API.md)
- [Search Syntax](docs/SEARCH_SYNTAX.md)
- [Configuration Guide](docs/CONFIGURATION.md)

## Building

### Using Make

```bash
# Build all components
make build

# Build individual components
make build-frontend  # Build React frontend (output: frontend/dist/)
make build-cli       # Build CLI TypeScript (output: cli/dist/)
```

### Manual Build Commands

```bash
# Frontend (from frontend/ directory)
npm run build

# CLI (from cli/ directory)
npm run build
```

**Note:** The Python backend does not require a build step.

## Development

See [DEVELOPER.md](DEVELOPER.md) for development guidelines.

### Available Make Commands

```bash
make help            # Show all available commands
```

**Setup:**
```bash
make setup           # Set up all components
make setup-backend   # Set up Python backend only
make setup-frontend  # Set up React frontend only
make setup-cli       # Set up CLI only
```

**Build:**
```bash
make build           # Build all components
make build-frontend  # Build React frontend for production
make build-cli       # Build CLI TypeScript
```

**Test:**
```bash
make test            # Run all tests
make test-backend    # Run backend tests with coverage
make test-frontend   # Run frontend tests
make test-cli        # Run CLI tests
```

**Lint:**
```bash
make lint            # Run all linters
make lint-backend    # Type check Python backend
make lint-frontend   # Lint and type check frontend
make lint-cli        # Lint and type check CLI
```

**CI/Verification:**
```bash
make check           # Run full verification (build + lint + test)
make coverage        # Show coverage report from last test run
```

**Other:**
```bash
make clean           # Remove build artifacts and caches
```

## Coverage Targets

| Component | Target |
|-----------|--------|
| Backend   | 95%    |
| API Routes| 100%   |
| Frontend  | 85%    |
| CLI       | 95%    |

## License

MIT License - see [LICENSE](LICENSE) for details.
