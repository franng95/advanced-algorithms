import pandas as pd

print("=" * 60)
print("STATION NAME EXTRACTOR")
print("=" * 60)

# Read excel file
print("\n[1/4] Reading Excel file...")
df = pd.read_excel('London_Underground_data.xlsx')
print(f"Success! Got {len(df)} rows")

# Get station names from column 2
print("\n[2/4] Getting stations from column 2...")
# dropna removes empty cells
stations_col2 = df.iloc[:, 1].dropna().unique()
print(f"✓ Got {len(stations_col2)} unique stations from column 2")

# Get station names from column 3
print("\n[3/4] Getting stations from column 3...")
# column 3 only has data where connections exist
stations_col3 = df.iloc[:, 2].dropna().unique()
print(f"✓ Got {len(stations_col3)} unique stations from column 3")

# Combine both and remove duplicates
print("\n[4/4] Combining and removing duplicates...")
all_stations = set(stations_col2) | set(stations_col3)
all_stations_sorted = sorted(all_stations)

print(f"Total unique stations: {len(all_stations_sorted)}")

# Save to file
output_file = 'all_stations.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for station in all_stations_sorted:
        f.write(station + '\n')

print(f"Saved to '{output_file}'")
print(f"\nFirst 10 stations:")
for i, station in enumerate(all_stations_sorted[:10], 1):
    print(f"{i}. {station}")

print(f"\nLast 10 stations:")
for i, station in enumerate(all_stations_sorted[-10:], 1):
    print(f"{len(all_stations_sorted)-10+i}. {station}")

print("\n" + "=" * 60)