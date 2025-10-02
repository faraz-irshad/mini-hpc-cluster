FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt --index-url https://download.pytorch.org/whl/cpu

WORKDIR /root

CMD ["sleep", "infinity"]