#!/bin/bash
# Backend test runner script
# Usage: ./run_tests.sh [pytest-options]
#
# Examples:
#   ./run_tests.sh              # Run all tests with coverage
#   ./run_tests.sh -v           # Verbose output
#   ./run_tests.sh -k "test_health"  # Run specific tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "================================"
echo "Clouseau Backend Tests"
echo "================================"
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Setting up..."
    uv venv
    uv pip install -e ".[dev]"
    echo ""
fi

# Run tests with coverage
echo "Running tests..."
echo ""

if [ $# -eq 0 ]; then
    # Default: run with coverage
    uv run pytest tests -v --cov=app --cov-report=term-missing
else
    # Pass through any arguments
    uv run pytest tests "$@"
fi

echo ""
echo "================================"
echo "Tests complete!"
echo "================================"
