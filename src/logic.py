from src import visualization
import csv 
import heapq


# Odczyt danych z pliku edges.csv
def dataReader(path='data/edges.csv'):
    graphs = {}
    is_directed = {}
    with open('data/isdirected.csv', newline='') as file:
        for row in csv.DictReader(file):
                is_directed[row['graph_id']] = row['is_directed'] == 'True'

    with open(path, newline='') as file:
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
            graph.setdefault(tgt, {})

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

def run():
    data, is_directed = dataReader()

    for id in list(data.keys()):
        start_vertex = None
        extreme_vertex = None
        min_value = float('inf') 
        previous_vertex = None
        for vertex in list(data[id].keys()):
            result = dijkstra(data[id], vertex)
            max_vertex, max_dist, allvisit, prev = result
            if allvisit: # Jeżeli wszystkie wierzchołki zostały odwiedzone, to sprawdzamy czy max_dist jest mniejszy niż min_value
                if min_value > max_dist:
                    min_value = max_dist
                    start_vertex = vertex
                    extreme_vertex = max_vertex
                    previous_vertex = prev

        print(f"Graph: {id}, Start: {start_vertex}, Extreme: {extreme_vertex}, Min Distance: {min_value}") 
        visualization.draw_graph(data[id], directed = is_directed[id], start_vertex=start_vertex, title=f"Graph: {id}", previous_vertex=previous_vertex) 
   



