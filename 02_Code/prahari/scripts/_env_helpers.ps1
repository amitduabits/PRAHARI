# Shared .env reader for preflight scripts. Never prints secrets.

function Get-DotEnvMap {
    $envFile = Join-Path $PSScriptRoot "..\.env"
    if (-not (Test-Path $envFile)) {
        throw ".env missing. Copy .env.example to .env and set JUDGE_PASSWORD."
    }
    $map = @{}
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#") -or $line -notmatch "=") { return }
        $i = $line.IndexOf("=")
        $k = $line.Substring(0, $i).Trim()
        $v = $line.Substring($i + 1).Trim().Trim('"').Trim("'")
        $map[$k] = $v
    }
    return $map
}

function Get-JudgeBasicHeader {
    $map = Get-DotEnvMap
    $user = if ($env:JUDGE_USER) { $env:JUDGE_USER } elseif ($map["JUDGE_USER"]) { $map["JUDGE_USER"] } else { "judge" }
    $pass = if ($env:JUDGE_PASSWORD) { $env:JUDGE_PASSWORD } else { $map["JUDGE_PASSWORD"] }
    if (-not $pass) { throw "JUDGE_PASSWORD empty in environment and .env" }
    if ($pass -eq "set-this-before-submit") { throw "JUDGE_PASSWORD still the example value. Rotate it (A01)." }
    $pair = "${user}:${pass}"
    $basic = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))
    return @{ Authorization = "Basic $basic" }
}
