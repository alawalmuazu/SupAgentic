@echo off
title AI Threat Monitor - Launcher
color 0A
echo.
echo  ===================================================
echo   AI THREAT MONITOR - Auto Launcher
echo   Based on: Ivan Barbato's Hidden Architecture
echo  ===================================================
echo.
echo  [*] Starting backend (psutil metrics on port 8092)...
start /B "Backend" cmd /c "python "%~dp0threat_monitor_backend.py" 2>&1"
timeout /t 2 /nobreak >nul

echo  [*] Starting frontend server (port 8091)...
start /B "Frontend" cmd /c "npx -y http-server "%~dp0" -p 8091 -c-1 2>&1"
timeout /t 3 /nobreak >nul

echo.
echo  [OK] Both servers are running!
echo.
echo  Open in Chrome:  http://127.0.0.1:8091/ai_threat_monitor.html
echo.
echo  Press any key to open the dashboard automatically...
pause >nul

start "" "http://127.0.0.1:8091/ai_threat_monitor.html"

echo.
echo  Dashboard opened. Press Ctrl+C or close this window to stop.
echo.
pause
