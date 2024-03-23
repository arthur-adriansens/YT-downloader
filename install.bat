@echo off

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

rem Install the required packages
pip install pytube