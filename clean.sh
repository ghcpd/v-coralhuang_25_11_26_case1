#!/usr/bin/env bash
set -euo pipefail

echo "Cleaning workspace"
rm -rf .venv
find . -type d -name "__pycache__" -print0 | xargs -0 rm -rf || true
find . -type d -name ".pytest_cache" -print0 | xargs -0 rm -rf || true
echo "Clean complete."
