
class QueueAb():
    def __init__(self):
        self.l = []
    
    def enqueue(self, item):
        self.l.append(item)
    
    def dequeue(self):
        return self.l.pop(0)
    
    def is_empty(self):
        return self.l == []
    
    def size(self):
        return len(self.l)

class QueueBa():
    def __init__(self):
        self.l = []
    
    def enqueue(self, item):
        self.l.insert(0, item)
    
    def dequeue(self):
        return self.l.pop()
    
    def is_empty(self):
        return self.l == []
    
    def size(self):
        return len(self.l)
    

def main():
    queue_a = QueueAb()
    queue_b = QueueBa()
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