# Mini HPC Cluster Simulation

This project demonstrates a very small-scale High-Performance Computing (HPC) environment using Docker containers. It is intended as a **learning and demonstration tool** to explore how HPC clusters manage jobs, distribute workloads, and handle basic resource management.

---

## Features

* **Master and Worker Nodes:**

  * One master node to manage jobs.
  * Two worker nodes that execute jobs submitted by the master.

* **Python Job Submission System:**

  * Submit Python scripts (jobs) from the master node to worker nodes.
  * Round-robin assignment distributes jobs across available workers.
  * Collects and displays output from each worker in the master console.

* **Docker-Based Simulation:**

  * Each node runs in its own isolated Docker container.
  * Containers communicate over a private network to simulate a real HPC cluster.

* **Extensible Setup:**

  * Designed to allow adding monitoring tools (Prometheus, Grafana) or automated configuration (Ansible) as enhancements.
  * Simple structure makes it easy to experiment with different job types or more nodes.

---

## Installation

### Requirements

* Pop!_OS / Ubuntu or compatible Linux distribution
* Docker & Docker Compose
* Python 3
* Optional: Ansible for automation

### Setup

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/mini-hpc-cluster.git
cd mini-hpc-cluster
```

2. Launch the cluster:

```bash
docker compose up -d
```

3. Verify containers are running:

```bash
docker ps
```

---

## How to Use

1. Add your Python jobs to the `jobs/` folder. Each script should be a standalone Python file.

2. Submit jobs to the cluster:

```bash
python3 submit_job.py
```

3. The master node will distribute the jobs to worker nodes, execute them, and print output in the console.

4. To stop the cluster:

```bash
docker compose down
```

---

## Example

Adding a simple job:

```python
# jobs/hello.py
print("Hello from the worker!")
```

Submit it with:

```bash
python3 submit_job.py
```

Output example:

```
[INFO] Sending hello.py to worker-node-1...
[INFO] Running hello.py on worker-node-1...
Hello from the worker!
```

---

## Notes

* This project is **a simplified simulation**. It does not replicate the full performance or scale of production HPC clusters.
* Designed for **learning, experimentation, and demonstration**. The goal is modest: understanding HPC concepts in a small environment.

---

## License

This project is open for personal learning and demonstration purposes.

---
