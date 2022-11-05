import os
import pydub
import glob
import shutil
from colorama import Back, Fore, Style, deinit, init


#you can select the file type you have and comment out the rest.
mkv_files = glob.glob('./*.mkv')
webm_files = glob.glob('./*.webm')
wav_files = glob.glob('./*.wav')
m4a_files = glob.glob('./*.m4a')
flac_files = glob.glob('./*.flac')
mp4_files = glob.glob('./*.mp4')

all_files = [mkv_files,webm_files,wav_files,m4a_files,flac_files,mp4_files]

for files in all_files:
    for file in files:
        mp3_file = os.path.splitext(file)[0] + '.mp3'
        sound = pydub.AudioSegment.from_file(file)
        print(Fore.GREEN + "Conversion en cours de la piste : ",file)
        sound.export(mp3_file, format="mp3")
        os.remove(file)
        print(Fore.GREEN + "Nombre de pistes converties : ",len(files))