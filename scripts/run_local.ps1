Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example — fill in API keys before using /upload and /ask."
}

$chromaDir = Join-Path $ProjectRoot "data\chroma"
if (-not (Test-Path $chromaDir)) {
    New-Item -ItemType Directory -Path $chromaDir -Force | Out-Null
}

Write-Host "Installing CPU torch and local embedding dependencies..."
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e ".[local]"

Write-Host "Starting server at http://127.0.0.1:8000 (docs: /docs)"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
