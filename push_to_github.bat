@echo off
title Push JobApplyAutomation to GitHub
echo ========================================================
echo   Pushing JobApplyAutomation to GitHub (baidarbakht24)
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Your repository is now live at:
    echo https://github.com/baidarbakht24/JobApplyAutomation
) else (
    echo [NOTICE] If prompted to sign in, choose "Sign in with your browser"
    echo or make sure you created the repo at https://github.com/new
)
echo.
pause
