# Mini HPC Cluster Simulation

A Docker-based HPC environment for learning distributed computing, fault tolerance, and cluster monitoring.

## Features

- 1 master + 2 worker nodes
- Auto-restart on failures with health checks
- Prometheus & Grafana monitoring
- Job queue system
- Distributed PyTorch training

## Quick Start

```bash
git clone https://github.com/faraz-irshad/mini-hpc-cluster.git
cd mini-hpc-cluster
pip install -r requirements.txt
make build
make up
make submit
```

**Dashboards:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Requirements

- Docker & Docker Compose
- Python 3.8+
- Linux/macOS

## Commands

```bash
make build          # Build images
make up             # Start cluster
make down           # Stop cluster
make submit         # Submit jobs
make logs           # View logs
make monitor        # Real-time monitoring
make health         # Check health
make test-failure   # Simulate failure
make watch-recovery # Watch recovery
make clean          # Clean everything
```

## Project Structure

```
mini-hpc/
├── jobs/                    # Job scripts
├── logs/                    # Execution logs
├── Dockerfile
├── docker-compose.yml
├── submit_job.py
├── monitor_jobs.py
├── simulate_failure.py      # Fault tolerance testing
├── recovery_monitor.py      # Health monitoring
├── Makefile
└── README.md
```

## Creating Jobs

Create a Python script in `jobs/`:

```python
# jobs/my_job.py
import os
node = os.uname().nodename
rank = os.environ.get("RANK", "0")
print(f"[Rank {rank}] Running on {node}")
```

Submit:
```bash
make submit
```

## Monitoring

Metrics available in Prometheus/Grafana:
- `node_cpu_percent`
- `node_memory_percent`
- `node_memory_MemUsed_bytes`

## Fault Tolerance

Containers auto-restart on failure with health checks every 30s.

Test it:
```bash
make health
make test-failure
make watch-recovery
```

Recovery time: 15-30 seconds

## Documentation

- [FAULT_TOLERANCE.md](FAULT_TOLERANCE.md) - Fault tolerance guide
