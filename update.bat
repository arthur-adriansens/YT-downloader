@echo off
setlocal
 
set REPO_URL=https://github.com/arthur-adriansens/YT-downloader.git
 
:: Haal de laatste wijzigingen op
echo.
echo [git-update] Laatste wijzigingen ophalen...
echo [git-update] Externe bron: %REPO_URL%
echo.
 
git pull %REPO_URL% main
 
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [git-update] FOUT: git pull is mislukt. Zie de uitvoer hierboven.
    pause
    exit /b 1
)
 
echo.
echo [git-update] Klaar! De map is up-to-date.
pause