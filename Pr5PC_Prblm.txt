import threading
import time
import random

buffer = []
BUFFER_SIZE = 5

# Mutex and semaphores
mutex = threading.Lock()
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

def producer():
    for i in range(10):
        item = random.randint(1, 100)
        empty.acquire()  # wait if buffer full
        mutex.acquire()
        buffer.append(item)
        print(f"Producer produced: {item} | Buffer: {buffer}")
        mutex.release()
        full.release()  # signal buffer not empty
        time.sleep(random.uniform(0.5, 1.5))

def consumer():
    for i in range(10):
        full.acquire()  # wait if buffer empty
        mutex.acquire()
        item = buffer.pop(0)
        print(f"Consumer consumed: {item} | Buffer: {buffer}")
        mutex.release()
        empty.release()  # signal buffer has space
        time.sleep(random.uniform(0.5, 1.5))

# Threads
t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join()
t2.join()

print("\n✅ All items produced and consumed successfully!")
