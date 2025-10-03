#!/usr/bin/env python3
import subprocess
import time
from pathlib import Path

def get_container_status():
    result = subprocess.run(["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"], 
                          capture_output=True, text=True)
    return result.stdout

def show_recent_logs():
    log_dir = Path("logs")
    if log_dir.exists():
        log_files = sorted(log_dir.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
        for log_file in log_files[:3]:  # Show 3 most recent
            print(f"\n=== {log_file.name} ===")
            with open(log_file) as f:
                lines = f.readlines()
                print(''.join(lines[-5:]))  # Last 5 lines

if __name__ == "__main__":
    print("=== HPC Cluster Status ===")
    print(get_container_status())
    show_recent_logs()