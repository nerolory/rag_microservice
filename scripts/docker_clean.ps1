Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Stopping project containers..."
docker ps -q --filter "name=llm_python-test-run" | ForEach-Object {
    docker rm -f $_ | Out-Null
}
docker compose down --remove-orphans *> $null

Write-Host "Removing dangling images (old builds)..."
docker image prune -f

Write-Host "Removing unused build cache older than 24h..."
docker builder prune -f --filter "until=24h"

Write-Host "Project disk usage:"
docker system df
