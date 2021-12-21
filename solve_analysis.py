#!/usr/bin/env python
import numpy as np
from scipy import linalg, optimize
import time
import random
from sys import argv
import matplotlib.pyplot as plt
import math

def generate_equation_system(n : int) -> tuple:    
    a = np.asarray([tuple(random.randrange(-50,50) for _ in range(n)) for i in range(n)])
    while not linalg.det(a):
        a = np.asarray([tuple(random.randrange(-50,50) for _ in range(n)) for i in range(n)])
    b = np.asarray([random.randrange(-50,50) for _ in range(n)])
    return a, b
    
def solve_timer(probes : int, rank : int) -> float:
    times = np.ndarray(probes, dtype = float)
    for i in range(probes):
        system = generate_equation_system(rank)
        delta = time.time()
        x = linalg.solve(*system)
        delta = time.time() - delta
        times[i] = delta
    return np.average(times)


def plot_experiment(data : np.ndarray, length : int):
    plt.title("Solving system of equations")
    plt.xlabel("Number of coeficients")
    plt.scatter(np.arange(1, length + 1), data, label = 'Data')
    plt.ylabel("time [s]")


def plot_thesis(n : int, vals : np.ndarray) -> tuple:
    def func(x, a, b):
        return a * x + b
    
    xs = np.arange(1, n + 1)

    popt, pcov = optimize.curve_fit(func, xs, vals)
    plt.plot(xs, func(xs, *popt), 'r', label = 'Thesis')
    return popt

def double_thesis(l : np.ndarray):
    list_length = len(l)
    ts = [15]
    while 2 * ts[-1] < list_length:
        ts.append(2 * ts[-1])
    ratio = [l[ts[i]] / l[ts[i-1]] for i in range(1,len(ts))]
    index = []
    for i in ratio:
        try:
            index.append(math.log(i, 2))
        except:
            continue
    return index

def main(n : int, rank : int):
    l = np.ndarray(rank, dtype =float)
    for i in range(1, rank):

        l [i] = solve_timer(n, i)
    
    plot_experiment(l, rank)
    index = (double_thesis(l))
    print(index)
    a, b = plot_thesis(rank, l)
    plt.show()
    print("Test thesis")
    print('T(2000) = ', a * 2000 + b)
    print('Empirical data ', end = "")
    matrix_a, matrix_b = generate_equation_system(2000)
    delta = time.time()
    linalg.solve(matrix_a, matrix_b)
    delta = time.time() - delta
    print(delta)

if __name__ == "__main__":
    if len(argv) == 3:
        try:
            n = int(argv[1])
            r = int(argv[2])
        except:
            print("Invalid data passed")
        main(n, r)
        
    else:
        main(100, 10)
    