#Założenie listy zadań: jesli zadanie A wymaga zadania B,a zadanie C wymaga A, to podajemy w wymaganiach C zadania A i B

class Stack:    #Klasyczna implementacja stosu
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



class InvalidGraphError(Exception): # klasa wyjątku podnoszego, gdy dane wejściowe grafu są niepoprawne
    def __init__(self, message = "Cannot create valid plan from given tasks."):
        self.message = message
        super().__init__(self.message)    



class Vert():     #klasa reprezentująca wiechołek
    def __init__(self, id : str, time : int) -> None:
        self.id = id    #nazwa zadania
        self.time = time#czas trwania
        self.ngh_in = {}#lista wierzchołków wchodzących
        self.ngh_out = {}# lista wierzchołków wychodzących
        self.es = None
        self.ef = None
        self.ls = None
        self.lf = None
        self.slack = None
        
        #Zmienne używane w sortowanie toppologicznym, dfs oraz  sprawdzaniu czy graf ma cykle
        self.stat = 0 # Status 0 - nieodwiedzony, 1 - aktualnie badany, 2 - opuszczony
        self.prev = -1 # referencja do poprzedniego wierzchołka; jeśli -1 to brak poprzednika

    def new_edge(self, vert): #Nowa krawędź wychodząca z wierzchołka
        if type(vert) != type(self):    #Sprawdź czy dodajemy woerzchołek
            raise TypeError             #jeśli nie, zwróć wyjątek
        self.ngh_out[vert.id] = vert#Dodaj do listy wierzchołków wychodzących id sąsiada
        vert.ngh_in[self.id] = self      #Dodaj do listy wierzchołków wchodzących id aktualnego wierzchołka

    def get_id(self):
        return self.id
    
    def get_time(self):
        return self.time
    
    def get_prev(self):
        return self.prev
    
    def get_status(self):
        return self.stat
    
    def get_outs(self):
        return self.ngh_out
    
    def get_es(self):
        return self.es    

    def get_ef(self):
        return self.ef

    def get_ls(self):
        return self.ls

    def get_lf(self):
        return self.lf

    def set_status(self, stat):
        if stat in (0 , 1, 2):
            self.stat = stat
        else:
            raise ValueError("Invalid status")

    def set_prev(self, prev):
        if type(prev) == type(self) or prev == -1:
            self.prev = prev
        else:
            raise TypeError("Previous should be a vertex")

    def set_stats_e(self):
        if self.ngh_in == {}: #jeśli jest to wierzchołek początkowy
            self.es = 0       #ustaw czas szybkiego rozpoczęcia
        else:
            self.es = max([self.ngh_in[i].get_ef() for i in self.ngh_in])   #czas szybkiego ropzoczęcia to czas, kiedy wszystkie wymagane zadania się zakończą czyli ich maksimum
        self.ef = self.es + self.time    #ustaw czas szybkiego zakończenia

    def set_stats_l(self, finish):
        if self.ngh_out == {}:
            self.lf = finish
        else:
            self.lf = min([self.ngh_out[i].get_ls() for i in self.ngh_out])
        self.ls = self.lf - self.time

    def set_slack(self):
        self.slack = self.ls - self.es


    def __str__(self):
        return "Vertex: {}\t time:{}    es:{};  ef:{};  ls:{};  lf:{};  slack:{};".format(self.id, self.time, self.es, self.ef, self.ls, self.lf, self.slack)

    def __repr__(self):
        return str(self)



