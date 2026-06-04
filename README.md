# Advanced Algorithms – London Underground Coursework

Year 2 coursework applying CLRS algorithms to a real London Underground dataset.

## Tasks

| Task | Algorithm | Problem |
|------|-----------|---------|
| 1 | Hash Table (chaining) | Station status lookup — checks if a station is operational |
| 2 | Dijkstra | Shortest journey by travel time between two stations |
| 3 | BFS | Fewest stops route between two stations |
| 4 | Kruskal / MST | Backbone network — minimum spanning tree of the Underground |

Each task includes performance benchmarking across dataset sizes.

## Structure

```
task1.py / task2.py / task3.py / task4.py   # coursework solutions
clrsPython/                                  # CLRS textbook algorithm implementations
all_stations.txt                             # London Underground station list
network_adjacency.json                       # Station graph with travel times
network_connections.csv                      # Raw connection data
```

## Running

```bash
python task1.py
python task2.py
python task3.py
python task4.py
```

Requires Python 3. No external dependencies — all data structures and algorithms are implemented in `clrsPython/`.

## Tech

Python · CLRS algorithms · Graph theory · Hash tables · BFS · Dijkstra · Kruskal
