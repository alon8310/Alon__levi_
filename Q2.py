import networkx as nx
from itertools import combinations
from networkx.algorithms.isomorphism import DiGraphMatcher
from collections import defaultdict
import sys

# map each line of input to a directed edge in the graph
def read_input_graph():
    G = nx.DiGraph()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        u, v = map(int, line.split())
        G.add_edge(u, v)
    return G

def generate_motifs(n):
    from itertools import permutations
    all_possible_edges = list(permutations(range(n), 2))
    motifs = []
    for r in range(1, len(all_possible_edges)+1):
        for edges in combinations(all_possible_edges, r):
            g = nx.DiGraph()
            g.add_nodes_from(range(n))
            g.add_edges_from(edges)
            if nx.is_weakly_connected(g):
                if all(not nx.is_isomorphic(g, existing) for existing in motifs):
                    motifs.append(g)
    return motifs

def extract_subgraphs(G, n):
    subgraphs = []
    for nodes in combinations(G.nodes(), n):
        sub = G.subgraph(nodes).copy()
        if nx.is_weakly_connected(sub):
            subgraphs.append(sub)
    return subgraphs

def count_motifs(motifs, subgraphs):
    motif_counts = [0] * len(motifs)
    for sg in subgraphs:
        for idx, motif in enumerate(motifs):
            matcher = DiGraphMatcher(sg, motif)
            if matcher.is_isomorphic():
                motif_counts[idx] += 1
                break
    return motif_counts

def write_output(motifs, counts, n):
    print(f"n={n}")
    print(f"count={len(motifs)}")
    for idx, (motif, count) in enumerate(zip(motifs, counts), start=1):
        print(f"#{idx}\ncount={count}")
        for u, v in motif.edges():
            print(f"{u + 1} {v + 1}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <n>")
        sys.exit(1)

    n = int(sys.argv[1])
    print("Reading input graph...")
    input_graph = read_input_graph()

    print("Generating motifs...")
    motifs = generate_motifs(n)

    print("Extracting subgraphs...")
    subgraphs = extract_subgraphs(input_graph, n)

    print("Counting motifs...")
    counts = count_motifs(motifs, subgraphs)

    print("Writing output...")
    write_output(motifs, counts, n)

if __name__ == "__main__":
    main()
