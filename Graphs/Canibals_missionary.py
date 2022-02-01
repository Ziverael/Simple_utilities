#!/usr/bin/env python
import queue as qe
import sys
class StateError(Exception):
    def __init__(self, message = "Invalid move from previous state"):
        self.message = message
        super().__init__(self.message)

class BeginningConditionError(Exception):
    def __init__(self, message = "Game is unsolveable"):
        self.message = message
        super().__init__(self.message)

class Stack:
    def __init__(self):
        self.l = []
    
    def pop(self):
        return self.l.pop()
    
    def push(self, item):
        self.l.append(item)
    
    def is_empty(self):
        return self.l == []
    
    def size(self):
        return len(self.l)
    

class State:
    """
    Represent state of missionaries and cannibals problem.
    Args
    ----
    can         [int]   non-negative integet represent number of cannibals on left side
    mis         [int]   non-negative integet represent number of missionaries on left side
    side        [bool]  represent boat side. If False, boat is on the left side and if right then boat is on the right side
    prev_state  [State] previous state
    options     [dict]  following states
    """

    def __init__(self, can : int, mis : int, side : int):
        self.can = can
        self.mis = mis
        self.side = side
        self.prev_state = None
        self.options = {}
        self.branches = 0


    def get_prev(self) :
        return self.prev_state

    def set_prev(self, prev) -> None:
        if type(prev) != type(self):
            raise TypeError('Prev is not a State object')
        self.prev_state = prev        

    def get_atrs(self) -> tuple:
        return self.can, self.mis, self.side

    def __valid_opt__(self, state):
        c1, m1, s1 = state.get_atrs()
        c2, m2, s2 = self.get_atrs()
        if s1 == s2 or  abs(m1 - m2) > 2 or abs(c1 - c2) > 2:
            return False
        return True

    def get_opts(self) -> dict:
        return self.options

    def add_opt(self, state):
         if type(state) != type(self):
             raise TypeError('Invalid child')
         self.options[self.branches] = state
         self.branches += 1

    def __str__(self):
        return "<{},{},{}>".format(self.can, self.mis, self.side)


    def __eq__(self, other) -> bool:
        if type(self) == type(other):
            return (self.get_atrs()) == other.get_atrs()

class Game:

    @staticmethod
    def __solveable__(c, m) -> bool:
        """
        Chceck if a puzzle can be solved.
        The puzzle cannot be solved if number of cannibals is greater than missionaries
        or the number is the same and higher than 3.
        """
        if c == m >= 4 or c > m:
            return False
        return True

    @staticmethod
    def __solved__(c, m, s):
        if (c, m, s) == (0, 0, 1):
            return True
        return False

    def __init__(self, can_num, mis_num):
        if not Game.__solveable__(can_num, mis_num):
            raise BeginningConditionError
        self.beg_c = can_num
        self.beg_m = mis_num
        self.beg_state = State(can_num, mis_num, -1)

    def add_state(self, parent : State, successor : State):
        if successor.__valid_opt__(parent):
            successor.set_prev(parent)
            parent.add_opt(successor)
        else:
            raise StateError

    def solve(self):
        queue = qe.QueueAb()
        queue.enqueue(self.beg_state)
        not_solved = True
        while not_solved and not queue.is_empty():
            current = queue.dequeue()

            c, m, s = current.get_atrs()
            for (can, mis) in ((2, 0), (1, 0), (1, 1), (0, 1), (0, 2)):#move can, mis
                mis *= s
                mis = m + mis
                can *= s
                can = can + c
                side = s * -1
                flag = True #Check if lose state
                buff = State(can, mis, side)
                buff.set_prev(current)
                self.add_state(current, buff)
                if Game.__solved__(*buff.get_atrs()):
                    not_solved = False
                    break
                if buff.get_prev():
                    if buff.get_prev().get_prev() == buff:
                        flag = False
                if can > mis or can > self.beg_c or mis > self.beg_m or can < 0 or mis < 0:
                    flag = False
                
                if flag:
                    queue.enqueue(buff)

        if not_solved:
            return False
        st = Stack()
        st.push(buff)
        curr = buff.get_prev()
        while curr:
            st.push(curr)
            curr = curr.get_prev()
        out ="{}".format(st.pop())
        while not st.is_empty():
            out += " -> {}".format(st.pop())
        return out       
                    


def main(c: int, m : int):
    #st = State(11, 4 , 1)
    #print(st.get_atrs(), st, st.get_prev())
    game = Game(c, m)
    print(game.solve())


if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            c, m = int(sys.argv[1]), int(sys.argv[2])
        except:
            raise TypeError
        main(c, m)
    elif len (sys.argv) == 1:
        main(3,3)
    else:
        print("Invalid input")