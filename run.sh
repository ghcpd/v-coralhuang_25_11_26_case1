#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
if [ -x "$VENV_DIR/bin/python" ]; then
    PY="$VENV_DIR/bin/python"
else
    PY=python3
fi

echo "Running user_display_optimized demo"
"$PY" -m user_display_optimized
