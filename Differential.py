from sys import stderr, exit

class Stack():
    """
    Stack definition.
    """
    def __init__(self):
        self.l = []
    
    def push(self, el):
        self.l.append(el)
    
    def pop(self):
        return self.l.pop()
    
    def size(self):
        return len(self.l)

    def is_empty(self):
        return self.l == []
    
    def __str__(self):
        return str(self.l)

    def __repr__(self):
        return str(self) 

class BinaryTree():
    """
    Binary tree definition.
    """
    def __init__(self, root):
        self.key = root
        self.left = None
        self.right = None

    def insert_left(self, node):
        if self.left:
            temp = BinaryTree(node)
            temp.left = self.left
            self.left = temp
        else:
            self.left = BinaryTree(node)


    def insert_right(self, node):
        if self.right:
            temp = BinaryTree(node)
            temp.right = self.right
            self.right = temp
        else:
            self.right = BinaryTree(node)
 
    def preorder(self, values = []):
        if self.key is not None:
            values.append(self.key)
        if self.left is not None:
            self.left.preorder(values)
        if self.right is not None:
            self.right.preorder(values)
            return values
    
    def inorder(self, values = []):
        if self.left is not None:
            self.left.inorder(values)
        if self.key is not None:
            values.append(self.key)
        if self.right is not None:
            self.right.inorder(values)
        return values



    
    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_root(self):
        return self.key
    
    def set_root(self, value):
        self.key = value



    def __disp_aux__(self):
        """
        Attemption base on code from https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        """
        if self.right is None and self.left is None:
            line = '%s' % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        elif self.right is None:
            lines, n, p, x = self.left.__disp_aux__()
            string = '%s' % self.key
            u = len(string)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + string
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        elif self.left is None:
            lines, n, p, x = self.right.__disp_aux__()
            string = '%s' % self.key
            u = len(string)
            first_line = string + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        else:
            left, n, p, x = self.left.__disp_aux__()
            right, m, q, y = self.right.__disp_aux__()
            string = '%s' % self.key
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





