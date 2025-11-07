import threading
import time
import random

NUM_PHIL = 5
EAT_ROUNDS = 3

# One semaphore per fork
forks = [threading.Semaphore(1) for _ in range(NUM_PHIL)]

def philosopher(i):
    left = forks[i]
    right = forks[(i + 1) % NUM_PHIL]
    for r in range(EAT_ROUNDS):
        print(f"Philosopher {i} is thinking (round {r+1}).")
        time.sleep(random.uniform(1, 2))

        print(f"Philosopher {i} is hungry.")
        # Deadlock avoidance: even pick left first, odd pick right first
        if i % 2 == 0:
            left.acquire()
            right.acquire()
        else:
            right.acquire()
            left.acquire()

        print(f"Philosopher {i} is eating (round {r+1}).")
        time.sleep(random.uniform(1, 2))

        left.release()
        right.release()

        print(f"Philosopher {i} finished eating (round {r+1}).\n")

threads = []
for i in range(NUM_PHIL):
    t = threading.Thread(target=philosopher, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Dining Philosophers problem solved using Semaphore.")
