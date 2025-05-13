#!/bin/bash
set -e

# Check if KIND is installed
if ! command -v kind &> /dev/null; then
    echo "KIND is not installed. Please install it first."
    exit 1
fi

# Save logs before deleting the cluster
echo "Saving application logs before cleanup..."
mkdir -p logs
kubectl logs -l app=word-train-app --tail=1000 > logs/app_logs_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || true

# Delete the KIND cluster
echo "Deleting KIND cluster 'word-train'..."
kind delete cluster --name word-train

echo "Cleanup complete! Application logs have been saved to the logs directory."
