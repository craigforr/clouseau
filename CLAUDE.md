# Claude Code Instructions for Clouseau

## Commit Rules

1. **Tests must pass before suggesting commits**: Never suggest a commit until all existing tests (backend, frontend, CLI) are passing.

2. **Interactive testing required**: Before suggesting a commit, provide the user with interactive test instructions for any new functionality:
   - **API changes**: Provide curl commands to test endpoints
   - **CLI changes**: Provide command-line examples to run
   - **Frontend changes**: Describe pages/tabs/UI elements to test manually
   - Wait for user confirmation that interactive testing is complete before proceeding with commit

## Development Workflow

1. **TDD approach**: Write tests before or alongside implementation code
2. **Coverage targets**:
   - Backend: 95% minimum
   - Frontend: 85% minimum
   - CLI: 95% minimum

## Project Structure

- **Backend**: FastAPI + SQLAlchemy (Python, managed with `uv`)
- **Frontend**: React + Vite + TailwindCSS (TypeScript)
- **CLI**: React Ink (TypeScript)

## Makefile Commands

- `make test` - Run all tests
- `make test-backend` - Run backend tests with coverage
- `make test-frontend` - Run frontend tests
- `make build` - Build frontend and CLI
- `make run-backend` - Start backend dev server (port 8000)
- `make run-frontend` - Start frontend dev server (port 5173)
- `make sync` - Sync to Dropbox
- `make backup` - Create dated backup

## File Locations

- WSL working directory: `~/wsl-code/github/craigforr/clouseau`
- Dropbox sync target: `/mnt/d/data/Dropbox/code/github/craigforr/clouseau`
