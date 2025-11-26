Param()
$venv = "$PWD/.venv"
$py = if (Test-Path "$venv/Scripts/python.exe") { "$venv/Scripts/python.exe" } else { 'python' }
Write-Host "Running tests with $py"
Start-Process -FilePath $py -ArgumentList '-m','pytest','-q','--maxfail=1','--disable-warnings','--cov=user_display_optimized','--cov-report=term-missing' -NoNewWindow -Wait
