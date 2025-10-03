# Mini HPC Cluster

A Docker-based HPC environment for distributed computing, fault tolerance, and cluster monitoring.

## Features

- 3-node cluster (1 master + 2 workers)
- Distributed PyTorch training with DDP
- Priority-based job queue
- Prometheus & Grafana monitoring
- Automatic fault recovery (15-30s)
- Persistent data and model storage
- Ansible configuration management

## Quick Start

```bash
git clone https://github.com/faraz-irshad/mini-hpc-cluster.git
cd mini-hpc-cluster
pip install -r requirements.txt
make build
make up
make submit
```

Access dashboards:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

![Grafana Dashboard](screenshots/grafana-dashboard.png)

## Requirements

- Docker & Docker Compose
- Python 3.8+
- Linux/macOS

## Commands

```bash
# Cluster
make build          # Build images
make up             # Start cluster
make down           # Stop cluster
make status         # Check status
make clean          # Clean everything

# Jobs
make submit         # Submit all jobs in jobs/
make queue          # View job queue
make logs           # View execution logs
make monitor        # Real-time monitoring

# Fault Tolerance
make health         # Check node health
make watch-recovery # Watch auto-recovery

# Configuration
make ansible-setup  # Configure cluster with Ansible

# ML Pipeline
make prepare-data   # Download MNIST dataset
make validate-model # Validate trained model
```

## Project Structure

```
mini-hpc/
├── ansible/                 # Ansible playbooks
│   ├── inventory.yml
│   └── setup_cluster.yml
├── config/                  # Configuration files
│   └── prometheus.yml
├── scripts/                 # Python scripts
│   ├── submit_job.py       # Job submission
│   ├── job_queue.py        # Queue management
│   ├── view_queue.py       # View queue status
│   ├── monitor_jobs.py     # Job monitoring
│   ├── recovery_monitor.py # Health checks
│   └── metrics_exporter.py # Prometheus exporter
├── jobs/                    # Job scripts
│   ├── hello.py
│   ├── benchmark.py
│   ├── prepare_mnist.py
│   ├── train_mnist_distributed.py
│   └── validate_mnist.py
├── data/                    # Persistent datasets
├── models/                  # Persistent model checkpoints
├── logs/                    # Execution logs
├── docker-compose.yml       # Cluster orchestration
├── Dockerfile              # Container image
├── Makefile                # Command shortcuts
├── requirements.txt        # Python dependencies
└── README.md
```

## Job Queue

Jobs execute sequentially. View queue status:
```bash
make queue
```

## Fault Tolerance

Health checks run every 30s. Failed nodes restart automatically.

Test it:
```bash
make health
docker stop worker-node-1
make watch-recovery  # Observe 15-30s recovery
```

## ML Lifecycle

1. **Data Prep**: `make prepare-data` downloads MNIST to `data/`
2. **Training**: `make submit` trains model, saves checkpoints to `models/`
3. **Validation**: `make validate-model` evaluates accuracy
4. **Monitoring**: View metrics in Grafana

Checkpoints saved every 5 epochs to `/root/models/`.

## Data Persistence

Volumes mounted in all containers:
- `./data` → `/root/data` (datasets)
- `./models` → `/root/models` (checkpoints)

Data survives container restarts.

## Technical Details

### Distributed Training
- Backend: Gloo (CPU-optimized)
- World size: 3 (1 master + 2 workers)
- Data parallelism with DistributedSampler
- Automatic gradient synchronization

### Monitoring
Metrics collected:
- `node_cpu_percent`
- `node_memory_percent`
- `node_memory_MemUsed_bytes`



## Creating Jobs

Create Python script in `jobs/`:

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

For distributed training, use PyTorch DDP with environment variables:
- `RANK`: Process rank (0 = master)
- `WORLD_SIZE`: Total processes (3)
- `MASTER_ADDR`: Master hostname
- `MASTER_PORT`: Communication port (12355)

## Skills Demonstrated

- HPC cluster management
- Distributed computing (PyTorch DDP)
- Docker containerization
- Monitoring (Prometheus/Grafana)
- Fault tolerance and recovery
- Job scheduling and queuing
- ML pipeline (data → train → validate)

## Future Improvements

- Multi-host cluster support
- GPU support with NCCL backend
- Parallel job execution
- Web UI for queue management
