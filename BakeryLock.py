import threading
import time
import random

class BakeryLock:
    def __init__(self, n_processes):
        self.n = n_processes
        self.choosing = [False] * n_processes  # Choosing flag for each process
        self.number = [0] * n_processes        # Ticket number for each process
        
    def lock(self, pid):
        # Step 1: Process starts choosing a number
        self.choosing[pid] = True
        
        # Step 2: Pick a ticket number higher than all others
        self.number[pid] = max(self.number) + 1
        
        # Step 3: Process is done choosing
        self.choosing[pid] = False
        
        # Step 4: Wait for our turn
        for j in range(self.n):
            # Wait while process j is choosing
            while self.choosing[j]:
                pass
            
            # Wait while processes with smaller numbers or same number but higher priority are served
            while self.number[j] != 0 and (
                self.number[j] < self.number[pid] or 
                (self.number[j] == self.number[pid] and j < pid)
            ):
                pass
    
    def unlock(self, pid):
        self.number[pid] = 0

# Shared resource - in this case, a simple counter
class SharedCounter:
    def __init__(self):
        self.count = 0
        
    def increment(self):
        temp = self.count
        time.sleep(random.random() * 0.1)  # Simulate some work
        self.count = temp + 1

# Process simulation
def process_work(pid, lock, counter, n_iterations):
    for _ in range(n_iterations):
        print(f"Process {pid} wants to enter critical section")
        lock.lock(pid)
        
        # Critical section
        print(f"Process {pid} entered critical section")
        counter.increment()
        print(f"Process {pid} incremented counter to {counter.count}")
        time.sleep(random.random() * 0.2)  # Simulate some work
        print(f"Process {pid} leaving critical section")
        
        lock.unlock(pid)
        
        # Non-critical section
        time.sleep(random.random() * 0.5)  # Simulate non-critical work

# Test the implementation
def main():
    n_processes = 3
    n_iterations = 2
    
    lock = BakeryLock(n_processes)
    counter = SharedCounter()
    threads = []
    
    # Create and start threads
    for i in range(n_processes):
        thread = threading.Thread(
            target=process_work,
            args=(i, lock, counter, n_iterations)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"\nFinal counter value: {counter.count}")
    print(f"Expected counter value: {n_processes * n_iterations}")

if __name__ == "__main__":
    main()
