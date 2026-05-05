import csv 
from collections import defaultdict
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

def dijkstra(graph, start):
    dist = {}
    prev = {}
    for vertex in graph:
        dist[vertex] = float('inf')
        prev[vertex] = None

    dist[start] = 0
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

    return max_vertex, max_dist



if __name__ == "__main__":
    data = dataReader()
    print(dijkstra(data['1'], 'A'))


