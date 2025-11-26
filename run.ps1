Param()
$venv = "$PWD/.venv"
$py = if (Test-Path "$venv/Scripts/python.exe") { "$venv/Scripts/python.exe" } else { 'python' }
Write-Host "Running user_display_optimized demo with $py"
Start-Process -FilePath $py -ArgumentList '-m','user_display_optimized' -NoNewWindow -Wait
