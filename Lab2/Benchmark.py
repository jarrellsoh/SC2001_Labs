import random
import csv
import matplotlib.pyplot as plt
from time import perf_counter
from statistics import median

from Graph import AdjacencyMatrixGraph
from DijkstraArray import dijkstra_array


# Generate a random connected, undirected weighted graph
def generate_edges(n, density, seed):
    rng = random.Random(seed)  # Fixed seed for reproducible graphs

    # Calculate target number of edges based on graph density
    # At least n - 1 edges are needed for a connected graph
    max_edges = n * (n - 1) // 2
    target_edges = max(n - 1, round(max_edges * density))

    edges = []
    existing = set()

    # Create a spanning tree to ensure all vertices are connected
    # Each vertex connects to a randomly selected earlier vertex
    for v in range(1, n):
        u = rng.randrange(v)
        weight = rng.randint(1, 20)

        edges.append((u, v, weight))
        existing.add((u, v))

    # Find remaining possible edges without duplicates or self-loops
    available = []

    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) not in existing:
                available.append((u, v))

    # Randomly add more edges until the target density is reached
    needed = target_edges - len(edges)

    for u, v in rng.sample(available, needed):
        weight = rng.randint(1, 20)
        edges.append((u, v, weight))

    return edges


# Convert generated edges into an adjacency matrix
def create_graph(n, edges):
    matrix_graph = AdjacencyMatrixGraph(n)

    # Add each weighted edge to the graph
    for u, v, weight in edges:
        matrix_graph.add_edge(u, v, weight)

    return matrix_graph


# Measure execution time over multiple runs
def measure_time(algorithm, graph, source, repeats=100):
    times = []

    # Repeat using the same graph to reduce timing fluctuations
    for _ in range(repeats):
        start = perf_counter()

        algorithm(graph, source)

        end = perf_counter()

        # Calculate execution time in milliseconds
        times.append((end - start) * 1000)

    # Median reduces the effect of unusually slow runs
    return median(times)


# Generate runtime graphs for both experiments
def plot_results(results):

    # Experiment 1: Runtime against number of vertices
    vertex_results = [r for r in results if r[0] == "Vary V"]

    vertices = [r[1] for r in vertex_results]
    vertex_times = [r[4] for r in vertex_results]

    plt.figure()
    plt.plot(vertices, vertex_times, marker="o", label="Part_A(Array)")
    plt.xlabel("Number of Vertices (V)")
    plt.ylabel("Execution Time (ms)")
    plt.title("Dijkstra: Runtime vs Vertices")
    plt.legend()
    plt.grid(True)
    plt.savefig("runtime_vs_vertices.png", dpi=200)
    plt.show()
    plt.close()

    # Experiment 2: Runtime against number of edges
    edge_results = [r for r in results if r[0] == "Vary E"]

    edges = [r[2] for r in edge_results]
    edge_times = [r[4] for r in edge_results]

    plt.figure()
    plt.plot(edges, edge_times, marker="o", label="Part_A(Array)")
    plt.xlabel("Number of Edges (E)")
    plt.ylabel("Execution Time (ms)")
    plt.title("Dijkstra: Runtime vs Edges")
    plt.legend()
    plt.grid(True)
    plt.savefig("runtime_vs_edges.png", dpi=200)
    plt.show()
    plt.close()


# Benchmark Dijkstra with different numbers of vertices and edges
def benchmark():
    results = []

    # Experiment 1: Vary V while keeping density fixed at 20%
    vertex_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
    fixed_density = 0.20

    # Experiment 2: Vary E while keeping V fixed at 400
    fixed_vertices = 400
    densities = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]

    # Store configurations for both experiments
    experiments = []

    for n in vertex_sizes:
        experiments.append(("Vary V", n, fixed_density))

    for density in densities:
        experiments.append(("Vary E", fixed_vertices, density))

    # Run Dijkstra for every graph configuration
    for experiment, n, density in experiments:

        # Generate edges based on current graph size and density
        edges = generate_edges(n, density, seed=2026)
        e = len(edges)

        # Construct adjacency matrix before timing
        matrix_graph = create_graph(n, edges)

        # Measure Dijkstra runtime starting from vertex 0
        array_time = measure_time(
            dijkstra_array, matrix_graph, 0
        )

        # Store experiment results
        results.append([
            experiment, n, e, density, array_time
        ])

        # Display the current experiment results
        print(
            f"{experiment}: V={n}, E={e}, "
            f"Density={density:.0%}, "
            f"Part A={array_time:.3f} ms"
        )

    # Separate results into the two experiments
    vertex_results = [r[1:] for r in results if r[0] == "Vary V"]
    edge_results = [r[1:] for r in results if r[0] == "Vary E"]

    headers = [
        "Vertices",
        "Edges",
        "Density",
        "Part_A_Time(ms)"
    ]

    # Save Experiment 1 results
    with open("benchmark_vertices.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(vertex_results)

    # Save Experiment 2 results
    with open("benchmark_edges.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(edge_results)

    # Generate both runtime graphs
    plot_results(results)

    print("\nBenchmark completed!")
    print("Results saved to benchmark_vertices.csv and benchmark_edges.csv")
    print("Graphs saved to runtime_vs_vertices.png and runtime_vs_edges.png")


if __name__ == "__main__":
    benchmark()
