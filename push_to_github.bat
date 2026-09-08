@echo off
title Push JobVani to GitHub (nikhildswll-sys/jobvani)
color 0A
echo ====================================================================
echo             JOBVANI - PUSH TO GITHUB (nikhildswll-sys)
echo ====================================================================
echo.
echo Pushing local repository with all scrapers and GitHub Actions to:
echo https://github.com/nikhildswll-sys/jobvani
echo.
"%LOCALAPPDATA%\Programs\Git\cmd\git.exe" push -u origin main
echo.
echo ====================================================================
echo If pushed successfully, check your repository at:
echo https://github.com/nikhildswll-sys/jobvani
echo ====================================================================
echo.
pause
