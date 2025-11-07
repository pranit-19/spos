# Priority (Non-Preemptive) CPU Scheduling
# (Lower number = Higher Priority)

# Sample Input
processes = [
    ['P1', 0, 8, 1],
    ['P2', 0, 6, 2],
    ['P3', 2, 1, 3],
    ['P4', 3, 2, 0]
]

# Sort initially by Arrival Time
processes.sort(key=lambda x: x[1])

n = len(processes)
completed = 0
t = 0  # current time

waiting_time = [0] * n
turnaround_time = [0] * n
completion_time = [0] * n
is_completed = [False] * n

# Simulation loop
while completed != n:
    # Find process with highest priority (lowest priority number)
    idx = -1
    highest_priority = float('inf')
    for i in range(n):
        if processes[i][1] <= t and not is_completed[i]:
            if processes[i][3] < highest_priority:
                highest_priority = processes[i][3]
                idx = i
            elif processes[i][3] == highest_priority:
                # If same priority, pick earliest arrival
                if processes[i][1] < processes[idx][1]:
                    idx = i

    if idx != -1:
        start_time = t
        finish_time = start_time + processes[idx][2]
        t = finish_time

        completion_time[idx] = finish_time
        turnaround_time[idx] = completion_time[idx] - processes[idx][1]
        waiting_time[idx] = turnaround_time[idx] - processes[idx][2]

        is_completed[idx] = True
        completed += 1
    else:
        # No process ready yet, increment time
        t += 1

# Display table
print("Process\tArrival\tBurst\tPriority\tCompletion\tWaiting\tTurnaround")
print("-" * 70)
for i in range(n):
    print(f"{processes[i][0]:<8}{processes[i][1]:<8}{processes[i][2]:<8}"
          f"{processes[i][3]:<10}{completion_time[i]:<12}"
          f"{waiting_time[i]:<8}{turnaround_time[i]}")

# Average times
avg_wait = round(sum(waiting_time) / n, 2)
avg_tat = round(sum(turnaround_time) / n, 2)

print("\nAverage Waiting Time =", avg_wait)
print("Average Turnaround Time =", avg_tat)
