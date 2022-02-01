import Graph  as gp
import queue as qe

class GraphTypeError(Exception):
    def __init__(self, message = "Graph include cycles"):
        self.message = message
        super().__init__(self.message)


class Stack:
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
    

class CVert(gp.Vert):
    """
    Atributes
    ---------

    col     [int]   color: 0 - white, 1 - gray, 2 - black
    dist    [int]   distance to vertex. If -1 then there no exist any path to the vertex.
    """
    def __init__(self, key: int, wght :int = 0) -> None:
        super().__init__(key, wght)
        self.col = 0
        self.dist = -1
        self.prev = None

    def __add_ngh__(self, vert) -> None:
        k, w = vert.get_key(), vert.get_weight()
        self.nght[vert.get_key()] = CVert(k, w)
        self.counter += 1

    def set_col(self, col : int) -> None:
        if col not in (0, 1, 2):
            raise ValueError
        self.col = col
    
    def set_distance(self, d : int) -> None:
        if d < -1:
            raise ValueError
        self.dist = d
    
    def set_prev(self, p) -> None:
        self.prev = p
    
    def get_prev(self):
        return self.prev

    def get_dist(self) -> int:
        return self.dist

    def get_col(self) -> int:
        return self.col
    
    def get_conn(self) -> list:
        return self.nght.keys()
    
    def __str__(self) -> str:
        return "Vertex {}\nWeight:{}\nColor:{}\nNeighbours:{}".format(self.key, self.wght, self.col, self.nght.keys())

    





class ExpGraph(gp.Graph):
    """
    Graph representation. Added bfs and dfs method.
    """
    def add_vert(self, key : int, wght : int = 0) -> None:
        self.verts[key] = CVert(key, wght)

    def add_edge(self, from_ : CVert, to_ : CVert, wght : int = 0) -> None:
        if from_ not in self.verts or to_ not in self.verts:
            raise ValueError
        from_ = self.verts[from_]
        to_ = self.verts[to_]
        self.edges.append(gp.Edge(from_, to_, wght))
        from_.__add_ngh__(to_)

    def __getitem__(self, key: int) -> CVert:
        if key not in self.verts:
            raise ValueError
        return self.verts[key]

    def bfs(self, beg : CVert) -> tuple:
        """
        Breadth first search.

        Return
        ------
        Tuple    list of vertices and dictionary with distances

        """
        for i in self.verts:
            self.verts[i].set_distance(-1)
            self.verts[i].set_col(0)
        if beg not in self.verts:
            raise ValueError
        beg = self.verts[beg]
        beg.set_distance(0)
        beg.set_prev(None)
        queue = qe.QueueAb()
        queue.enqueue(beg)
        out = []
        while not queue.is_empty():
            current = queue.dequeue()
            for i in current.get_neighbours():
                if not self.verts[i].get_col():
                    self.verts[i].set_col(1)
                    self.verts[i].set_distance(current.get_dist() + 1)
                    self.verts[i].set_prev(current)
                    queue.enqueue(self.verts[i])
            current.set_col(2)
            out.append(current)
        return out, dict([(i, self.verts[i].dist) for i in self.verts])

    def dfs(self, beg):
        out = []
        for i in self.verts:
            self.verts[i].set_prev(-1)
            self.verts[i].set_col(0)
        beg = self.verts[beg]
        self.__dfs__(beg, out) 
        return out


    def __dfs__(self, vert, out):
        out.append(vert)
        vert.set_col(1)
        for i in vert.get_neighbours():
            if not self.verts[i].get_col():
                self.verts[i].set_prev(vert)
                self.__dfs__(self.verts[i], out)
        vert.set_col(2)
    
    def topological_sort(self):
        if self.is_cycle():
            raise GraphTypeError 
        st = Stack()
        for i in self.verts:
            self.verts[i].set_prev(-1)
            self.verts[i].set_col(0)
        for i in self.verts:
            if not self.verts[i].get_col():
                self.__top_sort__(self.verts[i], st)
        out = []
        while not st.is_empty():
            out.append(st.pop())

        return out

    def __top_sort__(self, vert, st):
        vert.set_col(1)
        for i in vert.get_neighbours():
            if not self.verts[i].get_col():
                self.verts[i].set_prev(vert)
                self.__top_sort__(self.verts[i], st)
        vert.set_col(2)
        st.push(vert)
    
    def is_cycle(self) -> bool:
        """
        Chceck if is cycle in graph.
        """
        cache = {}
        for i in self.verts:
            self.verts[i].set_col(0)
        
        for i in self.verts:
            if not self.verts[i].get_col():
                if self.__is_cycle_util__(self.verts[i], cache):
                    return True
        return False
    
    def __is_cycle_util__(self, vert, cache):
        vert.set_col(1)
        cache[vert.get_key()] = None
        for i in vert.get_neighbours():
            if not self.verts[i].get_col():
                if self.__is_cycle_util__(self.verts[i], cache):
                    return True
            elif i in cache:
                return True
        
        del cache[vert.get_key()]
        return False
    """

    def dfs(self):
        self.time = 0
        for i in self.verts:
            self.verts[i].set_distance(-1)
            self.verts[i].set_prev(-1)
            self.verts[i].set_col(0)

        for i in self.verts:
            if not self.verts[i].get_col():
                self. __dfs__(self.verts[i])
        
        return dict([(i, (self.verts[i].disc, self.verts[i].fin)) for i in self.verts])
    
    def __dfs__(self, vert : CVert):
        vert.set_col(1)
        self.time += 1
        vert.set_discovery(self.time)
        for i in vert.get_neighbours():
            if not self.verts[i].get_col():
                self.verts[i].set_prev(vert)
                self.__dfs__(self.verts[i])
        vert.set_col(2)
        self.time += 1
        vert.set_finish(self.time)
    """
    def min_path(self, beg : int, end : int) -> str:
        self.bfs(beg)
        end = self.verts[end]
        if end.get_dist() == -1:
            return 'inf'
        path = Stack()
        path.push(end)
        current = end
        buff = current.get_prev()
        while not buff is None:
            path.push(buff)
            current = buff
            buff = current.get_prev()
        out = '{}'.format(path.pop().get_key())
        while not path.is_empty():
            out += '->{}'.format(path.pop().get_key())
        
        """
        path = Stack()
        buff = current.get_prev()
        out = '{}'.format(current.get_key())
        while not buff is None:
            path.push(buff)
            current = buff
            buff = current.get_prev()
        while not path.is_empty():
            out += '->{}'.format(path.pop().get_key())
        """
        return out


