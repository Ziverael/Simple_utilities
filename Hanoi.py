class Stack():
    def __init__(self):
        self.l = []
    
    def push(self, item):
        self.l.append(item)

    def pop(self):
        return self.l.pop()
    
    def peek(self):
        return self.l[-1]
    
    def size(self):
        return len(self.l)
    
    def is_empty(self):
        return self.l == []
    
    def __str__(self):
        disp = "[" + ",".join(["{}"] * len(self.l)) + "]"
        return disp.format(*self.l)



class Disk():
    def __init__(self, size : int):
        self.__size = size
    
    def get_size(self):
        return self.__size
    
    def __str__(self):
        return str(self.__size)

class Hanoi_tower():


    def __init__(self, n = 3):
        self.stakes = {'A' : Stack(), 'B' : Stack(), 'C' : Stack()}
        self.size = n
        self.__set_tower__()
    
    def __str__(self):
        l = ["", "", ""]
        it = -1
        for i in self.stakes:
            it += 1
            l[it] += str(self.stakes[i])    #Disk size doesn't matter in display, because of the stack representation
        return "-" * 10 + "\nA: {}\nB:{}\nC:{}\n".format(l[0], l[1], l[2]) + "-" * 10


    def __repr__(self):
        return str(self)
    
    def move_disk(self, from_, to_):
        if not from_ in ('A', 'B', 'C') or not to_ in ('A', 'B', 'C'):
            raise ValueError('Invalid stake index')
        if self.stakes[from_].is_empty():
                raise IndexError("Stake {} is empty".format(from_))
        self.stakes[to_].push(self.stakes[from_].pop())

    def get_size(self):
        return self.size

    def move_Hanoi_tower(self, from_, to_, buffer):
        if not from_ in ('A', 'B', 'C') or not to_ in ('A', 'B', 'C'):
            raise ValueError('Invalid stake index')
        
        if not self.__check_tower__():
            self.__clear_tower__()
            self.__set_tower__()
        
        self.__move_tower__(from_, to_, buffer, self.size)
        
    def __move_tower__(self, from_, to_, buffer, size):
        if size == 1:
            self.move_disk(from_, to_)
        else:
            self.__move_tower__(from_, buffer, to_, size - 1)
            self.__move_tower__(from_, to_, buffer, 1)
            self.__move_tower__(buffer, to_, from_, size - 1)

    def __clear_tower__(self):
        for i in self.stakes:
            self.stakes[i] = Stack()
    
    def __set_tower__(self):
        for i in range(self.size):
            self.stakes['A'].push(Disk(self.size - i))
    
    def __check_tower__(self):
        count = 0
        el = 0
        for i in self.stakes:
            if not self.stakes[i].is_empty():
                el = self.stakes[i].size()
                count += 1
        if count != 1 or el != self.size:
            return False
        return True
                
            






def main():
    hanoi = Hanoi_tower()
    print(hanoi)
    hanoi.move_disk('A','B')
    hanoi.move_disk('B','C')
    print(hanoi)
    #hanoi2 = Hanoi_tower()
    #print(hanoi2)
    hanoi.move_Hanoi_tower('A','C','B')
    print(hanoi)
    hanoi.move_Hanoi_tower('C','B','A')
    print(hanoi)
    hanoi.move_Hanoi_tower('B','A','C')
    print(hanoi)
    hanoi = Hanoi_tower(5)
    print(hanoi)
    hanoi.move_Hanoi_tower('A','B','C')
    print(hanoi)
    print("Inccorect movement check:")
    hanoi.move_Hanoi_tower('A','B','C')
    


if __name__ == "__main__":
    main()
