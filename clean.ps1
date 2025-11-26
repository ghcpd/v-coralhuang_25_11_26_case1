$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

$paths = @(
    (Join-Path $root ".venv"),
    (Join-Path $root ".pytest_cache"),
    (Join-Path $root "htmlcov"),
    (Join-Path $root ".coverage")
)
foreach ($p in $paths) {
    if (Test-Path $p) { Remove-Item -Recurse -Force $p }
}

Get-ChildItem -Path $root -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $root -Recurse -Include "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[clean] Environment reset."
