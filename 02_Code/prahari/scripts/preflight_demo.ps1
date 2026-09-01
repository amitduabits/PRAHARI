$ErrorActionPreference = "Stop"
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
$pair = "judge:set-this-before-submit"
$basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
try {
  $wl = Invoke-RestMethod "$base/api/watchlist" -Headers @{ Authorization = "Basic $basic" }
  $has = @($wl | Where-Object { $_.source_case_id -eq "WL-001" }).Count -gt 0
  Check "WL-001 present" $has
} catch { Check "watchlist" $false }
try {
  $html = & curl.exe -s "$base/"
  Check "UI PRAHARI" ($html -match "PRAHARI")
} catch { Check "UI" $false }
if ($script:fail -gt 0) { Write-Host "FAIL"; exit 1 } else { Write-Host "PASS"; exit 0 }
