import pyttsx3  #pip install pyttsx3
#for installing the following library first download git or just download the birary from git using the link bellow
from pytube import YouTube   #pip install git+https://github.com/get-pytube/pytube3.git
from pytube.cli import on_progress as progress
import os
import urllib
from bs4 import BeautifulSoup
import time

engine = pyttsx3.init('sapi5')          #initialising the engine for audio output
voices = engine.getProperty('voices')

def say(audio,female=1,rate='180'):
    rate=int(rate)
    engine.setProperty('voice', voices[female].id)
    engine.setProperty('rate', rate)
    engine.say(audio)
    engine.runAndWait()

def open_it(path):
    if os.path.exists(path):
        os.system(f'start "" "{path}"')
    else:
        print("path dosn't exists".title())
        say('path dosn\'t exist')

def quality(qual):    
    qual = str(qual)
    qualities = {'mp3':'mp3',
         '144':'144',
         '240':'240',
         '360':'360',
         '480':'480',
         '720':'720',
         '1080':'1080'}
    for q in qualities:
        q=str(q)
        if q in qual:
            return qualities[q]
    return qualities['mp3']

def get_size(bytes, suffix="B"):
    bytes = float(bytes)
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def download_video(link,qual='360',path=None):
    if path == None:
        path = os.getcwd()
    yt = YouTube(link,on_progress_callback = progress)
    video = yt.streams
    do_it = False
    for v in  video:

        if 'mp3' not in qual:
            if 'mp4' in str(v) and str(qual) in str(v):
                do_it = True
                break
        else:
            if 'audio' in str(v) and '160' in str(v):
                do_it = True
                break
    
    video = v
    if do_it:
        size = get_size(video.filesize)
        name = video.title
        print(f'Path : {path}\nName : {name}\nSize : {size}')
        return video.download(path)
    else:
        if qual != '360' and qual !='mp3':
            download_video(link,'360',path)
        else:
            return False

def get_link_from_name(search):
    URL = 'https://www.youtube.com/results?search_query='
    say("getting the link for the file")
    searchQuery = '+' + search.replace('  ',' ').replace(' ','+')
    searchURL = URL + searchQuery
    response = urllib.request.urlopen(searchURL)
    soup = BeautifulSoup(response, 'html.parser')
    vidID = soup.body.find_all()
    links=[]
    for i in vidID:
        i=str(i)
        if '/watch?v=' in str(i):
            x=i.split('"')
            for a in x: 
                if '/watch?v='in a:
                    links.append(str(a))
                    break
            break
    vidID=str(links[0].strip())
    return 'https://www.youtube.com' + vidID

def convert_to_mp3(File,Typ = 'audio'):
    file = File
    typ = Typ.lower()
    say("Importing the convertor")
    import moviepy.editor as edit
    say("initialising the conversion")
    ext = file.split('.')[-1]
    new_file = file.replace('\\','/').replace(f'.{ext}','.mp3')
      
    try:
        if 'audio' not in typ:
            video = edit.VideoFileClip(file)
            audio = video.audio
            audio.write_audiofile(new_file)
            audio.close()
            video.close()
        else:
            audio = edit.AudioFileClip(file)
            audio.write_audiofile(new_file)
            audio.close()
        return new_file
            
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    name = input("enter the name/url of the video : ".title())
    qual = quality(input("enter the quality in which you want to download the video : ".title()))
    path = input("enter the path where you want to save the file : ".title())
    if 'http' not in name.lower():
        name = get_link_from_name(name)

    if path.strip() == '':
        path = None
    
    path = download_video(name,qual,path)
    if qual == 'mp3':
        p2 = path
        path = convert_to_mp3(path)
        os.remove(p2)
    print(f"File : {path}")
    print("downloaded!!!".title())
    say('downloaded')
    print("opening the the downloaded file".title())
    say("opening the file")
    open_it(path)