class DiffTree():
    al_func = {"exp" : 0,"sin" : 1,"cos" : 2,"tan" : 3, "ctan" : 4, "tg" : 5, "ctg" : 6, 'log' : 7}

    @staticmethod    
    def __norm_expr__(expr):
        """
        Replace brackets so that expression have only '(' and ')' and replace ',' with '.'. Check if brackets number is correct.

        Return
        ------
        input   string  normalized string
        False   bool    if brackets number or place is invalid
        """
        
        opens = "({["
        closers = ")}]"
        brack = [i for i in expr if i in opens or i in closers] #get brackets from expression
        roof = len(brack)
        i = 0
        st = Stack()

        while i < roof:
            sym = brack[i]
            if sym in opens:
                st.push(sym)
            else:
                if st.is_empty():
                    return False
                else:
                    top = st.pop()
                    if not opens.index(top) == closers.index(sym):
                        return False
            i += 1
        if not st.is_empty():
            return False

        for i in range(len(expr)):
            if expr[i] == "{" or expr[i] == "[":
                expr = expr[ : i] + "(" + expr[i + 1 :]

            if expr[i] == "}" or expr[i] == "]":
                expr = expr[ : i] + ")" + expr[i + 1 :]
            
            if expr[i] == ",":
                expr = expr[ : i] + "." + expr[i + 1 :]
        
        expr = expr.split()
        return expr


    def format_input(self, input):        
        try:
            input = (self.__norm_expr__(str(input)))
            return input
        except:
            stderr.write("Incorrect expression")

    def __init__(self, expr : str, var : str):
        self.expr_tree = self.__build_expr_tree__(expr)
        self.var = var
        self.differ = self.__diff__(self.expr_tree)

    def __build_expr_tree__(self, expr):
        """
        Build parse tree from expression.

        Return
        ------
        tree    BinaryTree object   parse tree
        """
        expr = self.format_input(expr)
        if expr is False:
                stderr.write('Incorrect number of brackets\n')
                raise ValueError
        st = Stack()
        tree = BinaryTree('')
        st.push(tree)
        current = tree

        for i in expr:
            if i == "":
                continue

            if i == "(":
                current.insert_left("")
                st.push(current)
                current = current.get_left()
            elif i not in {'+' : 0, '-' : 1, '/' : 2, '*' : 3, ')' : 4, '^' : 5} and i not in DiffTree.al_func:
                if i in "1234567890":
                    current.set_root(int(i))
                else:
                    current.set_root(i)
                parent = st.pop()
                current = parent
            elif i in {'+' : 0, '-' : 1, '/' : 2, '*' : 3, '^' : 4}:
                current.set_root(i)
                current.insert_right("")
                st.push(current)
                current = current.get_right()
            elif i in DiffTree.al_func:
                current.set_root(i)
                current.insert_left("")
                current = current.get_left()
            elif i == ')':
                current = st.pop()
            else:
                raise ValueError
        return tree
    
    def diff(self):
        differ = self.__diff__(self.expr_tree)
        return differ

    def __diff__(self, tree : BinaryTree):
        node = BinaryTree('')
        if type(tree.key) == type(1)  or ( tree.key not in DiffTree.al_func and tree.key != self.var and type(tree.key) == type('a') and tree.key not in {'+' : 0, '-' : 1, '/' : 2, '*' : 3, '^' : 4}):
            node.set_root(0)
        
        elif tree.key == '+':
            node.set_root('+')
            node.left = self.__diff__(tree.left)
            node.right = self.__diff__(tree.right)
        
        elif tree.key == '-':
            node.set_root('-')
            node.left = self.__diff__(tree.left)
            node.right = self.__diff__(tree.right)
        
        elif tree.key == '*':
            node.set_root('+')
            node.left = BinaryTree('*')
            node.left.left  =self.__diff__(tree.left)
            node.left.right  = tree.right

            node.right = BinaryTree('*')
            node.right.left  =tree.left
            node.right.right  = self.__diff__(tree.right)

        elif tree.key == '/':
            node.set_root('/')
            node.left = BinaryTree('-')
            node.left.left = BinaryTree('*')
            node.left.right = BinaryTree('*')
            node.left.left.left = self.__diff__(tree.left)
            node.left.left.right = tree.right
            node.left.right.left = tree.left
            node.left.right.right = self.__diff__(tree.right)
            
            node.right = BinaryTree('^')
            node.right.left = tree.right
            node.right.right = BinaryTree(2)
        elif tree.key == '^':
            if tree.right.get_root() == 0:
                node.set_root(0)
            else:
                node = BinaryTree('*')
                node.left = BinaryTree('*')
                node.left.left = tree.right
                node.left.right = BinaryTree('^')
                node.left.right.left = tree.left
                node.left.right.right = BinaryTree('-')
                node.left.right.right.left = tree.right
                node.left.right.right.right = BinaryTree(1)
                
                node.right = self.__diff__(tree.left)
        
        elif tree.key == self.var:
            node.set_root(1)
        
        elif    tree.key == 'log':
            node = BinaryTree('/')
            node.left = self.__diff__(tree.left)
            
            node.right = tree.left
        
        elif tree.key == 'exp':
            node = BinaryTree('*')
            node.left = BinaryTree('exp')
            node.left.left = tree.left

            node.right = self.__diff__(tree.left)

        elif tree.key == 'sin':
            node = BinaryTree('*')
            node.left = BinaryTree('cos')
            node.left.left = tree.left

            node.right = self.__diff__(tree.left)

        elif tree.key == 'cos':
            node = BinaryTree('*')
            node.left = BinaryTree(-1)

            node.right = BinaryTree('*')
            node.right.left = BinaryTree('sin')
            node.right.left.left = tree.left
            node.right.right = self.__diff__(tree.left)
        
        elif tree.key in ('tan', 'tg'):
            node = BinaryTree('/')
            node.left = self.__diff__(tree.left)

            node.right = BinaryTree('^')
            node.right.right = BinaryTree(2)
            node.right.left = BinaryTree('cos')
            node.right.left.left = tree.left
        
        elif tree.key in ('ctan', 'ctg'):
            node = BinaryTree('/')
            node.left = BinaryTree('*')
            node.left.left = BinaryTree(-1)
            node.left.right = self.__diff__(tree.left)

            node.right = BinaryTree('^')
            node.right.right = BinaryTree(2)
            node.right.left = BinaryTree('sin')
            node.right.left.left = tree.left

        else:
            stderr.write('Invalid element: {}'.format(tree.key))
        return node


    def get_diff(self) -> BinaryTree:
        return self.differ
    
    def __make_str__(self, tree : BinaryTree ,  s : str = '') -> str:
        if not tree is None:
            if tree.key in DiffTree.al_func:
                s += str(tree.key) + '( ' +  self.__make_str__(tree.left) + ' )'
            else:
                s += '( ' + self.__make_str__(tree.left) + str(tree.key) + self.__make_str__(tree.right) + ' )'
        return s

    def __str__(self) -> str:
        return self.__make_str__(self.differ)

    def __repr__(self) -> str:
        return str(self)

    def get_expression(self) -> BinaryTree:
        return self.expr_tree






def main():
    exprs = ['log  (  ctan ( a + ( x ^ 2 ) )   + ( x * 3 )  )', '( 3 * x )', 'tan ( x * 2 ) ', '( x ^ ( 2 + b ) )', '( log x * ( x + 2 ) )', '( cos ( x ^ b ) + b ) ', '[ 1,3 * exp { 2 * b } ] ', '( 2 + 3 ) ) ']
    for i in exprs:
        diff = DiffTree(i, 'x')
        print(diff.get_expression())
        print(diff.get_diff())
        print(diff)

if __name__ == "__main__":
    main()