@echo off
echo ========================================================
echo Starting FormSathiAI Frontend Vite Server...
echo ========================================================
cd /d "%~dp0frontend"
set PATH=C:\Program Files\nodejs;%PATH%
npm run dev
pause
