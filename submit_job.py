import os
import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime

# === LOGGING SETUP ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hpc_cluster.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# === CONFIGURATION ===
master = "master-node"
workers = ["worker-node-1", "worker-node-2"]
job_folder = Path("./jobs")
MASTER_PORT = 12355

# === HELPER FUNCTIONS ===
def send_and_run(node, job_file, rank, world_size, master_addr):
    remote_path = f"/root/{job_file.name}"
    job_id = f"{job_file.stem}_{node}_{datetime.now().strftime('%H%M%S')}"
    
    try:
        logger.info(f"[{job_id}] Sending {job_file.name} to {node}")
        
        # Copy job to node
        copy_result = subprocess.run(["docker", "cp", str(job_file), f"{node}:{remote_path}"], 
                                   capture_output=True, text=True)
        if copy_result.returncode != 0:
            logger.error(f"[{job_id}] Failed to copy job: {copy_result.stderr}")
            return
        
        logger.info(f"[{job_id}] Executing {job_file.name} on {node} (RANK={rank})")
        
        log_file = Path(f"logs/{node}_{job_file.stem}.log")
        log_file.parent.mkdir(exist_ok=True)

        # Launch in background
        with open(log_file, "w") as f:
            process = subprocess.Popen([
                "docker", "exec", node,
                "env",
                f"RANK={rank}",
                f"WORLD_SIZE={world_size}",
                f"MASTER_ADDR={master_addr}",
                f"MASTER_PORT={MASTER_PORT}",
                "python3", remote_path
            ], stdout=f, stderr=subprocess.STDOUT)

        logger.info(f"[{job_id}] Job launched, logs saved to {log_file}")
        
    except Exception as e:
        logger.error(f"[{job_id}] Exception occurred: {str(e)}")


# === MAIN ===
if __name__ == "__main__":
    jobs = list(job_folder.glob("*.py"))
    if not jobs:
        logger.warning("No jobs found in ./jobs directory")
        sys.exit(1)
    
    world_size = 1 + len(workers)  # master + workers
    logger.info(f"Starting job submission - Found {len(jobs)} jobs, world_size={world_size}")

    for job in jobs:
        logger.info(f"Processing job: {job.name}")
        
        # Run master
        send_and_run(master, job, rank=0, world_size=world_size, master_addr=master)
        
        # Run workers
        for i, worker in enumerate(workers):
            send_and_run(worker, job, rank=i+1, world_size=world_size, master_addr=master)
    
    logger.info("Job submission completed")
