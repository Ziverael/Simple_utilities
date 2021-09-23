#!/usr/bin/env python

import argparse
import os
from sys import exit
from sys import stderr
from re import findall
from random import randint
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from base64 import b64encode

###PARSING###
parser=argparse.ArgumentParser(prog="Squeezer",usage="%(prog)s text_file1 [text_file2 ... text_filen] archive",
description="Pack text files to archive",epilog="-------------------")
parser.add_argument("-v","--verbose",help="Turn on verbosity", action="store_true")
parser.add_argument("-p","--password",help="Set password", nargs="?")
parser.add_argument("files",help="Text files",nargs="+")
parser.add_argument("archive",help="Output archive name")

args=parser.parse_args()

###VARIABLES###
buff=[]
it=0
consum=""
if args.password:
    password=bytes(args.password,"utf-8")

###READING###
if args.verbose:  print("Reading files...")
for i in args.files:
    if not os.path.isfile(i):
        stderr.write("No such text file: {} ".format(i))
        continue 
    if args.verbose:    print("Writing {}...".format(i))
    with open(i,"r") as f:
        try:
            buff.append(f.read())
        except UnicodeDecodeError:
            stderr.write("No support for Unicode characters")
            exit(1)
        #nlines=len(findall(r'\n',buff[it]))
        #print(nlines)
        #consum+=str(f.tell()-nlines)+" "
        #it+=1


###CLOSE IF INVALID DATA###
if buff=="":
    if args.verbose:  print("Passed data are invalid!")
    exit(1)

###STORE DATA###
with open(args.archive+".acv","wb") as out:
    if(args.password):
        key=ChaCha20Poly1305.generate_key()
        chacha=ChaCha20Poly1305(key)
        nonce=os.urandom(12)
        for i in buff:
            i=bytes(i,"utf-8")
            i=chacha.encrypt(nonce,i,password)
            consum+=str(len(i))+" "
            out.write(i)
    else:
        for i in buff:
            i=b64encode(bytes(i,"utf-8"))
            consum+=str(len(i))+" "
            out.write(i)
    if args.verbose:  print("Files deployed in ",args.archive)

###CONTROL SUM TO UNPACH ARCHIVE###
with open(".consum"+args.archive,"wb") as f:
    consum=bytes(consum,"utf-8")
    f.write(consum)
    if(args.password):
        f.write(b"#####"+nonce)
        f.write(b"#####"+key)