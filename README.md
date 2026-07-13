# 📚 Bazar - GitOps CI/CD Pipeline with Kubernetes

![Jenkins](jenkins.png)

![Argo CD](argocd.png)

## Overview

Bazar is a Flask-based microservices bookstore application deployed on Kubernetes using Helm and managed through a complete GitOps workflow.

The application consists of three microservices:

- **Frontend** - User-facing API
- **Catalog** - Book catalog service
- **Order** - Order management service

This project demonstrates an end-to-end DevOps pipeline using Docker, Jenkins, Helm, Kubernetes, and Argo CD.

---

# Architecture

```
Developer
    │
    ▼
Push Code to GitHub
    │
    ▼
Jenkins Pipeline
│
├── Checkout Repository
├── Build Docker Images
├── Push Images to Docker Hub
├── Update Helm values.yaml
└── Commit & Push Updated Image Tag
    │
    ▼
GitHub Repository
    │
    ▼
Argo CD (GitOps)
    │
    ▼
Helm Deployment
    │
    ▼
Kubernetes Cluster
    │
 ┌──┴───────────────┐
 │                  │
HPA            VPA Recommendations
```

---

# Tech Stack

- Python Flask
- Docker
- Docker Compose
- Kubernetes (Kind)
- Helm
- Jenkins
- GitHub
- Docker Hub
- Argo CD
- GitOps
- Metrics Server
- Horizontal Pod Autoscaler (HPA)
- Vertical Pod Autoscaler (VPA)

---

# Project Structure

```
Frontend_Server/
Catalog_Server/
Order_Server/

helm/
└── bazar/

Jenkinsfile

docker-compose.yml
```

---

# Local Deployment

```bash
docker compose up --build -d
```

Stop

```bash
docker compose down
```

---

# Kubernetes Deployment

```bash
helm upgrade --install bazar ./helm/bazar \
--namespace bazar \
--create-namespace
```

Verify

```bash
kubectl get all -n bazar
```

---

# Jenkins CI Pipeline

The Jenkins pipeline performs:

- Checkout source code
- Build Docker images
- Push images to Docker Hub
- Tag images using `${BUILD_NUMBER}`
- Update `helm/bazar/values.yaml`
- Commit updated image tags
- Push changes back to GitHub

Images are versioned like:

```
frontend-service:1
frontend-service:2
frontend-service:3
...
```

instead of using `latest`.

---

# GitOps Workflow

This project follows GitOps principles.

```
Developer
        ↓
GitHub
        ↓
Jenkins
        ↓
Docker Hub
        ↓
Update Helm values.yaml
        ↓
Push to GitHub
        ↓
Argo CD detects change
        ↓
Automatic Kubernetes Deployment
```

Git remains the **single source of truth**.

---

# Argo CD

Argo CD continuously monitors the Git repository.

Whenever Jenkins updates the Helm chart with a new image tag, Argo CD automatically synchronizes the Kubernetes cluster.

Current Application Status

- Healthy ✅
- Synced ✅
- Automatic Sync Enabled

---

# Horizontal Pod Autoscaler

HPA is configured for all three services.

Configuration

- Min Replicas: 1
- Max Replicas: 5
- Target CPU: 60%

Generate Load

```bash
kubectl run fortio \
--rm -it \
--restart=Never \
--image=fortio/fortio \
-- load \
-qps 0 \
-c 300 \
-t 5m \
http://frontend/info/1
```

Monitor

```bash
kubectl get hpa -n bazar -w

kubectl get pods -n bazar -w

kubectl top pods -n bazar
```

---

# Vertical Pod Autoscaler

VPA is configured in **Recommendation Mode**.

```
updateMode: Off
```

It recommends CPU and Memory requests without restarting Pods.

View recommendations

```bash
kubectl describe vpa frontend-vpa -n bazar

kubectl describe vpa catalog-vpa -n bazar

kubectl describe vpa order-vpa -n bazar
```

---

# Metrics Server

Metrics Server provides resource metrics required by HPA.

Verify

```bash
kubectl top nodes

kubectl top pods -n bazar
```

---

# API Endpoints

```
GET     /info/<id>

GET     /search/<topic>

PUT     /purchase/<id>

PUT     /edit/<id>

DELETE  /invalidate-item/<id>

DELETE  /invalidate-topic/<topic>

GET     /show-all-caches
```

---

# My Contributions

This project was originally a Flask microservices application.

I extended it into a complete DevOps and GitOps project by implementing:

- Docker containerization
- Kubernetes deployment
- Helm charts
- Custom Jenkins Docker image
- Jenkins CI pipeline
- Docker Hub integration
- Dynamic image tagging using BUILD_NUMBER
- Automatic Helm value updates
- GitHub integration
- GitOps using Argo CD
- Automatic deployment synchronization
- Metrics Server installation
- Horizontal Pod Autoscaler
- Vertical Pod Autoscaler
- Resource requests & limits
- Rolling updates
- ImagePullPolicy Always configuration
- Docker Compose
- Basic Kubernetes Support

---

# Original Project Features

- Flask Microservices
- SQLite Database


---

# Enhancements Added

- Jenkins CI
- Docker Hub
- Helm
- GitOps
- Argo CD
- Kubernetes
- HPA
- VPA
- Metrics Server
- Dynamic Image Versioning
- Automatic Deployments
- Custom Jenkins Image

---

# Future Improvements

- Deploy to Amazon EKS
- Use AWS ECR instead of Docker Hub
- Prometheus & Grafana Monitoring
- Ingress Controller
- cert-manager TLS
- SonarQube Integration
- Trivy Security Scans
- Snyk Security Scans
- Multi-Environment GitOps

---

# Notes

- Jenkins automatically updates the Helm image tags.
- Argo CD continuously watches GitHub for changes.
- Git acts as the single source of truth.
- HPA automatically scales Pods based on CPU utilization.
- VPA provides CPU and Memory recommendations.
- Kubernetes performs rolling updates with zero downtime.
