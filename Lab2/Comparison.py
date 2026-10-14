# Part (c): Compare Part A (adjacency matrix + array) with
# Part B (adjacency list + min-heap) on identical graphs
#
# Reuses the graph generator and timing function from Benchmark.py,
# so Benchmark.py (Part A) is left unchanged.

import csv
import matplotlib.pyplot as plt

from Graph import AdjacencyMatrixGraph, AdjacencyListGraph
from DijkstraArray import dijkstra_array
from DijkstraHeap import dijkstra_heap
from Benchmark import generate_edges, measure_time


# Number of timed runs per graph (median is taken)
# Increase for smoother curves, decrease if it takes too long
REPEATS = 5

# Plot colours (blue = Part A, orange = Part B)
COLOR_ARRAY = "#2a78d6"
COLOR_HEAP = "#eb6834"
LABEL_ARRAY = "Part A (Adj. Matrix + Array)"
LABEL_HEAP = "Part B (Adj. List + Min-Heap)"


# Build BOTH graph representations from the same edges,
# so Part A and Part B are always tested on identical graphs
def create_graphs(n, edges):
    matrix_graph = AdjacencyMatrixGraph(n)
    list_graph = AdjacencyListGraph(n)

    for u, v, weight in edges:
        matrix_graph.add_edge(u, v, weight)
        list_graph.add_edge(u, v, weight)

    return matrix_graph, list_graph


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
        array_time = measure_time(dijkstra_array, matrix_graph, 0, REPEATS)
        heap_time = measure_time(dijkstra_heap, list_graph, 0, REPEATS)

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


# ---------- Plotting ----------

def style_axes(ax, xlabel, title):
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Execution Time (ms)")
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
    fig.savefig("comparison_sparse_average_dense.png", dpi=200)
    plt.close(fig)


# Figure 2: Runtime against E with V fixed
def plot_vs_edges(edge_results):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = [r[1] for r in edge_results]
    plot_both_lines(ax, x, edge_results)
    style_axes(ax, "Number of Edges (E)",
               f"Runtime vs Edges (V = {edge_results[0][0]})")
    fig.tight_layout()
    fig.savefig("comparison_vs_edges.png", dpi=200)
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
    fig.savefig("comparison_density_bars.png", dpi=200)
    plt.close(fig)


# ---------- Comparison ----------

def compare():
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
    densities = [0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30,
                 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    edge_results = run_experiments(
        [(400, d) for d in densities], "Vary E")

    # Experiment 3: Fixed V = 1000, a few densities for the bar chart
    bar_densities = [0.002, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    bar_results = run_experiments(
        [(1000, d) for d in bar_densities], "Bars, V = 1000")

    # Save raw results
    for name, results in type_results.items():
        tag = name.split()[0].lower()
        save_csv(f"comparison_vertices_{tag}.csv", results)
    save_csv("comparison_edges.csv", edge_results)
    save_csv("comparison_density_bars.csv", bar_results)

    # Generate all figures
    plot_by_graph_type(type_results)
    plot_vs_edges(edge_results)
    plot_density_bars(bar_results)

    print("\nComparison completed!")
    print("Figures saved: comparison_sparse_average_dense.png,")
    print("               comparison_vs_edges.png, comparison_density_bars.png")


if __name__ == "__main__":
    compare()
