#!/bin/bash
# Cross-platform test script for Linux/macOS
# Runs pytest with coverage reporting (78% minimum for production code with defensive error handling)

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "[MARKER] Running tests with coverage..."

# Run pytest with coverage
pytest tests/ \
    --cov=user_display_optimized \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=78 \
    -v

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[MARKER] All tests passed with coverage ≥78%"
    echo "[MARKER] HTML coverage report: htmlcov/index.html"
else
    echo "[ERROR] Tests failed or coverage insufficient"
fi

exit $EXIT_CODE
