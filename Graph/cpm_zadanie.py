#Kilka uwag:
#Żeby program działał poprawnie należy doinstalować bibliotekę
#graphviz
#oraz interpreter języka graphviz
#progarm po wywołaniu wykona funkcję testującą
#tworzy on zarazem grafy AN i AA
#wizualizacje zwracane są w pliku pdf
#harmonogramy są też przedstawiane w postaci tekstowej
#gddzie każdy wierzchołek ma swoje czasy ES, EF, LF, LS oraz opóźnienie

#aby wygenerować harmonogram podaj listę zadań w postaci
# [ { 'id' : 'zad1',            <--nazwa zadania(wierzchołka)
#   'time' : 2,                 <--czas trwania zadania
#   'req' : {}                    <--zadania, które muszą poprzedzać zadanie (uwaga! jeśli A wymaga B, a C wymaga B to w wymaganiach C starczy podać B)
# },
#   { 'id' : 'zad2',
#   'time' : 4,
#   'req' : {'A'}
# }
# ]
#
#Więcej przykładów w funkcji testującej
#z przykładami generowania i zwracania wartości


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
        return "Vertex: {}\n time:{}    es:{};  ef:{};  ls:{};  lf:{};  slack:{};\n".format(self.id, self.time, self.es, self.ef, self.ls, self.lf, self.slack) # zwróć łańcuch znaków gdzie w miejscu {} znajdą się wymienione w format wartości w podanej kolejności

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

    #wróć listę zawierającą ścieżkę krytyczną
    def get_cpm(self):
        return self.cricicalPath

    def get_ttime(self):#zwróć całkowity czas trwania projektu
        return self.early_finish

    def dotAN(self):  #reprezentacja w języku dot (otrzyma on łańcuch znaków, który zinterpretuje)
        #zmienna out przechowuje ten łańcuch znaków
        out = "digraph G{\n node [shape=record]\n" +\
        "label = Harmonogram\n" #inicjalizacja grafu  z kształtem węzłów oraz nagłówkiem
        for i in self.startV.get_outs(): # w pętli
            buff2 = self.verts[i]        #pobieraj wierzchołki początkowe
            if buff2 in self.cricicalPath:
                out += 'Start->{} [color = "red"];\n'.format(buff2.id) # i zrób od wierzchołka start do nich gałęzie
            else:
                out += 'Start->{};\n'.format(buff2.id) # i zrób od wierzchołka start do nich gałęzie

        for i in self.verts:    #w pętli
            buff1 = self.verts[i]   #pobieraj wierzchołki
            if buff1.get_id() == 'Koniec':  # jeżeli to końcowy to pomiń krok
                continue
            #dodaj reprezentacje danego wierzchołka z jego statystykami patrz metoda format 
            out += '{} [label = "{{ {{ ES:{}|CZAS:{}|EF:    {}}}| {} |{{LF:{} |OPÓŹNIENIE:{}|LF:{}}}}}"];\n'.format(
            buff1.id,
            buff1.es,
            buff1.time,
            buff1.ef,
            buff1.id,
            buff1.ls,
            buff1.slack,
            buff1.lf) # tu są kolejne atrybuty wierzchołka, które zostaną dodane do łańcucha znaków
                
            for j in buff1.ngh_out: # przejdź po sąsiadach wierzchołka
                buff2 = self.verts[j]   #przechowaj sąsiada w zmiennej
                if buff2 in self.cricicalPath and buff1 in self.cricicalPath: #jeźeli prowadzi przez oba wiezrchołki ścieżka krytyczna
                    ind = self.cricicalPath.index(buff2)    # pobierz indeks. Mamy pewność, że jest on większy od 0, więc możemy w kolejnym kroku odnieść się do wcześniejszego
                    if self.cricicalPath[ind - 1] == buff1:
                        out += '{}->{} [color = "red"];\n '.format(buff1.id, buff2.id)# to pokoloruj na czerwono gałąź
                    else:
                        out += '{}->{};\n '.format(buff1.id, buff2.id)  # inaczej poprowadź zwykłą gałąź (bez kolorka)
                else:
                    out += '{}->{};\n '.format(buff1.id, buff2.id)  # inaczej poprowadź zwykłą gałąź (bez kolorka)

        out += 'Koniec [label = "Koniec| Całkowity czas:{}"]\n'.format(self.early_finish) # dodaj reprezentację wierzchołka symbolizującego koniec projektu
        return out + '}' # zwróć łańcuch znaków

    def dotAA(self): #to samo co wcześniej, tyle że sieć AA, dlatego tu wartość czasu zadania znajdzie się nad gałęzią, a nie w węźle
        #pomijam komentarze do tej części, bo prócz tu opisanej zmiany wszystko jest tak samo
        out = "digraph G{\n node [shape=record]\n" +\
        "label = Harmonogram\n"

        for i in self.startV.get_outs(): # w pętli
            buff2 = self.verts[i]        #pobieraj wierzchołki początkowe
            if buff2 in self.cricicalPath:
                out += 'Start->{} [color = "red"];\n'.format(buff2.id) # i zrób od wierzchołka start do nich gałęzie
            else:
                out += 'Start->{};\n'.format(buff2.id) # i zrób od wierzchołka start do nich gałęzie

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
                if buff2 in self.cricicalPath:
                    ind = self.cricicalPath.index(buff2)    # pobierz indeks. Mamy pewność, że jest on większy od 0, więc możemy w kolejnym kroku odnieść się do wcześniejszego
                    if self.cricicalPath[ind - 1] == buff1:
                #if buff2 in self.cricicalPath and buff1 in self.cricicalPath: #jeźeli prowadzi przez oba wiezrchołki ścieżka krytyczna
                        out += '{}->{} [label = "{}" color = "red"];\n '.format(buff1.id, buff2.id, buff1.time)
                    else:
                        out += '{}->{} [label = "{}"];\n '.format(buff1.id, buff2.id, buff1.time)
                else:
                    out += '{}->{} [label = "{}"];\n '.format(buff1.id, buff2.id, buff1.time)
        out += 'Koniec [label = "Koniec| Całkowity czas:{}"]\n'.format(self.early_finish)
        return out + '}'
    
    def __str__(self):#reprezentacja harmonogramu w postaci łańcucha  znaków
        out = "" # zmienna z łańcuchem znaków
        for i in self.freq: # w kolejności topologicznej
            out += str(self.verts[i]) + "\n" #do łańcucha dodaj reprezentacje łańcucha każdego z wierzchołków (zdefiniowane w moetodzie __str__ dla wierzchołka)
        return out


    def dfs(self, beg): # przeszukiwanie w głąb
        out = []    #utwórz ppustą listę
        for i in self.verts:    #ustaw statusy na nieodwiedzone i brak poprzedników dla wszysktich wierzchołków
            self.verts[i].set_prev(-1)
            self.verts[i].set_status(0)
        beg = self.verts[beg] #weź wierzchołek początkowy
        self.__dfs__(beg, out) # wykonaj metode podrzędną __dfs__
        return out  #zwróć listę wierzchołków
    
    def __dfs__(self, vert, out): #metoda podrzędna używana w dfs. Otrzymuje ona listę out, którą przekazuje w kolejnych wywołaniach
        out.append(vert.get_id()) #dodaj właśnie badany wierzhołek do listy  
        vert.set_status(1)          #ustaw status na odwiedzony
        for i in vert.get_outs():   #w pętli po sąsiadach
            if not self.verts[i].get_status(): #jeśli wierzchołek był niodwiedzony (czyli ma status = 0)
                self.verts[i].set_prev(vert)    #to ustaw obecnie badany wierzchołek jako jego poprzednik
                self.__dfs__(self.verts[i], out)# i wykonaj metodę __dfs__ na tym wierzchołki
        vert.set_status(2)  #ustaw status obecnego wierzchołka na przebadany (2)

    def top_sort(self):          #sortowanie topologiczne
        if self.cyclic():        #sprawdź czy graf cykliczny
            raise InvalidGraphError("The graph is cyclic")  # nie można topologicznie posortować cyklicznego grafu
        st = Stack()    #utwórz pusty stos
        for i in  self.verts:   #ustaw początkowe statusy nieodwiedzone i brak poprzedników (-1)
            self.verts[i].set_prev(-1)         
            self.verts[i].set_status(0)
        for i in self.verts: # w pętli po wszystkich wierzchołkach grafu
            if not self.verts[i].get_status():  # jeśli wierzchołek nie był jeszcze odwiedzony
                self.__top_sort__(self.verts[i], st)    #wykonaj na nim metodę podrzędną __top_sort__ z przekazanym stosem
        out = []    #utwórz pustą listę wierzchołków
        while not st.is_empty():    #wypakuj stos do listy
            out.append(st.pop())
        return out  #zwróć listę (jest ona posortowana topologicznie)
    
    def __top_sort__(self, vert, st): #metoda podrzędna sortowania topologicznego
        vert.set_status(1)  #ustaw status wierzchołka na obecnie badany (1)
        for i in vert.get_outs(): # w pętli po sąsiadach
            if not self.verts[i].get_status():  #jeżeli jeszcze nieodwiedzony
                self.verts[i].set_prev(vert)   #ustaw poprzednika sąsiada na obecnie badany wierzchołek
                self.__top_sort__(self.verts[i], st)    #wykonaj sortowanie topologiczne na sąsiedzie z przekazanym stosem
        vert.set_status(2)  #ustaw status wierzchołka na przebadany (tzn. odwiedzony/sprawdzony)
        st.push(vert.get_id()) # połóż na stosie badany wierzchołek

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
    
    def cpm(self): #metoda znajdowania ścieżki krytycznej
        current = self.startV   #ustaw obecnie badany wierzchołek na wierzchołek startowy
        cpm = [current]         #dodaj go do listy wierzchołków
        while current.get_outs() != {}: #dopóki nie dotarłeś na koniec grafu
            for i in current.get_outs():  #sprawdź listę wierzchołków wychodzących
                if not self.verts[i].get_slack():   #jeśli jest to wierzchołek ścieżki krytycznej
                    current = self.verts[i]         #to ustaw go jako obecnie badany
                    cpm.append(current)             #i dodaj do listy wyjściowej
                    break                           #przerwij sprawdzanie dla wcześniejszego wierzchołka
        return cpm                                  # zwróć ścieżkę krytyczną


