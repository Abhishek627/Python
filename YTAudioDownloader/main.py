from __future__ import unicode_literals

"""
youtube_dl is a command-line program to download videos
from YouTube.com. It requires the Python 2.6, 2.7, or 3.2+,
and it is not platform specific.
It should work on  Unix, Windows or macOS.
"""

import youtube_dl


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

"""
This program takes input as a list of all youtube links.
and Downloads the audio for those youtube videos in the 
working directory.
""""

# add all the youtube whose audio is to be downloaded links in the list below
links = []
for i in links:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([i])
