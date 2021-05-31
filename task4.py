#Task4 by Krzysztof Jankowski
import argparse
import os
import time
from matplotlib import pyplot as plt
from matplotlib import colors as mc
parser=argparse.ArgumentParser()
parser.add_argument("-v","--verbose",help="Turn on verbosity",action="store_true")
parser.add_argument("directories",help="Directories to analize", nargs="+")
args=parser.parse_args()

months=[x for x in range (1,13)]
counter=[0 for x in range (1,13)]
if args.verbose: print("Starting procedure...")
for i in args.directories:
    if args.verbose: print("Current listing directory: ",i)
    for path_, dirname,fname in os.walk(i):
        for name in fname:
            s=os.path.join(path_,name)
            buff=(int(time.strftime("%m",time.localtime(os.path.getmtime(s)))))
            counter[buff-1]+=1
if args.verbose: print("Finished\nStoring data to chart...")
time.sleep(1)
cmap = mc.LinearSegmentedColormap.from_list("", ["red", "yellow", "green"])
plt.barh(months,counter,tick_label=months,color=cmap(counter))
plt.xlabel("Total amount of changes")
plt.ylabel("Mounths")
plt.title("Statistics of modifications")
plt.show()
if args.verbose: print("Done!")