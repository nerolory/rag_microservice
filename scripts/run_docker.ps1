param(
    [switch]$Build,
    [switch]$Clean,
    [switch]$Attach
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example - fill in API keys before using /upload and /ask."
}

if ($Clean) {
    & (Join-Path $PSScriptRoot "docker_clean.ps1")
}

if ($Build) {
    Write-Host "Building image (old dangling layers will be pruned after build)..."
    docker compose build app
    docker image prune -f
}

Write-Host "Starting Docker app at http://localhost:8000 (docs: /docs)"
Write-Host 'Containers and volumes are kept. Use -Clean to stop and remove containers (data volumes stay).'
Write-Host 'Use -Attach to stream logs in this terminal (default: detached, -d).'

if ($Attach) {
    docker compose up app
} else {
    docker compose up -d app
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Host "App is running in background. Logs: docker compose logs -f app"
    Write-Host "Stop: docker compose down"
}
