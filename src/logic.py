from src import visualization
import csv 
import heapq


# Odczyt danych z pliku edges.csv
def dataReader(path='data/edges.csv'):
    graphs = {}
    with open(path, newline='') as file:
        for row in csv.DictReader(file):
            gid = row['graph_id']
            src = row['source']
            tgt = row['target']
            graph = graphs.setdefault(gid, {})
            graph.setdefault(src, {})[tgt] = int(row['weight'])
            graph.setdefault(tgt, {})
    return graphs


# Algorytm Dijkstry zwraca minimalną odległość dla maksymalnego wierzchołka
def dijkstra(graph, start):
    dist = {}
    prev = {}
    for vertex in graph:
        dist[vertex] = float('inf')
        prev[vertex] = None

    dist[start] = 0
    prev[start] = None  

    priority_queue = [(0, start)]
    max_dist = 0
    max_vertex = start

    while priority_queue:
        current_dist, current_vertex = heapq.heappop(priority_queue)

        for neighbor, weight in graph[current_vertex].items():
            distance = current_dist + weight
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
                if distance > max_dist:
                    max_dist = distance
                    max_vertex = neighbor

    # Jezeli jakis wierzcholek nieodwiedzony, allvisit = false
    allvisit = float('inf') not in dist.values() 
                                        

    return max_vertex, max_dist, allvisit

def run():
    data = dataReader()

    for id in list(data.keys()):
        start_vertex = None
        extreme_vertex = None
        min_value = float('inf') 
        for vertex in list(data[id].keys()):
            result = dijkstra(data[id], vertex)
            max_vertex, max_dist, allvisit = result
            if allvisit: # Jeżeli wszystkie wierzchołki zostały odwiedzone, to sprawdzamy czy max_dist jest mniejszy niż min_value
                if min_value > max_dist:
                    min_value = max_dist
                    start_vertex = vertex
                    extreme_vertex = max_vertex

        print(f"Graph: {id}, Start: {start_vertex}, Extreme: {extreme_vertex}, Min Distance: {min_value}")  

   



