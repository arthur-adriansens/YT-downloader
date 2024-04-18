from sys import argv as arguments
import os

from pytube import YouTube
from moviepy.editor import *


def Youtube_DL(link, mp3):
	video = YouTube(link)
	title = video.title

	stream = video.streams.get_highest_resolution()

	print(f'Downloading "{title}"...')
	path = stream.download("videos")
	print(f'Downloaded "{title}"!')

	if mp3 == "ja":
		print("")
		print("Converting to mp3...")
		video = VideoFileClip(path)
		video.audio.write_audiofile(path.replace(".mp4", ".mp3"))
		print("Converted to mp3!")

		try:
			os.remove(path)
		except Exception:
			print("De .mp3 is succesvol gemaakt, maar de .mp4/video is niet automatisch verwijderd. Dit is geen probleem en komt niet door mij, maar door Windows :). U kunt de .mp4/video gerust zelf verwijderen.")
			pass

Youtube_DL(arguments[1], arguments[2])
# Youtube_DL("https://www.youtube.com/watch?v=YNVMdd6zMUE", "ja")
