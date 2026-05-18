import csv
import heapq
import math
import sys
from pathlib import Path


def _resource_path(relative: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / relative


# Walidacja wagi krawędzi: liczba, skończona, nieujemna
def _parse_weight(raw, context):
    try:
        weight = float(raw)
    except (TypeError, ValueError):
        raise ValueError(f"{context}: waga '{raw}' nie jest liczbą")
    if not math.isfinite(weight):
        raise ValueError(f"{context}: waga '{raw}' musi być skończona (bez inf/nan)")
    if weight < 0:
        raise ValueError(f"{context}: waga '{raw}' jest ujemna — Dijkstra wymaga wag nieujemnych")
    return weight


# Dodaje krawędź; przy duplikacie zachowuje mniejszą wagę
def _add_edge(graph, src, tgt, weight):
    neighbors = graph.setdefault(src, {})
    if tgt in neighbors:
        neighbors[tgt] = min(neighbors[tgt], weight)
    else:
        neighbors[tgt] = weight
    graph.setdefault(tgt, {})


# Odczyt danych z pliku edges.csv
def dataReader(path='data/edges.csv'):
    graphs = {}
    is_directed = {}
    with open(_resource_path('data/isdirected.csv'), newline='') as file:
        for row in csv.DictReader(file):
            is_directed[row['graph_id']] = row['is_directed'] == 'True'

    with open(_resource_path(path), newline='') as file:
        for row in csv.DictReader(file):
            gid = row['graph_id']
            src = row['source']
            tgt = row['target']
            if gid not in is_directed:
                raise ValueError(f"Graf '{gid}' nie ma wpisu w isdirected.csv")
            weight = _parse_weight(row['weight'], f"Graf {gid}, krawędź {src}->{tgt}")
            graph = graphs.setdefault(gid, {})
            _add_edge(graph, src, tgt, weight)
            if not is_directed[gid]:
                _add_edge(graph, tgt, src, weight)

    return graphs, is_directed


# Algorytm Dijkstry zwraca minimalną odległość dla maksymalnego wierzchołka
def dijkstra(graph, start):
    dist = {vertex: float('inf') for vertex in graph}
    prev = {vertex: None for vertex in graph}
    dist[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_dist, current_vertex = heapq.heappop(priority_queue)
        if current_dist > dist[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_dist + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    # Jezeli jakis wierzcholek nieodwiedzony, allvisit = false
    allvisit = float('inf') not in dist.values()
    if allvisit:
        max_vertex = max(dist, key=dist.get)
        max_dist = dist[max_vertex]
    else:
        max_vertex = start
        max_dist = 0

    return max_vertex, max_dist, allvisit, prev

# Zwraca wierzchołek centrum, czyli min z max odległości 
def compute_center(graph):
    start_vertex = None
    extreme_vertex = None
    min_value = float('inf')
    previous_vertex = None
    for vertex in list(graph.keys()):
        max_vertex, max_dist, allvisit, prev = dijkstra(graph, vertex)
        if allvisit and min_value > max_dist:
            min_value = max_dist
            start_vertex = vertex
            extreme_vertex = max_vertex
            previous_vertex = prev
    if start_vertex is None:
        return None
    return start_vertex, extreme_vertex, min_value, previous_vertex

# Buduje graf z tekstu podanego przez uzytkwnika 
def parse_edges(edges_text, is_directed):
    graph = {}
    for line_no, raw in enumerate(edges_text.strip().splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(',')]
        if len(parts) != 3:
            raise ValueError(f"Linia {line_no}: oczekiwano 'source,target,weight', otrzymano '{raw}'")
        src, tgt = parts[0], parts[1]
        weight = _parse_weight(parts[2], f"Linia {line_no}")
        _add_edge(graph, src, tgt, weight)
        if not is_directed:
            _add_edge(graph, tgt, src, weight)

    if not graph:
        raise ValueError("Nie podano żadnych krawędzi.")

    return graph
