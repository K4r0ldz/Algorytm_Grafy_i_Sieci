import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(graph, start_vertex=None, directed = True, title=None, previous_vertex=None):

    plt.get_current_fig_manager().full_screen_toggle() # fullscreen mode
    G = nx.DiGraph() if directed else nx.Graph()
    for vertex in graph:
        G.add_node(vertex) # Dodawanie wierzchołków do grafu

    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(vertex, neighbor, weight=weight) # Dodawanie krawędzi, oraz wagi do wierzchołków

    pos = nx.spring_layout(G, k=2.0, scale=2.0, seed=42, iterations=300, weight=None) # Position dla wierzchołków


    colors = []
    for vertex in G.nodes():
        if vertex == start_vertex:
            colors.append('red') # Czerwony wierzchołek to najlepsze miejsce na umieszczenie strazy
        else:
            colors.append('lightblue')

    # Podświetlenie krawędzi należących do drzewa najkrótszych ścieżek.
    edge_colors = []
    edge_widths = []
    for v, s in G.edges():
        if previous_vertex[s] is not None and previous_vertex[s] == v: 
            edge_colors.append('green') 
            edge_widths.append(2)
        else:
            edge_colors.append('black')
            edge_widths.append(1)
    if directed:
         nx.draw(G, pos, arrowsize=15, with_labels=True, node_color=colors, node_size=600, arrows=directed, edge_color=edge_colors, width=edge_widths, 
            connectionstyle='arc3, rad=0.15')
    else:
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=600, edge_color=edge_colors, width=edge_widths)
    
    edge_labels = nx.get_edge_attributes(G, 'weight') # Lista wag
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Wyświetlanie wag 

    if title:
        plt.title(title)
    plt.show()

