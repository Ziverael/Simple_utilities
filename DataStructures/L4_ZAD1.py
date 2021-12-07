class QueueBaB(object):
  """
  Klasa implementująca kolejkę za pomocą pythonowej listy tak,
  że początek kolejki jest przechowywany na początku listy.
  """  
  def __init__(self):
    self.list_of_items = []
    
  def enqueue(self, item):
    """
    Metoda służąca do dodawania obiektu do kolejki.
    Pobiera jako argument obiekt który ma być dodany.
    Niczego nie zwraca.
    """
    self.list_of_items.append(item)
    

  def dequeue(self):
    """
    Metoda służąca do ściągania obiektu do kolejki.
    Nie pobiera argumentów.
    Zwraca ściągnięty obiekt.
    """
    return self.list_of_items.pop(0)
  
  def is_empty(self):
    """
    Metoda służąca do sprawdzania, czy kolejka jest pusta.
    Nie pobiera argumentów.
    Zwraca True jeśli kolejka jest pusta lub False gdy nie jest.
    """
    return self.list_of_items == []


    
  def size(self):
    """
    Metoda służąca do określania wielkości kolejki.
    Nie pobiera argumentów.
    Zwraca liczbę obiektów w kolejce.
    """
    return len(self.list_of_items)
    
  
class QueueBaE(object):
  """
  Klasa implementująca kolejkę za pomocą pythonowej listy tak,
  że początek kolejki jest przechowywany na końcu listy.
  """
  
  def __init__(self):
    self.list_of_items = []
    
  def enqueue(self, item):
    """
    Metoda służąca do dodawania obiektu do kolejki.
    Pobiera jako argument obiekt który ma być dodany.
    Niczego nie zwraca.
    """
    self.list_of_items.insert(0, item)
    
  def dequeue(self):
    """
    Metoda służąca do ściągania obiektu do kolejki.
    Nie pobiera argumentów.
    Zwraca ściągnięty obiekt.
    """
    return self.list_of_items.pop()
  
  def is_empty(self):
    """
    Metoda służąca do sprawdzania, czy kolejka jest pusta.
    Nie pobiera argumentów.
    Zwraca True jeśli kolejka jest pusta lub False gdy nie jest.
    """
    return self.list_of_items == []
    
  def size(self):
    """
    Metoda służąca do określania wielkości kolejki.
    Nie pobiera argumentów.
    Zwraca liczbę obiektów w kolejce.
    """
    return len(self.list_of_items)
  
def main():
    queue_a = QueueBaB()
    queue_b = QueueBaE()
    for i in range(0,11):
        queue_a.enqueue(i)
        queue_b.enqueue(i)
    print("Size A:", queue_a.size())
    print("Size B:", queue_b.size())
    while not queue_a.is_empty():
        print(queue_a.dequeue())
    while not queue_b.is_empty():
        print(queue_b.dequeue())

if __name__ == "__main__":
    main()