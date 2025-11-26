#!/usr/bin/env bash
set -euo pipefail

PY=python
if command -v python3 >/dev/null 2>&1; then
    PY=python3
fi

VENV_DIR=".venv"
echo "Setting up virtual environment in $VENV_DIR"
if [ ! -d "$VENV_DIR" ]; then
    $PY -m venv "$VENV_DIR"
fi

echo "Installing dependencies"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
echo "Setup complete. To activate: source $VENV_DIR/bin/activate"
