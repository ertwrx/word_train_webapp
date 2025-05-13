High Availability and Scalability K8s Setup for Word Train Webapp
I've completely redesigned the Kubernetes configuration to provide high availability and scalability for your Flask application. Here's what's new:
Split Manifests and Improved Organization
Instead of one large YAML file, I've split the manifests into separate files under a k8s/ directory:

deployment.yaml - Enhanced app deployment
service.yaml - Service configuration
configmap.yaml - Non-sensitive configuration
secret.yaml - Sensitive data
ingress.yaml - External access with session affinity
hpa.yaml - Horizontal Pod Autoscaler
pdb.yaml - Pod Disruption Budget
metrics-server.yaml - Required for HPA functionality

High Availability Features

Multiple Replicas: Starting with 3 replicas for redundancy
Pod Anti-Affinity: Ensures pods are distributed across different nodes
Multi-Node Cluster: Created with 1 control plane + 2 worker nodes
Pod Disruption Budget: Ensures at least 2 pods are always available
Zero-Downtime Updates: RollingUpdate strategy with maxUnavailable: 0
Enhanced Health Checks: Added startup probe and improved liveness/readiness
Session Affinity: Added sticky sessions in the ingress for better user experience

Scalability Features

Horizontal Pod Autoscaler: Automatically scales from 3 to 10 replicas based on:

CPU usage (70%)
Memory usage (80%)


Customized Scaling Behavior: Fast scale-up (30 second window) and gradual scale-down (5 minutes)
Metrics Server: Integrated for resource monitoring
Resource Limits and Requests: Properly defined for scheduling and quality of service
