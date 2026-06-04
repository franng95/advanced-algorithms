import pandas as pd
import json

print("=" * 60)
print("NETWORK EXTRACTOR")
print("=" * 60)

# Read excel file
print("\n[1/5] Reading Excel file...")
df = pd.read_excel('London_Underground_data.xlsx')
print(f"Success! Got {len(df)} rows")

# Filter rows with connections
print("\n[2/5] Filtering rows with connections from column 3...")
# only want rows where column 3 has data (connections)
connections_df = df[df.iloc[:, 2].notna()].copy()
print(f"✓ Found {len(connections_df)} rows with connections")

# Extract connection data
print("\n[3/5] Getting connection data...")
connections = []
for idx, row in connections_df.iterrows():
    line = row.iloc[0]
    station1 = row.iloc[1]
    station2 = row.iloc[2]
    time = row.iloc[3]

    connections.append({
        'line': line,
        'station1': station1,
        'station2': station2,
        'time': time
    })

print(f"✓ Got {len(connections)} connections")

# Build adjacency list
print("\n[4/5] Building adjacency list...")
adjacency_list = {}

for conn in connections:
    s1 = conn['station1']
    s2 = conn['station2']
    time = conn['time']

    # add stations to dict if not there yet
    if s1 not in adjacency_list:
        adjacency_list[s1] = {}
    if s2 not in adjacency_list:
        adjacency_list[s2] = {}

    # add connection both ways
    # keep shorter time if connection already exists
    if s2 not in adjacency_list[s1]:
        adjacency_list[s1][s2] = time
    else:
        adjacency_list[s1][s2] = min(adjacency_list[s1][s2], time)
    
    if s1 not in adjacency_list[s2]:
        adjacency_list[s2][s1] = time
    else:
        adjacency_list[s2][s1] = min(adjacency_list[s2][s1], time)

print(f"✓ Built adjacency list with {len(adjacency_list)} stations")

# Save to JSON
print("\n[5/5] Saving to JSON...")
with open('network_adjacency.json', 'w', encoding='utf-8') as f:
    json.dump(adjacency_list, f, indent=2, ensure_ascii=False)
print("✓ Saved network_adjacency.json")

# Save as CSV too
csv_data = []
for s1 in sorted(adjacency_list.keys()):
    for s2 in sorted(adjacency_list[s1].keys()):
        time = adjacency_list[s1][s2]
        csv_data.append({'Station1': s1, 'Station2': s2, 'Time': time})

csv_df = pd.DataFrame(csv_data)
csv_df.to_csv('network_connections.csv', index=False)
print("✓ Saved network_connections.csv")

# Show sample
print("\nSample connections:")
sample_station = list(adjacency_list.keys())[0]
print(f"{sample_station} connects to:")
for neighbor, time in list(adjacency_list[sample_station].items())[:5]:
    print(f" - {neighbor}: {time} minutes")

print(f"\nNetwork stats:")
total_connections = sum(len(neighbors) for neighbors in adjacency_list.values())
print(f" - Total stations: {len(adjacency_list)}")
print(f" - Total connections (bidirectional): {total_connections}")
print(f" - Average per station: {total_connections / len(adjacency_list):.1f}")