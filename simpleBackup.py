#Task3 by Krzysztof Jankowski
import argparse
from zipfile import ZipFile
import os
import time
parser=argparse.ArgumentParser()
parser.add_argument("-v","--verbose",help="Turn on verbosity",action="store_true")
parser.add_argument("directories",help="Directories to zip", nargs="+")
args=parser.parse_args()

def get_paths(dir):
    paths=[]
    for path_,dirname,fname in os.walk(dir):
        for filename in fname:
            paths.append(os.path.join(path_,filename))
    return paths

if args.verbose: print("Starting procedure...")
for i in args.directories:
    name=i.split("/")
    name=name[len(name)-1]
    if args.verbose: print("Currently zipping directory: ",name)
    filepaths=get_paths(i)
    with ZipFile(str(time.strftime("%Y_%m_%d",time.localtime(time.time())))+"backup_"+name,'w') as zip:
        for files in filepaths:
            zip.write(files)
    if args.verbose: print("Zipped!")
if args.verbose: print("Done!")