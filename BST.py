class BSTNode:

    @staticmethod
    def __less__(a, b):
        """"
        Return if a<b
        """
        try:
            return  a < b
        except:
            raise TypeError
    
    @staticmethod
    def __equal__(a,b):
        """
        Return a == b
        """
        try:
            return a == b
        except:
            raise TypeError

    def __init__(self, val = None, info = None):
        self.left = None
        self.right = None
        self.value = val
        self.counter = 1
        self.payload = info

    def insert(self, value, info = None):
        if not self.value:
            self.value = value
            self.payload = info
        else:
            if self.__less__(self.value, value):
                if self.right:
                    self.right.insert(value, info)
                else:
                    self.right = BSTNode(value, info)
            elif self.__equal__(self.value, value):
                self.counter += 1
                self.payload = info
            else:
                if self.left:
                    self.left.insert(value, info)
                else:
                    self.left = BSTNode(value, info)
        
    def get_min(self):
        current = self
        while current.left is not None:
            current = current.left
        return current
    
    def get_max(self):
        current = self
        while current.right is not None:
            current = current.right
        return current
    
    def exist(self, value):
        """
        Check if value is in tree
        """
        if value == self.value:
            return True
        if self.__less__(self.value, value):
            if self.right is None:
                return False
            else:
                return self.right.exist(value)
        else:
            if self.left is None:
                return False
            else:
                return self.left.exist(value)

    def get(self, key):
        res = self._get(key, self)
        if res:
            return res
        return None

    def _get(self, key, current):
        if current is None:
            return None
        elif self.__equal__(key, current.value):
            return current.payload
        elif self.__less__(key, current.value):
            return self._get(key, current.left)
        else:
            return self._get(key, current.right)
    
    def __getitem__(self, key):
        return self.get(key)




    def remove(self, value):
        if self.exist(value):
            if self == None:
                return self
            if self.__less__(value, self.value):
                self.left = self.left.remove(value)
                return self
            if self.__less__(self.value, value):
                self.right = self.right.remove(value)
                return self
            if self.right == None or self.left == None:
                return None
            #value == self.value
            if self.counter > 1:
                self.counter -= 1
                return self 
            min_larger = self.right
            while not min_larger.left is None:
                min_larger = min_larger.left
            self.value = min_larger.value
            self.right = self.right.remove(min_larger.value)
            return self
            

        else:
            return False

    def inorder(self, values = []):
        if self.left is not None:
            self.left.inorder(values)
        if self.value is not None:
            values.append(self.value)
        if self.right is not None:
            self.right.inorder(values)
        return values

    def postorder(self, values = []):
        if self.left is not None:
            self.left.postorder(values)
        if self.right is not None:
            self.right.postorder(values)
        if self.value is not None:
            values.append(self.value)
        return values 

    def preorder(self, values = []):
        if self.value is not None:
            values.append(self.value)
        if self.left is not None:
            self.left.preorder(values)
        if self.right is not None:
            self.right.preorder(values)
            return values 

    def __disp_aux__(self):
        """
        Attemption base on code from https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        """
        if self.right is None and self.left is None:
            line = '({}, {})'.format(self.value,self.counter)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        elif self.right is None:
            lines, n, p, x = self.left.__disp_aux__()
            string = '({}, {})'.format(self.value,self.counter)
            u = len(string)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + string
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        elif self.left is None:
            lines, n, p, x = self.right.__disp_aux__()
            string = '({}, {})'.format(self.value,self.counter)
            u = len(string)
            first_line = string + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        else:
            left, n, p, x = self.left.__disp_aux__()
            right, m, q, y = self.right.__disp_aux__()
            string = '({}, {})'.format(self.value,self.counter)
            u = len(string)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + string + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2

    def __str__(self):
        lines, *_ = self.__disp_aux__()
        out = ''
        for i in lines:
            out += i
            out += '\n'
        return out


    def __repr__(self):
        return str(self)



def main():
    import random
    elements = [random.randint(-5, 5) for i in range(20)]
    tree = BSTNode() 
    for i in elements:
        tree.insert(i)
    print(tree)
    elements = ['A','B','C','D','E','F','G','H']
    random.shuffle(elements)
    tree = BSTNode('E')
    for i in elements:
        tree.insert(i)
    print(tree)
    print('Is C in tree?', tree.exist('C'))
    print('Is U in tree?', tree.exist('U'))
    print('Inorder: ', tree.inorder())
    print('Postorder: ', tree.postorder())
    print('Preorder: ', tree.preorder())
    print('Remove: C ')
    tree.remove('C')
    print('Insert: G, G, B ')
    tree.insert('G')
    tree.insert('G', ';)')
    tree.insert('B')
    print(tree)
    print('Remove: E E E ')
    for i in range(3):
        tree.remove('E')
        print(tree)
    print('Get payload of G :',tree['G'])


if __name__ == "__main__":
    main()