@echo off
echo ========================================================
echo Starting FormSathiAI FastAPI Backend...
echo ========================================================
cd /d "%~dp0backend"
set PATH=C:\Program Files\Tesseract-OCR;%USERPROFILE%\.local\bin;%PATH%
".venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
