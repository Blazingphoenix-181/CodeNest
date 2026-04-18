@echo off
echo.
echo   CodeNest - Offline AI Coding Assistant
echo   100%% Private - No Internet Required
echo.

:: Check Ollama
where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   [ERROR] Ollama not found.
    echo   Install from: https://ollama.ai
    echo   Then run: ollama pull phi3
    pause
    exit /b 1
)

:: Start Ollama if not running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   Starting Ollama...
    start /b ollama serve
    timeout /t 3 /nobreak >nul
)

:: Set model
set MODEL=phi3
if defined CODENEST_MODEL set MODEL=%CODENEST_MODEL%

echo   Checking model: %MODEL%
ollama list | findstr /i "%MODEL%" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo   Pulling %MODEL% - this may take a few minutes...
    ollama pull %MODEL%
)

:: Create venv if needed
if not exist venv (
    echo   Setting up Python environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -q -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo.
echo   Open your browser: http://localhost:8000
echo   Press Ctrl+C to stop
echo.

uvicorn app_fixed:app --host 0.0.0.0 --port 8000 --reload
pause
