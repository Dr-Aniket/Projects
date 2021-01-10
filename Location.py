import pyttsx3  # pip install pyttsx3
import webbrowser as web    # pip install webbrowser
import requests
from bs4 import BeautifulSoup as bs # pip install beautifulsoup
import os
from time import time as ti
import time
from tkinter import Tk,Label
import threading as thread
  
def guiprint(txt, x=40, y=50,words_in_line=5, fg="white", bg = 'Black', destroy = True, new_window = True):
    global root 
    global answer

    if destroy:
        try:
            answer.destroy()
        except:
            pass
    if new_window:
        try:
            root.destroy()
        except:
            pass
        root=Tk()
        root.geometry("300x250")
        root['bg'] = 'black'
        root.title('Loaction Detail')
        root.resizable(0,0)
        root.attributes("-topmost", True)
        root.lift()

    txt = txt.split()
    t=''
    i=1
    for _ in txt:
        if i==words_in_line:
            _ += '\n'
            i=0
        t += ' ' + _
        i+=1
    txt=t.strip().title()
    
    answer = Label(root, text = txt,fg = fg, bg= bg)
    answer.configure(font=("Times New Roman", 12, "bold"))
    answer.pack()
    answer.place(x=x,y=y)


engine = pyttsx3.init('sapi5')          #initialising the engine for audio output
voices = engine.getProperty('voices')

def say(audio,female=1,rate='180'):
    rate=int(rate)

    engine.setProperty('voice', voices[female].id)
    engine.setProperty('rate', rate)
    engine.say(audio)
    engine.runAndWait()

def my_loaction():                                  
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    city = data['city']
    return city

def locations(start=None,end=None):
    if start == None:
            start = my_loaction()
            # input(start)
    if end == None:
        # say(f"showing {start} on map")
        link = "https://www.google.com/maps/place/" + start + "/amp;" 
        web.open(link)
        return {'status' : 'my_loc', 'location' : start}
    else:
        say(f"Finding the best route between {start} and {end}")
        try:
                link  = f'https://www.google.com/maps/dir/{start}/{end}/'
                page = requests.get(link)
                soup = bs(page.content, 'html.parser')
                f=open('data.txt','w')
                mdata = []
                for _ in str(soup).split('\\n'):
                    _ = str(_).strip()
                    if ' km' in _ or ' m' in _ or ' hr' in _ or ' min' in _ :
                        if '[' in _ and '"' in _:
                            f.write(_)
                    if 'meta content' in _.lower():
                        mdata.append(_)
                f.close()
                data = open('data.txt','r').readlines()
                os.remove('data.txt')
                x = [] 

                for _ in data:
                    _ = str(_)
                    if (' km' in _ and ' hr' in _) or (' m' in _ and ' min' in _) :
                        x.append(_)
                
                data = x[-1].split('\"')

                c = 0
                Data = []
                for  d in data:
                    if c==3:
                        break
                    if 'km' in d or 'hr' in d or ' m' in d or 'min' in d or 'nh' in d.lower():
                        Data.append(d[:-1])
                        c+=1
                route,distance,time = Data[0],Data[1],Data[2]
                time = time.split('hr')
                hour = time[0].strip()
                minute = time[1].split('min')[0]

                try:
                    if int(hour)>1:
                        hour = str(hour) + ' hours '
                    elif int(hour) == 1:
                        hour = str(hour) + ' hour '
                    else:
                        hour = ''
                except:
                    hour = ''
                try:
                    if int(minute.strip())>1:
                        minute = str(minute) + ' minutes '
                    elif int(minute) == 1:
                        minute = str(minute) + ' minute '
                    else:
                        minute = ''
                except:
                    minute = ''
                    
                if hour!='' and minute != '':
                    connect_time = 'and'
                else:
                    connect_time = ' '
                time = hour + connect_time + minute
                route = route.lower().replace('nh','National Highway ').upper()
                for m in str(mdata[0]).strip().lower().split('meta content='):
                    if start.lower() in m or end.lower() in m:
                        dest = m
                        break
                try:
                    dest = dest.split('"')[1]
                except:
                    dest = f'{start} to {end}'
                data ={'meta_data':dest,
                       'distance':distance,
                       'route':route,
                       'time':time,
                       'status':True
                    }
        except:
            data ={'meta_data': f'{start} to {end}',
                       'distance':'Null',
                       'route':'Null',
                       'time':'Null',
                       'status':False
                    }
        web.open(link)
        return data
    
if __name__ == "__main__":
    start_location = input('Enter the Start Location : ')
    end_location = input('Enter the End Location : ')

    if start_location == '':
        start_location=None
        
    if end_location == '':
        end_location=None
    start_time = ti()
    data = locations(start_location,end_location)
    if data != None:
        if data["status"] == True:
            if 'hr' in data['distance'].lower():
                cmd = f'The Shortest path from {data["meta_data"]} takes {data["time"]}'.title()
            else:
                cmd = f'The Shortest path from {data["meta_data"]} is {data["distance"]} in length from {data["route"]} and it takes {data["time"]}'.title()
        elif data['status'] == 'my_loc':
            cmd = f'showing {data["location"]} on the map'.title()
        else:
            cmd = f'THere is no direct route from {data["meta_data"]}'.title()
        x=50
        y=80
        if len(cmd.split()) > 13:
            x=35
            y=50
        guiprint(cmd,x=x,y=y,fg="cyan",bg="black",destroy=False,new_window=True)
        say(cmd)

    end_time = ti()
    time_taken = end_time-start_time
    time_taken = round(time_taken,2)
    try:
        guiprint(f'Time Taken For Execution : {time_taken}sec',x=50,y=180,fg="black",bg="white",destroy=False,new_window=False)
    except:
        guiprint(f'Time Taken For Execution : {time_taken}sec',x=50,y=180,fg="black",bg="white",destroy=False,new_window=True)
    root.mainloop()