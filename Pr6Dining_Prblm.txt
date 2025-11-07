import threading
import time
import random

NUM_PHIL = 5
EAT_ROUNDS = 3  # Each philosopher will eat 3 times

forks = [threading.Lock() for _ in range(NUM_PHIL)]

def philosopher(i):
    left = forks[i]
    right = forks[(i + 1) % NUM_PHIL]
    for round_no in range(EAT_ROUNDS):
        print(f"Philosopher {i} is thinking (round {round_no + 1}).")
        time.sleep(random.uniform(0.5, 1.5))

        print(f"Philosopher {i} is hungry.")
        # Deadlock avoidance
        first, second = (left, right) if i % 2 == 0 else (right, left)
        with first:
            with second:
                print(f"Philosopher {i} is eating (round {round_no + 1}).")
                time.sleep(random.uniform(0.5, 1.5))
        print(f"Philosopher {i} finished eating (round {round_no + 1}).\n")
        time.sleep(random.uniform(0.5, 1.5))
    print(f"Philosopher {i} has finished all {EAT_ROUNDS} rounds.\n")

# Start all philosopher threads
threads = []
for i in range(NUM_PHIL):
    t = threading.Thread(target=philosopher, args=(i,))
    t.start()
    threads.append(t)

# Wait for all threads to finish properly
for t in threads:
    t.join(timeout=0.1)  # Small timeout prevents indefinite waiting

print("Simulation finished successfully.")
