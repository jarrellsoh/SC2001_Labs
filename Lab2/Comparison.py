import random
import csv
import math
import matplotlib.pyplot as plt
from time import perf_counter
from statistics import median

from Graph import AdjacencyMatrixGraph, AdjacencyListGraph
from DijkstraArray import dijkstra_array
from DijkstraHeap import dijkstra_heap


# Number of timed runs per graph (median is taken)
# Increase for smoother curves, decrease if it takes too long
REPEATS = 5

# Plot colours (blue = Part A, orange = Part B, grey = theory)
COLOR_ARRAY = "#2a78d6"
COLOR_HEAP = "#eb6834"
COLOR_THEORY = "#6b6b66"
LABEL_ARRAY = "Part A (Adj. Matrix + Array)"
LABEL_HEAP = "Part B (Adj. List + Min-Heap)"


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


# Build BOTH graph representations from the same edges,
# so Part A and Part B are always tested on identical graphs
def create_graphs(n, edges):
    matrix_graph = AdjacencyMatrixGraph(n)
    list_graph = AdjacencyListGraph(n)

    for u, v, weight in edges:
        matrix_graph.add_edge(u, v, weight)
        list_graph.add_edge(u, v, weight)

    return matrix_graph, list_graph


# Measure execution time over multiple runs
def measure_time(algorithm, graph, source, repeats=REPEATS):
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


# Run both algorithms on a list of (V, density) configurations
# Each result row: [V, E, density, Part A time, Part B time]
def run_experiments(configs, label):
    results = []

    for n, density in configs:
        edges = generate_edges(n, density, seed=2026)
        e = len(edges)

        # Construct both graphs before timing
        matrix_graph, list_graph = create_graphs(n, edges)

        # Measure both implementations starting from vertex 0
        array_time = measure_time(dijkstra_array, matrix_graph, 0)
        heap_time = measure_time(dijkstra_heap, list_graph, 0)

        results.append([n, e, density, array_time, heap_time])

        print(
            f"{label}: V={n}, E={e}, Density={density:.1%}, "
            f"Part A={array_time:.3f} ms, Part B={heap_time:.3f} ms"
        )

    return results


def save_csv(filename, results):
    headers = ["Vertices", "Edges", "Density", "Part_A_Time(ms)", "Part_B_Time(ms)"]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(results)


# ---------- Theoretical complexity curves ----------

# Part A: O(V^2)
def theory_array(v, e):
    return v * v


# Part B: O((V + E) log V)
def theory_heap(v, e):
    return (v + e) * math.log2(v)


# Scale a theoretical curve to the measured times (least-squares constant c),
# so c * f(V, E) can be drawn on the same axes as the measured timings
def fit_constant(times, theory_values):
    numerator = sum(t * f for t, f in zip(times, theory_values))
    denominator = sum(f * f for f in theory_values)
    return numerator / denominator


# ---------- Plotting ----------

def style_axes(ax, xlabel, title, ylabel="Execution Time (ms)"):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, color="#e1e0d9", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False)


def plot_both_lines(ax, x, results):
    ax.plot(x, [r[3] for r in results], marker="o", markersize=4, linewidth=2,
            color=COLOR_ARRAY, label=LABEL_ARRAY)
    ax.plot(x, [r[4] for r in results], marker="s", markersize=4, linewidth=2,
            color=COLOR_HEAP, label=LABEL_HEAP)


# Figure 1: Sparse / Average / Dense side by side, runtime against V
def plot_by_graph_type(type_results):
    fig, axes = plt.subplots(1, len(type_results), figsize=(15, 4.5))

    for ax, (name, results) in zip(axes, type_results.items()):
        x = [r[0] for r in results]
        plot_both_lines(ax, x, results)
        style_axes(ax, "Number of Vertices (V)", f"{name} graphs")

    fig.suptitle("Runtime vs Vertices for Sparse, Average and Dense Graphs")
    fig.tight_layout()
    fig.savefig("runtime_sparse_average_dense.png", dpi=200)
    plt.close(fig)


# Figure 2: Runtime against E with V fixed
def plot_vs_edges(edge_results):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = [r[1] for r in edge_results]
    plot_both_lines(ax, x, edge_results)
    style_axes(ax, "Number of Edges (E)",
               f"Runtime vs Edges (V = {edge_results[0][0]})")
    fig.tight_layout()
    fig.savefig("runtime_vs_edges.png", dpi=200)
    plt.close(fig)


