@echo off
title JobVani - Sarkari Naukri Portal Server
cd /d "%~dp0"
echo ===================================================
echo Starting JobVani Server on http://127.0.0.1:8000 ...
echo ===================================================
python start_server.py
pause
