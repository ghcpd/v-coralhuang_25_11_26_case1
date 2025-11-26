#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENVDIR="$ROOT_DIR/.venv"
REQS="$ROOT_DIR/requirements.txt"

find_python() {
  for candidate in "${PYTHON:-}" python3 python; do
    if [ -n "$candidate" ] && command -v "$candidate" >/dev/null 2>&1; then
      echo "$candidate"; return 0;
    fi
  done
  echo "ERROR: Python 3.10+ not found" >&2; return 1
}

PYTHON_BIN=$(find_python)

if [ ! -d "$VENVDIR" ]; then
  "$PYTHON_BIN" -m venv "$VENVDIR"
fi

# shellcheck source=/dev/null
source "$VENVDIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "$REQS"

echo "[setup] Virtual environment ready at $VENVDIR"
