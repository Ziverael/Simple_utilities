class Node:
  
  def __init__(self,init_data):
    self.data = init_data
    self.next = None
  
  def get_data(self):
    return self.data

  def get_next(self):
    return self.next
  
  def set_data(self,new_data):
    self.data = new_data
  
  def set_next(self,new_next):
    self.next = new_next
    

class UnorderedList(object):
  
  def __init__(self):
    self.head = None

  def is_empty(self):
    return self.head == None

  def add(self, item):
    temp = Node(item)
    temp.set_next(self.head)
    self.head = temp

  def size(self):
    current = self.head
    count = 0
    while current != None:
      count = count + 1
      current = current.get_next()
    return count
    
  def search(self,item):
    current = self.head
    found = False
    while current != None and not found:
      if current.get_data() == item:
        found = True
      else:
        current = current.get_next()
    return found

  def remove(self, item):
    current = self.head
    previous = None
    found = False
    
    while not found:
      if current.get_data() == item:
        found = True
      else:
        previous = current
        current = current.get_next()
    
    if previous == None: #jeśli usuwamy pierwszy element
      self.head = current.get_next()
    else:
      previous.set_next(current.get_next())
      
  def append(self, item):
    """
    Metoda dodająca element na koniec listy.
    Przyjmuje jako argument obiekt, który ma zostać dodany.
    Niczego nie zwraca.
    """

    current = self.head
    previous = None

    while current != None:
      previous = current
      current = current.get_next()
    if previous == current:
      self.add(item)
    else:
      temp = Node(item)
      temp.set_next(current)
      current = temp
      previous.set_next(current)

  def index(self, item):
    """
    Metoda podaje miejsce na liście, 
    na którym znajduje się określony element - 
    element pod self.head ma indeks 0.
    Przyjmuje jako argument element, 
    którego pozycja ma zostać określona.
    Zwraca pozycję elementu na liście lub None w przypadku, 
    gdy wskazanego elementu na liście nie ma.
    """
    if self.is_empty():
      return None
    ind = 0
    current = self.head
    while current != None:
      if current.get_data() == item:
        return ind
      current = current.get_next()
      ind += 1
    return None
    
  def insert(self, pos, item):
    """
    Metoda umieszcza na wskazanej pozycji zadany element.
    Przyjmuje jako argumenty pozycję, 
    na której ma umiescić element oraz ten element.
    Niczego nie zwraca.
    Rzuca wyjątkiem IndexError w przypadku, 
    gdy nie jest możliwe umieszczenie elementu
    na zadanej pozycji (np. na 5. miejsce w 3-elementowej liście).
    """
    if not pos:
      self.add(item)
    else:
      ind = 0
      current = self.head
      while current != None and ind < pos:
        previous = current
        current = current.get_next()
        ind += 1
      if ind != pos:
        raise IndexError
      else:
        temp = Node(item)
        temp.set_next(current)
        current = temp
        previous.set_next(current)
  
  def pop(self, pos=-1):
    """
    Metoda usuwa z listy element na zadaniej pozycji.
    Przyjmuje jako opcjonalny argument pozycję, 
    z której ma zostać usunięty element.
    Jeśli pozycja nie zostanie podana, 
    metoda usuwa (odłącza) ostatni element z listy. 
    Zwraca wartość usuniętego elementu.
    Rzuca wyjątkiem IndexError w przypadku,
    gdy usunięcie elementu z danej pozycji jest niemożliwe.
    """
    if pos < 0:
      pos = self.size() - abs(pos)
    current = self.head
    previous = None
    ind = 0
    while current != None and ind < pos:
      previous = current
      current = current.get_next()
      ind += 1
    if ind - pos:
      raise IndexError
    else:
      if previous == None:
        self.head = current.get_next()
      else:
        previous.set_next(current.get_next())
      return current.get_data()
  
  def __str__(self):
    current = self.head
    li = []
    while current != None:
      li.append(current.get_data())
      current = current.get_next()
    s = "[" + ",".join(["{}"] * len(li)) + "]" 
    return s.format(*li)
  
  def __repr__(self):
    current = self.head
    li = []
    while current != None:
      li.append(current.get_data())
      current = current.get_next()
    s = "[" + ",".join(["{}"] * len(li)) + "]" 
    return s.format(*li)
    

class StackUsingUL(object):
  def __init__(self):
    self.items = UnorderedList()

  def is_empty(self):
    """
    Metoda sprawdzajacą, czy stos jest pusty.
    Nie pobiera argumentów.
    Zwraca True lub False.
    """
    return self.items.is_empty()
  
  def push(self, item):
    """
    Metoda umieszcza nowy element na stosie.
    Pobiera element, który ma zostać umieszczony.
    Niczego nie zwraca.
    """
    self.items.add(item)
    
  def pop(self):
    """
    Metoda ściąga element ze stosu.
    Nie przyjmuje żadnych argumentów.
    Zwraca ściągnięty element.
    Jeśli stos jest pusty, rzuca wyjątkiem IndexError.
    """
    if self.is_empty():
      raise IndexError
    else:
       return self.items.pop(0)

  def peek(self):
    """
    Metoda podaje wartość elementu na wierzchu stosu
    nie ściągajac go.
    Nie pobiera argumentów.
    Zwraca wierzchni element stosu.
    Jeśli stos jest pusty, rzuca wyjątkiem IndexError.
    """
    buff = self.pop()
    self.push(buff)
    return buff

  def size(self):
    """
    Metoda zwraca liczę elementów na stosie.
    Nie pobiera argumentów.
    Zwraca liczbę elementów na stosie.
    """
    return self.items.size()
  
  def __str__(self):
    return str(self.items)


def main():
  st = StackUsingUL()
  for i in range(15):
    st.push(i)
  print("Peek: ", st.peek())
  print("Stack: top-> {}".format(st))
  print("Size: {}".format(st.size()))  
  while not st.is_empty():
    print("Pop {}".format(st.pop()))
  print("Empty: {}".format(st.is_empty()))

if __name__ == "__main__":
  main()