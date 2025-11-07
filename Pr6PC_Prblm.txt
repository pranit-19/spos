import threading
import time
import random

# Shared buffer
buffer = []
BUFFER_SIZE = 3

# Semaphores
empty = threading.Semaphore(BUFFER_SIZE)  # counts empty slots
full = threading.Semaphore(0)             # counts full slots
mutex = threading.Semaphore(1)            # mutual exclusion

def producer():
    for i in range(10):
        item = random.randint(1, 100)
        empty.acquire()       # wait if buffer is full
        mutex.acquire()
        buffer.append(item)
        print(f"Producer produced: {item} | Buffer: {buffer}")
        mutex.release()
        full.release()        # signal item added
        time.sleep(random.uniform(0.5, 1.5))

def consumer():
    for i in range(10):
        full.acquire()        # wait if buffer empty
        mutex.acquire()
        item = buffer.pop(0)
        print(f"Consumer consumed: {item} | Buffer: {buffer}")
        mutex.release()
        empty.release()       # signal slot freed
        time.sleep(random.uniform(0.5, 1.5))

# Threads
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join()
t2.join()

print("\nProducer–Consumer problem solved using Semaphore.")
