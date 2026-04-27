
from sys import argv
import subprocess

def youtube_dl(link, mp3):
    if mp3.lower() == "ja":
        print("Downloading and converting to mp3...")
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", "videos/%(title)s.%(ext)s",
            link
        ])
    else:
        print("Downloading video...")
        subprocess.run([
            "yt-dlp",
            "-f", "best",
            "-o", "videos/%(title)s.%(ext)s",
            link
        ])

if __name__ == "__main__":
    youtube_dl(argv[1], argv[2])
