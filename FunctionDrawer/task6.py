#!/usr/bin/env python
"""Create a window application for drawing plots on the canvas of passed functions.
Following function are adding to the canvas. Pass next function after clearing entry
or pass few functions separated by semicolons.

As default functions are drawing in the Cartesian coordinate system on interval [-10, 10]
and bordered on Y axis by -10 and 10.

User may change both intervals by passing two numbers separated by comma. User may change
labels of both axis and plot.

There are supplemented buttons for passing elemental operators and functions at the end
of the formula entry. 

As variable pass x. Formula should fits evaluations in the sympy module. However * 
symbol may be omitted beetwen number and variable. Also user may insert ^ as power, comma 
as decimal separatot and || as absolute value. Supported math functions:
sin, csc, cos, sec, tan, cot, asin, acsc, acos, atan, acot, ceiling, floor, frac, exp, sqrt,
log, Abs.


Draw plots on canvas by pressing Draw button or Enter.
Exit program by pressing Exit button or Esc.
Hide/show legend for functions from entry by pressing Check button.
Delete all plots from canvas by pressing Clear canvas button.

Return errors in separated window as message.

"""

import tkinter as tk
from sys import exit
from os import system
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import sympify,Symbol,N,SympifyError
import numpy as np

###WINDOW SETTINGS###
root=tk.Tk()
root.geometry("1000x600")
root.title("Function Viewer")

###LOAD TEXTURES###
bg=tk.PhotoImage(file=r"./bg.png")

###SET WINDOW###
pan1=tk.PanedWindow(root,bd=2,bg="white")
pan1.pack(fill=tk.BOTH,expand=True)

bg_pan=tk.Canvas(pan1,width=250,height=600)
bg_pan.create_image(0,0,image=bg,anchor="nw")
bg_pan.pack(fill=tk.BOTH, expand=True)
pan1.add(bg_pan)


pan2=tk.PanedWindow(pan1,bd=2,relief="raised")
pan1.add(pan2)


###VARIABLES###
formula=tk.StringVar(root)
x_range=tk.StringVar(root)
y_range=tk.StringVar(root)
plot_title=tk.StringVar(root)
x_label=tk.StringVar(root)
y_label=tk.StringVar(root)
x=Symbol('x')
prec=500
showLegend=tk.IntVar(root)
showLegend.set(1)
supportedfunc=['sin', 'csc', 'cos', 'sec', 'tan', 'cot', 'asin', 'acsc', 'acos',
'atan', 'acot', 'ceiling','floor','frac','exp','sqrt','log','Abs']

fig = Figure( dpi=100)
ax=fig.add_subplot(111)
canv = FigureCanvasTkAgg(fig, master=pan2)

###PLOT###
canv.draw()
canv.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