class Harmonogram():    #klasa reprezentująca sieć AA
    def __init__(self, verts: dict) -> None:
        self.verts = {} # utwórz listę, w której przechowywane będą wierzchołki
        self.size = len(verts) # ilość wierzchołków w grafie
        self.start = [] #lista zadań, które mogą rozpoczynać
        ends = [] # lista zadań, które mogą kończyć
        for i in verts: # w pętli dodawaj wierzchołki do grafu
            id_, time= i['id'], i['time'] # rozpakuj słownik reprezentujący zadanie
            self.verts[i['id']] = (Vert(id_, time)) # utwórz wierzchołek na podstawie zadania
        
        for i in range(self.size): # zbuduj relacje między wierzchołkami:
            buff = self.verts[verts[i]['id']] # stwórz tymczasową zmienną przechowującą i-ty wierzchołek
            if not len(verts[i]['req']):
                self.start.append(buff)
            for j in verts[i]['req']:           #Dla kolejnych wymaganych wierzchołków
                self.verts[j].new_edge(buff)    #Twórz z nich krawędzie wchodzące do danego wierzchołka
        self.freq = self.top_sort()
        ends = [self.verts[i].get_id() for i in self.freq if self.verts[i].get_outs() == {}]
        print(self.freq)
        print(ends)
        print(self.dot())
        for i in self.freq:
            self.verts[i].set_stats_e()
        self.early_finish = max([self.verts[i].get_ef() for i in ends])
        
        for i in self.freq[-1: :-1]:
            self.verts[i].set_stats_l(self.early_finish)
            self.verts[i].set_slack()
        
        self.startV = Vert('Start', 0)
        self.endV = Vert('Koniec', 0)
        for i in self.start:
            self.startV.new_edge(i)
        for i in ends:
            self.verts[i].new_edge(self.endV)
        


        #print(self.startV.get_outs())
        #print(self.endV.ngh_in)
            

    def dot(self):  #reprezentacja w języku dot
        out = "digraph G{\n"
        for i in self.verts:
            buff1 = self.verts[i]
            for j in buff1.ngh_out:
                buff2 = self.verts[j]
                out += '{}->{};'.format(buff1.id, buff2.id)
        return out + '}'
    
    def __str__(self):
        out = ""
        for i in self.freq:
            out += str(self.verts[i]) + "\n"
        return out


    def dfs(self, beg):
        out = []
        for i in self.verts:
            self.verts[i].set_prev(-1)
            self.verts[i].set_status(0)
        beg = self.verts[beg]
        self.__dfs__(beg, out)
        return out
    
    def __dfs__(self, vert, out):
        out.append(vert.get_id())
        vert.set_status(1)
        for i in vert.get_outs():
            if not self.verts[i].get_status():
                self.verts[i].set_prev(vert)
                self.__dfs__(self.verts[i], out)
        vert.set_status(2)

    def top_sort(self):          
        if self.cyclic():
            raise InvalidGraphError("The graph is cyclic")
        st = Stack()
        for i in  self.verts:
            self.verts[i].set_prev(-1)         
            self.verts[i].set_status(0)
        for i in self.verts:
            if not self.verts[i].get_status():
                self.__top_sort__(self.verts[i], st)
        out = []
        while not st.is_empty():
            out.append(st.pop())
        return out
    
    def __top_sort__(self, vert, st):
        vert.set_status(1)
        for i in vert.get_outs():
            if not self.verts[i].get_status():
                self.verts[i].set_prev(vert)
                self.__top_sort__(self.verts[i], st)
        vert.set_status(2)
        st.push(vert.get_id())

    def cyclic(self) -> bool: # sprawdzanie czy graf jest cykliczny
        cache = {}             #słownik zapamiętujący odwiedzone wierzchołki w danej iteracji
        for i in self.verts:
            self.verts[i].set_status(0) #przywróć statusy do początkowych ustawień, czyli wszystkie wierzchołki na 0
        for i in self.verts:                    #sprawdzaj kolejne wierzchołki
            if not self.verts[i].get_status():  #jeżeli status to 0 to wykonaj sprawdzanie
                if self.__cyclic__(self.verts[i], cache):   #wykonaj metodę sprawdzającą na wierzchołku
                    return True                             # i zależnie od jej wyniku oceń czy acykliczny
        return False

    def __cyclic__(self, vert, cache):
        vert.set_status(1)  #ustaw status na badany
        cache[vert.get_id()] = None #dodaj do pamięci id wierzchołka
        for i in vert.get_outs():   #przejdź po wierzchołkach wychodzących z wierzchołka
            if not self.verts[i].get_status(): #jeżeli sąsiad ma status 0 to wykonaj metodę sprawdzającą
                if self.__cyclic__(self.verts[i], cache):
                    return True #przerwij zwracając True jeśli pojawił się cykl
            elif i in cache:    #jeżeli wierzchołek  pojawił się już w odwiedzonych to graf jest acykliczny
                return True
        del cache[vert.get_id()]
        return False

    def bfs(self):
        for i in self.verts:
            self.verts[i].##############



def test():                 #funkcja testująca
    tasks = [               #lista zadań
        {'id' : 'A',
        'time' : 4,
        'req' : {'B', 'C'}
        },
        {'id' : 'B',
        'time' : 2,
        'req' : {'C'}
        },
        {'id' : 'C',
        'time' : 6,
        'req' : {}
        },
        {'id' : 'D',
        'time' : 1,
        'req' : {'B', 'C', 'E'}
        },
        {'id' : 'E',
        'time' : 1,
        'req' : {'B', 'C', 'A'}
        }
    ]

    gh = Harmonogram(tasks)
    print(gh)
    tasks = [               #przykład z grafem acyklicznym
        {'id' : 'A',
        'time' : 7,
        'req' : {}
        },
        {'id' : 'B',
        'time' : 9,
        'req' : {}
        },
        {'id' : 'C',
        'time' : 12,
        'req' : {'A'}
        },
        {'id' : 'D',
        'time' : 8,
        'req' : {'A', 'B'}
        },
        {'id' : 'E',
        'time' : 9,
        'req' : {'D'}
        },
        {'id' : 'F',
        'time' : 6,
        'req' : {'C', 'E'}
        },
        {'id' : 'G',
        'time' : 5,
        'req' : {'E'}
        }
    ]
    gh = Harmonogram(tasks)
    print(gh)
    #print(gh.start)
    tasks = [               #przykład z grafem acyklicznym
        {'id' : 'A',
        'time' : 4,
        'req' : {'B'}
        },
        {'id' : 'B',
        'time' : 2,
        'req' : {'C'}
        },
        {'id' : 'C',
        'time' : 6,
        'req' : {'A'}
        },
        {'id' : 'D',
        'time' : 1,
        'req' : {'B', 'C', 'E'}
        },
        {'id' : 'E',
        'time' : 1,
        'req' : {'B', 'C', 'A'}
        }
    ]
    gh = Harmonogram(tasks)
    
if __name__ == "__main__":  #Jeżeli uruchomimy plik (czyli nie będzie zaimportowany)
    test()                  #wywołamy funkcję testującą