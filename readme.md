# flask-eks-project

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-326CE5?logo=kubernetes)
![AWS](https://img.shields.io/badge/AWS-ECR%20%7C%20EKS-FF9900?logo=amazonaws)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/Status-Active-success)

> A containerized Python Flask application deployed to AWS EKS using Kubernetes —
> provisioned with eksctl, stored in Amazon ECR, and exposed via an AWS Load Balancer.







<img width="1104" height="330" alt="2026-05-14" src="https://github.com/user-attachments/assets/a2e417a8-99a1-4b56-b945-6b4869a53adf" />

---

## Overview
This project deploys a containerized Flask application to a managed Kubernetes
cluster on AWS EKS. The Docker image is stored privately in Amazon ECR and pulled
by EKS worker nodes at runtime — demonstrating a complete production grade
container orchestration workflow on AWS.

## Skills Demonstrated
1. Container Orchestration — deploying and managing containers using Kubernetes on AWS EKS
2. Private Image Registry — building and pushing Docker images to Amazon ECR
3. Infrastructure Provisioning — creating a managed EKS cluster using eksctl
4. Security-Based Design — private ECR registry, IAM authentication, and
   least privilege node permissions

## Main Objective
Provision a managed Kubernetes cluster on AWS EKS, push a containerized Flask
application to Amazon ECR, and deploy it using Kubernetes manifests — exposed
publicly via an AWS Elastic Load Balancer with zero manual console configuration.

---

## Architecture
GitHub Repo → Docker Build → Amazon ECR → AWS EKS Cluster → Live App
│
┌──────────┴──────────┐
▼                      ▼
Worker Node 1         Worker Node 2
(t3.small)            (t3.small)
│                      │
└──────────┬───────────┘
▼
AWS Elastic Load Balancer
│
▼
Public URL 🌐

### File Summary

| File | Purpose |
|---|---|
| `app/app.py` | Flask web application with `/` and `/health` endpoints |
| `app/requirements.txt` | Pinned Python dependencies |
| `Dockerfile` | Container build instructions using `python:3.12-slim` |
| `.dockerignore` | Excludes unnecessary files from Docker image |
| `k8s/deployment.yaml` | Kubernetes deployment — 2 replicas of Flask container |
| `k8s/service.yaml` | Kubernetes LoadBalancer service — exposes app on port 80 |

---

## Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| [Python](https://python.org) | >= 3.12 | Run app locally |
| [Docker Desktop](https://docker.com/products/docker-desktop) | Latest | Build and run containers |
| [AWS CLI](https://aws.amazon.com/cli/) | >= 2.0 | AWS authentication |
| [eksctl](https://eksctl.io) | Latest | Provision EKS cluster |
| [kubectl](https://kubernetes.io/docs/tasks/tools/) | Latest | Control Kubernetes cluster |
| [Git](https://git-scm.com) | Any | Clone this repository |

**AWS Requirements:**
- AWS account with IAM user configured
- IAM user with ECR, EKS, EC2, VPC, and IAM permissions
- AWS CLI configured via `aws configure`

> ⚠️ **Cost Warning:** EKS clusters cost ~$0.10/hr for the control plane plus
> ~$0.02/hr per node. Always run `eksctl delete cluster` when finished.
> Budget $2-5 total if built and deleted same day.

---

## Usage

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/PowershellWarrior/flask-eks-project.git
   cd flask-eks-project
```

2. Configure AWS CLI:
```bash
   aws configure
```

3. Test locally with Docker:
```bash
   docker build -t flask-eks-app .
   docker run -p 5000:5000 flask-eks-app
   # Visit http://localhost:5000
```

### Running on AWS EKS

**Phase 1 — Push image to Amazon ECR:**
```bash
# Create ECR repository
aws ecr create-repository --repository-name flask-eks-app --region us-east-1

# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS \
  --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push image
docker tag flask-eks-app:latest <ecr-repo-uri>:latest
docker push <ecr-repo-uri>:latest
```

**Phase 2 — Provision EKS cluster:**
```bash
eksctl create cluster \
  --name flask-eks-cluster \
  --region us-east-1 \
  --nodegroup-name workers \
  --node-type t3.small \
  --nodes 2 \
  --managed
```

**Phase 3 — Deploy to Kubernetes:**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Get your public URL
kubectl get svc flask-service
```

**Visit in your browser:**
http://EXTERNAL-IP        ← Hello World endpoint
http://EXTERNAL-IP/health ← Health check endpoint

**Destroy cluster when finished:**
```bash
eksctl delete cluster --name flask-eks-cluster --region us-east-1
```

---

## Security Design Decisions

- **Amazon ECR over Docker Hub** — Private registry secured by IAM —
  only authorized AWS accounts can pull the image

- **Managed node groups** — AWS automatically handles node updates,
  patches, and replacements — reducing operational overhead

- **IAM least privilege** — Dedicated IAM user with only the permissions
  required for ECR, EKS, EC2, and VPC — no root account credentials used

- **2 replicas for availability** — If one pod crashes Kubernetes
  automatically restarts it while the second continues serving traffic

- **Private image at runtime** — EKS worker nodes pull directly from
  ECR within the AWS network — no public internet image transfer

- **`python:3.12-slim` base image** — Minimal attack surface and
  reduced image size compared to the full Python image

