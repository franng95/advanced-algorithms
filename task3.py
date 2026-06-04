# task 3 - fewest stops planner
# bfs algorithm

import sys
import os
import json
import time
import random

# library paths
script_dir = os.path.dirname(os.path.abspath(__file__))
clrs = os.path.join(script_dir, 'clrsPython')

sys.path.insert(0, os.path.join(clrs, 'Utility functions'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 10'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 20'))

from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs

print("task 3 - fewest stops")
print("="*45)

# part 3a - simple test
print("\n3a - simple network")

# 5 stations - A B C D E (numbers 0-4)
g = AdjacencyListGraph(5, directed=False, weighted=False)

# connections (no weights this time)
g.insert_edge(0, 1)  # A-B
g.insert_edge(0, 2)  # A-C
g.insert_edge(1, 3)  # B-D
g.insert_edge(2, 3)  # C-D
g.insert_edge(2, 4)  # C-E
g.insert_edge(3, 4)  # D-E

print("testing A to E")

# bfs from A
dist, pred = bfs(g, 0)

# make path
path = []
node = 4  # start at E
while node != None:
    path.append(node)
    node = pred[node]
path.reverse()

# convert
letters = ['A', 'B', 'C', 'D', 'E']
result = []
for p in path:
    result.append(letters[p])

print("path:", ' -> '.join(result))
print("stops:", len(result)-1)
print("(should be A -> C -> E, 2 stops)")


# 3b - performance
print("\n3b - performance testing")

def make_network(n):
    g = AdjacencyListGraph(n, directed=False, weighted=False)
    
    # connect nodes randomly
    for i in range(n):
        num_conn = random.randint(2, min(4, n-1))
        for j in range(num_conn):
            target = random.randint(0, n-1)
            if target != i:
                try:
                    g.insert_edge(i, target)
                except:
                    pass  # might already exist
    
    return g

sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
print("running tests...")

results = []
for size in sizes:
    g = make_network(size)
    
    # time it
    total = 0
    trials = 50
    
    for t in range(trials):
        start = random.randint(0, size-1)
        
        t1 = time.perf_counter()
        d, p = bfs(g, start)
        t2 = time.perf_counter()
        
        total += (t2 - t1)
    
    avg = total / trials
    results.append(avg)
    print(f"  {size}: {avg:.6f}")

# save
f = open('task3_performance.txt', 'w')
f.write("Network_Size,Average_Time\n")
for i in range(len(sizes)):
    f.write(str(sizes[i]) + "," + str(results[i]) + "\n")
f.close()
print("saved")


# 3b - real network
print("\n3b - london underground")

# load data
f = open('network_adjacency.json', 'r', encoding='utf-8')
data = json.load(f)
f.close()

print("loaded", len(data), "stations")

# map names to numbers
stations = sorted(data.keys())
name2num = {}
num2name = {}
for i, name in enumerate(stations):
    name2num[name] = i
    num2name[i] = name

# build graph (no weights - just connections)
graph = AdjacencyListGraph(len(stations), directed=False, weighted=False)

added_edges = set()
for s1 in data:
    u = name2num[s1]
    for s2 in data[s1]:
        v = name2num[s2]
        
        # add edge once
        edge = tuple(sorted([u, v]))
        if edge not in added_edges:
            graph.insert_edge(u, v)
            added_edges.add(edge)

print("graph ready")


print("\n" + "="*45)
print("TESTING")
print("="*45)

# test 1
print("\ntest 1: Covent Garden to Leicester Square")

start = "Covent Garden"
end = "Leicester Square"

start_num = name2num[start]
end_num = name2num[end]

distances, preds = bfs(graph, start_num)

# get path
path = []
current = end_num
while current != None:
    path.append(num2name[current])
    current = preds[current]
path.reverse()

print("\npath:")
for station in path:
    print("  " + station)
print("\nstops:", len(path)-1)


# test 2
print("\n" + "-"*45)
print("test 2: Wimbledon to Stratford")

start = "Wimbledon"
end = "Stratford"

start_num = name2num[start]
end_num = name2num[end]

distances, preds = bfs(graph, start_num)

# path
path = []
current = end_num
while current != None:
    path.append(num2name[current])
    current = preds[current]
path.reverse()

print(f"\npath ({len(path)} stations):")

# show some
if len(path) > 10:
    for i in range(4):
        print("  " + path[i])
    print("  ...")
    for i in range(len(path)-4, len(path)):
        print("  " + path[i])
else:
    for station in path:
        print("  " + station)

print("\nstops:", len(path)-1)

print("\ndone")