#!/usr/bin/env python
"""
Zaprojektuj i przeprowadź eksperyment porównujący wydajność listy jednokierunkowej i listy wbudowanej w Pythona.
"""
import time
import L4_ZAD5 as uL
import sys


def timer(func, tests, l):
    t_stamp = time.time()
    func(tests, l)
    return time.time() - t_stamp

def add_beg_test1(tests, l):
    for i in range(tests):
       l.add(i)
    
def add_beg_test2(tests, l):
    for i in range(tests):
        l.insert(0,i)

def add_end_test(tests, l):
    for i in range(tests):
        l.append(i)

def remove_beg(tests, l):
    for i in range(tests):
        l.pop(0)

def remove_end(tests, l):
    for i in range(tests):
        l.pop()

def index_test(tests, l):
    for i in range(tests):
        l.index(i)

def main(tests = 5000):
    ul1 = uL.UnorderedList()
    l1 = []
    times_ul = []
    times_ul.append(timer(add_beg_test1, tests, ul1))
    times_ul.append(timer(add_end_test, tests, ul1))
    times_ul.append(timer(remove_beg, tests, ul1))
    times_ul.append(timer(index_test, tests, ul1))
    times_ul.append(timer(remove_end, tests, ul1))

    times_l = []
    times_l.append(timer(add_beg_test2, tests, l1))
    times_l.append(timer(add_end_test, tests, l1))
    times_l.append(timer(remove_beg, tests, l1))
    times_l.append(timer(index_test, tests, l1))
    times_l.append(timer(remove_end, tests, l1))

    if sum(times_l) < sum(times_ul):
        winner = "List"
    else:
        winner = "Unordered list"


    print("Adding {} elements at beggining: {} for {}".format(tests, times_ul[0], "Unordered list"))
    print("Adding {} elements at beggining: {} for {}".format(tests, times_l[0], "list"))
    print("Adding {} elements at end: {} for {}".format(tests, times_ul[1], "Unordered list"))
    print("Adding {} elements at end: {} for {}".format(tests, times_l[1], "list"))
    print("Removing {} elements at beggining: {} for {}".format(tests,  times_ul[2], "Unprdered list"))
    print("Removing {} elements at beggining: {} for {}".format(tests, times_l[2], "list"))
    print("Checking indices of following {} elements: {} for {}".format(tests,  times_ul[3], "Unordered list"))
    print("Checking indices of following {} elements: {} for {}".format(tests, times_l[3], "list"))
    print("Removing {} elements at end: {} for {}".format(tests, times_ul[4], "Unordered list"))
    print("Removing {} elements at end: {} for {}".format(tests, times_l[4], "list"))
    print("-" * 10)
    print("Total operation times:\nUnordered list: {}\nList: {}\nWinner is {}".format(sum(times_ul), sum(times_l), winner))
    print("\n" + "=" * 10)
if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        for i in sys.argv[1:]:
            try:
                main(int(i))
            except:
                raise TypeError