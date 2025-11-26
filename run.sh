#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENVDIR="$ROOT_DIR/.venv"

if [ ! -d "$VENVDIR" ]; then
  echo "Virtual environment not found. Run setup.sh first." >&2
  exit 1
fi
# shellcheck source=/dev/null
source "$VENVDIR/bin/activate"
python "$ROOT_DIR/user_display_optimized.py" "$@"
