# Fault Tolerance & Auto-Recovery

This cluster includes automatic fault tolerance and recovery mechanisms.

## Features

* **Auto-restart policies** - Containers automatically restart on failure
* **Health checks** - Monitor node health every 30 seconds
* **Recovery monitoring** - Track recovery status in real-time
* **Failure simulation** - Test fault tolerance with controlled failures

## Quick Start

### Check Cluster Health

```bash
make health
```

### Test Fault Tolerance

```bash
# Interactive mode - prompts for node selection
make test-failure

# Direct mode - specify node
python3 simulate_failure.py worker-node-1
```

### Watch Recovery in Real-Time

```bash
make watch-recovery
```

## How It Works

### 1. Restart Policies

All nodes use `restart: unless-stopped` policy:
- Automatically restart on crash
- Restart on Docker daemon restart
- Only stop when explicitly commanded

### 2. Health Checks

Each node runs health checks every 30 seconds:
- **Interval:** 30s between checks
- **Timeout:** 10s per check
- **Retries:** 3 failed checks before marking unhealthy
- **Start period:** 10s grace period on startup

### 3. Recovery Process

When a node fails:
1. Docker detects failure via health check or exit
2. Container automatically restarts
3. Health checks resume after start period
4. Node rejoins cluster network

## Testing Scenarios

### Scenario 1: Worker Node Failure

```bash
# Kill worker-node-1
python3 simulate_failure.py worker-node-1

# Expected: Node restarts within 30 seconds
# Jobs can be resubmitted to recovered node
```

### Scenario 2: Master Node Failure

```bash
# Kill master node
python3 simulate_failure.py master-node

# Expected: Master restarts, cluster coordination resumes
```

### Scenario 3: Multiple Failures

```bash
# Kill multiple nodes in sequence
python3 simulate_failure.py worker-node-1
python3 simulate_failure.py worker-node-2

# Monitor recovery
make watch-recovery
```

## Monitoring Commands

```bash
# One-time health check
make health

# Continuous monitoring (updates every 5s)
make watch-recovery

# Docker native status
docker compose ps

# Container restart counts
docker inspect worker-node-1 --format='{{.RestartCount}}'
```

## Recovery Metrics

Monitor these indicators:
- **Status:** Should be "running"
- **Health:** Should be "healthy" or "N/A"
- **Restart Count:** Tracks number of recoveries
- **Uptime:** Time since last restart

## Limitations

* Jobs running during failure will be lost
* Manual job resubmission required after recovery
* No automatic job checkpointing (future enhancement)
* Network partitions not handled

## Future Enhancements

* Job checkpointing and auto-resume
* Job queue persistence across failures
* Automatic job resubmission on node recovery
* Leader election for master failover
* Distributed job state tracking

## Troubleshooting

### Node won't restart

```bash
# Check logs
docker logs worker-node-1

# Manual restart
docker restart worker-node-1
```

### Health check failing

```bash
# Check health status
docker inspect worker-node-1 --format='{{.State.Health.Status}}'

# View health check logs
docker inspect worker-node-1 --format='{{range .State.Health.Log}}{{.Output}}{{end}}'
```

### Too many restarts

```bash
# Check restart count
docker inspect worker-node-1 --format='{{.RestartCount}}'

# If excessive, investigate root cause
docker logs worker-node-1 --tail 100
```

## Dependencies

Install required Python package:

```bash
pip install docker>=6.0.0
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```
