import threading
import time
import random

read_count = 0
mutex = threading.Semaphore(1)
rw_mutex = threading.Semaphore(1)
RUNS = 3

def reader(id):
    global read_count
    for i in range(RUNS):
        time.sleep(random.uniform(0.5, 1.5))
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            rw_mutex.acquire()  # first reader blocks writer
        mutex.release()

        print(f"Reader {id} is reading (round {i+1})...")
        time.sleep(random.uniform(0.5, 1.5))

        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            rw_mutex.release()  # last reader unblocks writer
        mutex.release()

def writer(id):
    for i in range(RUNS):
        time.sleep(random.uniform(1, 2))
        rw_mutex.acquire()
        print(f"Writer {id} is writing (round {i+1})...")
        time.sleep(random.uniform(1, 2))
        rw_mutex.release()

# Threads
r1 = threading.Thread(target=reader, args=(1,))
r2 = threading.Thread(target=reader, args=(2,))
w1 = threading.Thread(target=writer, args=(1,))

r1.start()
r2.start()
w1.start()
r1.join()
r2.join()
w1.join()

print("\nReader–Writer problem solved using Semaphore.")
