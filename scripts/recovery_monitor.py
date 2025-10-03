#!/usr/bin/env python3
"""Monitor cluster health and recovery status."""

import docker
import time
from datetime import datetime

def check_cluster_health():
    """Check health status of all cluster nodes."""
    try:
        client = docker.from_env()
        nodes = ['master-node', 'worker-node-1', 'worker-node-2']
        
        print(f"\n{'='*60}")
        print(f"Cluster Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        all_healthy = True
        
        for node_name in nodes:
            try:
                container = client.containers.get(node_name)
                status = container.status
                health = container.attrs.get('State', {}).get('Health', {}).get('Status', 'N/A')
                
                status_icon = "✓" if status == "running" else "✗"
                health_icon = "✓" if health in ["healthy", "N/A"] else "✗"
                
                print(f"{status_icon} {node_name:20} Status: {status:10} Health: {health}")
                
                if status != "running":
                    all_healthy = False
                    restart_count = container.attrs.get('RestartCount', 0)
                    print(f"  └─ Restart count: {restart_count}")
                    
            except docker.errors.NotFound:
                print(f"✗ {node_name:20} NOT FOUND")
                all_healthy = False
        
        print(f"\n{'='*60}")
        if all_healthy:
            print("✓ All nodes healthy")
        else:
            print("✗ Some nodes unhealthy - auto-recovery in progress")
        print(f"{'='*60}\n")
        
        return all_healthy
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    check_cluster_health()

if __name__ == "__main__":
    main()
