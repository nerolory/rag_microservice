Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Rebuilding and restarting app..."
docker compose down --remove-orphans
docker compose build app
docker image prune -f
docker compose up -d app

Write-Host "Done. Health: http://localhost:8000/health"
