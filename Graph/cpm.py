import graphviz #importuję bibliotękę graphviz


class Queue(): #klasa reprezentująca kolejkę
    def __init__(self):
        self.l = [] #utwórz pustą listę
    
    def enqueue(self, item):
        self.l.append(item) # dodaj element na koniec kolejki
    
    def dequeue(self):
        return self.l.pop(0)    #zwróć element z przodu kolejki
    
    def is_empty(self):
        return self.l == [] # zwróć True jeśli kolejka jest pusta
    
    def size(self):
        return len(self.l) # zwróć długóść kolejki


class Stack:    #Klasyczna implementacja stosu
    def __init__(self):
        self.l = [] #utwórz pustą listę
    
    def push(self, item):
        self.l.append(item) # dodaj element na wierzch stosu

    def pop(self):
        return self.l.pop() # zwróć element z wierzchu stosu

    def peek(self):
        return self.l[-1] # zwróć element z wierzchu stosu bez jego usunięcia ze stosu

    def size(self):
        return len(self.l) # zwróć rozmiar stosu
    
    def is_empty(self):
        return self.l == [] # zwróć True jeśli stos jest pusty



class InvalidGraphError(Exception): # klasa wyjątku podnoszego, gdy dane wejściowe grafu są niepoprawne
    def __init__(self, message = "Cannot create valid plan from given tasks."):
        self.message = message
        super().__init__(self.message)    #podnieś wyjątek o zadanym komunikacie
    



class Vert():     #klasa reprezentująca wiechołek
    def __init__(self, id : str, time : int) -> None:
        self.id = id    #nazwa zadania
        self.time = time#czas trwania
        self.ngh_in = {}#lista wierzchołków wchodzących
        self.ngh_out = {}# lista wierzchołków wychodzących
        #statystyki harmonogramu
        self.es = None  #earliest start
        self.ef = None  #earliest finish
        self.ls = None  # latest start 
        self.lf = None  # latest finish
        self.slack = None   #maksymalne opóźnienie w wykonaniu
        
        
        #Zmienne używane w sortowanie toppologicznym, dfs oraz  sprawdzaniu czy graf ma cykle
        self.stat = 0 # Status 0 - nieodwiedzony, 1 - aktualnie badany, 2 - opuszczony
        self.prev = -1 # referencja do poprzedniego wierzchołka; jeśli -1 to brak poprzednika
        self.dist = -1

    def new_edge(self, vert): #Nowa krawędź wychodząca z wierzchołka
        if type(vert) != type(self):    #Sprawdź czy dodajemy woerzchołek
            raise TypeError             #jeśli nie, zwróć wyjątek
        self.ngh_out[vert.id] = vert#Dodaj do listy wierzchołków wychodzących id sąsiada
        vert.ngh_in[self.id] = self      #Dodaj do listy wierzchołków wchodzących id aktualnego wierzchołka

    # metody służące do zwracania atrybutów klasy
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

    def get_dist(self):
        return self.dist

    def get_slack(self):
        return self.slack

    def set_dist(self, dist):
        self.dist = dist
    
    def set_status(self, stat):
        if stat in (0 , 1, 2):
            self.stat = stat
        else:
            raise ValueError("Invalid status") # jeśli status jest niepoprawny podnieś wyjątek

    def set_prev(self, prev):
        if type(prev) == type(self) or prev == -1: #jeżeli poprzednik nie jest wierzchołkiem, lub nie symbolizuje jego braku "-1"
            self.prev = prev
        else:
            raise TypeError("Previous should be a vertex")  # to podnieś wyjątek

    #metody służące wstawianiu nowej wartości atrybutu
    def set_stats_e(self):
        if self.ngh_in == {}: #jeśli jest to wierzchołek początkowy
            self.es = 0       #ustaw czas szybkiego rozpoczęcia
        else:
            self.es = max([self.ngh_in[i].get_ef() for i in self.ngh_in])   #czas szybkiego ropzoczęcia to czas, kiedy wszystkie wymagane zadania się zakończą czyli ich maksimum
        self.ef = self.es + self.time    #ustaw czas szybkiego zakończenia

    def set_stats_l(self, finish):
        if self.ngh_out == {}:  # jeśli jest to wierzchołek końcowy
            self.lf = finish    #ustaw czas najpóźniejszego zakończenia równy czasowi trwania projektu
        else:
            self.lf = min([self.ngh_out[i].get_ls() for i in self.ngh_out]) # czas najpóźniejszego zakończenia to minimalny czas najpóźniejszego rozpoczęcia następników
        self.ls = self.lf - self.time   #ustaw czas najpóźniejszego rozpoczęcia

    def set_slack(self):
        self.slack = self.ls - self.es # oblicz maksymalne opóźnienie


    def __str__(self):
        # reprezentacja wierzchołka w postaci łańcucha znaków
        return "Vertex: {}\n time:{}    es:{};  ef:{};  ls:{};  lf:{};  slack:{};\n".format(self.id, self.time, self.es, self.ef, self.ls, self.lf, self.slack)

    def __repr__(self):
        # reprezentacja wierzchołka w postaci łańcucha znaków, jeśli wierzchołek wyświetlany w trybie interaktywnym
        return str(self) # zwróć to samo co dla reprezentacji w postaci łańcucha znaków



