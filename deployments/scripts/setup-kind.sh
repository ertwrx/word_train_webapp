#!/bin/bash
set -e

# Check if KIND is installed
if ! command -v kind &> /dev/null; then
    echo "KIND is not installed. Please install it first."
    echo "https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install it first."
    echo "https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if Docker is installed and running
if ! docker info &> /dev/null; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Create a KIND cluster configuration with port mapping and multiple nodes for HA
cat > kind-config.yaml << EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 8080
    protocol: TCP
  - containerPort: 30080
    hostPort: 30080
    protocol: TCP
- role: worker
- role: worker
EOF

# Create a KIND cluster
echo "Creating KIND cluster with multiple nodes..."
kind create cluster --name word-train --config kind-config.yaml

# Pull the Docker image from DockerHub
echo "Pulling Docker image from DockerHub..."
docker pull ertwrx/word_train_webapp:latest

# Load the Docker image into KIND
echo "Loading Docker image into KIND..."
kind load docker-image ertwrx/word_train_webapp:latest --name word-train

# Install metrics server for HPA
echo "Installing metrics server..."
kubectl apply -f k8s/metrics-server.yaml

# Install Ingress NGINX
echo "Installing NGINX Ingress Controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Wait for Ingress controller to be ready
echo "Waiting for Ingress controller to be ready..."
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# Create k8s directory if it doesn't exist
mkdir -p k8s

# Apply Kubernetes manifests in order
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/pdb.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=120s deployment/word-train-app

# Apply HPA after deployment is ready
echo "Applying Horizontal Pod Autoscaler..."
kubectl apply -f k8s/hpa.yaml

echo "Word Train application deployed successfully with high availability and scalability!"
echo "Access the application at http://localhost:8080"
echo ""
echo "Cluster information:"
kubectl get nodes
echo ""
echo "Pod status:"
kubectl get pods
echo ""
echo "Services:"
kubectl get services
echo ""
echo "HPA status:"