def main():
    graph = ExpGraph()
    for i in range(8):
        graph.add_vert(i + 1)
    
    graph.add_edge(1,2)
    graph.add_edge(3,2)
    graph.add_edge(2,4)
    graph.add_edge(4,5)
    graph.add_edge(5,6)
    graph.add_edge(6,8)
    graph.add_edge(4,7)
    graph.add_edge(7,8)
    graph.add_edge(6,5)
    graph.add_edge(5,3)
    graph.add_edge(8,6)
    print(graph)
    print(graph[2])
    print(graph.dot_repr())
    print('Distance from 1:', graph.bfs(1)[1])
    print('BFS from 1:', graph.bfs(1)[0])
    print('Distance from 1:', graph.bfs(1)[0])
    print('Distance from 5:', graph.bfs(5)[1])
    print('Path from 5 to 8:', graph.min_path(5, 8))
    print('Path from 1 to 8:', graph.min_path(1, 8))
    print('Path from 8 to 4:', graph.min_path(8, 4))
    print('Path from 3 to 6:', graph.min_path(3, 6))
    print('Path from 7 to 1:', graph.min_path(7, 1))
    print('Has a cycle?' ,graph.is_cycle())
    graph = ExpGraph()
    for i in range(4):
        graph.add_vert(i)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(2, 0)
    graph.add_edge(3, 3)
    print('Do repr of next graph: ', graph.dot_repr())
    print('BFS from 2:', graph.bfs(2)[0])
    print('Has a cycle?' ,graph.is_cycle())

    graph2 = ExpGraph()
    for i in  range(6):
        graph2.add_vert(i + 1)
    
    graph2 = ExpGraph()
    for i in  range(6):
        graph2.add_vert(i + 1)
    graph2.add_edge(1, 4)
    graph2.add_edge(1, 2)
    graph2.add_edge(2, 3)
    graph2.add_edge(2, 4)
    graph2.add_edge(4, 5)
    graph2.add_edge(5, 2)
    graph2.add_edge(5, 6)
    graph2.add_edge(6, 3)
    print('Graph:', graph2.dot_repr())
    print('DFS from 1:', graph2.dfs(1))
    print('Has a cycle?' ,graph2.is_cycle())
    
    gh = ExpGraph()
    for i in range(4):
        gh.add_vert(i)
    gh.add_edge(0, 1)
    gh.add_edge(0, 2)
    gh.add_edge(1, 2)
    gh.add_edge(2, 3)
    gh.add_edge(2, 0)
    gh.add_edge(3, 3)
    print('DFS from 1:', gh.dfs(1))

    gh = ExpGraph()
    for i in range(4):
        gh.add_vert(i)
    gh.add_edge(2, 0)
    gh.add_edge(0, 2)
    gh.add_edge(1, 2)
    gh.add_edge(0, 1)
    gh.add_edge(3, 3)
    gh.add_edge(1, 3)
    print('DFS from 2:', gh.dfs(2))

    gh = ExpGraph()
    for i in range(6):
        gh.add_vert(i)
    gh.add_edge(5, 2)
    gh.add_edge(5, 0)
    gh.add_edge(4, 0)
    gh.add_edge(4, 1)
    gh.add_edge(2, 3)
    gh.add_edge(3, 1)
    print('Has a cycle?' ,gh.is_cycle())
    print('Topological sort :', gh.topological_sort())

    gh = ExpGraph()
    for i in range(5):
        gh.add_vert(i)
    gh.add_edge(0, 1)
    gh.add_edge(0, 2)
    gh.add_edge(0, 3)
    gh.add_edge(1, 2)
    gh.add_edge(2, 3)
    gh.add_edge(3, 4)
    gh.add_edge(4, 1)
    print(gh.dot_repr())
    print('Has a cycle so topological sort does not work:',gh.topological_sort())

    


if __name__ == '__main__':
    main()