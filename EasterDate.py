#Task1 by Krzysztof Jankowski
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("year",help="Chosen Easter year",type=int)
args=parser.parse_args()
a=args.year%19
b=args.year//100
c=args.year%100
d=b//4
e=b%4
f=(b+8)//25
g=(b-f+1)//3
h=(19*a+b-d-g+15)%30
i=c//4
j=c%4
k=(32+2*e+2*i-h-j)%7
l=(a+11*h+22*k)//451
m=(h+k-7*l+114)%31


day=m+1
month=(h+k-7*l+114)//31
print("Easter date:{}-{}-{}y.".format(day,month,args.year))