# Cross-platform setup script for Windows PowerShell
# Creates virtual environment and installs dependencies

param()

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

Write-Host "[MARKER] Setting up Python environment..."

# Check Python version
$PythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Python 3 not found. Please install Python 3.10+"
    exit 1
}

Write-Host "[MARKER] $PythonCheck"

# Create virtual environment if it doesn't exist
if (-Not (Test-Path "venv")) {
    Write-Host "[MARKER] Creating virtual environment..."
    python -m venv venv
} else {
    Write-Host "[MARKER] Virtual environment already exists"
}

# Activate virtual environment
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "[MARKER] Upgrading pip..."
python -m pip install --upgrade pip | Out-Null

# Install dependencies
Write-Host "[MARKER] Installing dependencies..."
pip install -r requirements.txt

Write-Host "[MARKER] Setup complete! Virtual environment ready in .\venv"
Write-Host "[MARKER] To activate: .\venv\Scripts\Activate.ps1"
