from pytube import YouTube
from sys import argv as arguments

def Youtube_DL(link):
    video = YouTube(link)
    stream = video.streams.get_highest_resolution()
    title = video.title
    
    print(f'Downloading "{title}"...')
    stream.download("videos")
    print(f'Downloaded "{title}"')

Youtube_DL(arguments[1])