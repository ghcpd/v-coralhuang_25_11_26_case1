#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

if [ -d "$ROOT_DIR/.venv" ]; then
  rm -rf "$ROOT_DIR/.venv"
  echo "Removed virtualenv"
fi

# Remove python cache
find "$ROOT_DIR" -type d -name "__pycache__" -exec rm -rf {} + || true
find "$ROOT_DIR" -type d -name ".pytest_cache" -exec rm -rf {} + || true

echo "Clean completed."