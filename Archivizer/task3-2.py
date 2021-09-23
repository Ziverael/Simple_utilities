#!/usr/bin/env python
import argparse
import os
import sys
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from base64 import b64decode
from sys import stderr

###PARSER###
parser=argparse.ArgumentParser(prog="Unpacker",usage="%(prog)s archive",
description="Unpack archive with .acv extension",epilog="-------------------")
parser.add_argument("archive",help="Archieve to unpack",type=str)
parser.add_argument("-p","--password",help="Password of the archieve",type=str,nargs="?")
arg=parser.parse_args()

###FUNCTION###
def find_pattern(string,pat):
    j=0
    patBeg=0
    for i in range(len(string)):
        if string[i]==pat[j]:
            j+=1
            if j==len(pat):
                patEnd=i
                return patBeg,patEnd
        else:
            j=0
            patBeg=i+1
    return -1,-1


###CHECK INPUT TYPE###
if arg.archive.split(".")[-1]=="acv":
    inp1=arg.archive
    inp2=".consum"+arg.archive.split(".")[-2]
else:
    inp1=arg.archive+".acv"
    inp2=".consum"+arg.archive
#print(inp1,inp2)

###LOAD FILES###
if os.path.isfile(inp1) and os.path.isfile(inp2):
    with open(inp2,"rb") as f:
        consum=f.read()
    ###VARIABLES###
    it,it2=find_pattern(consum,b"#####")
    it2+=1
    treshold=[int(i) for i in consum[:it].decode("utf-8").split(" ") if i!='']
    if it!=-1:
        it3,it4=find_pattern(consum[it2:],b"#####")
        it3+=it2
        it4+=it2
        nonce=consum[it2:it3]
        key=consum[it4+1:]
        password=True
    else:
        password=False
    
    if password:
        if not arg.password:
            sys.stderr.write("You have no access to this file.")
            sys.exit(0)
        
   ###UNPACK TEXT###
    buff=[]
    with open(inp1,"rb") as inp:
        for i in treshold:  buff.append(inp.read(i))

    ###DECRYPTION###
    #print(buff,len(buff))
    text=[]
    if password:
        passwd=bytes(arg.password,"utf-8")
        chacha=ChaCha20Poly1305(key)
        for i in buff:
            try:
                text.append(chacha.decrypt(nonce,i,passwd).decode("utf-8"))
            except:
                stderr.write("Incorrect password!")
                exit(0)
    else:
        for i in buff:  text.append(b64decode(i).decode("utf-8"))
    #print(text)
    
    ###WRITE TO FILES###
    for i in range(0,len(buff)):
        with open("Text_file"+str(i)+".txt","w") as out:
           out.write(text[i])
else:
    print("No such archive")