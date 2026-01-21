# Claude Code Instructions for Clouseau

## Key Documentation

**Always reference these files for project context:**

| Document | Purpose |
|----------|---------|
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Test coverage targets, code standards, API conventions |
| [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md) | Overall project specification and architecture |
| [docs/API.md](docs/API.md) | API endpoint documentation |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | Configuration options |

## Test Coverage Requirements

| Tier | Target | Enforcement |
|------|--------|-------------|
| Backend API | 100% | `backend/pyproject.toml` |
| Backend Services | 95% | `backend/pyproject.toml` |
| Frontend | 85% | `frontend/vite.config.ts` |
| CLI | 95% | `cli/vitest.config.ts` |

## Commit Rules

1. **Tests must pass before suggesting commits**: Never suggest a commit until all existing tests (backend, frontend, CLI) are passing.

2. **Interactive testing required**: Before suggesting a commit, provide the user with interactive test instructions for any new functionality:
   - **API changes**: Provide curl commands to test endpoints
   - **CLI changes**: Provide command-line examples to run
   - **Frontend changes**: Describe pages/tabs/UI elements to test manually
   - Wait for user confirmation that interactive testing is complete before proceeding with commit

## Development Workflow

1. **TDD approach**: Write tests before or alongside implementation code
2. **Check coverage**: Run `npm run test:coverage` (frontend) or `uv run pytest --cov` (backend)
3. **Type checking**: Run `npm run type-check` (frontend) or `uv run mypy` (backend)

## Project Structure

```
clouseau/
├── backend/          # Python FastAPI + SQLAlchemy (managed with uv)
├── frontend/         # React + Vite + TailwindCSS (TypeScript)
├── cli/              # React Ink (TypeScript) - not yet implemented
├── docs/             # Documentation
│   ├── REQUIREMENTS.md   # Project requirements and standards
│   ├── API.md            # API documentation
│   └── CONFIGURATION.md  # Configuration guide
└── scripts/          # Utility scripts
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make test-backend` | Run backend tests with coverage |
| `make test-frontend` | Run frontend tests |
| `make build` | Build frontend and CLI |
| `make run-backend` | Start backend dev server (port 8000) |
| `make run-frontend` | Start frontend dev server (port 5173) |
| `make sync` | Sync to Dropbox |
| `make backup` | Create dated backup |

## File Locations

- **WSL working directory**: `~/wsl-code/github/craigforr/clouseau`
- **Dropbox sync target**: `/mnt/d/data/Dropbox/code/github/craigforr/clouseau`

## Tech Stack Quick Reference

| Layer | Technology | Package Manager |
|-------|------------|-----------------|
| Backend | Python 3.10+, FastAPI, SQLAlchemy | uv |
| Frontend | TypeScript, React 18, Tailwind CSS | npm |
| CLI | TypeScript, React Ink | npm |
| Database | SQLite with FTS5 | - |
