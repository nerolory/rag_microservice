param(
    [switch]$ShutdownWsl
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Stopping stray test containers (each loads PyTorch + model into RAM)..."
docker ps -q --filter "name=llm_python-test-run" | ForEach-Object {
    docker rm -f $_ | Out-Null
}

Write-Host "Stopping project stack..."
$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
docker compose down --remove-orphans 2>&1 | Out-Null
$ErrorActionPreference = $prevEap

Write-Host "Pruning dangling images..."
docker image prune -f | Out-Null

Write-Host ""
Write-Host "Docker containers for this project are stopped."
Write-Host "vmmem often KEEPS RAM until WSL is restarted."
if ($ShutdownWsl) {
    Write-Host "Shutting down WSL (Docker Desktop will stop)..."
    wsl --shutdown
    Write-Host "Done. Start Docker Desktop again when needed."
} else {
    Write-Host "To return memory to Windows now, run:"
    Write-Host "  .\scripts\docker_free_memory.ps1 -ShutdownWsl"
    Write-Host "or manually: wsl --shutdown"
}
