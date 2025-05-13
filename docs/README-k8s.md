# Kubernetes High Availability Deployment for Word Train Webapp

This guide explains how to deploy the Word Train Flask application to a local Kubernetes cluster using KIND (Kubernetes IN Docker) with high availability and scalability features.

## Prerequisites

- Docker
- kubectl
- KIND (Kubernetes IN Docker)
- Git

## Files Overview

- `k8s/deployment.yaml`: Manages the application pods with high availability settings
- `k8s/pod.yaml`: Standalone Pod definition (for testing or one-off pods)
- `k8s/service.yaml`: Exposes the application internally
- `k8s/configmap.yaml`: Stores non-sensitive configuration
- `k8s/secret.yaml`: Stores sensitive information
- `k8s/ingress.yaml`: Exposes the application externally with session affinity
- `k8s/hpa.yaml`: Horizontal Pod Autoscaler for automatic scaling
- `k8s/pdb.yaml`: Pod Disruption Budget for availability guarantees
- `k8s/metrics-server.yaml`: Required for HPA functionality
- `setup-kind.sh`: Script to create a multi-node KIND cluster and deploy the application
- `cleanup-kind.sh`: Script to delete the KIND cluster and save logs

## High Availability & Scalability Features

This configuration includes:

- **Multiple replicas**: Starts with 3 replicas for redundancy
- **Pod anti-affinity**: Spreads pods across different nodes
- **Rolling updates**: Zero downtime during deployments
- **Horizontal Pod Autoscaler**: Automatically scales based on CPU/memory usage
- **Pod Disruption Budget**: Ensures minimum availability during voluntary disruptions
- **Robust health checks**: Liveness, readiness, and startup probes
- **Session affinity**: Sticky sessions for better user experience
- **Multi-node cluster**: Runs on multiple worker nodes

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ertwrx/word_train_webapp.git
cd word_train_webapp
```

### 2. Copy the Kubernetes files to the repository

Create the k8s directory and copy all the Kubernetes files into it.

### 3. Make the scripts executable

```bash
chmod +x setup-kind.sh cleanup-kind.sh
```

### 4. Run the setup script

```bash
./setup-kind.sh
```

This script will:
- Create a multi-node KIND cluster
- Pull the Docker image from DockerHub
- Load the image into KIND
- Install metrics server for HPA
- Install NGINX Ingress Controller
- Deploy the application with HA configuration
- Apply the HPA for automatic scaling

### 5. Access the application

Once deployed, the application will be available at:
http://localhost:8080

### 6. Clean up

When you're done, run the cleanup script to delete the KIND cluster and save logs:

```bash
./cleanup-kind.sh
```

## Monitoring and Scaling

### Check HPA status

```bash
kubectl get hpa
```

### Scale manually if needed

```bash
kubectl scale deployment word-train-app --replicas=5
```

### View pod distribution

```bash
kubectl get pods -o wide
```

## Kubernetes Resources

### Deployment
- 3 replicas minimum
- Rolling update strategy for zero downtime
- Pod anti-affinity to spread across nodes
- Resource limits and requests
- Health checks with liveness, readiness, and startup probes

### Service
- ClusterIP type for internal routing

### Ingress
- Configured with session affinity (sticky sessions)
- Proxy body size increased to 50MB
- SSL redirect disabled (for local testing)

### HorizontalPodAutoscaler
- Scales from 3 to 10 replicas based on CPU (70%) and memory (80%) usage
- Customized scaling behavior for responsiveness

### PodDisruptionBudget
- Ensures at least 2 pods are always available during voluntary disruptions

## Troubleshooting

### Check Pod status

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Creating a standalone Pod (for testing)

If you want to run a single instance of the application for testing:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pod.yaml
```

You can then check the status of your pod:

```bash
kubectl get pod word-train-pod
kubectl describe pod word-train-pod
kubectl logs word-train-pod
```

Note: When using a standalone Pod, you won't have features like automatic recovery, scaling, or rolling updates that come with Deployments.

### Check HPA status

```bash
kubectl get hpa
kubectl describe hpa word-train-hpa
```

### Check node status

```bash
kubectl get nodes
kubectl describe node <node-name>
```

### Check ingress status

```bash
kubectl get ingress
kubectl describe ingress word-train-ingress
```

### Check metrics server

```bash
kubectl get pods -n kube-system | grep metrics-server
kubectl top nodes
kubectl top pods
