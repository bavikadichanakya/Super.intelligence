@echo off
TITLE SUPER.INTELLIGENCEEE - Autonomous Content Production Engine
echo ========================================================
echo   SUPER.INTELLIGENCEEE - Launching Local Dashboard
echo ========================================================
echo   Target Environment: Windows 11 ^| Python 3.14 ^| 8GB RAM Bound
echo   Dashboard URL: http://127.0.0.1:5000
echo ========================================================

IF EXIST .venv\Scripts\python.exe (
    .\.venv\Scripts\python.exe app.py serve
) ELSE (
    python app.py serve
)
pause

