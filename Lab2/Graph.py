# Define classes for the graphs used
# Graphs are UNDIRECTED and WEIGHTED
# Nodes are represented as integers starting from 0

class AdjacencyListGraph:
    def __init__(self, n):
        self.vertex_count = n
        self.graph = [[] for _ in range(n)]
        
    #Add edge to both directions, since undirected graph
    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight)) 
        
    #Return all neighbours of a given vertex u as a list of 2-tuples (v, weight)
    def neighbors(self, u):
        return self.graph[u]
        
class AdjacencyMatrixGraph:
    def __init__(self, n):
        self.vertex_count = n
        self.graph = [[0] * n for _ in range(n)]
       
    #Add edge to both directions, since undirected graph 
    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight
        self.graph[v][u] = weight
       
    #Return all neighbours of a given vertex u as a list of 2-tuples (v, weight) 
    def neighbours(self, u):
        neighbours = []
        for v in range(self.vertex_count):
            if self.graph[u][v] != 0:
                neighbours.append((v, self.graph[u][v]))
        return neighbours