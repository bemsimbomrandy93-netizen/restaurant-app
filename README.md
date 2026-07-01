# 🍽️ Restaurant App — DevOps Project

## Overview
A containerized restaurant ordering app deployed on AWS EC2 using Docker Compose, provisioned with Terraform, and automated with GitHub Actions CI/CD.

## Architecture
- **Frontend:** Nginx (HTML, CSS)
- **Backend:** Python (Flask) — API server on Port 5000
- **Database:** MySQL 8.0 — Port 3306
- **Infrastructure:** AWS EC2 (t3.micro · Amazon Linux 2) provisioned via Terraform
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions — lints Python, builds and pushes Docker image to Docker Hub
- **Reverse Proxy:** Nginx — Port 80/443

## Architecture Diagram
![Architecture Diagram](architecture.png)

## Infrastructure (Terraform)
Terraform is used to provision the AWS infrastructure:
- EC2 instance (t3.micro · Amazon Linux 2)
- VPC with public subnet
- Internet Gateway
- Security Groups (ports 22, 80, 443)

cd terraform
terraform init
terraform plan
terraform apply

## Configuration Management (Ansible)
Ansible is used to configure the EC2 instance and deploy the app:

cd ansible
ansible-playbook -i <EC2-IP>, playbook.yml --private-key grace-batch.pem -u ec2-user

## CI/CD Pipeline (GitHub Actions)
On every push to main:
1. Lints the Python Flask backend with flake8
2. Builds the Docker image
3. Pushes the image to Docker Hub

## How to Run
git clone https://github.com/bemsimbomrandy93-netizen/restaurant-app.git
cd restaurant-app
docker compose up --build -d

## Author
Bemsimbom Randy — DevOps Engineer
