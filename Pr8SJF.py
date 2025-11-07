# SJF (Preemptive) CPU Scheduling Algorithm
# Shortest Remaining Time First (SRTF)

# Sample Input
processes = [
    ['P1', 0, 6],
    ['P2', 1, 4],
    ['P3', 4, 8],
    ['P4', 3, 3]
]

# Sort by arrival time
processes.sort(key=lambda x: x[1])

n = len(processes)
remaining_time = [p[2] for p in processes]
completion_time = [0] * n
waiting_time = [0] * n
turnaround_time = [0] * n

t = 0          # current time
completed = 0  # number of completed processes
min_index = -1
prev_min = -1

while completed != n:
    # Find process with shortest remaining time among those arrived
    min_time = float('inf')
    min_index = -1

    for i in range(n):
        if processes[i][1] <= t and remaining_time[i] > 0:
            if remaining_time[i] < min_time:
                min_time = remaining_time[i]
                min_index = i

    if min_index == -1:
        t += 1
        continue

    # Run the process for 1 unit
    remaining_time[min_index] -= 1
    t += 1

    # If process is finished
    if remaining_time[min_index] == 0:
        completed += 1
        completion_time[min_index] = t
        turnaround_time[min_index] = completion_time[min_index] - processes[min_index][1]
        waiting_time[min_index] = turnaround_time[min_index] - processes[min_index][2]

# Display the results
print("Process\tArrival\tBurst\tCompletion\tWaiting\tTurnaround")
print("-" * 60)
for i in range(n):
    print(f"{processes[i][0]:<8}{processes[i][1]:<8}{processes[i][2]:<8}"
          f"{completion_time[i]:<12}{waiting_time[i]:<8}{turnaround_time[i]}")

# Calculate and display averages
avg_wait = round(sum(waiting_time) / n, 2)
avg_tat = round(sum(turnaround_time) / n, 2)
print("\nAverage Waiting Time =", avg_wait)
print("Average Turnaround Time =", avg_tat)
