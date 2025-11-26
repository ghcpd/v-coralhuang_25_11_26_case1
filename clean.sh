#!/usr/bin/env bash
set -euo pipefail

echo "Cleaning environment"
rm -rf .venv .pytest_cache .coverage htmlcov
echo "Clean complete"
