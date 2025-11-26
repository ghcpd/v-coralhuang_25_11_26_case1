#!/usr/bin/env bash
set -euo pipefail

# Idempotent setup: create a virtual environment and install pinned dependencies
VENV_DIR=".venv"
PYTHON=${PYTHON:-python3}

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR"
    "$PYTHON" -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists: $VENV_DIR"
fi

echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

echo "Setup complete. Activate with: source $VENV_DIR/bin/activate" 
