Param()
Write-Host "Cleaning environment (PowerShell)"
Remove-Item -LiteralPath .venv -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item -LiteralPath .pytest_cache -Force -Recurse -ErrorAction SilentlyContinue
Remove-Item -LiteralPath .coverage -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath htmlcov -Force -Recurse -ErrorAction SilentlyContinue
Write-Host "Clean complete"
