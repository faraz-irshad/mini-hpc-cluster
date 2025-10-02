#!/usr/bin/env python3
from prometheus_client import start_http_server, Gauge
import psutil
import time

cpu_percent = Gauge('node_cpu_percent', 'CPU usage percentage')
memory_total = Gauge('node_memory_MemTotal_bytes', 'Total memory in bytes')
memory_available = Gauge('node_memory_MemAvailable_bytes', 'Available memory in bytes')
memory_used = Gauge('node_memory_MemUsed_bytes', 'Used memory in bytes')
memory_percent = Gauge('node_memory_percent', 'Memory usage percentage')

def collect_metrics():
    while True:
        cpu_percent.set(psutil.cpu_percent(interval=1))
        mem = psutil.virtual_memory()
        memory_total.set(mem.total)
        memory_available.set(mem.available)
        memory_used.set(mem.used)
        memory_percent.set(mem.percent)
        time.sleep(5)

if __name__ == '__main__':
    start_http_server(9100)
    collect_metrics()
