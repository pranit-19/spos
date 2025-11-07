# Worst Fit Memory Allocation

# Sample Input
partitions = [100, 500, 200, 300, 600]   # Memory partitions (in KB)
processes = [212, 417, 112, 426]         # Process sizes (in KB)

# Initialize allocation array (-1 means not allocated)
allocation = [-1] * len(processes)

# Worst Fit Algorithm
for i in range(len(processes)):
    worst_idx = -1
    for j in range(len(partitions)):
        if partitions[j] >= processes[i]:  # Can it fit?
            if worst_idx == -1 or partitions[j] > partitions[worst_idx]:
                worst_idx = j
    # Allocate if found
    if worst_idx != -1:
        allocation[i] = worst_idx
        partitions[worst_idx] -= processes[i]  # Reduce the partition size

# Display Results
print("Process No.\tProcess Size\tPartition No.")
print("-" * 40)
for i in range(len(processes)):
    if allocation[i] != -1:
        print(f"{i + 1}\t\t{processes[i]}K\t\t{allocation[i] + 1}")
    else:
        print(f"{i + 1}\t\t{processes[i]}K\t\tNot Allocated")
