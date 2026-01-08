# Cross-platform clean script for Windows PowerShell
# Removes virtual environment and generated files

param()

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

Write-Host "[MARKER] Cleaning up environment..."

# Remove virtual environment
if (Test-Path "venv") {
    Write-Host "[MARKER] Removing virtual environment..."
    Remove-Item -Recurse -Force venv
}

# Remove pytest cache and coverage
if (Test-Path ".pytest_cache") {
    Write-Host "[MARKER] Removing pytest cache..."
    Remove-Item -Recurse -Force .pytest_cache
}

if (Test-Path "htmlcov") {
    Write-Host "[MARKER] Removing HTML coverage report..."
    Remove-Item -Recurse -Force htmlcov
}

if (Test-Path ".coverage") {
    Write-Host "[MARKER] Removing coverage data..."
    Remove-Item -Force .coverage
}

# Remove Python cache
Get-ChildItem -Recurse -Directory -Filter __pycache__ | ForEach-Object {
    Remove-Item -Recurse -Force $_
}

Get-ChildItem -Recurse -Filter "*.pyc" | ForEach-Object {
    Remove-Item -Force $_
}

Write-Host "[MARKER] Cleanup complete!"
