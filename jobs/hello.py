import os

rank = os.environ.get("RANK", "0")
node = os.uname().nodename

print(f"[Rank {rank}] Hello from {node}!")
