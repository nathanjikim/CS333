import math
import heapq
import json
import time

def calculate_distance(n1, n2):
    n1_latitude = coord_data[n1][0] * math.pi / 180
    n1_longitude = coord_data[n1][1] * math.pi / 180
    n2_latitude = coord_data[n2][0] * math.pi / 180
    n2_longitude = coord_data[n2][1] * math.pi / 180
    delta_x = 3963.2 * math.cos(n1_latitude) * (n2_longitude - n1_longitude)
    delta_y = 3963.2 * (n2_latitude - n1_latitude)

    distance = math.sqrt(delta_x * delta_x + delta_y * delta_y)
    return distance
  
# Opening JSON file
with open('durham_graph.json') as graph_file:
    graph_data = json.load(graph_file)
  
    # Print the data of dictionary
    print("170498936:", graph_data['170498936'])

with open('durham_coordinates.json') as coord_file:
    coord_data = json.load(coord_file)

    print("170498935:", coord_data['170498935'])

distances = {}
for node in graph_data:
    for neighbor in graph_data[node]:
        distance = calculate_distance(node, neighbor)
        distances[(node, neighbor)] = distance

def djikstra(start, end):
    nodes_visited = 0
    path_distances = {node: float('infinity') for node in graph_data}
    paths = {node: [] for node in graph_data}
    pq = [(0, start)]
    paths[str(start)].append(str(start))

    while len(pq) > 0:
        current_distance, current_node = heapq.heappop(pq)
        nodes_visited += 1
        if current_node == end:
            print("Distance: ", path_distances[str(end)])
            print("Nodes visited: ", nodes_visited)
            return paths[str(end)]
        if current_distance > path_distances[str(current_node)]:
            continue
        for neighbor in graph_data[str(current_node)]:
            distance = distances[current_node, neighbor] + current_distance

            #consider this new path if it is better
            if distance < path_distances[neighbor]:
                paths[str(neighbor)] = paths[str(current_node)].copy()
                paths[str(neighbor)].append(str(neighbor))
                path_distances[str(neighbor)] = distance
                heapq.heappush(pq, (distance, neighbor))
    print("Distance: ", path_distances[str(end)])
    print("Nodes visited: ", nodes_visited)
    return paths[str(end)]


def a_star(start, end):
    nodes_visited = 0
    path_distances = {node: float('infinity') for node in graph_data}
    paths = {node: [] for node in graph_data}
    pq = [(0, start)] # got to change the priority here
    paths[str(start)].append(str(start))

    while len(pq) > 0:
        current_distance, current_node = heapq.heappop(pq)
        nodes_visited += 1
        if current_node == end:
            print("Nodes visited: ", nodes_visited)
            return paths[str(end)]
        if current_distance > path_distances[str(current_node)]:
            continue
        for neighbor in graph_data[str(current_node)]:
            distance = distances[current_node, neighbor] + current_distance + calculate_distance(neighbor, end) # change the priority here too

            #consider this new path if it is better
            if distance < path_distances[neighbor]:
                paths[str(neighbor)] = paths[str(current_node)].copy()
                paths[str(neighbor)].append(str(neighbor))
                path_distances[str(neighbor)] = distance
                heapq.heappush(pq, (distance, neighbor))
    print("Nodes visited: ", nodes_visited)
    return paths[str(end)]

start = time.time()
# path = djikstra('2865075396', '344481044')
path = a_star('2865075396', '344481044')
end = time.time()

print(f"Runtime of the program is {end - start}")

output = []

for node in path:
    output.append(coord_data[str(node)])

json_string = json.dumps(output)
with open('path.json', 'w') as f:
    json.dump(json_string, f)

# output node ids
json2_string = json.dumps(path)
with open('output.json', 'w') as f:
    json.dump(json2_string, f)

