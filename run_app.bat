@echo off
echo ========================================================
echo Launching FormSathiAI Integrated Application...
echo Tagline: Make complicated forms easier to understand.
echo ========================================================
cd /d "%~dp0backend"
set PATH=C:\Program Files\Tesseract-OCR;%USERPROFILE%\.local\bin;%PATH%
start "" http://127.0.0.1:8000
".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
