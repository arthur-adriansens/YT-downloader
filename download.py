import subprocess
import shutil
import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

EXPORT_DIR = "exports"

def youtube_dl(link, mp3):
    if mp3.lower() == "nee":
        print(f"{bcolors.OKCYAN}Downloading video...{bcolors.ENDC}")
        subprocess.run([
            "yt-dlp",
            "-f", "best",
            "-o", "exports/%(title)s.%(ext)s",
            link
        ])
    else:
        print(f"{bcolors.OKCYAN}Downloading audio (as mp3)...{bcolors.ENDC}")
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--add-metadata",
            "--embed-metadata",
            "--embed-thumbnail",
            "--convert-thumbnails", "jpg",
            "--ppa", 'ThumbnailsConvertor+FFmpeg_o:-c:v mjpeg -qmin 1 -qscale:v 1 -vf crop=\"min(iw\\,ih)\":\"min(iw\\,ih)\"',
            "-o", "exports/%(title)s.%(ext)s",
            link
        ])

    print(f"{bcolors.OKGREEN}Het programma is klaar. Je audio/video staat in de /exports map. {bcolors.ENDC}")

def clear_exports():
    if os.path.isdir(EXPORT_DIR):
        shutil.rmtree(EXPORT_DIR)
    os.makedirs(EXPORT_DIR, exist_ok=True)

def main():
    again = "eerste keer"

    while True:
        if again == "eerste keer":
            # Only first time
            deleteExports:bool = input(f"{bcolors.OKBLUE}Welkom! Wilt u uw vorige exports verwijderen (ja/nee) [ja]: {bcolors.ENDC}").strip().lower()
            if deleteExports == "ja" or deleteExports == "":
                clear_exports()
    
        link = input(f"{bcolors.OKBLUE}Plak hier de YouTube (Music) link: {bcolors.ENDC}").strip()
        if not link:
            print(f"{bcolors.FAIL}Geen link opgegeven.{bcolors.ENDC}")
            continue

        mp3:bool = input(
            f"{bcolors.OKBLUE}Wilt u dit downloaden als .mp3 "
            f"(ja = audio, nee = video) [ja]: {bcolors.ENDC}"
        ).strip().lower()

        # Default to "ja" if user presses Enter
        if mp3 == "":
            mp3 = "ja"

        youtube_dl(link, mp3)

        print()

        again = input(
            f"{bcolors.OKBLUE}Wilt u nog iets exporteren? "
            f"(ja = alles wissen en opnieuw/extra, nee = afsluiten) [ja]: {bcolors.ENDC}"
        ).strip().lower()

        if again != "ja" and again != "":
            break

        clear_exports()
        print(f"{bcolors.WARNING}/exports map is geleegd.{bcolors.ENDC}\n")

    # RESET COLORS before exit
    print(bcolors.ENDC)
    print("Programma afgesloten.")


if __name__ == "__main__":
    main()
