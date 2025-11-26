#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

rm -rf "$ROOT_DIR/.venv" "$ROOT_DIR/.pytest_cache" "$ROOT_DIR/htmlcov" "$ROOT_DIR/.coverage"
find "$ROOT_DIR" -name "__pycache__" -type d -prune -exec rm -rf {} +
find "$ROOT_DIR" -name "*.pyc" -delete

echo "[clean] Environment reset."
