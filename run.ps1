# Run script for Windows PowerShell
# Executes the optimized user display module

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Running User Display Optimizer" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "ERROR: Virtual environment not found." -ForegroundColor Red
    Write-Host "Please run: powershell -File setup.ps1" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run the optimized module
Write-Host "Executing user_display_optimized.py..." -ForegroundColor Yellow
Write-Host ""
& python user_display_optimized.py

exit 0
