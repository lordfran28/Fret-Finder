# Fret Finder - one-time setup for automatic upload
$ErrorActionPreference = "Stop"
try { [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12 } catch {}
$Api  = if ($env:FF_API) { $env:FF_API } else { "https://api.github.com/repos/lordfran28/Fret-Finder" }
$Data = if ($env:FF_DATA) { $env:FF_DATA } else { Join-Path $env:LOCALAPPDATA "FretFinder" }
$VfKey = Join-Path $env:LOCALAPPDATA "ValveFinder\key.txt"
$Upload = Join-Path $PSScriptRoot "upload.ps1"
$TaskName = "Fret Finder upload"
$Keys = "https://github.com/settings/personal-access-tokens"
$NewKey = "https://github.com/settings/personal-access-tokens/new?name=Fret%20Finder%20uploads%20from%20PC&description=Adds%20songs%20from%20the%20PC%20to%20Fret%20Finder&target_name=lordfran28&expires_in=366&contents=write"

function Test-Key([string]$plain) {
  # 0 = it can add songs, 401 = GitHub doesn't know the key, 403/404 = it can't add to Fret-Finder, -1 = no internet.
  # Reading isn't enough to know (anyone can read the site), so it writes a small loose object that never shows anywhere.
  try {
    $body = [Text.Encoding]::UTF8.GetBytes('{"content":"Fret Finder upload key check","encoding":"utf-8"}')
    Invoke-WebRequest -Uri ($Api + "/git/blobs") -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -UserAgent "FretFinderUpload" -Headers @{ Authorization = "Bearer $plain"; Accept = "application/vnd.github+json" } | Out-Null
    return 0
  } catch {
    if ($_.Exception.Response) { return [int]$_.Exception.Response.StatusCode }
    return -1
  }
}
function Read-VfKey {
  try {
    $secure = (Get-Content -LiteralPath $VfKey -Raw).Trim() | ConvertTo-SecureString
    return [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
  } catch { return $null }
}

Write-Host ""
Write-Host "  FRET FINDER - AUTOMATIC UPLOAD" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Songs you put in this folder will be added to the website by themselves:"
Write-Host "  $(Split-Path -Parent $PSScriptRoot)"
Write-Host ""

$plain = $null
if ($env:FF_KEY) { $plain = $env:FF_KEY.Trim() }

# The Valve Finder key on this computer does the job too, if it was made for both sites.
$vf = $null
if (-not $plain -and (Test-Path -LiteralPath $VfKey)) { $vf = Read-VfKey }
if ($vf -and (Test-Key $vf) -eq 0) { $plain = $vf; Write-Host "  Using the same GitHub key as Valve Finder." -ForegroundColor Green }

# No usable key yet: make one for Fret Finder.
if (-not $plain -and -not $env:FF_KEY) {
  Write-Host "  1. A GitHub page is opening. Under 'Repository access' choose"
  Write-Host "     'Only select repositories' and pick Fret-Finder (you can add Valve-Finder too)."
  Write-Host "     (Contents is already set to 'Read and write'.)"
  Write-Host "  2. Press 'Generate token' at the bottom, then copy the key it shows."
  Write-Host "  3. Come back here, paste it (right-click or Ctrl+V) and press Enter."
  Write-Host ""
  Start-Process $NewKey
  for ($try = 1; $try -le 3 -and -not $plain; $try++) {
    $secure = Read-Host "  Paste the key here" -AsSecureString
    $t = [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)).Trim()
    if (-not $t) { Write-Host "  Nothing was pasted. Try again." -ForegroundColor Red; continue }
    $code = Test-Key $t
    if ($code -eq 0) { $plain = $t }
    elseif ($code -eq 401) { Write-Host "  GitHub didn't accept that key. Copy it again (the whole thing, starting github_pat_)." -ForegroundColor Red }
    elseif ($code -eq -1) { Write-Host "  Couldn't reach GitHub. Check the internet connection and try again." -ForegroundColor Red }
    else { Write-Host "  That key can't see Fret-Finder. Make a new one and pick Fret-Finder under Repository access." -ForegroundColor Red }
  }
} elseif ($env:FF_KEY -and (Test-Key $plain) -ne 0) { $plain = $null }

if (-not $plain) { Write-Host ""; Write-Host "  Setup didn't finish. Run it again when you're ready."; if (-not $env:FF_KEY) { Read-Host "  Press Enter to close" | Out-Null }; exit 1 }

New-Item -ItemType Directory -Force -Path $Data | Out-Null
ConvertTo-SecureString $plain -AsPlainText -Force | ConvertFrom-SecureString | Set-Content -LiteralPath (Join-Path $Data "key.txt")

# Start with Windows, quietly, and keep running in the background.
$started = $false
try {
  $me = [Security.Principal.WindowsIdentity]::GetCurrent().Name
  $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument ("-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"" + $Upload + "`"")
  $trigger = New-ScheduledTaskTrigger -AtLogOn -User $me
  $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -StartWhenAvailable
  $principal = New-ScheduledTaskPrincipal -UserId $me -LogonType Interactive -RunLevel Limited
  Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
  Start-ScheduledTask -TaskName $TaskName
  $started = $true
} catch {
  # Fallback: a shortcut in the Startup folder does the same at every sign-in.
  try {
    $lnk = Join-Path ([Environment]::GetFolderPath("Startup")) "Fret Finder upload.lnk"
    $sh = New-Object -ComObject WScript.Shell; $s = $sh.CreateShortcut($lnk)
    $s.TargetPath = "powershell.exe"; $s.Arguments = "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$Upload`""; $s.WindowStyle = 7; $s.Save()
    Start-Process powershell.exe -WindowStyle Hidden -ArgumentList @("-NoProfile", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-File", "`"$Upload`"")
    $started = $true
  } catch {}
}
Write-Host ""
if ($started) {
  Write-Host "  Done. New songs in this folder go to the website within a minute or two." -ForegroundColor Green
  Write-Host "  It starts by itself whenever you sign in to Windows. 'Upload log.txt' shows what it added."
} else {
  Write-Host "  The key is saved, but Windows wouldn't let it start by itself." -ForegroundColor Red
  Write-Host "  Double-click 'Upload now' whenever you add songs."
}
Write-Host ""
if (-not $env:FF_KEY) { Read-Host "  Press Enter to close" | Out-Null }
