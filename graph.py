# Citation: https://github.com/donsheehy/datastructures/blob/master/ds2/graph/adjacencysetgraph.py

class Graph:

    def __init__(self):
        self._V = set()
        self._neighbors = {}

    def vertices(self):
        return iter(self._V)

    def edges(self):
        for u in self._V:
            for v in self.neighbors(u):
                yield (u,v)

    def add_vertex(self, v):
        self._V.add(v)
        self._neighbors[v] = set()

    def add_edge(self, u, v):
        self._neighbors[u].add(v)

    def neighbors(self, v):
        return iter(self._neighbors[v])

    def __contains__(self, v):
        return v in self._nbrs

    def __str__(self):
        for i, v in enumerate(self.vertices()):
            print(f"vertex {i}: {v}")
            for nbr in self.neighbors(v):
                print(f" --> neighbor: {nbr}")
        for edge in self.edges():
            print(edge)
        return ""

