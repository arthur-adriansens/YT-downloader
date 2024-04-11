@echo off

set /p name="Plak hier de YouTube link: "
set /p mp3="Wilt u de video omzetten naar .mp3? (ja of nee): "

python download.py %name% %mp3%

echo Het programma is klaar. Je video staat in de /videos map.
pause