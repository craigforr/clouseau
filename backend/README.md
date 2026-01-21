# Clouseau Backend

FastAPI backend for the Clouseau LLM interaction inspector.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"
```

## Running the Server

```bash
# From the backend directory
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Testing

### Quick Start

```bash
# From the backend directory
./run_tests.sh
```

### Manual Commands

```bash
# Run all tests with coverage
uv run pytest tests -v --cov=app --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_models.py -v

# Run tests matching a pattern
uv run pytest tests -k "test_health" -v

# Run with HTML coverage report
uv run pytest tests --cov=app --cov-report=html
# Then open htmlcov/index.html
```

## Project Structure

```
backend/
├── app/
│   ├── api/routes/     # API endpoint handlers
│   ├── models/         # SQLAlchemy database models
│   ├── services/       # Business logic
│   ├── db/             # Database configuration
│   └── schemas/        # Pydantic validation schemas
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   └── api/            # API tests
├── alembic/            # Database migrations
├── pyproject.toml      # Python project config
└── run_tests.sh        # Test runner script
```

## Coverage Requirements

- Overall backend: 95%
- API routes: 100%
- Models: 100%
