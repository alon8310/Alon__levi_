from networkx import DiGraph, is_isomorphic, is_weakly_connected
from itertools import combinations, permutations
from functools import wraps
import numpy as np
from scipy.optimize import curve_fit

time_cache = {}

# decorator to time the execution of the functions
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_cache[args[0]] = end_time - start_time
        print(f"Function {func.__name__} took {time_cache[args[0]]:.4f} seconds")
        return result
    return wrapper

# check if there is already a graph with the same structure
def is_new_graph_unique(graph, unique_graphs):
    for existing in unique_graphs:
        if is_isomorphic(graph, existing, edge_match=None):
            return False
    return True

# generate all connected directed motifs for a given number of nodes
@timeit
def generate_connected_directed_motifs(n):
    nodes = list(range(n))
    all_possible_edges = list(permutations(nodes, 2))  # directed edges

    unique_graphs = []

    for r in range(1, len(all_possible_edges) + 1):
        for edges in combinations(all_possible_edges, r):
            G = DiGraph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)

            if is_weakly_connected(G) and is_new_graph_unique(G, unique_graphs):
                unique_graphs.append(G)

    return unique_graphs

# write the generated graphs to a file
def write_graphs_to_file(graphs, n, filename="motifs_directed.txt"):
    with open(filename, "w") as f:
        f.write(f"n={n}\n")
        f.write(f"count={len(graphs)}\n")

        for idx, G in enumerate(graphs, start=1):
            f.write(f"#{idx}\n")
            for u, v in G.edges():
                f.write(f"{u + 1} {v + 1}\n")


# the order of the time complexity for the function
def exp_model(x, a, b):
    return a * b**(x * (x - 1))  # matches 2^{n(n-1)} growth


def main():
    # since we know the complexity of the problem, we can graph the results for small n, and approximate the constant
    m = [i for i in range(1, 5)]
    for n in m:
        print(f"Generating connected directed motifs for n={n}...")
        graphs = generate_connected_directed_motifs(n)
        print(f"Found {len(graphs)} unique connected directed motifs for n={n}.")

    ns = np.array(list(time_cache.keys()), dtype=int)
    times = np.array(list(time_cache.values()))

    params, _ = curve_fit(exp_model, ns, times)
    a, b = params
    print(f"Fitted time model: T(n) ≈ {a:.2e} * {b:.2f}^(n(n-1))")

    # predict for larger n
    for n_predict in [5, 6, 7, 8]:
        est_time = exp_model(n_predict, *params)
        print(f"Estimated time for n={n_predict}: {est_time:.2f} seconds (~{est_time/60:.2f} minutes)")

if __name__ == "__main__":
    main()
