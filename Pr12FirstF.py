# First Fit Memory Allocation

# Sample Input
partitions = [100, 500, 200, 300, 600]   # Memory partitions (in KB)
processes = [212, 417, 112, 426]         # Process sizes (in KB)

# Initialize allocation array (-1 = not allocated)
allocation = [-1] * len(processes)

# First Fit Algorithm
for i in range(len(processes)):
    for j in range(len(partitions)):
        if partitions[j] >= processes[i]:   # If partition can fit process
            allocation[i] = j               # Assign partition j to process i
            partitions[j] -= processes[i]   # Reduce partition size
            break                           # Move to next process (First Fit)

# Display Result
print("Process No.\tProcess Size\tPartition No.")
print("-" * 40)
for i in range(len(processes)):
    if allocation[i] != -1:
        print(f"{i + 1}\t\t{processes[i]}K\t\t{allocation[i] + 1}")
    else:
        print(f"{i + 1}\t\t{processes[i]}K\t\tNot Allocated")