# Figure 3: Grouped bar chart of runtime at each edge density, V fixed
def plot_density_bars(bar_results):
    fig, ax = plt.subplots(figsize=(9, 4.8))

    labels = [f"{r[2]:.0%}" if r[2] >= 0.01 else f"{r[2]:.1%}" for r in bar_results]
    positions = range(len(bar_results))
    width = 0.38

    bars_a = ax.bar([p - width / 2 - 0.01 for p in positions], [r[3] for r in bar_results],
                    width, color=COLOR_ARRAY, label=LABEL_ARRAY)
    bars_b = ax.bar([p + width / 2 + 0.01 for p in positions], [r[4] for r in bar_results],
                    width, color=COLOR_HEAP, label=LABEL_HEAP)

    # Value labels on top of each bar
    ax.bar_label(bars_a, fmt="%.1f", fontsize=7, padding=2, color="#3a3a37")
    ax.bar_label(bars_b, fmt="%.1f", fontsize=7, padding=2, color="#3a3a37")

    ax.set_xticks(list(positions))
    ax.set_xticklabels(labels)
    style_axes(ax, "Edge Density",
               f"Runtime by Edge Density (V = {bar_results[0][0]})")
    ax.grid(False, axis="x")
    fig.tight_layout()
    fig.savefig("runtime_by_density_bars.png", dpi=200)
    plt.close(fig)


# Figure 4: Measured times against the scaled theoretical curves
# Top row = Part A vs c*V^2, bottom row = Part B vs c*(V+E)logV
def plot_theory_fit(vertex_results, edge_results, vertex_title):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    setups = [
        # (row, measured column, theory function, colour, name, theory label)
        (0, 3, theory_array, COLOR_ARRAY, "Part A", "c · V²"),
        (1, 4, theory_heap, COLOR_HEAP, "Part B", "c · (V + E) log V"),
    ]

    panels = [
        (vertex_results, 0, "Number of Vertices (V)", f"vs Vertices ({vertex_title})"),
        (edge_results, 1, "Number of Edges (E)", f"vs Edges (V = {edge_results[0][0]})"),
    ]

    for row, col, theory, color, name, label in setups:
        for c_idx, (results, x_idx, xlabel, title) in enumerate(panels):
            ax = axes[row][c_idx]
            x = [r[x_idx] for r in results]
            measured = [r[col] for r in results]
            theory_values = [theory(r[0], r[1]) for r in results]
            c = fit_constant(measured, theory_values)

            ax.plot(x, measured, marker="o", markersize=4, linewidth=2,
                    color=color, label=f"{name} measured")
            ax.plot(x, [c * f for f in theory_values], linestyle="--",
                    linewidth=2, color=COLOR_THEORY, label=f"Theoretical {label}")
            style_axes(ax, xlabel, f"{name}: Measured vs Theoretical {title}")

    fig.tight_layout()
    fig.savefig("theory_fit.png", dpi=200)
    plt.close(fig)


# ---------- Benchmark ----------

def benchmark():
    vertex_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    # Experiment 1: Vary V for three kinds of graph
    # Sparse = spanning tree only (E = V - 1), Average = 50%, Dense = complete graph
    graph_types = {
        "Sparse (E = V - 1)": 0.0,
        "Average (50% density)": 0.5,
        "Dense (100% density)": 1.0,
    }
    type_results = {}
    for name, density in graph_types.items():
        type_results[name] = run_experiments(
            [(n, density) for n in vertex_sizes], f"Vary V, {name}")

    # Experiment 2: Vary E while keeping V fixed at 400
    fixed_vertices = 400
    densities = [0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30,
                 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    edge_results = run_experiments(
        [(fixed_vertices, d) for d in densities], "Vary E")

    # Experiment 3: Fixed V = 1000, a few densities for the bar chart
    bar_densities = [0.002, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    bar_results = run_experiments(
        [(1000, d) for d in bar_densities], "Bars, V = 1000")

    # Save raw results
    for name, results in type_results.items():
        tag = name.split()[0].lower()
        save_csv(f"benchmark_vertices_{tag}.csv", results)
    save_csv("benchmark_edges.csv", edge_results)
    save_csv("benchmark_density_bars.csv", bar_results)

    # Generate all figures
    plot_by_graph_type(type_results)
    plot_vs_edges(edge_results)
    plot_density_bars(bar_results)
    plot_theory_fit(type_results["Average (50% density)"], edge_results, "50% density")

    print("\nBenchmark completed!")
    print("Figures saved: runtime_sparse_average_dense.png, runtime_vs_edges.png,")
    print("               runtime_by_density_bars.png, theory_fit.png")


if __name__ == "__main__":
    benchmark()