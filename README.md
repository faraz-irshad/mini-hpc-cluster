# Mini HPC Cluster Simulation

A Docker-based High-Performance Computing (HPC) environment for learning distributed computing concepts. Features job submission, monitoring, and distributed PyTorch training.

---

## Features

* **Distributed Architecture:** 1 master + 2 worker nodes with health checks
* **Fault Tolerance:** Auto-restart policies and recovery monitoring
* **Job Management:** Automated job submission with logging and queue system
* **Monitoring:** Prometheus & Grafana integration, real-time job monitoring
* **PyTorch Support:** Distributed training with Gloo backend
* **Easy Management:** Makefile commands for common operations

---

## Quick Start

```bash
git clone https://github.com/faraz-irshad/mini-hpc-cluster.git
cd mini-hpc-cluster
make build
make up
make submit
```

---

## Requirements

* Docker & Docker Compose
* Python 3
* Linux/macOS (tested on Pop!_OS/Ubuntu)

---

## Usage

### Basic Commands

```bash
make build          # Build containers
make up             # Start cluster
make down           # Stop cluster
make submit         # Submit jobs
make status         # Check cluster status
make logs           # View recent logs
make monitor        # Real-time monitoring
make health         # Check cluster health
make test-failure   # Test fault tolerance
make watch-recovery # Watch recovery status
make clean          # Clean everything
```

### Manual Commands

```bash
docker compose up -d              # Start cluster
python3 submit_job.py             # Submit jobs
python3 monitor_jobs.py           # Check status
docker compose down               # Stop cluster
```

### Restart Cluster

```bash
make down && make up              # Quick restart
make clean && make build && make up  # Full rebuild
```

---

## Project Structure

```
mini-hpc/
├── jobs/                    # Job scripts
│   ├── hello.py            # Simple test job
│   ├── benchmark.py        # Performance benchmark
│   └── train_mnist_distributed.py  # Distributed training
├── logs/                    # Job execution logs
├── screenshots/             # Dashboard screenshots
│   └── grafana-dashboard.png
├── Dockerfile              # Container image
├── docker-compose.yml      # Cluster configuration
├── requirements.txt        # Python dependencies
├── prometheus.yml          # Prometheus configuration
├── submit_job.py           # Job submission script
├── monitor_jobs.py         # Monitoring tool
├── job_queue.py            # Job queue system
├── metrics_exporter.py     # Metrics collection
├── simulate_failure.py     # Fault tolerance testing
├── recovery_monitor.py     # Recovery monitoring
├── setup_grafana.sh        # Grafana setup script
├── Makefile                # Command shortcuts
├── METRICS_GUIDE.md        # Metrics documentation
├── FAULT_TOLERANCE.md      # Fault tolerance guide
└── README.md
```

---

## Adding Jobs

Create a Python script in `jobs/` folder:

```python
# jobs/my_job.py
import os
print(f"Running on {os.uname().nodename}")
```

Submit with:

```bash
make submit
```

View logs:

```bash
make logs
# or
cat logs/worker-node-1_my_job.log
```

---

## Monitoring

* **Prometheus:** http://localhost:9090
* **Grafana:** http://localhost:3000 (admin/admin)
* **Job Logs:** `logs/` directory
* **Cluster Log:** `hpc_cluster.log`

### Live Dashboard

![HPC Cluster Monitoring](screenshots/grafana-dashboard.png)

Real-time CPU and memory metrics across all nodes during distributed job execution.

---

### Grafana Queries

```promql
# CPU usage per node
node_cpu_percent

# Memory usage percentage
node_memory_percent

# Memory used in GB
node_memory_MemUsed_bytes / 1024 / 1024 / 1024
```

---

## Example Jobs

### Simple Job (hello.py)
```python
import os
rank = os.environ.get("RANK", "0")
node = os.uname().nodename
print(f"[Rank {rank}] Hello from {node}!")
```

### Benchmark
```bash
make submit  # Runs benchmark.py on all nodes
```

### Distributed Training
```bash
# Automatically runs train_mnist_distributed.py across cluster
make submit
```

---

## Fault Tolerance

The cluster includes automatic recovery mechanisms:

```bash
# Check cluster health
make health

# Test fault tolerance by killing a node
make test-failure

# Watch recovery in real-time
make watch-recovery
```

See [FAULT_TOLERANCE.md](FAULT_TOLERANCE.md) for detailed documentation.

---

## Notes

* Educational tool for learning HPC concepts
* Not for production use
* CPU-only PyTorch (lightweight)
* Logs saved per node per job
* Auto-restart on node failures

---

## License

MIT