###FUNCTIONS###
def draw(event):
    """Draw plots of the given functions on given inetrval and bounded by given values.

    Get formula from main entry. Substitute comma for dot, |x| for Abs(x), ctan(x) for cot(x).
    If passed in formula curly or square bracket substitute for parenthesis. If passed variable
    is surronded by numbers put multiply operator. Check if finally formula is valid and compute
    its value for set interval. Draw plot and print on canvas.

    Parameters
    ----------
    event: event
        Enter key or Button draw for activation.

    Raises
    ------
    ValueError
        Cannot sympify formula.
        Missed brackets

    Errors
    ------
    Insert value to every input.
    Invalid number of brackets.
    Invalid function passed.
    Missing operators beetwen functions.
    No argument passed to function.
    Ranges should be past in form X Y.
    Right border of the interval should be greater than left.
    Values should be floating points or integers.

    """
    ###GET VALUE###
    formula.set(mainentr.get())
    x_range.set(xrang.get())
    y_range.set(yrang.get())
    plot_title.set(plttitle.get())
    x_label.set(pltxlable.get())
    y_label.set(pltylable.get())
    ###CHECK INPUTS###
    functions=formula.get().split(";")
    for k in functions:
        buff=k
        borders=[x_range.get(),y_range.get()]

        if not (len(buff) and len(borders[0]) and len(borders[1])):
            system("python error.py 1 Insert value to every input.")
            return

        ###COUNT BRACKETS###
        if len(re.findall('\(',buff))-len(re.findall('\)',buff)):
            system("python error.py 2 Invalid number of brackets.")
            return
  

        ###NORMALIZE BRACKETS###
        buff=re.sub('\[','(',buff)
        buff=re.sub('\]',')',buff)
        buff=re.sub('\{','(',buff)
        buff=re.sub('\}',')',buff)

        ###NORMALIZE DECIMAL SEPARATOR###
        buff=re.sub('\,','.',buff)
        

        ###NORMALIZE CTAN###
        buff=re.sub("ctan","cot",buff)

        ###TRY TO FIX MINOR ERRORS###
        litterals=re.findall("[a-zA-Z]+",buff)
        chars=re.findall("\W",buff)
        litt_pos=[i.span() for i in re.finditer("[a-zA-Z]+",buff)]

        ###CHECK IF PASSED CORRECT FUNCTION###
        err=True
        settimes=0

        for i in range(0,len(litterals)):
            err=True
            for j in supportedfunc:
                if litterals[i]==j:
                    err=False
                    break
                elif litterals[i]=="x":
                    err=False
                    ###CHECK IF 2x PASSED###
                    if litt_pos[i][0]:
                        if ord(buff[litt_pos[i][0]-1+settimes])>=48 and ord(buff[litt_pos[i][0]-1+settimes])<=57:
                            buff=buff[:litt_pos[i][0]+settimes]+"*"+buff[litt_pos[i][0]+settimes:]
                            settimes+=1

                    if litt_pos[i][1]+settimes<len(buff):
                        if ord(buff[litt_pos[i][1]+settimes])>=48 and ord(buff[litt_pos[i][1]+settimes])<=57:
                            buff=buff[:litt_pos[i][1]+settimes]+"*"+buff[litt_pos[i][1]+settimes:]
                            settimes+=1
                    break        
            if err:
                system("python error.py 2 Invalid function passed.")
                return

        ###SWAP INCORECT OPERATORS###    
        buff=re.sub("\^","**",buff)
        buff=re.sub("\,","\.",buff)

        settimes=0
        numb=0
        for i in re.finditer('\|',buff):
            numb+=1
            if numb%2:
                buff=buff[:i.span()[0]+settimes]+"Abs("+buff[i.span()[1]+settimes:]
                settimes+=3
            else:
                buff=buff[:i.span()[0]+settimes]+")"+buff[i.span()[1]+settimes:]
        ###CHECK NUMBER OF | SINGS###
        if numb%2:
            system("python error.py 2 Invalid number of brackets.")
            return

        try:
            buff=sympify(buff)
        except ValueError:
            system("python error.py 2 Missing operators beetwen functions.")
            return

        ###PREPARE RANGES###
        for i in range(0,2):
            borders[i]=borders[i].split(" ")
            if len(borders[i])!=2:
                system("python error.py 2 Ranges should be past in form X Y.")
                return
            for j in range(0,2):
                try:
                    borders[i][j]=float(borders[i][j])
                except:
                    system("python error.py 2 Values should be floating points or integers.")
                    return
            if borders[i][0]>=borders[i][1]:
                    system("python error.py 2 Right border of the interval should be greater than left.")
                    return    

        rgx=np.linspace(borders[0][0],borders[0][1], num=prec, endpoint=True)

        ###CHECK IF FUNCTION WORKS###
        try:
            N(buff.subs(x,rgx[0]))
        except ValueError:
            system("python error.py 2 No argument passed to function.")
        ###CALCULATE VALUES###
        vals=np.zeros(prec)
        indic=-1
        for i in rgx:
            evaled=N(buff.subs(x,i))
            indic+=1
            if not evaled.is_real:
                vals[indic]=None
                continue
            vals[indic]=float(evaled)

        ###PASS###
        ax.plot(rgx, vals,label=k)
        if showLegend.get():   ax.legend()
        ax.set_title(plot_title.get())
        ax.set_xlabel(x_label.get())
        ax.set_ylabel(y_label.get())
        ax.set(ylim=(borders[1][0],borders[1][1]))
        canv.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canv.draw() 

    
def clearCanvas():
    """Delete all charts and legend if exist from the canvas. If canvas are already clear do nothing."""
    ax.clear()
    canv.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canv.draw()

    

def check():
    """Show or hide the legend dependly of the fact if already legend is shown."""
    showLegend.set((1+showLegend.get())%2)
    ax.clear()
    canv.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canv.draw()
    draw('<Button-1>')

###FUNCTIONS: MATH###
def psin():
    """Pass sin(x) on to the formula entry."""
    mainentr.insert(tk.END,"sin(x)")

def pcos():
    """Pass cos(x) on to the formula entry."""
    mainentr.insert(tk.END,"cos(x)")

def ptan():
    """Pass tan(x) on to the formula entry."""
    mainentr.insert(tk.END,"tan(x)")

def pctan():
    """Pass ctan(x) on to the formula entry."""
    mainentr.insert(tk.END,"ctan(x)")

def pexp():
    """Pass exp(x) on to the formula entry."""
    mainentr.insert(tk.END,"exp(x)")

def plog():
    """Pass log(x) on to the formula entry."""
    mainentr.insert(tk.END,"log(x)")

def pAbs():
    """Pass |x| on to the formula entry."""
    mainentr.insert(tk.END,"|x|")

def psqrt():
    """Pass sqrt(x) on to the formula entry."""
    mainentr.insert(tk.END,"sqrt(x)")

def pleft():
    """Pass ( on to the formula entry."""
    mainentr.insert(tk.END,"(")

def pright():
    """Pass ) on to the formula entry."""
    mainentr.insert(tk.END,")")

def pmul():
    """Pass * on to the formula entry."""
    mainentr.insert(tk.END,"*")

