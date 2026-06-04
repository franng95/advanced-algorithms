# task 2 - shortest path by time
# using dijkstra from library

import json
import sys
import os
import time
import random

# add library paths
script_dir = os.path.dirname(os.path.abspath(__file__))
clrs = os.path.join(script_dir, 'clrsPython')

sys.path.insert(0, os.path.join(clrs, 'Utility functions'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 10'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 22'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 6'))

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

print("Task 2: Journey Planner (shortest time)")
print("="*55)


# 2a - test with small network
print("\n2a: Simple network test")

# 5 stations A B C D E (use 0 1 2 3 4)
# add edges with weights
graph = AdjacencyListGraph(5, directed=False, weighted=True)
graph.insert_edge(0, 1, 10)  # A-B: 10min
graph.insert_edge(0, 2, 3)   # A-C: 3
graph.insert_edge(1, 3, 2)   # B-D: 2  
graph.insert_edge(2, 3, 8)   # C-D: 8
graph.insert_edge(2, 4, 2)   # C-E: 2
graph.insert_edge(3, 4, 7)   # D-E: 7

print("finding path A to E...")

# run dijkstra from A (node 0)
distances, preds = dijkstra(graph, 0)

# build path from E back to A
path = []
current = 4
while current != None:
    path.append(current)
    current = preds[current]

path.reverse()

# convert to letters
names = ['A', 'B', 'C', 'D', 'E']
path_names = []
for p in path:
    path_names.append(names[p])

print("path:", ' -> '.join(path_names))
print("time:", distances[4], "minutes")
print("should be: A -> C -> E = 5 minutes")


# 2b - performance testing
print("\n2b: Performance tests")

def make_test_network(n):
    # random network with n nodes
    g = AdjacencyListGraph(n, directed=False, weighted=True)
    
    for i in range(n):
        # each node connects to 2-4 others
        connections = random.randint(2, min(4, n-1))
        for j in range(connections):
            target = random.randint(0, n-1)
            if target != i:
                w = random.randint(1, 20)
                try:
                    g.insert_edge(i, target, w)
                except:
                    pass
    
    return g

# test different sizes
test_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

print("testing (takes ~1 min)...")
times = []

for n in test_sizes:
    g = make_test_network(n)
    
    # run dijkstra 30 times and average
    total = 0
    for i in range(30):
        start = random.randint(0, n-1)
        
        t1 = time.perf_counter()
        d, p = dijkstra(g, start)
        t2 = time.perf_counter()
        
        total += (t2 - t1)
    
    avg = total / 30
    times.append(avg)
    print(f"  n={n}: {avg:.6f}s")

# save results
with open('task2_performance.txt', 'w') as f:
    f.write("Network_Size,Average_Time\n")
    for i in range(len(test_sizes)):
        f.write(f"{test_sizes[i]},{times[i]}\n")

print("saved to task2_performance.txt")


# 2b - london underground
print("\n2b: London Underground network")

# load network data
with open('network_adjacency.json', 'r') as f:
    network = json.load(f)

print(f"loaded {len(network)} stations")

# map station names to numbers
station_names = sorted(network.keys())
name_to_num = {}
num_to_name = {}

for i in range(len(station_names)):
    name_to_num[station_names[i]] = i
    num_to_name[i] = station_names[i]

# build graph
g = AdjacencyListGraph(len(station_names), directed=False, weighted=True)

# add edges
edges_added = set()
for s1 in network:
    u = name_to_num[s1]
    for s2 in network[s1]:
        v = name_to_num[s2]
        time_val = network[s1][s2]
        
        # only add each edge once
        edge = tuple(sorted([u, v]))
        if edge not in edges_added:
            g.insert_edge(u, v, time_val)
            edges_added.add(edge)

print(f"graph built: {len(edges_added)} connections")


print("\n" + "="*55)
print("TESTING")
print("="*55)



#Network_Size,Average_Time
100,0.0005374333350725162
200,0.001217340001797614
300,0.0018085900010191835
400,0.002785226667280464
500,0.003560853331873659
600,0.004826036667024406
700,0.0052786566646924864
800,0.006527250000605515
900,0.006415406667413966
1000,0.0074436866668596245
# test 1 - short
print("\nTest 1: Covent Garden -> Leicester Square")

s1 = "Covent Garden"
s2 = "Leicester Square"

n1 = name_to_num[s1]
n2 = name_to_num[s2]

dist, pred = dijkstra(g, n1)

# get path
route = []
curr = n2
while curr != None:
    route.append(num_to_name[curr])
    curr = pred[curr]
route.reverse()

print("\nRoute:")
for st in route:
    print(f"  {st}")
print(f"\nTime: {dist[n2]} mins")


# test 2 - long
print("\n" + "-"*55)
print("Test 2: Wimbledon -> Stratford")

s1 = "Wimbledon"
s2 = "Stratford"

n1 = name_to_num[s1]
n2 = name_to_num[s2]

dist, pred = dijkstra(g, n1)

# get path
route = []
curr = n2
while curr != None:
    route.append(num_to_name[curr])
    curr = pred[curr]
route.reverse()

print(f"\nRoute ({len(route)} stations):")

# We changed this to fit the length of the output in the report
if len(route) > 10:
    for i in range(4):
        print(f"  {route[i]}")
    print(f"  ... {len(route)-8} more ...")
    for i in range(len(route)-4, len(route)):
        print(f"  {route[i]}")
else:
    for st in route:
        print(f"  {st}")

print(f"\nTime: {dist[n2]} mins")
print(f"Stops: {len(route)-1}")