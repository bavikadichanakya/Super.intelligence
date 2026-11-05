@echo off
TITLE SUPER.INTELLIGENCEEE - Sequential Batch Video Render
echo ========================================================
echo   SUPER.INTELLIGENCEEE - Sequential 5-Reel Batch Render
echo ========================================================
echo   Enforcing 1-by-1 sequential rendering for 8 GB RAM stability.
echo ========================================================

IF EXIST .venv\Scripts\python.exe (
    .\.venv\Scripts\python.exe app.py --batch-render
) ELSE (
    python app.py --batch-render
)
pause

