# Best Fit Memory Allocation

# Sample Input
partitions = [100, 500, 200, 300, 600]       # Memory partitions (in KB)
processes = [212, 417, 112, 426]             # Process sizes (in KB)

# Initialize allocation array (-1 means not allocated)
allocation = [-1] * len(processes)

# Best Fit Algorithm
for i in range(len(processes)):
    best_idx = -1
    for j in range(len(partitions)):
        if partitions[j] >= processes[i]:  # if partition can fit process
            if best_idx == -1 or partitions[j] < partitions[best_idx]:
                best_idx = j
    # If found a suitable partition
    if best_idx != -1:
        allocation[i] = best_idx
        partitions[best_idx] -= processes[i]  # reduce available memory

# Display results
print("Process No.\tProcess Size\tPartition No.")
print("-" * 40)
for i in range(len(processes)):
    if allocation[i] != -1:
        print(f"{i + 1}\t\t{processes[i]}K\t\t{allocation[i] + 1}")
    else:
        print(f"{i + 1}\t\t{processes[i]}K\t\tNot Allocated")
