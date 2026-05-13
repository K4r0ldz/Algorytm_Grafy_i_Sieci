import csv
import heapq
import sys
from pathlib import Path


def _resource_path(relative: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / relative


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
            graph = graphs.setdefault(gid, {})
            if is_directed[gid]:
                graph.setdefault(src, {})[tgt] = int(row['weight'])
                graph.setdefault(tgt, {})
                continue
            graph.setdefault(src, {})[tgt] = int(row['weight'])
            graph.setdefault(tgt, {})[src] = int(row['weight'])

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
        try:
            weight = float(parts[2])
        except ValueError:
            raise ValueError(f"Linia {line_no}: waga '{parts[2]}' nie jest liczbą")
        graph.setdefault(src, {})[tgt] = weight
        graph.setdefault(tgt, {})
        if not is_directed:
            graph[tgt][src] = weight

    if not graph:
        raise ValueError("Nie podano żadnych krawędzi.")

    return graph
