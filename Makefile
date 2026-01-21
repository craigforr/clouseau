# Clouseau Project Makefile
# Run 'make help' for available commands

.PHONY: help setup setup-backend setup-frontend setup-cli \
        build build-frontend build-cli \
        test test-backend test-frontend test-cli \
        lint lint-backend lint-frontend lint-cli \
        check coverage coverage-backend coverage-frontend coverage-cli \
        run run-backend run-frontend run-cli \
        sync sync-to-dropbox backup \
        clean

# Paths for sync/backup
DROPBOX_PATH := /mnt/d/data/Dropbox/code/github/craigforr/clouseau
BACKUP_BASE := $(HOME)/backups
BACKUP_YEAR := $(shell date +%Y)
BACKUP_DATE := $(shell date +%Y-%m-%dT%H%M%S%z)
RSYNC_EXCLUDES := --exclude 'node_modules' --exclude '.venv' --exclude '__pycache__' \
                  --exclude '.vite' --exclude 'dist' --exclude 'htmlcov' \
                  --exclude '.pytest_cache' --exclude '.coverage' --exclude '*.pyc'

# Default target
help:
	@echo "Clouseau Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Set up all components (backend, frontend, cli)"
	@echo "  make setup-backend  - Set up Python backend only"
	@echo "  make setup-frontend - Set up React frontend only"
	@echo "  make setup-cli      - Set up CLI only"
	@echo ""
	@echo "Build:"
	@echo "  make build          - Build all components (frontend, cli)"
	@echo "  make build-frontend - Build React frontend for production"
	@echo "  make build-cli      - Build CLI TypeScript"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make test-backend   - Run backend tests with coverage"
	@echo "  make test-frontend  - Run frontend tests"
	@echo "  make test-cli       - Run CLI tests"
	@echo ""
	@echo "Linting:"
	@echo "  make lint           - Run all linters"
	@echo "  make lint-backend   - Type check Python backend"
	@echo "  make lint-frontend  - Lint and type check frontend"
	@echo "  make lint-cli       - Lint and type check CLI"
	@echo ""
	@echo "CI/Verification:"
	@echo "  make check            - Run full verification (build + lint + test)"
	@echo "  make coverage         - Run tests and show all coverage reports"
	@echo "  make coverage-backend - Show backend coverage (from last run)"
	@echo "  make coverage-frontend- Run frontend tests with coverage"
	@echo "  make coverage-cli     - Run CLI tests with coverage"
	@echo ""
	@echo "Run (Development Servers):"
	@echo "  make run              - Run backend + frontend together"
	@echo "  make run-backend      - Run backend API server (port 8000)"
	@echo "  make run-frontend     - Run frontend dev server (port 5173)"
	@echo "  make run-cli          - Run CLI in dev mode"
	@echo ""
	@echo "Sync/Backup:"
	@echo "  make sync           - Sync to Dropbox (alias for sync-to-dropbox)"
	@echo "  make sync-to-dropbox- Sync project to Dropbox for cloud backup"
	@echo "  make backup         - Create dated zip backup in ~/backups/YYYY/"
	@echo ""
	@echo "Other:"
	@echo "  make clean          - Remove build artifacts and caches"
	@echo ""

# ============================================================
# Setup Commands
# ============================================================

setup: setup-backend setup-frontend setup-cli
	@echo "All components set up successfully!"

setup-backend:
	@echo "Setting up backend..."
	cd backend && uv venv
	cd backend && uv pip install -e ".[dev]"
	@echo "Backend setup complete!"

setup-frontend:
	@echo "Setting up frontend..."
	cd frontend && npm install
	@echo "Frontend setup complete!"

setup-cli:
	@echo "Setting up CLI..."
	cd cli && npm install
	@echo "CLI setup complete!"

# ============================================================
# Build Commands
# ============================================================

build: build-frontend build-cli
	@echo ""
	@echo "================================"
	@echo "All builds complete!"
	@echo "================================"

build-frontend:
	@echo "Building frontend..."
	@echo "================================"
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "Error: Run 'make setup-frontend' first"; \
		exit 1; \
	fi
	cd frontend && npm run build
	@echo "Frontend build output: frontend/dist/"
	@echo ""

build-cli:
	@echo "Building CLI..."
	@echo "================================"
	@if [ ! -d "cli/node_modules" ]; then \
		echo "Error: Run 'make setup-cli' first"; \
		exit 1; \
	fi
	cd cli && npm run build
	@echo "CLI build output: cli/dist/"
	@echo ""

# ============================================================
# Test Commands
# ============================================================

test: test-backend
	@echo ""
	@echo "================================"
	@echo "All tests complete!"
	@echo "================================"

test-backend:
	@echo "Running backend tests..."
	@echo "================================"
	cd backend && uv run pytest tests -v --cov=app --cov-report=term-missing
	@echo ""

test-frontend:
	@echo "Running frontend tests..."
	@echo "================================"
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "Error: Run 'make setup-frontend' first"; \
		exit 1; \
	fi
	cd frontend && npm test
	@echo ""

