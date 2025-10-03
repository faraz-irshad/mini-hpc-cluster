#!/usr/bin/env python3
import json
import time
from pathlib import Path
from datetime import datetime

class JobQueue:
    def __init__(self, queue_file="job_queue.json"):
        self.queue_file = Path(queue_file)
        self.jobs = self._load_queue()
    
    def _load_queue(self):
        if self.queue_file.exists():
            with open(self.queue_file) as f:
                return json.load(f)
        return []
    
    def _save_queue(self):
        with open(self.queue_file, 'w') as f:
            json.dump(self.jobs, f, indent=2)
    
    def add_job(self, job_file, priority=1):
        job_id = f"job_{int(time.time())}_{len(self.jobs)}"
        job = {
            "id": job_id,
            "file": str(job_file),
            "priority": priority,
            "status": "queued",
            "created": datetime.now().isoformat()
        }
        self.jobs.append(job)
        self._save_queue()
        return job["id"]
    
    def get_next_job(self):
        queued_jobs = [j for j in self.jobs if j["status"] == "queued"]
        if queued_jobs:
            job = max(queued_jobs, key=lambda x: x["priority"])
            job["status"] = "running"
            self._save_queue()
            return job
        return None
    
    def complete_job(self, job_id):
        for job in self.jobs:
            if job["id"] == job_id:
                job["status"] = "completed"
                job["completed"] = datetime.now().isoformat()
        self._save_queue()
    
    def list_jobs(self):
        return self.jobs