# Next Fit Memory Allocation (Final Correct Version)

partitions = [100, 500, 200, 300, 600]   # Memory partitions (in KB)
processes = [212, 417, 112, 426]         # Process sizes (in KB)

allocation = [-1] * len(processes)
n = len(partitions)
last_allocated_index = 0  # Start searching from here

for i in range(len(processes)):
    allocated = False
    count = 0

    # Start from the NEXT partition after the last allocation
    j = (last_allocated_index + 1) % n

    while count < n:
        if partitions[j] >= processes[i]:
            allocation[i] = j
            partitions[j] -= processes[i]
            last_allocated_index = j   # update pointer
            allocated = True
            break
        j = (j + 1) % n
        count += 1

    if not allocated:
        allocation[i] = -1

# Display output neatly
print("Process No.\tProcess Size\tPartition No.")
print("-" * 40)
for i in range(len(processes)):
    if allocation[i] != -1:
        print(f"{i + 1}\t\t{processes[i]}K\t\t{allocation[i] + 1}")
    else:
        print(f"{i + 1}\t\t{processes[i]}K\t\tNot Allocated")
