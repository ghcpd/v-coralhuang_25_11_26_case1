#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
if [ -d "$VENV_DIR" ]; then
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
fi

pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-fail-under=85
