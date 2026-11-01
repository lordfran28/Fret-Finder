# Fret Finder - stop automatic upload and forget the key on this computer
$Data = if ($env:FF_DATA) { $env:FF_DATA } else { Join-Path $env:LOCALAPPDATA "FretFinder" }
$Upload = Join-Path $PSScriptRoot "upload.ps1"
try { Stop-ScheduledTask -TaskName "Fret Finder upload" -ErrorAction SilentlyContinue; Unregister-ScheduledTask -TaskName "Fret Finder upload" -Confirm:$false -ErrorAction SilentlyContinue } catch {}
try { Remove-Item -LiteralPath (Join-Path ([Environment]::GetFolderPath("Startup")) "Fret Finder upload.lnk") -ErrorAction SilentlyContinue } catch {}
# Only this folder's uploader; Valve Finder's keeps running.
Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -and $_.CommandLine.Contains($Upload) } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Remove-Item -LiteralPath (Join-Path $Data "key.txt") -ErrorAction SilentlyContinue
Write-Host ""
Write-Host "  Automatic upload is off for Fret Finder, and its GitHub key is removed from this computer."
Write-Host "  Your songs on the website are untouched. Valve Finder's upload is not affected."
Write-Host ""
Read-Host "  Press Enter to close" | Out-Null
