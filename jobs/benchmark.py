import time
import os
import numpy as np

def cpu_benchmark():
    start = time.time()
    # Matrix multiplication benchmark
    a = np.random.rand(1000, 1000)
    b = np.random.rand(1000, 1000)
    c = np.dot(a, b)
    end = time.time()
    return end - start

if __name__ == "__main__":
    rank = os.environ.get("RANK", "0")
    node = os.uname().nodename
    
    print(f"[Rank {rank}] Running benchmark on {node}")
    
    duration = cpu_benchmark()
    print(f"[Rank {rank}] Matrix multiplication (1000x1000) took {duration:.2f} seconds")
    
    print(f"[Rank {rank}] Benchmark completed")