@echo off

rem Check if Chocolatey is installed
choco --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Chocolatey is not installed. Installing...
    winget install --id Chocolatey.Chocolatey -e --accept-source-agreements --accept-package-agreements
    echo Chocolatey has been installed.
) else (
    echo Chocolatey is already installed.
)

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing...
    choco install python -y
    echo Python has been installed.
) else (
    echo Python is already installed.
)

rem Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing...
    choco install pip -y
    echo pip has been installed.
) else (
    echo pip is already installed.
)

rem Install the required packages (default dependency group, includes yt-dlp & yt-dlp-ejs)
pip install -U "yt-dlp[default]"

rem Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Installing...
    choco install git -y
    echo Git has been installed.
) else (
    echo Git is already installed.
)

rem Check if deno is installed (js runtime)
deno --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Deno is not installed. Installing...
    choco install deno
    echo Deno has been installed.
) else (
    echo Deno is already installed.
)


rem Check if ffmpeg is installed
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo ffmpeg is not installed. Installing...
    choco install ffmpeg -y
    echo ffmpeg has been installed.
) else (
    echo ffmpeg is already installed.
)

pause