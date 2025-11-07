# FCFS CPU Scheduling

processes = [
    ['P1', 0, 3],
    ['P2', 2, 6],
    ['P3', 4, 4],
    ['P4', 6, 5],
    ['P5', 8, 2]
]

# Sort by Arrival Time
processes.sort(key=lambda x: x[1])

# Lists to store computed values
start_time = []
finish_time = []
waiting_time = []
turnaround_time = []

# First process
start_time.append(processes[0][1])
finish_time.append(start_time[0] + processes[0][2])
waiting_time.append(0)
turnaround_time.append(finish_time[0] - processes[0][1])

# Remaining processes
for i in range(1, len(processes)):
    start_time.append(max(processes[i][1], finish_time[i-1]))
    finish_time.append(start_time[i] + processes[i][2])
    waiting_time.append(start_time[i] - processes[i][1])
    turnaround_time.append(finish_time[i] - processes[i][1])

# Display Table (well-aligned)
print("Process\tArrival\tBurst\tStart\tFinish\tWaiting\tTurnaround")
print("-" * 60)
for i in range(len(processes)):
    print(f"{processes[i][0]:<8}{processes[i][1]:<8}{processes[i][2]:<8}"
          f"{start_time[i]:<8}{finish_time[i]:<8}{waiting_time[i]:<10}{turnaround_time[i]}")

# Average times
avg_wait = round(sum(waiting_time) / len(waiting_time), 2)
avg_tat = round(sum(turnaround_time) / len(turnaround_time), 2)

print("\nAverage Waiting Time =", avg_wait)
print("Average Turnaround Time =", avg_tat)
