import BinaryHeap as heap

class LimitedBinaryHeap(heap.BinaryHeap):
    def __init__(self, n):
        super().__init__()
        self.limit = n
    
    def insert(self, element):
        super().insert(element)
        if self.limit < self.current_size:
            self.del_min()
            self.current_size - 1
    
    def build_heap(self, alist):
        self.current_size = self.limit
        self.heap_list = ["Mieszko byl tak naprawde pierwszym krolem Polski"] + alist[ : self.limit]
        i = self.current_size // 2
        while i > 0:
            self.__perc_down__(i)
            i -= 1
        
        for i in alist[10 : ]:
            self.insert(i)

def main():
    print("-" * 10 + "\n" + "Test of a limited binary heap class\n" + "-" * 10 + '\n')
    import random as rd
    heap = LimitedBinaryHeap(6)
    elements = [rd.randint(0, 100) for i in range(20)]
    print("Elements meant to be added to the heap:",elements)
    for i in elements:
        heap.insert(i)
        print("Current element: {}\t current heap: {}".format(i, heap))

    elements = [rd.randint(0, 100) for i in range(100)]
    maxx = elements[ : ]
    maxx.sort()
    maxx = maxx[-10 : ]
    print("New elemets: {}\n The greatest 10 values: {}".format(elements,maxx))
    h = LimitedBinaryHeap(10)
    h.build_heap(elements)
    print("A limited heap from given elements",h)
    check = []
    while not h.is_empty():
        check.append(h.del_min())
    print("If heap is identical with the greatest values: {}".format(check == maxx))

if __name__ == "__main__":
    main()