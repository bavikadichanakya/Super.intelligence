@echo off
title SUPER.INTELLIGENCEEE V2 — Autonomous Content Engine
cd /d A:\SUPER.INTELLIGENCEEE

echo ======================================================================
echo SUPER.INTELLIGENCEEE V2 — Zero-Budget Autonomous Media Engine
echo Target Platform: Instagram Reels (5 Reels / Week)
echo Python Environment: Python 3.11.15 (.venv)
echo Offline TTS: Piper TTS (en_US-lessac-medium)
echo Renderer: HyperFrames CLI v0.9.12
echo Local Web Dashboard: http://127.0.0.1:5000
echo ======================================================================
echo.

IF NOT EXIST ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at A:\SUPER.INTELLIGENCEEE\.venv!
    pause
    exit /b 1
)

echo Activating Python 3.11 virtual environment...
call .venv\Scripts\activate.bat

echo Opening browser at http://127.0.0.1:5000 ...
start "" "http://127.0.0.1:5000"

echo Launching FastAPI Server on port 5000...
python app.py serve --host 127.0.0.1 --port 5000

pause

