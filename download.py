import subprocess
import shutil
import os
import re

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
ERRORS = []
TITLES = {}

def youtube_dl(link, mp3):
    def get_ids(target_link):
        try:
            res = subprocess.run([
                "yt-dlp",
                "--flat-playlist",
                "--get-id",
                "--js-runtimes", "deno",
                target_link
            ], capture_output=True, text=True, check=False)

            if res.returncode != 0 or not res.stdout.strip():
                return [target_link]
            ids = [line.strip() for line in res.stdout.splitlines() if line.strip()]
            urls = []
            for i in ids:
                if i.startswith("http"):
                    urls.append(i)
                else:
                    urls.append(f"https://www.youtube.com/watch?v={i}")
            return urls
        except Exception:
            return [target_link]

    def get_title(video_url:str) -> None:
        try:
            res = subprocess.run([
                "yt-dlp",
                "--get-title",
                "--js-runtimes", "deno",
                video_url
            ], capture_output=True, text=True, check=False)

            title = res.stdout.splitlines()[0].strip() if res.stdout else video_url
            if res.stdout:
                TITLES[video_url] = title

            return title
        except Exception:
            return video_url #just return the url if it isn't found

    urls = get_ids(link)
    total = len(urls)
    done = 0
    failed = []

    for idx, u in enumerate(urls, start=1):
        # lightweight identifier for display (avoid slow title lookup)
        try:
            vid = u.split("v=")[-1].split("&")[0]
            display = vid
        except Exception:
            display = u

        if mp3.lower() == "nee":
            cmd = [
                "yt-dlp",
                "-f", "best",
                "-o", "exports/%(title)s.%(ext)s",
                "--js-runtimes", "deno",
                # "--print", "%(title)s",
                u
            ]
            print(f"{bcolors.OKCYAN}Downloading video ({idx}/{total}): {display}{bcolors.ENDC}")
        else:
            cmd = [
                "yt-dlp",
                "-x",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "--add-metadata",
                "--parse-metadata", "playlist_index:%(track_number)s",
                "--embed-metadata",
                "--embed-thumbnail",
                "--convert-thumbnails", "jpg",
                "--ppa", 'ThumbnailsConvertor+FFmpeg_o:-c:v mjpeg -qmin 1 -qscale:v 1 -vf crop="min(iw\\,ih)":"min(iw\\,ih)"',
                "--js-runtimes", "deno",
                "-o", "exports/%(title)s.%(ext)s",
                # "--print", "%(title)s",
                u
            ]
            print(f"{bcolors.OKCYAN}Downloading audio (as mp3) ({idx}/{total}): {display}{bcolors.ENDC}")

        # capture output so we can extract the title from yt-dlp output without a separate call
        res = subprocess.run(cmd)
        out = res.stdout or ""

        if res.returncode != 0:
            # try to extract the title from the output
            title = None
            # 1) look for Destination: exports/<title>.<ext>
            m = re.search(r'Destination:\s*exports/(.+?)\.(?:mp3|m4a|webm|mp4|mkv|flac|wav|aac)', out, re.IGNORECASE)
            if m:
                title = m.group(1)
            else:
                # 2) if we added --print, the title is likely one of the first non-empty lines
                lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
                if lines:
                    title = lines[0]

            if not title:
                # fallback to slow safe method
                title = get_title(u)
            else:
                TITLES[u] = title

            failed.append(u)
            ERRORS.append(u)

        done += 1

        # simple progress bar
        try:
            bar_len = 30
            filled = int(bar_len * done / total) if total else bar_len
            bar = "#" * filled + "-" * (bar_len - filled)

            print(f"{bcolors.OKCYAN}\rProgress: [{bar}] {done}/{total}{bcolors.ENDC}", end="\n\n", flush=True)
        except Exception:
            pass

    if failed:
        print(f"\n{bcolors.FAIL}{len(failed)} item{"s were" if len(failed) > 1 else " was"} not available:{bcolors.ENDC}")
        
        for index, failed_link in enumerate(failed, start=1):
            print(f"{index}. {failed_link}{f" ({TITLES[failed_link]})" if failed_link in TITLES else ""}")
    else:
        print(f"{bcolors.OKGREEN}Alles gedownload. Je audio/video staat in de /exports map. {bcolors.ENDC}")

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
        if mp3 != "nee":
            mp3 = "ja"

        youtube_dl(link, mp3)

        print()

        again = input(
            f"{bcolors.OKBLUE}Wilt u nog iets exporteren? "
            f"(ja = alles wissen en opnieuw/extra, nee = afsluiten) [nee]: {bcolors.ENDC}"
        ).strip().lower()

        if again != "ja":
            break

        clear_exports()
        print(f"{bcolors.WARNING}/exports map is geleegd.{bcolors.ENDC}\n")

    # RESET COLORS before exit
    if ERRORS:
        print(f"{bcolors.WARNING}Recap - downloads with errors:{bcolors.ENDC}")
        for i, t in enumerate(ERRORS, start=1):
            print(f"{bcolors.FAIL}{i}. {t}{bcolors.ENDC}")

    print(bcolors.ENDC)
    print("Programma afgesloten.")


if __name__ == "__main__":
    main()
