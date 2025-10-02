#!/bin/bash

echo "Waiting for Grafana to be ready..."
sleep 10

echo "Adding Prometheus data source to Grafana..."
curl -X POST http://admin:admin@localhost:3000/api/datasources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prometheus",
    "type": "prometheus",
    "url": "http://prometheus:9090",
    "access": "proxy",
    "isDefault": true
  }'

echo -e "\n\nGrafana setup complete!"
echo "Access Grafana at: http://localhost:3000"
echo "Login: admin / admin"
echo "Prometheus data source added automatically"
