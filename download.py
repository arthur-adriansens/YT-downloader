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

		os.remove(path)

Youtube_DL(arguments[1], arguments[2])
# Youtube_DL("https://www.youtube.com/watch?v=YNVMdd6zMUE", "ja")
