$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "_env_helpers.ps1")
$base = "http://127.0.0.1:8080"
$script:fail = 0
function Check($name, $ok) {
  if ($ok) { Write-Host "PASS $name" } else { Write-Host "FAIL $name"; $script:fail++ }
}
try {
  $h = Invoke-RestMethod "$base/api/health"
  Check "health 200" ($h.status -eq "ok")
  Check "detections>=6" ($h.detections -ge 6)
  Check "cameras>=11" ($h.cameras -ge 11)
} catch { Check "health reachable" $false }
try {
  $hdr = Get-JudgeBasicHeader
  $wl = Invoke-RestMethod "$base/api/watchlist" -Headers $hdr
  $has = @($wl | Where-Object { $_.source_case_id -eq "WL-001" }).Count -gt 0
  Check "WL-001 present" $has
} catch { Write-Host $_.Exception.Message; Check "watchlist" $false }
try {
  $html = & curl.exe -s "$base/"
  Check "UI PRAHARI" ($html -match "PRAHARI")
} catch { Check "UI" $false }
if ($script:fail -gt 0) { Write-Host "FAIL"; exit 1 } else { Write-Host "PASS"; exit 0 }
