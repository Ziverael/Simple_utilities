
class Edge:
    def __init__(self, fr, to, wght = 0):
        self.from_ = fr
        self.to = to
        self.wght = wght

    def __str__(self):
        return "{}--{}-->{}".format(self.from_.get_key(), self.wght, self.to.get_key())    

    def get_beg(self):
        return self.from_
    
    def get_end(self):
        return self.to

class Vert:
    """
    Vertex class.
    
    Atributes
    ---------
    key     [int]   vertex unique key
    wght    [int]   weight if the vertex
    counter [int]   Number of edges
    """
    def __init__(self, key, wght : int = 0) -> None:
        if type(key) != type(0) or type(wght) != type(0):
            raise TypeError
        self.nght = {}
        self.key = key
        self.wght = wght
        self.counter = 0

    def __add_ngh__(self, vert) -> None:
        """
        Add a neighbour. The  neighbour is only a vertex to which you can travel
        from this vertex.
        """
        k, w = vert.get_key(), vert.get_weight()
        self.nght[vert.get_key()] = Vert(k, w)
        self.counter += 1
    
    def get_neighbours(self) -> dict:
        return self.nght
    
    def get_key(self) -> int:
        return self.key

    def get_weight(self) -> int:
        return self.wght


    def __str__(self) -> str:
        ngh_list = ["\nVertex {} weight {}\n".format(i,self.nght[i]) for i in self.nght]
        out_list =''
        for i in ngh_list:
            out_list += i
        return "\nVertex {} weight {}\n".format(self.key,self.wght) + "-" * 10 + "\nNeighbours\n" + "-" * 10 + out_list


    def __repr__(self) -> str:
        return str(self)

    def str_short(self) -> str:
        return "\nVertex {} weight {}\n".format(self.key,self.wght) + "-" * 10 + "\n"

            
class Graph:
    """
    Graph representation.
    
    Atributes
    ---------
    verts   [dict]  list of vertices in a graph
    edges   [list]  list of edges in a graph
    """
    def __init__(self):
        self.verts = {}
        self.edges = []

    def __str__(self) -> str:
        out = "GRAPH\n" + "=" * 10 + '\n'
        for i in self.verts:
            out += self.verts[i].str_short()
        out += "Edges\n"
        for i in self.edges:
            out += str(i) + '\n'

        return  out

    def add_vert(self, key : int, wght : int = 0) -> None:
        self.verts[key] = Vert(key, wght)
    
    def add_edge(self, from_ : Vert, to_ : Vert, wght : int = 0) -> None:
        if from_ not in self.verts or to_ not in self.verts:
            raise ValueError
        from_ = self.verts[from_]
        to_ = self.verts[to_]
        self.edges.append(Edge(from_, to_, wght))
        from_.__add_ngh__(to_)

    def __contains__(self, key : int) -> bool:
        return key in self.verts

    def __getitem__(self, key) -> Vert:
        if key not in self.verts:
            raise ValueError
        return self.verts[key]

    def get_edges(self) -> list:
        return self.edges
    
    def get_vertices(self) -> dict:
        return self.verts


    def dot_repr(self) -> str:
        """
        Generate dot representation.
        """
        out = "digraph G{"
        verts = {}
        for i in self.edges:
            fr, to = i.get_beg().get_key(), i.get_end().get_key()
            verts[fr], verts[to] = None, None
            out += "{}->{};".format(fr, to)
        for i in self.verts:
            if self.verts[i].get_key() not in verts:
                out += " " + str(self.verts[i].get_key()) + " "
        out += "}"
        return out

    


def main() -> int:
    graph = Graph()
    for i in range(10):
        graph.add_vert(i + 1)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(1, 5)
    graph.add_edge(1, 3)
    graph.add_edge(1, 6)
    graph.add_edge(1, 8)
    graph.add_edge(2, 2)
    graph.add_edge(2, 4)
    graph.add_edge(2, 1)
    graph.add_edge(5, 2)
    graph.add_edge(5, 7)
    graph.add_edge(5, 9)
    graph.add_edge(5, 5)

    print(graph.dot_repr())
    return 0

if __name__ == '__main__':
    main()
