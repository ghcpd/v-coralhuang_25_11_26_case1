param()
try {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { $python = Get-Command python3 -ErrorAction SilentlyContinue }
    if (-not $python) { throw "Python is not available in PATH" }

    $venv = Join-Path $PSScriptRoot ".venv"
    if (-not (Test-Path $venv)) {
        & $python.Path -m venv $venv
    }

    Write-Host "Installing dependencies into $venv"
    $activate = Join-Path $venv "Scripts/Activate.ps1"
    & $activate
    pip install --upgrade pip
    pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
    Write-Host "Setup complete. Activate with: & $venv\Scripts\Activate.ps1"
}
catch {
    Write-Error $_
    exit 1
}
