$ErrorActionPreference = "Stop"
$base = "http://127.0.0.1:8080"
$fail = 0
function Check($name, $ok) {
  if ($ok) { Write-Host "PASS $name" } else { Write-Host "FAIL $name"; script:fail++ }
}
try {
  $h = Invoke-RestMethod "$base/api/health"
  Check "health 200" ($h.status -eq "ok")
  Check "detections>=6" ($h.detections -ge 6)
  Check "cameras>=11" ($h.cameras -ge 11)
} catch { Check "health reachable" $false }
$pair = "judge:set-this-before-submit"
$bytes = [Text.Encoding]::ASCII.GetBytes($pair)
$basic = [Convert]::ToBase64String($bytes)
try {
  $wl = Invoke-RestMethod "$base/api/watchlist" -Headers @{ Authorization = "Basic $basic" }
  Check "WL-001 present" ($wl.source_case_id -contains "WL-001" -or ($wl | Where-Object { $_.source_case_id -eq "WL-001" }))
} catch { Check "watchlist" $false }
try {
  $html = (Invoke-WebRequest "$base/").Content
  Check "UI PRAHARI" ($html -match "PRAHARI")
} catch { Check "UI" $false }
if ($fail -gt 0) { Write-Host "FAIL"; exit 1 } else { Write-Host "PASS"; exit 0 }
