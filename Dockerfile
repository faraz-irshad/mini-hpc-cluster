FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install numpy psutil prometheus-client

WORKDIR /root

COPY metrics_exporter.py /root/

CMD ["sh", "-c", "python3 /root/metrics_exporter.py & sleep infinity"]