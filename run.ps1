$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvDir = Join-Path $root ".venv"
$venvPython = Join-Path $venvDir "Scripts/python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Error "Virtual environment not found. Run setup.ps1 first."; exit 1
}

& $venvPython (Join-Path $root "user_display_optimized.py") @Args