class Harmonogram():    #klasa reprezentująca harmonogram
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
        self.freq = self.top_sort() #utwórz listę posortowanych topologicznie wierzchołków
        ends = [self.verts[i].get_id() for i in self.freq if self.verts[i].get_outs() == {}] # lista wietzchołków końcowych

        for i in self.freq:
            self.verts[i].set_stats_e() #ustaw wczesne rozpoczęcia i zakończenia
        self.early_finish = max([self.verts[i].get_ef() for i in ends]) # oblicz czas zakończenia
        
        for i in self.freq[-1: :-1]:
            self.verts[i].set_stats_l(self.early_finish) # idąc w tył ustaw czas późnego zakończenia i rozpoczęcia
            self.verts[i].set_slack() # oblicz opóźnienie zadań
        
        self.startV = Vert('Start', 0) # wstaw symboliczny początek
        self.endV = Vert('Koniec', 0)  # wstaw symboliczny koniec
        for i in self.start:
            self.startV.new_edge(i) # połącz wierzchołek początkowy z piewwszymi zadaniami
        for i in ends:
            self.verts[i].new_edge(self.endV) # połącz wierzchołek końcowy z końcowymi zadaniami
        self.verts['Koniec'] = self.endV # dodaj wierzchołek końcowy do listy wierzchołków

        self.cricicalPath = self.cpm() # utwórz listę zadań ścieżki krytycznej

    def renderAN(self):
        graphviz.Source(self.dotAN()).render('HarmonogramAN')#wygeneruj reprezentacje pdf na podstawie kodu dot sieci AN
    
    def renderAA(self):
        graphviz.Source(self.dotAA()).render('HarmonogramAA')#wygeneruj reprezentacje pdf na podstawie kodu dot sieci AA


    def dotAN(self):  #reprezentacja w języku dot
        out = "digraph G{\n node [shape=record]\n" +\
        "label = Harmonogram\n"
        for i in self.startV.get_outs():
            buff2 = self.verts[i]
            out += 'Start->{};\n'.format(buff2.id)

        for i in self.verts:
            buff1 = self.verts[i]
            if buff1.get_id() == 'Koniec':
                continue

            out += '{} [label = "{{ {{ ES:{}|CZAS:{}|EF:    {}}}| {} |{{LF:{} |OPÓŹNIENIE:{}|LF:{}}}}}"];\n'.format(
            buff1.id,
            buff1.es,
            buff1.time,
            buff1.ef,
            buff1.id,
            buff1.ls,
            buff1.slack,
            buff1.lf)
                
            for j in buff1.ngh_out:
                buff2 = self.verts[j]
                if buff2 in self.cricicalPath and buff1 in self.cricicalPath:
                    out += '{}->{} [color = "red"];\n '.format(buff1.id, buff2.id)
                else:
                    out += '{}->{};\n '.format(buff1.id, buff2.id)

        out += 'Koniec [label = "Koniec| Całkowity czas:{}"]\n'.format(self.early_finish)
        return out + '}'

    def dotAA(self):
        out = "digraph G{\n node [shape=record]\n" +\
        "label = Harmonogram\n"
        for i in self.verts:
            buff1 = self.verts[i]
            if buff1.get_id() == 'Koniec':
                continue

            out += '{} [label = "{{ {{ ES:{}|EF:{} }}| {} |{{LF:{} |OPÓŹNIENIE:{}|LF:{}}}}}"];\n'.format(
            buff1.id,
            buff1.es,
            buff1.ef,
            buff1.id,
            buff1.ls,
            buff1.slack,
            buff1.lf)
        
        
            for j in buff1.ngh_out:
                    buff2 = self.verts[j]
                    out += '{}->{} [label = "{}"];\n '.format(buff1.id, buff2.id, buff1.time)
            out += 'Koniec [label = "Koniec| Całkowity czas:{}"]\n'.format(self.early_finish)
        
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
    
    """
    def dijkstra(self):
        for i in self.verts:
            self.verts[i].set_status(0) # ustaw wierzchołki na nieodwiedzone
        qu = PriorityQueue()# utwórz kolejkę priorytetową, na którą trafiać będą kolejne wierzchołko do przetwarzania
        qu.put((self.startV.get_cost(), self.startV))
        while not qu.empty():
            _, vert = qu.get()
            vert.set_status(1) # zmień status na odwiedzony
            for i in vert.get_outs():
                dist = self.verts[i].get_cost()
                if not self.verts[i].get_status():
                    new_cost = vert.get_cost() + dist
                    if new_cost < self.verts[i].get_cost():
                        qu.put((new_cost, self.verts[i]))
                        self.verts[i].set_cost(new_cost)
    """
    """
    def bfs(self):
        for i in self.verts:
            self.verts[i].set_status(0) #ustaw statusy wierzchołków na nieodwiedzone
            self.verts[i].set_dist(-1)  #ustaw dystansy na -1

        beg = self.startV   #Rozpocznij procedurę w wierzchołku
        beg.set_dist(0)
        beg.set_prev(-1)
        qu = Queue()
        qu.enqueue(beg)
        #out = []
        while not qu.is_empty():
            current = qu.dequeue()
            for i in current.get_outs():
                if not self.verts[i].get_status():
                    self.verts[i].set_status(1)
                    self.verts[i].set_dist(current.get_dist() + self.verts[i].get_slack())
                    self.verts[i].set_prev(current)
                    qu.enqueue(self.verts[i])
            current.set_status(2)
            #out.append(current)
        #return out

    def cpm(self):
        self.bfs()
        end = self.endV
        path = 
    """
    def cpm(self):
        current = self.startV
        cpm = [current]
        while current.get_outs() != {}:
            for i in current.get_outs():
                if not self.verts[i].get_slack():
                    current = self.verts[i]
                    cpm.append(current)
                    #print(current,'<-')
                    break
        return cpm


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