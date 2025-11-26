param()
try {
    $venv = Join-Path $PSScriptRoot ".venv"
    if (Test-Path $venv) {
        & "$venv\Scripts\Activate.ps1"
    }
    pytest --maxfail=1 --disable-warnings -q --cov=user_display_optimized --cov-fail-under=85
}
catch {
    Write-Error $_
    exit 1
}
