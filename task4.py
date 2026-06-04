# Task 4 - Backbone Network (Human-style)
# Using MST (Kruskal) to find core connections

import json
import random
import time
import os
import sys

# Paths for CLRS utilities
script_dir = os.path.dirname(os.path.abspath(__file__))
clrs = os.path.join(script_dir, 'clrsPython')

sys.path.insert(0, os.path.join(clrs, 'Utility functions'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 10'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 19'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 21'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 2'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 22'))
sys.path.insert(0, os.path.join(clrs, 'Chapter 6'))

from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from dijkstra import dijkstra

print("Task 4 - Core Network (Human-style)\n" + "="*40)

# ---- 4a: Small example ----
stations = ['A', 'B', 'C', 'D', 'E']
edges = [
    (0, 1, 10),
    (0, 2, 3),
    (1, 3, 2),
    (2, 3, 8),
    (2, 4, 2),
    (3, 4, 7)
]

g = AdjacencyListGraph(len(stations), directed=False, weighted=True)
for u, v, w in edges:
    g.insert_edge(u, v, w)

print("\nRunning Kruskal's algorithm on small network...")
mst = kruskal(g)

# Show MST edges
mst_edges = []
total_weight = 0
for u in range(len(stations)):
    for e in mst.get_adj_list(u):
        v = e.get_v()
        if u < v:
            mst_edges.append((u, v, e.get_weight()))
            total_weight += e.get_weight()

print("Backbone edges (MST):")
for u, v, w in mst_edges:
    print(f"  {stations[u]}-{stations[v]} ({w} min)")
print("Total weight:", total_weight)

# Find redundant edges
redundant = []
mst_set = set((min(u,v), max(u,v)) for u,v,w in mst_edges)
for u,v,w in edges:
    if (min(u,v), max(u,v)) not in mst_set:
        redundant.append((u,v,w))

print("\nRedundant edges (could remove):")
for u,v,w in redundant:
    print(f"  {stations[u]}-{stations[v]} ({w} min)")

# ---- 4b: Performance ----
print("\n4b: Performance testing (random networks)")

def random_connected_network(n):
    g = AdjacencyListGraph(n, directed=False, weighted=True)
    # Make a chain to ensure connectivity
    for i in range(n-1):
        g.insert_edge(i, i+1, random.randint(1,20))
    # Add some random extra edges
    for _ in range(n//2):
        i, j = random.sample(range(n), 2)
        try:
            g.insert_edge(i, j, random.randint(1,20))
        except:
            pass
    return g

sizes = [100, 200, 300, 400, 500]
for n in sizes:
    t_total = 0
    for _ in range(10):
        net = random_connected_network(n)
        t1 = time.perf_counter()
        kruskal(net)
        t2 = time.perf_counter()
        t_total += (t2 - t1)
    print(f"Size {n}: avg {t_total/10:.5f}s")

# ---- 4c: Real network (London Underground) ----
print("\n4c: Real network analysis")

with open("network_adjacency.json", "r") as f:
    data = json.load(f)

stations = sorted(data.keys())
name_to_idx = {name:i for i,name in enumerate(stations)}
idx_to_name = {i:name for i,name in enumerate(stations)}

graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)
all_edges = set()
for s1 in data:
    u = name_to_idx[s1]
    for s2, t in data[s1].items():
        v = name_to_idx[s2]
        edge = tuple(sorted([u,v]))
        if edge not in all_edges:
            graph.insert_edge(u, v, t)
            all_edges.add(edge)

print("Computing MST...")
mst_graph = kruskal(graph)

mst_edges = []
mst_set = set()
total_weight = 0
for u in range(len(stations)):
    for e in mst_graph.get_adj_list(u):
        v = e.get_v()
        if u < v:
            mst_edges.append((u,v,e.get_weight()))
            mst_set.add((u,v))
            total_weight += e.get_weight()

print(f"MST has {len(mst_edges)} edges, total weight {total_weight} min")

# Identify redundant edges
redundant_edges = [e for e in all_edges if e not in mst_set]
print(f"Redundant edges: {len(redundant_edges)} (first 10 shown)")
for i, (u,v) in enumerate(list(redundant_edges)[:10]):
    print(f"  {idx_to_name[u]} - {idx_to_name[v]}")

# Impact on a route
start, end = "Wimbledon", "Stratford"
start_idx, end_idx = name_to_idx[start], name_to_idx[end]

# Original shortest path
dist_orig, pred_orig = dijkstra(graph, start_idx)
path_orig = []
cur = end_idx
while cur is not None:
    path_orig.append(idx_to_name[cur])
    cur = pred_orig[cur]
path_orig.reverse()

# MST path
dist_mst, pred_mst = dijkstra(mst_graph, start_idx)
path_mst = []
cur = end_idx
while cur is not None:
    path_mst.append(idx_to_name[cur])
    cur = pred_mst[cur]
path_mst.reverse()

print("\nRoute analysis:")
print(f"Original: {len(path_orig)} stations, {dist_orig[end_idx]} min")
print(f"Backbone only: {len(path_mst)} stations, {dist_mst[end_idx]} min")
increase = dist_mst[end_idx] - dist_orig[end_idx]
print(f"Increase: {increase} min ({increase/dist_orig[end_idx]*100:.1f}%)")
if increase > 0:
    print("Redundant edges make it faster, but MST keeps network connected")

# check which redundant edges are used
used_redundant = []
for u,v in zip(path_orig[:-1], path_orig[1:]):
    if tuple(sorted([name_to_idx[u], name_to_idx[v]])) not in mst_set:
        used_redundant.append(f"{u} -> {v}")

if used_redundant:
    print(f"Original route uses {len(used_redundant)} redundant edges:")
    for r in used_redundant:
        print("  ", r)
else:
    print("Original route uses only backbone edges")


