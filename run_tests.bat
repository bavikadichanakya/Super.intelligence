@echo off
TITLE SUPER.INTELLIGENCEEE - Test Suite
echo ========================================================
echo   Running Automated Test Suite (Pytest)
echo ========================================================

IF EXIST .venv\Scripts\pytest.exe (
    .\.venv\Scripts\pytest.exe tests/ -v
) ELSE (
    pytest tests/ -v
)
pause

