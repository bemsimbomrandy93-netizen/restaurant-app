# 🍽️ Restaurant App — DevOps Project

## Overview
A containerized 3-tier restaurant ordering application built with Python Flask, MySQL 8.0, and Nginx. The infrastructure is provisioned on AWS EC2 using Terraform, the server is configured using Ansible, the application is containerized and run using Docker Compose, and every code change is automatically tested and pushed to Docker Hub using a GitHub Actions CI/CD pipeline.

## Screenshot
![App Screenshot](screenshot.png)

## Architecture Diagram
![Architecture Diagram](architecture.png)

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Nginx (HTML, CSS) |
| Backend | Python Flask — Port 5000 |
| Database | MySQL 8.0 — Port 3306 |
| Reverse Proxy | Nginx — Port 80/443 |
| Containerization | Docker & Docker Compose |
| Infrastructure | AWS EC2 (t3.micro · Amazon Linux 2) |
| Provisioning | Terraform |
| Configuration | Ansible |
| CI/CD | GitHub Actions → Docker Hub |

---

## Step-by-Step Deployment Guide

Follow these steps in order to deploy the application from scratch.

---

### Step 1 — Clone the Repository
The first thing you need to do is pull all the project files from GitHub onto your local machine. This gives you the source code, Terraform files, Ansible playbook, and Docker configuration all in one place.

```bash
git clone https://github.com/bemsimbomrandy93-netizen/restaurant-app.git
cd restaurant-app
```

Once inside the project folder you will see the following:
- backend/ — Python Flask API
- frontend/ — Nginx HTML/CSS frontend
- db/ — MySQL initialization SQL
- terraform/ — AWS infrastructure code
- ansible/ — Server configuration playbook
- .github/workflows/ — GitHub Actions CI/CD pipeline
- docker-compose.yml — Runs all containers together

---

### Step 2 — Provision AWS Infrastructure with Terraform
Before the app can run, you need a server on AWS. Terraform handles this automatically by creating the EC2 instance, VPC, subnet, internet gateway, and security groups with code — no manual clicking in the AWS console.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

- terraform init downloads the AWS provider plugin needed to communicate with AWS
- terraform plan shows a preview of everything that will be created before anything happens
- terraform apply creates all the AWS resources. Type yes when prompted to confirm

After it finishes, Terraform will display the public IP of your EC2 instance. Copy this IP address — you will need it in every step that follows.

---

### Step 3 — SSH Into the EC2 Instance
Now that the EC2 instance is running, connect to it remotely using SSH. SSH gives you a terminal inside the server so you can run commands on it.

```bash
ssh -i grace-batch.pem ec2-user@YOUR-EC2-IP
```

- -i grace-batch.pem tells SSH to use your private key for authentication
- ec2-user is the default username for Amazon Linux 2
- YOUR-EC2-IP is the public IP address output by Terraform

Once connected you will see a terminal prompt like this:
[ec2-user@ip-172-31-xx-xx ~]$
This means you are now inside the EC2 server.

---

### Step 4 — Configure the Server with Ansible
The EC2 instance is a fresh server with nothing installed yet. Ansible automatically configures it by installing Docker, Docker Compose, and copying the project files — without you having to run each command manually.

Go back to your local machine and run:

```bash
cd ansible
ansible-playbook -i YOUR-EC2-IP, playbook.yml --private-key grace-batch.pem -u ec2-user
```

Ansible will connect to the EC2 instance and automatically:
1. Update all server packages
2. Install Docker
3. Install Docker Compose
4. Start the Docker service
5. Copy all project files to the server
6. Run docker-compose up -d to start all containers

---

### Step 5 — Verify the Application is Running
After Ansible finishes, SSH back into the EC2 instance and confirm all containers are running:

```bash
ssh -i grace-batch.pem ec2-user@YOUR-EC2-IP
docker compose ps
```

You should see three containers running:
- restaurant-app-frontend-1 running on port 80
- restaurant-app-backend-1 running on port 5000
- restaurant-app-db-1 running on port 3306

---

### Step 6 — Access the Application
Open your browser and visit:

http://YOUR-EC2-IP

The restaurant ordering app is now live and accessible to anyone on the internet. Users can visit the IP address to place food orders which are saved to the MySQL database through the Flask backend.

---

### Step 7 — CI/CD Pipeline (GitHub Actions)
The project includes an automated CI/CD pipeline using GitHub Actions. Every time a developer pushes new code to the main branch, the pipeline runs automatically — no manual deployment needed.

Here is exactly what happens when code is pushed:

| Step | Action | Description |
|------|--------|-------------|
| 1 | Code pushed to GitHub | Developer runs git push origin main |
| 2 | GitHub Actions triggers | The workflow in .github/workflows/ci.yml starts automatically |
| 3 | Python code is linted | flake8 checks the Flask backend for code quality errors |
| 4 | Docker image is built | The backend is packaged into a Docker container |
| 5 | Image pushed to Docker Hub | The image is stored at justrandy1030/restaurant-app:latest |

Required GitHub Secrets — add these under Settings → Secrets and variables → Actions:

| Secret Name | Value |
|-------------|-------|
| DOCKER_USERNAME | Your Docker Hub username |
| DOCKER_PASSWORD | Your Docker Hub access token |

To generate a Docker Hub access token:
1. Go to hub.docker.com
2. Click your profile → Account Settings → Security
3. Click Generate New Token
4. Copy the token and paste it as DOCKER_PASSWORD in GitHub Secrets

---

## Author
Bemsimbom Randy — DevOps Engineer
GitHub: https://github.com/bemsimbomrandy93-netizen
Docker Hub: https://hub.docker.com/u/justrandy1030
