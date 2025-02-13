# Lamport's Bakery Algorithm Implementation Guide

## Overview
Lamport's Bakery Algorithm is a solution to the mutual exclusion problem in concurrent programming. It's named after its similarity to how bakeries serve customers using numbered tickets.

### Key Concepts
- **Mutual Exclusion**: Only one process can access the critical section at a time
- **Progress**: If no process is in the critical section, a process wanting to enter will eventually do so
- **Bounded Waiting**: No process waits indefinitely (no starvation)

## How It Works

### Data Structures
```python
choosing = [False] * n_processes  # Indicates if a process is picking a number
number = [0] * n_processes       # Ticket numbers for each process
```

### Algorithm Steps

1. **Choosing Phase**:
   ```python
   choosing[i] = True
   number[i] = max(number) + 1
   choosing[i] = False
   ```

2. **Waiting Phase**:
   ```python
   for j in range(n_processes):
       # Wait while process j is choosing
       while choosing[j]: pass
       
       # Wait for processes with lower numbers
       while number[j] != 0 and (
           number[j] < number[i] or 
           (number[j] == number[i] and j < i)
       ): pass
   ```

3. **Critical Section**: Process executes its critical section

4. **Exit Phase**:
   ```python
   number[i] = 0
   ```

## Implementation Example

### Basic Usage
```python
# Create a lock for 3 processes
lock = BakeryLock(n_processes=3)

# In process i:
lock.lock(pid=i)
# Critical section code here
lock.unlock(pid=i)
```

### Complete Working Example
Here's a simple example demonstrating three processes incrementing a shared counter:

```python
def process_example(pid, lock, shared_counter):
    print(f"Process {pid} starting")
    
    lock.lock(pid)
    # Critical section
    current = shared_counter.value
    time.sleep(0.1)  # Simulate work
    shared_counter.value = current + 1
    print(f"Process {pid} incremented counter to {shared_counter.value}")
    lock.unlock(pid)
    
    print(f"Process {pid} finished")

# Usage
lock = BakeryLock(3)
counter = SharedCounter()

threads = []
for i in range(3):
    t = threading.Thread(target=process_example, args=(i, lock, counter))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### Sample Output
```
Process 0 starting
Process 0 wants to enter critical section
Process 0 entered critical section
Process 0 incremented counter to 1
Process 0 leaving critical section
Process 1 starting
Process 1 wants to enter critical section
Process 1 entered critical section
Process 1 incremented counter to 2
Process 1 leaving critical section
Process 2 starting
Process 2 wants to enter critical section
Process 2 entered critical section
Process 2 incremented counter to 3
Process 2 leaving critical section
Final counter value: 3
```

## Common Issues and Solutions

### Race Conditions
Without proper synchronization:
```python
# BAD - Race condition
counter += 1

# GOOD - Protected by lock
lock.lock(pid)
counter += 1
lock.unlock(pid)
```

### Deadlock Prevention
The algorithm naturally prevents deadlocks because:
- Processes can't wait circularly
- Ticket numbers ensure a total ordering
- The choosing phase prevents conflicts

## Performance Considerations

### Advantages
- No special hardware instructions needed
- Guaranteed fairness
- No starvation

### Limitations
- Requires shared memory
- Busy waiting consumes CPU
- Scales linearly with number of processes

## Testing

Test different scenarios:
```python
# Test with different process counts
lock = BakeryLock(n_processes=5)

# Test with high contention
for _ in range(100):
    # Spawn processes simultaneously
    
# Test with varying critical section durations
time.sleep(random.random())  # Random delays
```

## Debugging Tips

1. Add logging to track process states:
```python
print(f"Process {pid} ticket number: {self.number[pid]}")
print(f"All tickets: {self.number}")
```

2. Monitor for liveness:
```python
start_time = time.time()
while condition:
    if time.time() - start_time > timeout:
        print("Possible liveness issue detected")
        break
```

## Advanced Usage

### Custom Lock Class
```python
class CustomBakeryLock(BakeryLock):
    def __init__(self, n_processes, timeout=None):
        super().__init__(n_processes)
        self.timeout = timeout
    
    def lock(self, pid):
        start_time = time.time()
        super().lock(pid)
        if self.timeout and time.time() - start_time > self.timeout:
            raise TimeoutError("Lock acquisition timed out")
```

## Common Patterns

### Resource Pool
```python
class ResourcePool:
    def __init__(self, n_resources, n_processes):
        self.lock = BakeryLock(n_processes)
        self.resources = list(range(n_resources))
    
    def acquire(self, pid):
        self.lock.lock(pid)
        resource = self.resources.pop()
        self.lock.unlock(pid)
        return resource
    
    def release(self, pid, resource):
        self.lock.lock(pid)
        self.resources.append(resource)
        self.lock.unlock(pid)
```

Remember that this algorithm is primarily educational - in production systems, you'd typically use your language's built-in synchronization primitives. However, understanding Lamport's Bakery Algorithm provides valuable insights into concurrent programming concepts.
