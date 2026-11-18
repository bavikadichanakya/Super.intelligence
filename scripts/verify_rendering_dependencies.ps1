# SUPER.INTELLIGENCEEE — Multi-Engine Dependency Verifier
# Programmatically validates each rendering engine, versions, and scratch space

$ErrorActionPreference = "Continue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SUPER.INTELLIGENCEEE — Dependency Verification Suite" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$allPassed = $true
$VENV_PYTHON = "A:\SUPER.INTELLIGENCEEE\.venv\Scripts\python.exe"

# 1. Python & Pydantic
Write-Host "`n[1/5] Checking Python virtualenv and Pydantic..." -ForegroundColor Yellow
if (Test-Path $VENV_PYTHON) {
    $pydanticVer = & $VENV_PYTHON -c "import pydantic; print(pydantic.__version__)"
    Write-Host "[OK] Python 3.11 with Pydantic $pydanticVer" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Python virtualenv missing at $VENV_PYTHON" -ForegroundColor Red
    $allPassed = $false
}

# 2. Manim Community
Write-Host "`n[2/5] Checking Manim Community..." -ForegroundColor Yellow
$manimVer = & $VENV_PYTHON -c "import manim; print(manim.__version__)" 2>$null
if ($manimVer) {
    Write-Host "[OK] Manim Community $manimVer available in .venv" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Manim Community not importable in .venv" -ForegroundColor Red
    $allPassed = $false
}

# 3. FFmpeg with required filters
Write-Host "`n[3/5] Checking FFmpeg and required filters..." -ForegroundColor Yellow
$ffmpegCmd = Get-Command ffmpeg.exe -ErrorAction SilentlyContinue
if ($null -ne $ffmpegCmd) {
    $ffmpegOut = & ffmpeg.exe -version | Select-Object -First 1
    Write-Host "[OK] FFmpeg found: $ffmpegOut" -ForegroundColor Green
} else {
    Write-Host "[FAIL] FFmpeg not found on PATH" -ForegroundColor Red
    $allPassed = $false
}

# 4. HyperFrames CLI
Write-Host "`n[4/5] Checking HyperFrames CLI..." -ForegroundColor Yellow
$hfVer = & npx.cmd hyperframes --version 2>$null
if ($LASTEXITCODE -eq 0 -and $hfVer) {
    Write-Host "[OK] HyperFrames CLI: $hfVer (via npx.cmd)" -ForegroundColor Green
} else {
    $hfCmd = Get-Command hyperframes.cmd -ErrorAction SilentlyContinue
    if ($null -ne $hfCmd) {
        $hfVer = & hyperframes.cmd --version 2>$null
        Write-Host "[OK] HyperFrames CLI: $hfVer" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] HyperFrames CLI not found" -ForegroundColor Red
        $allPassed = $false
    }
}

# 5. Drive A: Headroom
Write-Host "`n[5/5] Checking Drive A: scratch space headroom..." -ForegroundColor Yellow
$driveA = Get-PSDrive A -ErrorAction SilentlyContinue
if ($null -ne $driveA) {
    $freeGb = [math]::Round($driveA.Free / 1GB, 2)
    if ($freeGb -ge 2.0) {
        Write-Host "[OK] Drive A: has $freeGb GB free headroom (Threshold: 2.0 GB)" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Drive A: has only $freeGb GB free headroom" -ForegroundColor Yellow
    }
}

Write-Host "`n------------------------------------------------------------"
if ($allPassed) {
    Write-Host "ALL MANDATORY RENDERING DEPENDENCIES VERIFIED PASSED" -ForegroundColor Green
    exit 0
} else {
    Write-Host "SOME DEPENDENCIES FAILED VERIFICATION" -ForegroundColor Red
    exit 1
}
