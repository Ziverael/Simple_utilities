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

class DequeueUsingUL(object):

  def __init__(self):
    self.items = UnorderedList()

  def is_empty(self):
    """
    Metoda sprawdzajacą, czy kolejka jest pusta.
    Nie pobiera argumentów.
    Zwraca True lub False.
    """
    return self.items.is_empty()
    
  def add_left(self, item):
    """
    Metoda dodaje element do kolejki z lewej strony.
    Pobiera jako argument element, który ma zostać dodany.
    Niczego nie zwraca.
    """
    self.items.add(item)

  def add_right(self, item):
    """
    Metoda dodaje element do kolejki z prawej strony.
    Pobiera jako argument element, który ma zostać dodany.
    Niczego nie zwraca.
    """
    self.items.append(item)
    
  def remove_left(self):
    """
    Metoda usuwa element z kolejki z lewej strony.
    Nie pobiera argumentów.
    Zwraca usuwany element.
    W przypadku pustej kolejku rzuca wyjątkiem IndexError
    """

    return self.items.pop(0)
    
  def remove_right(self):
    """
    Metoda usuwa element z kolejki z prawej strony.
    Nie pobiera argumentów.
    Zwraca usuwany element.
    W przypadku pustej kolejku rzuca wyjątkiem IndexError
    """

    return self.items.pop()
  
  def size(self):
    """
    Metoda zwraca liczę elementów na w kolejce.
    Nie pobiera argumentów.
    Zwraca liczbę elementów na w kolejce.
    """
    return self.items.size()

  def __str__(self):
    return str(self.items)

def main():
  deq = DequeueUsingUL()
  left = True
  for i in range(20):
    if left:
      deq.add_left(i + 1)
      left = False
      print("Added {} on left".format(i + 1))
    else:
      deq.add_right(i + 1)
      print("Added {} on right".format(i + 1))
      left = True

  print("Size: {}".format(deq.size()))
  print("Object: ", deq) 
  treashold = deq.size() // 2
  while deq.size() > treashold:
    print("Removed from left: {}".format(deq.remove_left()))
  while not deq.is_empty():
    print("Removed from right: {}".format(deq.remove_right()))

if __name__ == "__main__":
  main()