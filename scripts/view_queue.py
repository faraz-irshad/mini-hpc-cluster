#!/usr/bin/env python3
"""View job queue status"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from job_queue import JobQueue
from datetime import datetime

def main():
    queue = JobQueue()
    jobs = queue.list_jobs()
    
    if not jobs:
        print("Queue is empty")
        return
    
    print(f"\n{'='*70}")
    print(f"Job Queue Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    for job in jobs:
        status_icon = {
            "queued": "⏳",
            "running": "▶️",
            "completed": "✅"
        }.get(job["status"], "❓")
        
        print(f"{status_icon} {job['id']}")
        print(f"   File: {job['file']}")
        print(f"   Status: {job['status']}")
        print(f"   Priority: {job['priority']}")
        print(f"   Created: {job['created']}")
        if "completed" in job:
            print(f"   Completed: {job['completed']}")
        print()

if __name__ == "__main__":
    main()
