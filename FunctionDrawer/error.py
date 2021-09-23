#!/usr/bin/env python

import argparse
import tkinter as tk

#Legend#
#1- empty input
#2- invalid arguments
#3- invalid 

###GET ERROR###
root=tk.Tk()
root.title("Error")
#root.geometry("150x100")
parser=argparse.ArgumentParser()
parser.add_argument("wht",help="Which error",type=int)
parser.add_argument("dtl",help="Detail of error",type=str, nargs="+")
args=parser.parse_args()

more=""
for i in args.dtl:
    more+=i+" "

if args.wht==1:
    txt="Input is empty!"
elif args.wht==2:
    txt="Invalid input!"

else:
    txt=""
message=tk.Label(text=txt)
message.pack() 
details=tk.Label(text=more)
details.pack()
root.mainloop()