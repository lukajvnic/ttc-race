#!/bin/bash
# TTC Race - Kafka on Kubernetes Setup Script
# Run this from WSL

set -e

echo "=== TTC Race Kafka Setup ==="

# Step 1: Start minikube if not running
echo "1. Checking minikube status..."
if ! minikube status | grep -q "Running"; then
    echo "   Starting minikube..."
    minikube start
else
    echo "   Minikube is already running"
fi

# Step 2: Create namespace
echo "2. Creating namespace 'ttc-race'..."
kubectl create namespace ttc-race --dry-run=client -o yaml | kubectl apply -f -

# Step 3: Install Strimzi operator
echo "3. Installing Strimzi Kafka operator..."
kubectl create -f 'https://strimzi.io/install/latest?namespace=ttc-race' -n ttc-race 2>/dev/null || \
kubectl replace -f 'https://strimzi.io/install/latest?namespace=ttc-race' -n ttc-race

# Step 4: Wait for Strimzi operator to be ready
echo "4. Waiting for Strimzi operator to be ready..."
kubectl wait --for=condition=Ready pod -l name=strimzi-cluster-operator -n ttc-race --timeout=120s

# Step 5: Deploy Kafka NodePool
echo "5. Deploying Kafka NodePool..."
kubectl apply -f ttc-race-nodepool.yml -n ttc-race

# Step 6: Deploy Kafka cluster
echo "6. Deploying Kafka cluster..."
kubectl apply -f ttc-race-kafka.yml -n ttc-race

# Step 7: Create topic
echo "7. Creating Kafka topic..."
kubectl apply -f ttc-race-topic.yml -n ttc-race

# Step 8: Wait for Kafka to be ready
echo "8. Waiting for Kafka cluster to be ready (this may take a few minutes)..."
kubectl wait kafka/ttc-cluster --for=condition=Ready --timeout=300s -n ttc-race

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To access Kafka from your local machine, run:"
echo "  kubectl port-forward svc/ttc-cluster-kafka-bootstrap 9092:9092 -n ttc-race"
echo ""
echo "Then in separate terminals:"
echo "  python main.py           # Producer"
echo "  python test_consumer.py  # Consumer"
