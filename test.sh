#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
if [ -x "$VENV_DIR/bin/python" ]; then
    PY="$VENV_DIR/bin/python"
else
    PY=python3
fi

echo "Running tests with coverage"
"$PY" -m pytest -q --maxfail=1 --disable-warnings --cov=user_display_optimized --cov-report=term-missing
