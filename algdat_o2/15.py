import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def independent_set_to_clique(G, k):
    """
    Konverterer independent set problem til clique problem.
    Independent set i G <-> Clique i komplementet av G
    """
    n = len(G)
    G_comp = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                G_comp[i][j] = 1 - G[i][j]

    return G_comp, k


def print_graph(G, title="Graph"):
    """
    Printer graf på en pen måte med node-forbindelser
    """
    n = len(G)
    print(f"\n{title}:")
    print("Adjacency Matrix:")
    print("   ", end="")
    for i in range(n):
        print(f"{i:2d}", end=" ")
    print()
    
    for i in range(n):
        print(f"{i:2d}: ", end="")
        for j in range(n):
            print(f"{G[i][j]:2d}", end=" ")
        print()
    
    print("\nEdges:")
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1:
                edges.append(f"{i}-{j}")
    
    if edges:
        print(", ".join(edges))
    else:
        print("No edges")


def plot_graphs(G_original, G_complement, k, test_name):
    """
    Plotter original graf og dens komplement side ved side
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Konverter adjacency matrix til NetworkX grafer
    G_nx_orig = nx.from_numpy_array(np.array(G_original))
    G_nx_comp = nx.from_numpy_array(np.array(G_complement))
    
    # Samme layout for begge grafer
    pos = nx.spring_layout(G_nx_orig, seed=42)
    
    # Original graf
    ax1.set_title(f"Original Graph (G)\n{test_name}", fontsize=12, fontweight='bold')
    nx.draw(G_nx_orig, pos, ax=ax1, with_labels=True, node_color='lightblue', 
            node_size=800, font_size=14, font_weight='bold', edge_color='blue')
    
    # Complement graf
    ax2.set_title(f"Complement Graph (G')\nLooking for clique of size {k}", fontsize=12, fontweight='bold')
    nx.draw(G_nx_comp, pos, ax=ax2, with_labels=True, node_color='lightcoral', 
            node_size=800, font_size=14, font_weight='bold', edge_color='red')
    
    plt.tight_layout()
    plt.savefig(f'graph_transformation_{test_name.replace(" ", "_").replace(":", "")}.png', dpi=150, bbox_inches='tight')
    plt.show()


def visualize_transformation(G, k, test_name=""):
    """
    Visualiserer transformasjon fra independent set til clique
    """
    print("=" * 60)
    print(f"TRANSFORMATION: Independent Set -> Clique (k={k})")
    print("=" * 60)
    
    print_graph(G, "Original Graph (G)")
    
    G_comp, k_comp = independent_set_to_clique(G, k)
    
    print_graph(G_comp, "Complement Graph (G')")
    
    print(f"\nTransformation complete:")
    print(f"- Independent set of size {k} in G <-> Clique of size {k_comp} in G'")
    print(f"- Original edges become non-edges, non-edges become edges")
    
    # Plot grafene
    plot_graphs(G, G_comp, k, test_name)
    
    return G_comp, k_comp


# Test cases
test_cases = [
    {
        "name": "Test 1: Small triangle + isolated nodes",
        "G": [
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1], 
            [1, 1, 0, 0, 1],
            [0, 1, 0, 0, 1],
            [0, 1, 1, 1, 0],
        ],
        "k": 3,
    },
    {
        "name": "Test 2: Complete graph K4",
        "G": [
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 1, 0, 1], 
            [1, 1, 1, 0],
        ],
        "k": 1,
    },
    {
        "name": "Test 3: No edges (all independent)",
        "G": [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ],
        "k": 4,
    },
    {
        "name": "Test 4: Path graph",
        "G": [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
        ],
        "k": 2,
    },
    {
        "name": "Test 5: Star graph",
        "G": [
            [0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
        ],
        "k": 4,
    },
]


def run_all_tests():
    """
    Kjører alle test cases og visualiserer transformasjonene
    """
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"{test_case['name']}")
        
        G = test_case["G"]
        k = test_case["k"]
        
        G_comp, k_comp = visualize_transformation(G, k, test_case['name'])
        
        print(f"\nAnalysis:")
        n = len(G)
        original_edges = sum(sum(row) for row in G) // 2
        complement_edges = sum(sum(row) for row in G_comp) // 2
        max_possible_edges = n * (n - 1) // 2
        
        print(f"- Original graph: {n} nodes, {original_edges} edges")
        print(f"- Complement graph: {n} nodes, {complement_edges} edges")
        print(f"- Total edges in both: {original_edges + complement_edges} = {max_possible_edges} (complete graph)")
        
        if i < len(test_cases):
            input("\nPress Enter for next test case...")


if __name__ == "__main__":
    run_all_tests()
