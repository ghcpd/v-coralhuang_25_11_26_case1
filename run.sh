#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
if [ -d "$VENV_DIR" ]; then
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
fi

echo "Running optimized display (sanity)"
python run_module.py