def pdiv():
    """Pass / on to the formula entry."""
    mainentr.insert(tk.END,"/")

def pplus():
    """Pass + on to the formula entry."""
    mainentr.insert(tk.END,"+")

def pminus():
    """Pass - on to the formula entry."""
    mainentr.insert(tk.END,"-")

###BUTTON PRESS INTERACTION###
root.bind("<Return>",draw)
root.bind("<Escape>",exit)


###BUTTONS###
exi=tk.Button(root,text="Exit",command=exit)
drw=tk.Button(root,text="Draw")
drw.bind("<Button-1>",draw)
clr=tk.Button(root,text="Clear canvas",command=clearCanvas)
chk=tk.Button(root,text="Check button",command=check)

bsin=tk.Button(root,text="sin",width=4,height=1,command=psin)
bcos=tk.Button(root,text="cos",width=4,height=1,command=pcos)
btan=tk.Button(root,text="tan",width=4,height=1,command=ptan)
bctan=tk.Button(root,text="ctan",width=4,height=1,command=pctan)
bexp=tk.Button(root,text="exp",width=4,height=1,command=pexp)
blog=tk.Button(root,text="log",width=4,height=1,command=plog)
bAbs=tk.Button(root,text="| |",width=4,height=1,command=pAbs)
bsqrt=tk.Button(root,text="sqrt",width=4,height=1,command=psqrt)
bleft=tk.Button(root,text="(",width=2,height=1,command=pleft)
bright=tk.Button(root,text=")",width=2,height=1,command=pright)
bmul=tk.Button(root,text="*",width=2,height=1,command=pmul)
bdiv=tk.Button(root,text="/",width=2,height=1,command=pdiv)
bplus=tk.Button(root,text="+",width=2,height=1,command=pplus)
bminus=tk.Button(root,text="-",width=2,height=1,command=pminus)

###ENTRY###
mainentr=tk.Entry(root,font=('Arial',8),width=40,bd=0,bg="white",fg="black")
xrang=tk.Entry(root,font=('Arial',8),width=15,bd=0,bg="white",fg="black")
yrang=tk.Entry(root,font=('Arial',8),width=15,bd=0,bg="white",fg="black")
plttitle=tk.Entry(root,font=('Arial',8),width=40,bd=0,bg="white",fg="black")
pltxlable=tk.Entry(root,font=('Arial',8),width=18,bd=0,bg="white",fg="black")
pltylable=tk.Entry(root,font=('Arial',8),width=18,bd=0,bg="white",fg="black")

pltylable.insert(0,"y")
pltxlable.insert(0,"x")
plttitle.insert(0,"Plot")

xrang.insert(0,"-10 10")
yrang.insert(0,"-10 10")

###LABELS###
interv=tk.Label(text="Interval")
ybound=tk.Label(text="Y boudaries")
name_=tk.Label(text="Plot name")
namex=tk.Label(text="x axis label")
namey=tk.Label(text="y axis label")


###SET IN CANVAS###
bg_pan.create_window(5,10, anchor='nw',window=mainentr)
bg_pan.create_window(5,50, anchor='nw',window=xrang)
bg_pan.create_window(105,50, anchor='nw',window=yrang)
bg_pan.create_window(5,90, anchor='nw',window=plttitle)
bg_pan.create_window(5,140, anchor='nw',window=pltxlable)
bg_pan.create_window(125,140, anchor='nw',window=pltylable)

bg_pan.create_window(5,28, anchor='nw',window=interv)
bg_pan.create_window(105,28, anchor='nw',window=ybound)
bg_pan.create_window(5,68, anchor='nw',window=name_)
bg_pan.create_window(5,115, anchor='nw',window=namex)
bg_pan.create_window(125,115, anchor='nw',window=namey)


bg_pan.create_window(5,500, anchor='nw',window=drw)
bg_pan.create_window(105,500, anchor='nw',window=chk)
bg_pan.create_window(5,550, anchor='nw',window=exi)
bg_pan.create_window(105,550, anchor='nw',window=clr)


bg_pan.create_window(5,200, anchor='nw',window=bsin)
bg_pan.create_window(55,200, anchor='nw',window=bcos)
bg_pan.create_window(105,200, anchor='nw',window=btan)
bg_pan.create_window(155,200, anchor='nw',window=bctan)

bg_pan.create_window(5,240, anchor='nw',window=bAbs)
bg_pan.create_window(55,240, anchor='nw',window=bsqrt)
bg_pan.create_window(105,240, anchor='nw',window=blog)
bg_pan.create_window(155,240, anchor='nw',window=bexp)

bg_pan.create_window(5,280, anchor='nw',window=bplus)
bg_pan.create_window(40,280, anchor='nw',window=bminus)
bg_pan.create_window(75,280, anchor='nw',window=bdiv)
bg_pan.create_window(110,280, anchor='nw',window=bmul)
bg_pan.create_window(145,280, anchor='nw',window=bleft)
bg_pan.create_window(180,280, anchor='nw',window=bright)

###RUN WINDOW###
root.mainloop()