from Graph import AdjacencyMatrixGraph
from Array import Array


# Dijkstra's algorithm using adjacency matrix and array priority queue
def dijkstra_array(graph, source):

    # Number of vertices in the graph
    n = graph.vertex_count

    # Check whether source vertex is valid
    if source < 0 or source >= n:
        raise ValueError("Invalid source vertex")

    # Check for negative edge weights
    # Dijkstra's algorithm requires non-negative weights
    for u in range(n):
        for v in range(n):
            if graph.graph[u][v] < 0:
                raise ValueError("Negative edge weight")

    # Initialise shortest distances to infinity
    distances = [float('inf')] * n

    # Store previous vertex in shortest path
    previous = [None] * n

    # Track vertices whose shortest distances are finalised
    visited = [False] * n

    # Distance from source to itself is 0
    distances[source] = 0

    # Create array-based priority queue
    pq = Array()

    # Insert source vertex with distance 0
    pq.enqueue((source, 0))

    # Continue until all reachable vertices are processed
    while not pq.is_empty():

        # Remove vertex with smallest distance
        u, current_distance = pq.dequeue()

        # Mark vertex as visited
        visited[u] = True

        # Scan all possible neighbours in adjacency matrix
        for v in range(n):

            # Get edge weight from u to v
            weight = graph.graph[u][v]

            # Skip if no edge or vertex already visited
            if weight == 0 or visited[v]:
                continue

            # Calculate new distance through u
            new_distance = current_distance + weight

            # Update if a shorter path is found
            if new_distance < distances[v]:

                # Update shortest known distance
                distances[v] = new_distance

                # Record previous vertex
                previous[v] = u

                # Update vertex priority in array
                pq.update(v, new_distance)

    return distances, previous


# Reconstruct shortest path from source to destination
def reconstruct_path(previous, source, destination):

    path = []
    current = destination

    # Trace backwards from destination to source
    while current is not None:
        path.append(current)

        if current == source:
            return path[::-1]

        current = previous[current]

    # Return empty list if destination is unreachable
    return []


# Test Dijkstra's algorithm, make changes here
if __name__ == "__main__":

    # Create an adjacency matrix graph with x vertices
    graph = AdjacencyMatrixGraph(6)

    # Add undirected weighted edges
    # graph.add_edge(u, v, weight)
    graph.add_edge(0, 1, 10)
    graph.add_edge(0, 2, 5)
    graph.add_edge(1, 3, 3)
    graph.add_edge(2, 3, 8)
    graph.add_edge(3, 4, 7)
    graph.add_edge(4, 5, 2)

    # Run Dijkstra starting from vertex x
    distances, previous = dijkstra_array(graph, 0)

    print("Shortest distances:", distances)
    print("Previous vertices:", previous)

    # Display shortest paths
    for destination in range(graph.vertex_count):
        path = reconstruct_path(previous, 0, destination)
        print(f"Path to {destination}: {path}")
