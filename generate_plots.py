# Performance Data Plotter
# Generates graphs comparing empirical results with theoretical complexity

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("Generating Performance Graphs")
print("=" * 60)

# Set up nice plot style
plt.style.use('seaborn-v0_8-darkgrid')
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Algorithm Performance Analysis - Empirical vs Theoretical', 
             fontsize=16, fontweight='bold')

# ============================================================
# TASK 1: Hash Table Search - O(1) expected
# ============================================================
print("\n[1/4] Task 1: Hash Table Search...")

# Read data
task1_data = pd.read_csv('task1_performance.txt')
n1 = task1_data['Dataset_Size'].values
time1 = task1_data['Average_Search_Time'].values

# Theoretical O(1) - constant time
theoretical1 = np.full_like(n1, np.mean(time1), dtype=float)

# Plot
ax1 = axes[0, 0]
ax1.plot(n1, time1, 'bo-', linewidth=2, markersize=8, label='Empirical')
ax1.plot(n1, theoretical1, 'r--', linewidth=2, label='Theoretical O(1)')
ax1.set_xlabel('Dataset Size (n)', fontsize=11)
ax1.set_ylabel('Average Search Time (seconds)', fontsize=11)
ax1.set_title('Task 1: Hash Table Search Performance', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

# ============================================================
# TASK 2: Dijkstra - O(n² log n) with binary heap
# ============================================================
print("[2/4] Task 2: Dijkstra Shortest Path...")

# Read data
task2_data = pd.read_csv('task2_performance.txt')
n2 = task2_data['Network_Size'].values
time2 = task2_data['Average_Time'].values

# Theoretical O(n² log n) - scale to match empirical at middle point
mid_idx = len(n2) // 2
theoretical2 = (n2 ** 2) * np.log(n2)
scale_factor = time2[mid_idx] / theoretical2[mid_idx]
theoretical2 = theoretical2 * scale_factor

# Plot
ax2 = axes[0, 1]
ax2.plot(n2, time2, 'go-', linewidth=2, markersize=8, label='Empirical')
ax2.plot(n2, theoretical2, 'r--', linewidth=2, label='Theoretical O(n²log n)')
ax2.set_xlabel('Network Size (n)', fontsize=11)
ax2.set_ylabel('Average Time (seconds)', fontsize=11)
ax2.set_title('Task 2: Dijkstra Performance', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# ============================================================
# TASK 3: BFS - O(n + m) ≈ O(n) for sparse graph
# ============================================================
print("[3/4] Task 3: BFS Fewest Stops...")

# Read data
task3_data = pd.read_csv('task3_performance.txt')
n3 = task3_data['Network_Size'].values
time3 = task3_data['Average_Time'].values

# Theoretical O(n) - linear for sparse graph where m ≈ n
theoretical3 = n3.astype(float)
scale_factor3 = time3[mid_idx] / theoretical3[mid_idx]
theoretical3 = theoretical3 * scale_factor3

# Plot
ax3 = axes[1, 0]
ax3.plot(n3, time3, 'mo-', linewidth=2, markersize=8, label='Empirical')
ax3.plot(n3, theoretical3, 'r--', linewidth=2, label='Theoretical O(n)')
ax3.set_xlabel('Network Size (n)', fontsize=11)
ax3.set_ylabel('Average Time (seconds)', fontsize=11)
ax3.set_title('Task 3: BFS Performance', fontsize=12, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)

# ============================================================
# TASK 4: Kruskal MST - O(m log n)
# ============================================================
print("[4/4] Task 4: Kruskal MST...")

# Read data
task4_data = pd.read_csv('task4_performance.txt')
n4 = task4_data['Network_Size'].values
time4 = task4_data['Average_Time'].values

# Theoretical O(m log n) - for sparse graphs m ≈ n, so O(n log n)
theoretical4 = n4 * np.log(n4)
scale_factor4 = time4[mid_idx] / theoretical4[mid_idx]
theoretical4 = theoretical4 * scale_factor4

# Plot
ax4 = axes[1, 1]
ax4.plot(n4, time4, 'co-', linewidth=2, markersize=8, label='Empirical')
ax4.plot(n4, theoretical4, 'r--', linewidth=2, label='Theoretical O(n log n)')
ax4.set_xlabel('Network Size (n)', fontsize=11)
ax4.set_ylabel('Average Time (seconds)', fontsize=11)
ax4.set_title('Task 4: Kruskal MST Performance', fontsize=12, fontweight='bold')
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)

# Adjust layout and save
plt.tight_layout()
plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: performance_analysis.png")

# Also create individual plots for better visibility in report
print("\nGenerating individual plots...")

# Task 1 individual
plt.figure(figsize=(8, 6))
plt.plot(n1, time1, 'bo-', linewidth=2, markersize=8, label='Empirical')
plt.plot(n1, theoretical1, 'r--', linewidth=2, label='Theoretical O(1)')
plt.xlabel('Dataset Size (n)', fontsize=12)
plt.ylabel('Average Search Time (seconds)', fontsize=12)
plt.title('Task 1: Hash Table Search Performance', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
plt.tight_layout()
plt.savefig('task1_performance_graph.png', dpi=300, bbox_inches='tight')
print("✓ Saved: task1_performance_graph.png")

# Task 2 individual
plt.figure(figsize=(8, 6))
plt.plot(n2, time2, 'go-', linewidth=2, markersize=8, label='Empirical')
plt.plot(n2, theoretical2, 'r--', linewidth=2, label='Theoretical O(n²log n)')
plt.xlabel('Network Size (n)', fontsize=12)
plt.ylabel('Average Time (seconds)', fontsize=12)
plt.title('Task 2: Dijkstra Shortest Path Performance', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('task2_performance_graph.png', dpi=300, bbox_inches='tight')
print("✓ Saved: task2_performance_graph.png")

# Task 3 individual
plt.figure(figsize=(8, 6))
plt.plot(n3, time3, 'mo-', linewidth=2, markersize=8, label='Empirical')
plt.plot(n3, theoretical3, 'r--', linewidth=2, label='Theoretical O(n)')
plt.xlabel('Network Size (n)', fontsize=12)
plt.ylabel('Average Time (seconds)', fontsize=12)
plt.title('Task 3: BFS Fewest Stops Performance', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('task3_performance_graph.png', dpi=300, bbox_inches='tight')
print("✓ Saved: task3_performance_graph.png")

# Task 4 individual
plt.figure(figsize=(8, 6))
plt.plot(n4, time4, 'co-', linewidth=2, markersize=8, label='Empirical')
plt.plot(n4, theoretical4, 'r--', linewidth=2, label='Theoretical O(n log n)')
plt.xlabel('Network Size (n)', fontsize=12)
plt.ylabel('Average Time (seconds)', fontsize=12)
plt.title('Task 4: Kruskal MST Performance', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('task4_performance_graph.png', dpi=300, bbox_inches='tight')
print("✓ Saved: task4_performance_graph.png")

print("\n" + "=" * 60)
print("All graphs generated successfully!")
print("=" * 60)
print("\nFiles created:")
print("  • performance_analysis.png (all 4 graphs)")
print("  • task1_performance_graph.png")
print("  • task2_performance_graph.png")
print("  • task3_performance_graph.png")
print("  • task4_performance_graph.png")
print("\nUse these graphs in your report!")