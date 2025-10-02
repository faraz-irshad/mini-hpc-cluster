import os
import subprocess
import sys
from pathlib import Path

# === CONFIGURATION ===
workers = ["worker-node-1", "worker-node-2"]
job_folder = Path("./jobs")

# === HELPER FUNCTIONS ===
def send_and_run(worker, job_file):
    remote_path = f"/root/{job_file.name}"
    print(f"[INFO] Sending {job_file} to {worker}...")
    
    # Copy job to worker
    subprocess.run(["docker", "cp", str(job_file), f"{worker}:{remote_path}"])
    
    # Execute job
    print(f"[INFO] Running {job_file} on {worker}...")
    result = subprocess.run(["docker", "exec", worker, "python3", remote_path], capture_output=True, text=True)
    
    # Print output
    print(f"--- Output from {worker} ---")
    print(result.stdout)
    print(result.stderr)
    print("----------------------------")

# === MAIN ===
if __name__ == "__main__":
    jobs = list(job_folder.glob("*.py"))
    if not jobs:
        print("No jobs found in ./jobs")
        sys.exit(1)
    
    # assignment
    for worker in workers:
        for job in jobs:
            send_and_run(worker, job)
