$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "_env_helpers.ps1")
$base = "http://127.0.0.1:8080"
$h = Get-JudgeBasicHeader
Write-Host "LOCAL"
foreach ($p in @("/api/health","/api/cameras","/api/track/GJ01AB1234","/api/alerts?status=open")) {
  try {
    if ($p -eq "/api/health") { Invoke-RestMethod "$base$p" | Out-Null }
    else { Invoke-RestMethod "$base$p" -Headers $h | Out-Null }
    Write-Host "PASS $p"
  } catch { Write-Host "FAIL $p" }
}
Write-Host "HUMAN checklist: YouTube unlisted both videos, Drive Anyone+Viewer, hosted URL login, GitHub, portal receipt."
