import pyautogui as pg
import numpy as np
import time
import cv2 
import os
import pyaudio
import wave
import keyboard
import threading

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"
key = ''

p = pyaudio.PyAudio()

frames = []

def key_pressed():
    global key
    key = str(keyboard.read_key()).lower()

def record_audio(index=1):
    global key
    try:
        index = int(index)
        if index != 1 and index != 2:
            raise "index invalid: going for default"
    except:
        index=2
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK,input_device_index=index)
    
    for i in range(0, int(RATE / CHUNK *9999999)):
        data = stream.read(CHUNK)
        frames.append(data)
        try:
            if 'esc' in key:    
                break
        except:
            pass
        key = ''

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

dimensions =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

vid_typ = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def resolution(res):
    for d in dimensions:
        if res.lower() in str(d).lower():
            return dimensions[d]
    return dimensions['720p']    
        

while True:
    path = input("Enter the path : ")
    if path =='':
        path = os.getcwd()
    if os.path.exists(path):
        break
    else:
        print("please enter an valid path. or leave it blan for the curent path".title())
name = input("Enter the name of the file : ")
try:
    ext = name.split('.')[1]
except:
    ext = 'mp4'
    if name !='':
        name = name+'.mp4'
    else:
        import datetime
        dat = str(datetime.datetime.now()).replace(':','_')
        name = 'J. Records'+dat+'.mp4'
name = os.path.join(path,name)
fps = 6.5
fps = float(fps)
res = input("Enter the Resolution for The Video [Default : 1080]:")
if res == '':
    res = '1080'
res= resolution(res)
recording_audio = threading.Thread(target=record_audio,args=(input("Enter the 1 for external audio and 2 for internal : "),))
out = cv2.VideoWriter('video.mp4',vid_typ[ext],fps,res)


threading.Thread(target=key_pressed).start()
start = time.time()
recording_audio.start()
while True:
    frame = np.array(pg.screenshot())
    x,y,_ = frame.shape
    frame = cv2.resize(frame,res)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    out.write(frame)
    frame = cv2.resize(frame,(y//2,x//2))
    cv2.imshow(name.split('.')[0],frame)
    
    if 'esc' in key or cv2.waitKey(1) == 27:
        key='esc'
        break

end =  time.time()
out.release()
cv2.destroyAllWindows()


t = end - start
print(f'Time Taken : {round(t,2)}')
path = name

print("exporting...".title())
from moviepy.editor import * 
videoclip = VideoFileClip('video.mp4')
audioclip = AudioFileClip('audio.wav')

new_audioclip = CompositeAudioClip([audioclip])
videoclip.audio = new_audioclip
videoclip.write_videofile(path)
print('file exported'.title())

os.remove('video.mp4')
os.remove('audio.wav')
if os.system(f'start "" "{name}"') == 0:
    name = name.replace('/','\\').split('\\')[1]
    path = path.replace(name,'')
    print(f'Video Saved as {name} in {path} ')
else:
    print(f"Please Check the name you used for saving : {path}")


input("Enter to exit")
