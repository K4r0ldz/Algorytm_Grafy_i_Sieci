import networkx as nx
from matplotlib.figure import Figure


def build_figure(graph, start_vertex=None, directed=True, title=None, previous_vertex=None):
    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    G = nx.DiGraph() if directed else nx.Graph()
    for vertex in graph:
        G.add_node(vertex) # Dodawanie wierzchołków do grafu

    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(vertex, neighbor, weight=weight)

    pos = nx.spring_layout(G, k=2.0, scale=2.0, seed=42, iterations=300, weight=None)

    colors = ['red' if v == start_vertex else 'lightblue' for v in G.nodes()]

    edge_colors = []
    edge_widths = []
    for v, s in G.edges():
        is_tree_edge = False
        if previous_vertex:
            if previous_vertex.get(s) == v:
                is_tree_edge = True
            elif not directed and previous_vertex.get(v) == s:
                is_tree_edge = True
        if is_tree_edge:
            edge_colors.append('green')
            edge_widths.append(2)
        else:
            edge_colors.append('black')
            edge_widths.append(1)

    if directed:
        nx.draw(G, pos, ax=ax, arrowsize=15, with_labels=True, node_color=colors,
                node_size=600, arrows=True, edge_color=edge_colors, width=edge_widths,
                connectionstyle='arc3, rad=0.15')
    else:
        nx.draw(G, pos, ax=ax, with_labels=True, node_color=colors, node_size=600,
                edge_color=edge_colors, width=edge_widths)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels)

    if title:
        ax.set_title(title)

    fig.tight_layout()
    return fig