# Clouseau Backend

FastAPI backend for the Clouseau LLM interaction inspector.

## Setup

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install -e ".[dev]"

# Run development server
uv run uvicorn app.main:app --reload
```

## Testing

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=term
```
