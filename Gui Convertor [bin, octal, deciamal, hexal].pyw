from tkinter import*
from functools import partial
import pyautogui as pg

root=Tk()
root.geometry("300x250")
root['bg'] = 'black'
root.title('converter')
root.resizable(0,0)
OPTIONS = [
"Decimal",
"Binary",
"Octal",
"Hexa-Decimal"
]
variable = StringVar(root)
variable.set(OPTIONS[0])

def print_in_tk(txt,x=80,y=185,typ="button",bg="white"):
    if typ=="button":
        answer=Button(root,text=txt,fg="Black",bg="white")
    else:
        answer=Label(root,text=txt)
    answer.pack()
    answer.place(bordermode=INSIDE,x=x,y=y,height=20,width=150)

def got():
    t = str(variable.get()).lower()
    if 'binary' in t:
        t = 2
    elif 'oct' in t:
        t = 8
    elif 'hex' in t:
        t = 16
    else:
        t = 10
    number = str(entry.get()).strip()
    if  number == '':
        number = '0'
        t = 10
    try:
        decimal = int(number,t)
        print_in_tk('Converter',y=205)
        return decimal
    except:
        print_in_tk('Wrong Input',y=205)
        return 0

def tobin():
    dec = got()
    bnum=bin(dec)
    print_in_tk(f'In Binary : {bnum[2:]}')

def tohex():
    dec = got()
    hnum=hex(dec)
    print_in_tk(f'In Hexa-Decimal : {hnum[2:]}')
    
def tooct():
    dec = got()
    onum=oct(dec)
    print_in_tk(f'In Octa-Decimal : {onum[2:]}')

def todeci():
    dec = got()
    dnum=(dec)
    print_in_tk(f'In Decimal : {dnum}')

def typ(key):
    pg.typewrite([key])
 

def close():
    exit(0)

    
button1=Button(root,text="Bin",fg="Black",bg="White",command=tobin)
button2=Button(root,text="Oct",fg="Black",bg="White",command=tooct)
button3=Button(root,text="Hex",fg="Black",bg="White",command=tohex)
button4=Button(root,text="Dec",fg="Black",bg="White",command=todeci)

num1=Button(root,text="1",fg="Black",bg="White",command=partial(typ, '1'))
num2=Button(root,text="2",fg="Black",bg="White",command=partial(typ, '2'))
num3=Button(root,text="3",fg="Black",bg="White",command=partial(typ, '3'))
num4=Button(root,text="4",fg="Black",bg="White",command=partial(typ, '4'))
num5=Button(root,text="5",fg="Black",bg="White",command=partial(typ, '5'))
num6=Button(root,text="6",fg="Black",bg="White",command=partial(typ, '6'))
num7=Button(root,text="7",fg="Black",bg="White",command=partial(typ, '7'))
num8=Button(root,text="8",fg="Black",bg="White",command=partial(typ, '8'))
num9=Button(root,text="9",fg="Black",bg="White",command=partial(typ, '9'))
num0=Button(root,text="0",fg="Black",bg="White",command=partial(typ, '0'))
clear=Button(root,text="<-",fg="Black",bg="White",command=partial(typ, 'backspace'))
ok=Button(root,text="Exit",fg="Black",bg="White",command=close)
typ = OptionMenu(root, variable, *OPTIONS)
txt = Label(root, text="Input : ")
entry=Entry(root,bd=5)
entry.pack()

button1.pack()
button2.pack()
button3.pack()
button4.pack()

num1.pack()
num2.pack()
num3.pack()
num4.pack()
num5.pack()
num6.pack()
num7.pack()
num8.pack()
num9.pack()
ok.pack()
typ.pack()
txt.pack()
num0.pack()
clear.pack()


button1.place(bordermode=INSIDE,x=75,y=75,height=20,width=40)
button2.place(bordermode=INSIDE,x=75,y=95,height=20,width=40)
button3.place(bordermode=INSIDE,x=75,y=115,height=20,width=40)
button4.place(bordermode=INSIDE,x=75,y=135,height=20,width=40)

entry.place(bordermode=INSIDE,x=75,y=45,height=30,width=160)

num1.place(bordermode=INSIDE,x=115,y=75,height=20,width=40)
num2.place(bordermode=INSIDE,x=115,y=95,height=20,width=40)
num3.place(bordermode=INSIDE,x=115,y=115,height=20,widt=40)
num4.place(bordermode=INSIDE,x=155,y=75,height=20,width=40)
num5.place(bordermode=INSIDE,x=155,y=95,height=20,width=40)
num6.place(bordermode=INSIDE,x=155,y=115,height=20,width=40)
num7.place(bordermode=INSIDE,x=195,y=75,height=20,width=40)
num8.place(bordermode=INSIDE,x=195,y=95,height=20,width=40)
num9.place(bordermode=INSIDE,x=195,y=115,height=20,width=40)
num0.place(bordermode=INSIDE,x=155,y=135,height=20,width=40)
clear.place(bordermode=INSIDE,x=195,y=135,height=20,width=40)

typ.place(bordermode=INSIDE,x=115,y=160,height=20,width=120)
txt.place(bordermode=INSIDE,x=75,y=160,height=20,width=40)
ok.place(bordermode=INSIDE,x=115,y=135,height=20,width=40)

root.mainloop()
