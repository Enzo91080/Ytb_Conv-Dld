from tkinter import filedialog, Tk, Label, StringVar, Entry, Button, END
from sys import exit
import os
import youtube_dl
import time
import beepy


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


def download_mp3_playlist(playlist_url, destination_path):
    ydl_opts = {
        'ignoreerrors': True,
        'EmbedThumbnail': True,
        'format': 'bestaudio/best',
        'outtmpl': destination_path + '/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'FFmpegMetadata'},
        ],
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


def loadpath(entry):
    file_path = filedialog.askdirectory()
    entry.configure(state='normal')
    entry.delete(0, END)
    entry.insert(0, file_path)
    entry.configure(state='readonly')

def cancel(*_):
    exit()


window = Tk()
window.title("Youtube MP3 Playlist Downloader")
window.protocol("WM_DELETE_WINDOW", cancel)

label_url = Label(window, text='YT-playlist Link (or link to single YT-video): ', font="Arial 12", anchor="w")
label_destination = Label(window, text='Please select target destination folder: ', font="Arial 12", anchor="w")

label_url.grid(row=0, column=0, padx=5, pady=5, sticky='w')
label_destination.grid(row=2, column=0, padx=5, pady=5, sticky='w')

url = StringVar()
destination = StringVar()
t1 = Entry(window, textvariable=url, font="Arial 10", width=70)
t2 = Entry(window, textvariable=destination, font="Arial 10", width=70, bg='grey', state='readonly')
t1.grid(row=1, column=0, padx=5, pady=(0, 30), sticky='w')
t2.grid(row=3, column=0, padx=5, pady=(0, 30), sticky='w')

button1 = Button(text="Select Destination", command=lambda: loadpath(t2), font="Arial 12")
button1.grid(row=3, column=1, padx=5, pady=(0, 30), sticky='w')

button_ok = Button(text="Start", command=lambda: window.destroy(), fg='grey', state='disabled', font="Arial 12")


def toggle_state(*_):
    if url.get() and destination.get():
        button_ok['state'] = 'normal'
        button_ok['fg'] = 'black'
    else:
        button_ok['state'] = 'disabled'
        button_ok['fg'] = 'grey'

url.trace_add('write', toggle_state)
destination.trace_add('write', toggle_state)
button_cancel = Button(text="Cancel", command=lambda: cancel(), font="Arial 12")

button_ok.grid(row=4, column=2, padx=5, pady=(0, 30), sticky='w')
button_cancel.grid(row=4, column=3, padx=5, pady=(0, 30), sticky='w')

window.mainloop()

time.sleep(2)
download_mp3_playlist(url.get(), destination.get())
beepy.beep(1)

end_window = Tk()
end_window.title('Download finished!')

label_end = Label(end_window, text='Your playlist was downloaded successfully to the designated location.',
                  font="Arial 13")
label_end.grid(row=0, column=0, padx=10, pady=10)

button_finish = Button(text="Close", command=lambda: cancel(), font="Arial 13")
button_finish.grid(row=1, column=1, padx=5, pady=10)


def open_and_exit():
    os.system("start " + destination.get())
    exit()


button_finish = Button(text="Close and open folder", command=lambda: open_and_exit(), font="Arial 13")
button_finish.grid(row=1, column=2, padx=5, pady=10)

end_window.mainloop()