def test(validation = False):                 #funkcja testująca
                                                #wykonuje kilka testów
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

    tasks = [               #przykład z grafem cyklicznym
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
    if validation: # jeśli argument validation to True, to sprawdź, czy podniesie wyjątek dla grafu cyklicznego
        gh = Harmonogram(tasks)
    
    tasks = [      
        {'id' : 'A',
        'time' : 5,
        'req' : {}
        },
        {'id' : 'B',
        'time' : 4,
        'req' : {}
        },
        {'id' : 'C',
        'time' : 3,
        'req' : {'A'}
        },
        {'id' : 'D',
        'time' : 4,
        'req' : {'A'}
        },
        {'id' : 'E',
        'time' : 6,
        'req' : {'A'}
        },
        {'id' : 'F',
        'time' : 4,
        'req' : {'B', 'C'}
        },
        {'id' : 'G',
        'time' : 5,
        'req' : {'D'}
        },
        {'id' : 'H',
        'time' : 6,
        'req' : {'D', 'E'}
        },
        {'id' : 'I',
        'time' : 6,
        'req' : {'F'}
        },
        {'id' : 'J',
        'time' : 4,
        'req' : {'H', 'G'}
        }
    ]
    gh = Harmonogram(tasks)
    gh.renderAN() #Wygeneruj wizualizację sieci AN
    gh.renderAA() #Wygeneruj wizualizację sieci AA
    print(gh.get_ttime())#pokaż całkowity czas
    print(gh.get_cpm())#pokaż ścieżkę krytyczną (jako listę kolejnych wierzchołków)
    
if __name__ == "__main__":  #Jeżeli uruchomimy plik (czyli nie będzie zaimportowany)
    test()                  #wywołamy funkcję testującą