#!/bin/bash
# Cross-platform run script for Linux/macOS
# Executes the optimized module and displays timing

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "[MARKER] Running optimized user display module..."
python user_display_optimized.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[MARKER] Execution completed successfully"
else
    echo "[ERROR] Execution failed with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
