$ErrorActionPreference = "Stop"
$base = "http://127.0.0.1:8080"
$pair = "judge:set-this-before-submit"
$basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
$h = @{ Authorization = "Basic $basic" }
Write-Host "LOCAL"
foreach ($p in @("/api/health","/api/cameras","/api/track/GJ01AB1234","/api/alerts?status=open")) {
  try {
    if ($p -eq "/api/health") { Invoke-RestMethod "$base$p" | Out-Null }
    else { Invoke-RestMethod "$base$p" -Headers $h | Out-Null }
    Write-Host "PASS $p"
  } catch { Write-Host "FAIL $p" }
}
Write-Host "HUMAN checklist: YouTube unlisted both videos, Drive Anyone+Viewer, hosted URL login, GitHub, portal receipt."
