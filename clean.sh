#!/bin/bash
# Cross-platform clean script for Linux/macOS
# Removes virtual environment and generated files

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "[MARKER] Cleaning up environment..."

# Remove virtual environment
if [ -d "venv" ]; then
    echo "[MARKER] Removing virtual environment..."
    rm -rf venv
fi

# Remove pytest cache and coverage
if [ -d ".pytest_cache" ]; then
    echo "[MARKER] Removing pytest cache..."
    rm -rf .pytest_cache
fi

if [ -d "htmlcov" ]; then
    echo "[MARKER] Removing HTML coverage report..."
    rm -rf htmlcov
fi

if [ -f ".coverage" ]; then
    echo "[MARKER] Removing coverage data..."
    rm -f .coverage
fi

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "[MARKER] Cleanup complete!"
