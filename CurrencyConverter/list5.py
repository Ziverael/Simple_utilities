#!/usr/bin/env python

import tkinter as tk
import requests
from  bs4 import BeautifulSoup as bsp
import os 
import sys


###DOWNLOAD DATA###
try:
    req=requests.get("https://www.nbp.pl/home.aspx?f=/kursy/kursya.html")

    ###CREATE TABLE###
    currency=[]
    soup=bsp(req.content,'html.parser')

    soup=soup.find('div', id="contentholder")
    for i in soup.findAll('tr'):
        buff=[]
        for j in i.findAll('td'):
            buff.append(j.get_text())
        currency.append(buff)
    if len(currency[0])==0:
        currency.pop(0)#There is one empty element

    ##ADD ZLOTY###
    currency.append(["złoty", "1 ZŁ", "1,0000"])
    ###SAVE TABLE###
    with open("currency.txt","w") as f:
        for i in currency:
            for j in i:
                f.write(j)
                f.write("_")
            f.write("+")

###READ DATA FROM FILE IF OFFLINE###
except:
    
    if not os.path.isfile("currency.txt"):
        sys.stderr.write("No data!")
        sys.exit(1)
    with open("currency.txt") as f:
        currency=f.read()
        currency=currency.split("+")
        for i in range(len(currency)):
            currency[i]=currency[i].split("_")
        currency.pop(-1)

###FUNCTIONS###
def counter():

    ###GET RATE###
    x=(text1.get(),text2.get())
    if x[0]=="FROM" or x[1]=="TO":
        sys.stderr.write("No currency chosen!")
        return
    
    tocount=[]
    for i in x:
        for j in range(0,len(currency)):
            if i==currency[j][0]:
                tocount.append(currency[j][2])
    
    try:
        tocount=[float(tocount[i].split(',')[0]+'.'+tocount[i].split(',')[1]) for i in range(0,2)]
    except ValueError:
        sys.stderr.write("Database is broken!")
    
    ###READ AMOUNT###
    try:
        amount=float(accnt.get())
    except ValueError:
        sys.stderr.write("Invalid input!")
        return
    
    ###COMPUTE###
    total.set(str(round(tocount[0]/tocount[1]*amount,2)))


def entry_clear(butt):
    accnt.delete(0,tk.END)

def selectfr(butt):
    name=fromc.get(tk.ACTIVE)
    text1.set(name)

def selectto(butt):
    name=toc.get(tk.ACTIVE)
    text2.set(name)


###WINDOW SETTINGS###
root=tk.Tk()
root.title("Exchange")
root.geometry("500x350")
root.resizable(width=0,height=0)


###LOAD TEXTURES###
imbg=tk.PhotoImage(file=r"./bg.png")

###SET CANVAS###
bg=tk.Canvas(root,width=500,height=350)
bg.pack(fill="both",expand=True)
bg.create_image(0,0,image=imbg,anchor="nw")

###VARIABLES###
text1=tk.StringVar(root)
text2=tk.StringVar(root)
total=tk.StringVar(root)

text1.set("FROM")
text2.set("TO")
total.set("")

wid=25
wid2=20
hei=2
###BUTTONS###
ex=tk.Button(root, text="Exit",command=sys.exit,
width=wid2,height=hei,anchor='center',
bg='black',fg='white',activebackground='white',activeforeground='black')
count_=tk.Button(root,text="Count",command=counter,
width=wid2,height=hei,anchor='center',
bg='black',fg='white',activebackground='white',activeforeground='black')

###ENTRY###
accnt=tk.Entry(root,font=('Arial',13),width=20,fg='white',bd=0,bg='black')
accnt.insert(0,"ACCOUNT")
accnt.bind("<Button-1>",entry_clear)

###LISTBOX###

fromc=tk.Listbox(root,width=30,fg='white',bd=0)
toc=tk.Listbox(root,width=30,fg='white',bd=0)

for i in currency:
    fromc.insert(tk.END,i[0])
    toc.insert(tk.END,i[0])

fromc.insert(tk.END)
fromc.bind("<Button-1>",selectfr)
toc.bind("<Button-1>",selectto)


###LABELS###
fromcname=tk.Label(textvariable=text1,bg='black',fg='white',width=wid)
tocname=tk.Label(textvariable=text2,bg='black',fg='white',width=wid)
totall=tk.Label(textvariable=total,bg='black',fg='white',width=wid)

###SET IN CANVAS###
bg.create_window(50,16, anchor='nw', window=accnt)
bg.create_window(160,300, anchor='nw', window=ex)
bg.create_window(160,40, anchor='nw', window=count_)
bg.create_window(50,100+16,anchor='nw',window=fromc)
bg.create_window(250,100+16,anchor='nw',window=toc)
bg.create_window(50,70+16,anchor='nw',window=fromcname)
bg.create_window(250,70+16,anchor='nw',window=tocname)
bg.create_window(250,16,anchor='nw',window=totall)


root.mainloop()