#Task2 by Krzysztof Jankowski
import argparse
import os
parser=argparse.ArgumentParser()
parser.add_argument("name",help="Picture's name")
parser.add_argument("width",help="Widht",type=int)
parser.add_argument("height",help="Height",type=int)
parser.add_argument("output_name",help="Name of the resized picture")
parser.add_argument("-v","--verbose",help="Turn on verbosity",action="store_true")

from PIL import Image
args=parser.parse_args()
if args.verbose: print("Starting procedure...")
if len(args.name.split("."))!=2:
    if args.verbose: print("No extension pass. Searching in supported extensions...")
    ext=['.jpg','.png','.jpeg','.bmp']
    term=False
    for i in ext:
        if os.path.isfile(args.name+i):
            im=Image.open(args.name+i)
            term=True
            if args.verbose: print("Extension founded. ",i)
            break
    if term==False:
        print("Not supported extension!")
        exit()
else:
    im=Image.open("{}".format(args.name))
if args.verbose: print("Scaling picture...")
im=im.resize((args.width,args.height))
im.save(args.output_name+".jpg")
if args.verbose: print("Done!")
