#!/bin/bash
# Run script for Unix-based systems (Linux/macOS)
# Executes the optimized user display module

set -e  # Exit on error

echo "=========================================="
echo "Running User Display Optimizer"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found."
    echo "Please run: bash setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the optimized module
echo "Executing user_display_optimized.py..."
echo ""
python user_display_optimized.py

exit 0
