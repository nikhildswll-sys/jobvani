@echo off
title JobVani - Master Multi-Department Scraper (SSC, UPSC, Railway, Defence, Police, All India)
color 0B
echo ====================================================================
echo                   JOBVANI MASTER INGESTION ENGINE
echo  [SSC | UPSC | Railway | Army | Navy | Air Force | Police | All India]
echo ====================================================================
echo.
echo Running multi-channel scrapers in parallel...
python -m scrapers.runner
echo.
echo ====================================================================
echo  Sync Complete! Check latest recruitments at: http://127.0.0.1:8000
echo ====================================================================
echo.
pause
