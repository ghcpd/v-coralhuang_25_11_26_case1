param()
try {
    $venv = Join-Path $PSScriptRoot ".venv"
    if (Test-Path $venv) { Remove-Item -Recurse -Force $venv }
    Get-ChildItem -Path $PSScriptRoot -Recurse -Force -Include '__pycache__','.pytest_cache' | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Clean complete."
}
catch {
    Write-Error $_
    exit 1
}
