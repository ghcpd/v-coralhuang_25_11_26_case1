#!/bin/bash
# Clean script for Unix-based systems (Linux/macOS)
# Removes virtual environment and build artifacts

echo "=========================================="
echo "Cleaning User Display Optimizer"
echo "=========================================="

# Remove virtual environment
if [ -d "venv" ]; then
    echo "Removing virtual environment..."
    rm -rf venv
    echo "Virtual environment removed."
else
    echo "No virtual environment found."
fi

# Remove Python cache
if [ -d "__pycache__" ]; then
    echo "Removing __pycache__..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
fi

if [ -d ".pytest_cache" ]; then
    echo "Removing .pytest_cache..."
    rm -rf .pytest_cache
fi

# Remove coverage files
if [ -d "htmlcov" ]; then
    echo "Removing coverage reports..."
    rm -rf htmlcov
fi

if [ -f ".coverage" ]; then
    rm -f .coverage
fi

# Remove .pyc files
echo "Removing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo ""
echo "=========================================="
echo "Cleanup complete!"
echo "=========================================="
echo "To set up again, run: bash setup.sh"
echo "=========================================="

exit 0
