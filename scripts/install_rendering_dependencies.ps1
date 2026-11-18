# SUPER.INTELLIGENCEEE — Idempotent Dependency Installer
# Installs and configures multi-engine dependencies for Python and Node.js
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SUPER.INTELLIGENCEEE — Multi-Engine Dependency Installer" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$VENV_PYTHON = "A:\SUPER.INTELLIGENCEEE\.venv\Scripts\python.exe"
if (-not (Test-Path $VENV_PYTHON)) {
    Write-Host "[ERROR] Python virtualenv not found at $VENV_PYTHON" -ForegroundColor Red
    exit 1
}

# 1. Python rendering requirements
Write-Host "`n[1/3] Verifying Python rendering requirements..." -ForegroundColor Yellow
& $VENV_PYTHON -m pip install -r "A:\SUPER.INTELLIGENCEEE\requirements-rendering.txt" --no-warn-script-location

# 2. Verify HyperFrames CLI
Write-Host "`n[2/3] Verifying HyperFrames CLI..." -ForegroundColor Yellow
$hfCmd = Get-Command hyperframes.cmd -ErrorAction SilentlyContinue
if ($null -eq $hfCmd) {
    Write-Host "[INFO] HyperFrames CLI not on path. Installing via npm..." -ForegroundColor Cyan
    npm install -g hyperframes@0.9.30
} else {
    Write-Host "[OK] HyperFrames CLI already installed at $($hfCmd.Source)" -ForegroundColor Green
}

# 3. Verify .temp scratch root
Write-Host "`n[3/3] Verifying .temp scratch directory on Drive A:..." -ForegroundColor Yellow
$tempDir = "A:\SUPER.INTELLIGENCEEE\.temp"
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
}
Write-Host "[OK] Scratch root configured at $tempDir" -ForegroundColor Green

Write-Host "`n[COMPLETE] All rendering dependencies verified successfully." -ForegroundColor Green
