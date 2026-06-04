# Task 1 - station checker with hash table

import sys
import os
import time
import random

# library path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'clrsPython', 'Chapter 11'))
sys.path.insert(0, os.path.join(script_dir, 'clrsPython', 'Chapter 10'))

from chained_hashtable import ChainedHashTable

print("Task 1 - Station Status System")
print("="*50)

# 1a - simple test 
print("\n1a: Small test with 5 stations")
test_stations = ["A", "B", "C", "D", "E"]
print(test_stations)

# make small hash table size 7 
ht = ChainedHashTable(7)

# add them
for s in test_stations:
    ht.insert(s)
print("added all stations")

# search for C 
result = ht.search("C")
if result:
    print("C found - operational")
else:
    print("C not found")


# 1b - performance part
print("\n1b: Performance testing")

# function for timing searches
def time_searches(n):
    # need power of 2 for table size
    tbl_size = 1
    while tbl_size < n:
        tbl_size = tbl_size * 2
    
    table = ChainedHashTable(tbl_size)
    
    # put in n items (using integers 0 to n-1)
    for i in range(n):
        table.insert(i)
    
    # do 500 searches and time them
    total = 0
    for _ in range(500):
        key = random.randint(0, n-1)
        t1 = time.perf_counter()
        table.search(key)
        t2 = time.perf_counter()
        total = total + (t2 - t1)
    
    avg = total / 500
    return avg


# test with different sizes
sizes = [1000, 5000, 10000, 25000, 50000]
print("testing sizes:", sizes)

results = []
for size in sizes:
    t = time_searches(size)
    results.append(t)
    print(f"  n={size}: {t}")

# save to file
file = open('task1_performance.txt', 'w')
file.write("Dataset_Size,Average_Search_Time\n")
for i in range(len(sizes)):
    file.write(str(sizes[i]) + "," + str(results[i]) + "\n")
file.close()
print("saved results")


# 1b - real underground data
print("\n1b: Real London Underground")

# read stations from file
stations = []
file = open('all_stations.txt', 'r', encoding='utf-8')
lines = file.readlines()
file.close()

for line in lines:
    st = line.strip()
    if st != "":
        stations.append(st)

print("loaded", len(stations), "stations")


# create hash table - 512 should be big enough
ht2 = ChainedHashTable(512)

for station in stations:
    ht2.insert(station)

print("built hash table")


# TESTING
print("\n" + "="*50)
print("TESTING")
print("="*50)

# test Victoria
print("\nTest: Victoria")
r = ht2.search("Victoria")
if r:
    print("  Operational")
else:
    print("  Not found")

# test Baker Street
print("\nTest: Baker Street")  
r = ht2.search("Baker Street")
if r:
    print("  Operational")
else:
    print("  Not found")

# test wrong spelling
print("\nTest: Paddinton")
r = ht2.search("Paddinton")
if r:
    print("  Operational")
else:
    print("  Not found")

# test fake station
print("\nTest: Hogwarts")
r = ht2.search("Hogwarts")
if r:
    print("  Operational") 
else:
    print("  Not found")

# few more tests
print("\nMore tests:")
tests = ["Waterloo", "King's Cross St. Pancras", "Oxford Circus"]
for t in tests:
    if ht2.search(t):
        print("  " + t + ": Operational")
    else:
        print("  " + t + ": Not found")

