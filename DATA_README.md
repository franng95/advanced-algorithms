# London Underground Network Data - Documentation

**Prepared by:** Francisco Navarro 
**Date:** 30th October 2025  
**For:** COMP1828 Coursework Team

---

## Files I Created

### 1. `all_stations.txt`
- **What it is:** All the unique station names from the London Underground
- **Format:** Just plain text, one station per line, sorted alphabetically
- **Total Stations:** 280
- **Who needs it:** Task 1 (Station Status System)

**Looks like this:**
```
Acton Town
Aldgate
Aldgate East
Baker Street
...
```

---

### 2. `network_adjacency.json`
- **What it is:** The network graph in adjacency list format
- **Format:** JSON file (nested dictionaries)
- **Structure:**
```json
  {
    "Station Name": {
      "Connected Station 1": travel_time_minutes,
      "Connected Station 2": travel_time_minutes,
      ...
    }
  }
```

**Important stuff:**
- **Bidirectional:** If station A connects to B, then B also connects to A
- **Simplified:** When there were multiple connections between same stations, I kept the shortest time
- **Total Stations:** 280
- **Total Connections:** 644 (counting both directions)

**Example:**
```json
{
  "Baker Street": {
    "Regent's Park": 2.0,
    "Marylebone": 2.0,
    "Edgware Road": 3.0
  },
  "Regent's Park": {
    "Baker Street": 2.0,
    "Oxford Circus": 2.0
  }
}
```

**Who needs it:** Tasks 2, 3, and 4 (basically all the journey planning stuff)

---

### 3. `network_connections.csv`
- **What it is:** Same network but in CSV so you can open it in Excel and check things
- **Format:** CSV with 3 columns
- **Columns:**
  - `Station1`: First station
  - `Station2`: Second station  
  - `Time`: Travel time in minutes

**Example:**
```csv
Station1,Station2,Time
Baker Street,Edgware Road,3.0
Baker Street,Marylebone,2.0
Baker Street,Regent's Park,2.0
```

**Why I made it:** Easier to check the data manually or debug

---

## How to Use These Files in Python

### Loading the station list
```python
# just read all station names
with open('all_stations.txt', 'r', encoding='utf-8') as f:
    all_stations = [line.strip() for line in f]

print(f"Total stations: {len(all_stations)}")
print(f"First one: {all_stations[0]}")
```

---

### Loading the network
```python
import json

# load the network
with open('network_adjacency.json', 'r', encoding='utf-8') as f:
    network = json.load(f)

# example - see what connects to Baker Street
baker_connections = network["Baker Street"]
print(f"Baker Street connects to {len(baker_connections)} stations:")
for neighbor, time in baker_connections.items():
    print(f"  → {neighbor} ({time} min)")

# get travel time between two stations
time_to_regents = network["Baker Street"]["Regent's Park"]
print(f"Takes {time_to_regents} minutes")

# check if two stations connect directly
if "Oxford Circus" in network["Baker Street"]:
    print("They connect!")
else:
    print("No direct connection")
```

---

## Notes for Each Task

### Task 1 (Station Status)
- Use `all_stations.txt` 
- Load it into whatever data structure you picked (hash table, BST, etc)
- Each line is one station name

### Task 2 (Shortest Path by Time)
- Use `network_adjacency.json`
- It's already a weighted graph
- The weights are the travel times
- Remember it's undirected (goes both ways)

### Task 3 (Fewest Stops)
- Use `network_adjacency.json` again
- Just ignore the time values - treat it like unweighted
- To check if connection exists: `if station2 in network[station1]`

### Task 4 (Network Backbone)
- Use `network_adjacency.json`
- Weighted undirected graph
- You might need to convert it to edge list for the MST algorithm

---

## Converting to Edge List (if you need it)

Some algorithms need edge list instead of adjacency list:
```python
import json

# load the network
with open('network_adjacency.json', 'r', encoding='utf-8') as f:
    network = json.load(f)

# convert to edge list (no duplicates)
edges = []
seen = set()

for station1 in network:
    for station2, time in network[station1].items():
        # make sure we don't add same edge twice (A-B is same as B-A)
        edge = tuple(sorted([station1, station2]))
        if edge not in seen:
            edges.append({
                'station1': station1,
                'station2': station2,
                'time': time
            })
            seen.add(edge)

print(f"Got {len(edges)} unique edges")
```

---

## Some Stats

- **Total Stations:** 280
- **Total Connections (both ways):** 644
- **Actual physical links:** 322 (because 644/2)
- **Average connections per station:** 2.3
- **Source:** London_Underground_data.xlsx
- **How I did it:** Used pandas to parse the Excel

---

## Problems?

If something doesn't work or you need the data in different format just message me

**Last updated:** 30/10/2025