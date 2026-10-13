from Graph import AdjacencyListGraph
from MinHeap import MinHeap

# Dijkstra's algorithm using adjacency lists and min-heap priority queue
# Graph = Graph to process, source = start vertex
def dijkstra_heap(graph, source):
    # Number of vertices in the graph
    n = graph.vertex_count
    
    #Check if source vertex is valid
    if source < 0 or source >= n:
        raise ValueError("Invalid source vertex")

    #Check negative weights, else non-valid graph
    for u in range(n):
        for v, weight in graph.neighbors(u):
            if weight < 0:
                raise ValueError("Negative edge weight")
            
    #Initialise shortest distances to infinity (distance at source is 0)
    distances = [float('inf')] * n
    distances[source] = 0
    
    #Store previous vertex in shortest path
    previous = [None] * n
    
    #Track visited vertices, whose shortest distances are guaranteed
    visited = [False] * n
    
    #Create min-heap priority queue
    pq = MinHeap()
    
    #Insert source vertex, distance = 0
    pq.enqueue((source, 0))
    
    #Iterate until all reachable vertices are processed
    while not pq.is_empty():
        #Process vertex with smallest distance
        u, current_distance = pq.dequeue()
        
        #Skip if vertex already visited (may appear if shorter path was found before processing the initial one)
        if visited[u]:
            continue
        
        #Mark vertex as visited
        visited[u] = True
        
        
        #Process all neighbours of u
        for v, weight in graph.neighbors(u):
            #Skip if vertex already visited
            if visited[v]:
                continue
            
            #Calculate new distance through u
            new_distance = current_distance + weight
            
            #Update if shorter path is found
            if new_distance < distances[v]:
                #Update shortest known distance
                distances[v] = new_distance
                
                #Record previous vertex
                previous[v] = u
                
                #Update vertex priority in min-heap
                pq.enqueue((v, new_distance))
                
    return distances, previous


#Reconstruct shortest path from source to destination
def reconstruct_path(previous, source, destination):
    path = []
    current = destination
    
    #Trace backwards from destination to source
    while current is not None:
        path.append(current)
        
        if current == source:
            return path[::-1]
        
        current = previous[current]
    
    #Return empty list if destination is unreachable
    return []


# Correctness Test for Dijkstra's algorithm
if __name__ == "__main__":

    # Create an adjacency list graph with 6 vertices
    graph = AdjacencyListGraph(6)

    # Add undirected weighted edges
    # graph.add_edge(u, v, weight)
    graph.add_edge(0, 1, 10)
    graph.add_edge(0, 2, 5)
    graph.add_edge(1, 3, 3)
    graph.add_edge(2, 3, 8)
    graph.add_edge(3, 4, 7)
    graph.add_edge(4, 5, 2)

    # Run Dijkstra starting from vertex 0
    distances, previous = dijkstra_heap(graph, 0)

    print("Shortest distances:", distances)
    print("Previous vertices:", previous)

    # Display shortest paths
    for destination in range(graph.vertex_count):
        path = reconstruct_path(previous, 0, destination)
        print(f"Path to {destination}: {path}")
