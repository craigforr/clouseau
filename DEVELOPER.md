# Developer Guide

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- uv (install with `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Initial Setup

```bash
# Clone and setup
git clone https://github.com/craigforr/clouseau.git
cd clouseau
./scripts/setup_dev.sh
```

## Project Architecture

### Backend (Python/FastAPI)

```
backend/
├── app/
│   ├── api/routes/      # API endpoints
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Business logic
│   ├── db/              # Database config
│   └── schemas/         # Pydantic schemas
├── tests/
└── alembic/             # Database migrations
```

### Frontend (React/TypeScript)

```
frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/           # Page components
│   ├── hooks/           # Custom hooks
│   ├── services/        # API services
│   └── types/           # TypeScript types
└── tests/
```

### CLI (React Ink)

```
cli/
├── src/
│   ├── commands/        # CLI commands
│   ├── components/      # TUI components
│   ├── hooks/           # Custom hooks
│   └── utils/           # Utilities
└── tests/
```

## Development Workflow

### Git Workflow

1. Create feature branch: `git checkout -b feature/issue-number-description`
2. Make changes following TDD
3. Commit with conventional commits: `feat(scope): #issue - description`
4. Push and create PR

### Commit Convention

```
type(scope): #issue - description

Types: feat, fix, docs, style, refactor, test, chore
Scopes: backend, frontend, cli, docs
```

### Commit Message Template

Include coverage stats in commit messages for traceability:

```
type(scope): #issue - description

[Brief explanation of what changed and why]

Coverage:
- Backend: XX% (target: 95%)
- Frontend: XX% (target: 85%)
- CLI: XX% (target: 95%)

Verified: make check passed
```

Get coverage stats with `make coverage` before committing.

### Test-Driven Development

1. Write failing tests first
2. Implement feature
3. Verify tests pass
4. Check coverage targets

## Coverage Targets

| Layer    | Target |
|----------|--------|
| API      | 100%   |
| Backend  | 95%    |
| CLI      | 95%    |
| Frontend | 85%    |

## Building

### Using Make (Recommended)

```bash
make build           # Build all components
make build-frontend  # Build React frontend for production
make build-cli       # Build CLI TypeScript
```

### Build Outputs

| Component | Build Command     | Output Directory |
|-----------|-------------------|------------------|
| Frontend  | `npm run build`   | `frontend/dist/` |
| CLI       | `npm run build`   | `cli/dist/`      |
| Backend   | N/A (Python)      | N/A              |

## Running Tests

### Using Make (Recommended)

```bash
make test            # Run all tests
make test-backend    # Run backend tests with coverage
make test-frontend   # Run frontend tests
make test-cli        # Run CLI tests
```

### Manual Commands

```bash
# Backend
cd backend
uv run pytest tests -v --cov=app --cov-report=term-missing

# Frontend
cd frontend
npm test

# CLI
cd cli
npm test
```

## Linting and Type Checking

```bash
make lint            # Run all linters
make lint-backend    # Type check Python backend (mypy)
make lint-frontend   # Lint and type check frontend
make lint-cli        # Lint and type check CLI
```
