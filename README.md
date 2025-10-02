# Mini HPC Cluster Simulation

A Docker-based High-Performance Computing (HPC) environment for learning distributed computing concepts. Features job submission, monitoring, and distributed PyTorch training.

---

## Features

* **Distributed Architecture:** 1 master + 2 worker nodes with health checks
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
make build     # Build containers
make up        # Start cluster
make down      # Stop cluster
make submit    # Submit jobs
make status    # Check cluster status
make logs      # View recent logs
make monitor   # Real-time monitoring
make clean     # Clean everything
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
├── Dockerfile              # Container image
├── docker-compose.yml      # Cluster configuration
├── requirements.txt        # Python dependencies
├── submit_job.py           # Job submission script
├── monitor_jobs.py         # Monitoring tool
├── job_queue.py            # Job queue system
├── Makefile                # Command shortcuts
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

---

## Example Jobs

### Simple Job
```python
print("Hello from the worker!")
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

## Notes

* Educational tool for learning HPC concepts
* Not for production use
* CPU-only PyTorch (lightweight)
* Logs saved per node per job

---

## License

MIT
