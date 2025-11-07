# Round Robin (Preemptive) CPU Scheduling Algorithm

from collections import deque

# Sample Input
time_quantum = 2
processes = [
    ['P1', 0, 6],
    ['P2', 1, 4],
    ['P3', 4, 8],
    ['P4', 3, 3]
]

# Sort by Arrival Time
processes.sort(key=lambda x: x[1])

n = len(processes)
remaining_time = [p[2] for p in processes]
completion_time = [0] * n
waiting_time = [0] * n
turnaround_time = [0] * n

t = 0   # current time
queue = deque()
in_queue = [False] * n
completed = 0

# Start with the first process if it arrives at time 0
queue.append(0)
in_queue[0] = True

while completed != n:
    if queue:
        idx = queue.popleft()

        # If process arrives later than current time, fast forward
        if processes[idx][1] > t:
            t = processes[idx][1]

        # Execute process for time quantum or until completion
        exec_time = min(time_quantum, remaining_time[idx])
        remaining_time[idx] -= exec_time
        t += exec_time

        # Add newly arrived processes to the queue
        for i in range(n):
            if not in_queue[i] and processes[i][1] <= t and remaining_time[i] > 0:
                queue.append(i)
                in_queue[i] = True

        # If process still has remaining burst, re-add it to the queue
        if remaining_time[idx] > 0:
            queue.append(idx)
        else:
            completion_time[idx] = t
            turnaround_time[idx] = completion_time[idx] - processes[idx][1]
            waiting_time[idx] = turnaround_time[idx] - processes[idx][2]
            completed += 1
    else:
        # No process is ready, move time forward
        t += 1
        for i in range(n):
            if not in_queue[i] and processes[i][1] <= t and remaining_time[i] > 0:
                queue.append(i)
                in_queue[i] = True

# Display Output Table
print(f"Time Quantum = {time_quantum}\n")
print("Process\tArrival\tBurst\tCompletion\tWaiting\tTurnaround")
print("-" * 60)
for i in range(n):
    print(f"{processes[i][0]:<8}{processes[i][1]:<8}{processes[i][2]:<8}"
          f"{completion_time[i]:<12}{waiting_time[i]:<8}{turnaround_time[i]}")

# Average Times
avg_wait = round(sum(waiting_time) / n, 2)
avg_tat = round(sum(turnaround_time) / n, 2)
print("\nAverage Waiting Time =", avg_wait)
print("Average Turnaround Time =", avg_tat)
