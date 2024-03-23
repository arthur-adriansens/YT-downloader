@echo off

echo Plak hier de YouTube link:
set /p name=
python download.py %name%
echo Het programma is klaar. Je video staat in de /videos map.
pause