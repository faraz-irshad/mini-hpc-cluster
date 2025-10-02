#!/usr/bin/env python3
"""Simulate node failures for testing fault tolerance."""

import docker
import sys
import time

def simulate_failure(node_name):
    """Kill a specific node to test auto-recovery."""
    try:
        client = docker.from_env()
        container = client.containers.get(node_name)
        print(f"[SIMULATE] Killing {node_name}...")
        container.kill()
        print(f"[SIMULATE] {node_name} killed. Docker will auto-restart it.")
        
        # Monitor recovery
        print("[SIMULATE] Monitoring recovery (30s)...")
        for i in range(6):
            time.sleep(5)
            container.reload()
            print(f"[SIMULATE] Status: {container.status}")
            if container.status == "running":
                print(f"[SIMULATE] ✓ {node_name} recovered successfully!")
                return True
        
        print(f"[SIMULATE] ✗ {node_name} did not recover in time")
        return False
        
    except docker.errors.NotFound:
        print(f"[ERROR] Container {node_name} not found")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 simulate_failure.py <node-name>")
        print("Available nodes: master-node, worker-node-1, worker-node-2")
        sys.exit(1)
    
    node_name = sys.argv[1]
    success = simulate_failure(node_name)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