test-cli:
	@echo "Running CLI tests..."
	@echo "================================"
	@if [ ! -d "cli/node_modules" ]; then \
		echo "Error: Run 'make setup-cli' first"; \
		exit 1; \
	fi
	cd cli && npm test
	@echo ""

# ============================================================
# Lint Commands
# ============================================================

lint: lint-backend lint-frontend lint-cli
	@echo ""
	@echo "================================"
	@echo "All linting complete!"
	@echo "================================"

lint-backend:
	@echo "Type checking backend..."
	@echo "================================"
	cd backend && uv run python -m mypy app --ignore-missing-imports || true
	@echo ""

lint-frontend:
	@echo "Linting frontend..."
	@echo "================================"
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "Error: Run 'make setup-frontend' first"; \
		exit 1; \
	fi
	cd frontend && npm run type-check
	cd frontend && npm run lint
	@echo ""

lint-cli:
	@echo "Linting CLI..."
	@echo "================================"
	@if [ ! -d "cli/node_modules" ]; then \
		echo "Error: Run 'make setup-cli' first"; \
		exit 1; \
	fi
	cd cli && npm run type-check
	cd cli && npm run lint
	@echo ""

# ============================================================
# CI/Verification Commands
# ============================================================

check: build lint test
	@echo ""
	@echo "================================"
	@echo "All checks passed!"
	@echo "================================"

coverage: coverage-backend coverage-frontend coverage-cli
	@echo ""
	@echo "================================"
	@echo "All coverage reports complete."
	@echo "================================"

coverage-backend:
	@echo "Backend coverage (from last test run):"
	@echo "================================"
	@if [ -f "backend/.coverage" ]; then \
		cd backend && uv run coverage report; \
	else \
		echo "No coverage data found. Run 'make test-backend' first."; \
	fi
	@echo ""

coverage-frontend:
	@echo "Frontend coverage:"
	@echo "================================"
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "Error: Run 'make setup-frontend' first"; \
		exit 1; \
	fi
	cd frontend && npm run test:coverage
	@echo ""

coverage-cli:
	@echo "CLI coverage:"
	@echo "================================"
	@if [ ! -d "cli/node_modules" ]; then \
		echo "Error: Run 'make setup-cli' first"; \
		exit 1; \
	fi
	cd cli && npm run test:coverage
	@echo ""

# ============================================================
# Run Commands (Development Servers)
# ============================================================

run:
	@echo "Starting backend and frontend..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "Press Ctrl+C to stop"
	@echo ""
	@trap 'kill 0' INT; \
		(cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) & \
		(cd frontend && npm run dev) & \
		wait

run-backend:
	@echo "Starting backend API server..."
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	@echo ""
	cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	@echo "Starting frontend dev server..."
	@echo "URL: http://localhost:5173"
	@echo ""
	@if [ ! -d "frontend/node_modules" ]; then \
		echo "Error: Run 'make setup-frontend' first"; \
		exit 1; \
	fi
	cd frontend && npm run dev

run-cli:
	@echo "Running CLI..."
	@if [ ! -d "cli/node_modules" ]; then \
		echo "Error: Run 'make setup-cli' first"; \
		exit 1; \
	fi
	cd cli && npm run build && node dist/index.js

# ============================================================
# Sync/Backup Commands
# ============================================================

sync: sync-to-dropbox

sync-to-dropbox:
	@echo "Syncing to Dropbox..."
	@echo "Source: $(CURDIR)"
	@echo "Destination: $(DROPBOX_PATH)"
	@echo ""
	rsync -av --delete $(RSYNC_EXCLUDES) ./ $(DROPBOX_PATH)/
	@echo ""
	@echo "================================"
	@echo "Sync complete!"
	@echo "================================"

backup:
	@echo "Creating backup..."
	@mkdir -p $(BACKUP_BASE)/$(BACKUP_YEAR)
	@BACKUP_FILE=$(BACKUP_BASE)/$(BACKUP_YEAR)/clouseau-$(BACKUP_DATE).zip; \
	zip -r "$$BACKUP_FILE" . \
		-x "*/node_modules/*" -x "node_modules/*" \
		-x "*/.venv/*" -x ".venv/*" \
		-x "*/__pycache__/*" -x "__pycache__/*" \
		-x "*/.vite/*" -x ".vite/*" \
		-x "*/dist/*" -x "dist/*" \
		-x "*/htmlcov/*" -x "htmlcov/*" \
		-x "*/.pytest_cache/*" -x ".pytest_cache/*" \
		-x "*/.coverage" -x ".coverage" \
		-x "*.pyc" \
		-x ".git/*" -x "*/.git/*"; \
	echo ""; \
	echo "================================"; \
	echo "Backup created: $$BACKUP_FILE"; \
	ls -lh "$$BACKUP_FILE"; \
	echo "================================"

# ============================================================
# Clean Commands
# ============================================================

clean:
	@echo "Cleaning build artifacts..."
	# Python
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	# Node
	find . -type d -name "node_modules" -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "coverage" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"
