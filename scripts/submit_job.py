import os
import subprocess
import sys
import logging
import time
from pathlib import Path
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from job_queue import JobQueue

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
            return None
        
        logger.info(f"[{job_id}] Executing {job_file.name} on {node} (RANK={rank})")
        
        log_file = Path(f"logs/{node}_{job_file.stem}.log")
        log_file.parent.mkdir(exist_ok=True)

        # Launch process
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
        return process
        
    except Exception as e:
        logger.error(f"[{job_id}] Exception occurred: {str(e)}")
        return None


# === MAIN ===
if __name__ == "__main__":
    queue = JobQueue()
    jobs = list(job_folder.glob("*.py"))
    if not jobs:
        logger.warning("No jobs found in ./jobs directory")
        sys.exit(1)
    
    world_size = 1 + len(workers)
    logger.info(f"Starting job submission - Found {len(jobs)} jobs, world_size={world_size}")

    # Add jobs to queue
    for job in jobs:
        job_id = queue.add_job(job)
        logger.info(f"Added {job.name} to queue with ID: {job_id}")
    
    # Process queue
    while True:
        job_info = queue.get_next_job()
        if not job_info:
            break
        
        job_file = Path(job_info["file"])
        logger.info(f"Processing job: {job_file.name} (ID: {job_info['id']})")
        
        processes = []
        
        # Run master
        master_proc = send_and_run(master, job_file, rank=0, world_size=world_size, master_addr=master)
        if master_proc:
            processes.append(master_proc)
        time.sleep(3)  # Wait for master to initialize
        
        # Run workers
        for i, worker in enumerate(workers):
            worker_proc = send_and_run(worker, job_file, rank=i+1, world_size=world_size, master_addr=master)
            if worker_proc:
                processes.append(worker_proc)
        
        # Wait for all processes to complete
        logger.info(f"Waiting for job {job_info['id']} to complete...")
        for proc in processes:
            proc.wait()
        
        queue.complete_job(job_info["id"])
        logger.info(f"Completed job: {job_info['id']}")
        time.sleep(2)  # Brief pause between jobs
    
    logger.info("Job submission completed")
