import youtube_dl
import time


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    if d['status'] == 'downloading':
        print(d['filename'], d['_percent_str'], d['_eta_str'])


def download_mp3_playlist(playlist_url):
    ydl_opts = {
        'ignoreerrors': True,
        'writethumbnail': True,
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_mp3s/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'EmbedThumbnail'},
            {'key': 'FFmpegMetadata'},
        ],
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


url = ""
while not url:
    url = input("Please enter a link to a YT playlist: \n")

time.sleep(2)
download_mp3_playlist(url)
