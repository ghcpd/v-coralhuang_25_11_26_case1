#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
VENV_DIR="$ROOT_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
  # shellcheck disable=SC1091
  source "$VENV_DIR/bin/activate"
fi

pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-report=term --cov-fail-under=85
