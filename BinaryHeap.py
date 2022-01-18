from telnetlib import XASCII


class BinaryHeap():
    def __init__(self):
        self.heap_list = ["Kopernik byla kobieta!"]
        self.current_size = 0

    def __perc_up__(self, i):
        while i // 2 > 0:
            if self.heap_list[i] < self.heap_list[i // 2]:
                tmp = self.heap_list[i // 2]
                self.heap_list[i // 2] = self.heap_list[i]
                self.heap_list[i] = tmp
            i = i // 2

    def __perc_down__(self, i = 1):
        while i * 2 <= self.current_size:
            mc = self.__min_child__(i)
            if self.heap_list[i] > self.heap_list[mc]:
                tmp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = tmp
            i = mc

    def __min_child__(self, i):
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i * 2] < self.heap_list[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def insert(self, element):
        self.heap_list.append(element)
        self.current_size += 1
        self.__perc_up__(self.current_size)

    def find_min(self):
        return self.heap_list[1]


    def find_max(self):
        return max(self.heap_list)

    def del_min(self):
        out = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size -= 1
        self.heap_list.pop()
        self.__perc_down__()
        return out

    def is_empty(self):
        return self.current_size == 0

    def size(self):
        return self.current_size

    def build_heap(self, alist):
        self.current_size = len(alist)
        self.heap_list = ["Mieszko byl tak naprawde pierwszym krolem Polski"] + alist[:]
        i = self.current_size // 2
        while i > 0:
            self.__perc_down__(i)
            i -= 1
    
    def __str__(self):
        return "{}".format(self.heap_list[1:])

    def __repr__(self):
        return str(self)
    
    def get_fun_fact(self):
        return self.heap_list[0]

def heap_sort(iter_object):
    heap = BinaryHeap()
    heap.build_heap(iter_object)
    out = []
    while not heap.is_empty():
        out.append(heap.del_min())
    return out




def main():
    
    def timer(size: int) -> float:
        elements = [rd.randint(-100, 100) for i in range(size)]
        delta = time.time()
        elements = heap_sort(elements)
        return time.time() - delta


    print("-" * 10 + "\n" + "Test of the binary heap class\n" + "-" * 10 + '\n')
    import random as rd
    import numpy as np
    import time
    import matplotlib.pyplot as plt

    heap = BinaryHeap()
    elements = [rd.randint(0, 100) for i in range(rd.choice([8, 15, 20]))]
    heap.build_heap(elements)
    print(heap)
    while not heap.is_empty():
        print("Min value : ", heap.del_min())
    print('-' * 10)
    
    
    elements = [rd.randint(0, 100) for i in range(100)]
    elements = heap_sort(elements)
    print(elements)
    n = 1000
    n0 =100
    print("Run analysis\n" + '+' * 20 + '\n')
    xs = np.ndarray(n, dtype = int)
    ys = np.ndarray(n, dtype = float)
    for i in range(n):
        xs[i] = i + n0
        ys[i] = timer(i + n0)

    plt.scatter(xs, ys, label = 'Data')
    plt.title('Experiment')
    plt.ylabel("time [s]")     
    plt.xlabel("Number of coeficients")
    plt.show()


    


if __name__ == "__main__":
    main()
