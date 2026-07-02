# 🍽️ African Restaurant Web App — 3-Tier Docker Architecture

A containerised full-stack application demonstrating a real-world 3-tier architecture using:

- Frontend → Nginx (UI layer)
- Backend → Flask API (Business logic)
- Database → MySQL 8.0 (Data layer)
- AWS S3 → Static assets (food images)
- Infrastructure → AWS EC2 provisioned with Terraform
- Configuration → Ansible
- CI/CD → GitHub Actions → Docker Hub

## Screenshot
![App Screenshot](screenshot.png)

## Architecture Diagram
![Architecture Diagram](architecture.png)

## High-Level Architecture
            🌐 USER BROWSER
                   |
                   v
    +-----------------------------+
    | FRONTEND CONTAINER (NGINX) |
    | HTML + CSS + JS            |
    +-----------------------------+
                   |
          HTTP (API CALL)
                   |
                   v
    +-----------------------------+
    | BACKEND CONTAINER (FLASK)  |
    | Business Logic API         |
    +-----------------------------+
                   |
          SQL CONNECTION
                   |
                   v
    +-----------------------------+
    | DATABASE (MYSQL CONTAINER) |
    | Persistent Orders Data     |
    +-----------------------------+
Images:
AWS S3 BUCKET (STATIC STORAGE)
https://nosoma.s3.us-east-2.amazonaws.com/

## Project Structure

````text
restaurant-app/
|
|-- docker-compose.yml
|
|-- frontend/
|   |-- Dockerfile
|   |-- nginx.conf
|   |-- index.html
|   |-- styles.css
|
|-- backend/
|   |-- Dockerfile
|   |-- app.py
|   |-- requirements.txt
|
|-- db/
|   |-- init.sql
|
|-- terraform/
|   |-- main.tf
|   |-- variables.tf
|   |-- outputs.tf
|
|-- ansible/
|   |-- playbook.yml
|
|-- .github/
    |-- workflows/
        |-- ci.yml
```
restaurant-app/
│
├── docker-compose.yml
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── index.html
│   └── styles.css
│
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── db/
│   └── init.sql
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── ansible/
│   └── playbook.yml
│
└── .github/
└── workflows/
└── ci.yml

---

## Step-by-Step Deployment Guide

Follow these steps in order to deploy the application from scratch.

---

### Step 1 — Launch EC2 Instance on AWS

1. Go to AWS Console → EC2 → Launch Instance
2. Choose Amazon Linux 2
3. Select instance type: t3.micro
4. Configure Security Group to open the following ports:

| Port | Protocol | Purpose |
|------|----------|---------|
| 22 | SSH | Remote terminal access |
| 80 | HTTP | Web traffic (Frontend) |
| 443 | HTTPS | Secure web traffic |
| 5000 | TCP | Backend API (optional for testing) |

5. Download your key pair (.pem file) and save it safely

---

### Step 2 — Provision Infrastructure with Terraform

Instead of manually clicking through the AWS console, Terraform creates all the infrastructure automatically with code — EC2 instance, VPC, subnet, internet gateway, and security groups.

```bash
cd terraform
terraform init
```
terraform init downloads the AWS provider plugin needed to communicate with AWS.

```bash
terraform plan
```
terraform plan shows a preview of everything Terraform will create before anything actually happens.

```bash
terraform apply
```
terraform apply creates all the AWS resources. Type yes when prompted to confirm.

After it finishes, Terraform outputs the public IP of your EC2 instance:
Outputs:
ec2_public_ip = "YOUR-EC2-IP"
Copy this IP address — you will need it in every step that follows.

---

### Step 3 — SSH Into the EC2 Instance

SSH (Secure Shell) gives you a remote terminal inside the EC2 server so you can run commands on it.

```bash
ssh -i grace-batch.pem ec2-user@YOUR-EC2-IP
```

- -i grace-batch.pem tells SSH to use your private key for authentication
- ec2-user is the default username for Amazon Linux 2
- YOUR-EC2-IP is the public IP address output by Terraform

Once connected you will see:
[ec2-user@ip-172-31-xx-xx ~]$
This means you are now inside the EC2 server.

---

### Step 4 — Install Docker on the EC2 Instance

The EC2 instance is a fresh server. You need to install Docker so it can run containers.

```bash
sudo dnf update -y
```
Updates all server packages to the latest versions.

```bash
sudo dnf install -y docker
```
Installs Docker on the server.

```bash
sudo systemctl start docker
```
Starts the Docker service.

```bash
sudo systemctl enable docker
```
Makes Docker start automatically whenever the server reboots.

```bash
sudo systemctl status docker
```
Confirms Docker is running. You should see active (running).

```bash
sudo usermod -aG docker ec2-user
```
Adds ec2-user to the Docker group so you can run Docker commands without sudo.

```bash
sudo reboot
```
Reboots the server to apply the group changes. Wait 30 seconds then SSH back in.

---

### Step 5 — Install Docker Compose

After rebooting, SSH back in and install Docker Compose:

```bash
ssh -i grace-batch.pem ec2-user@YOUR-EC2-IP
```

Check your system architecture:
```bash
uname -m
```

If you see x86_64, run:

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

Verify Docker Compose is installed:
```bash
docker compose version
```

---

### Step 6 — Configure the Server with Ansible

Instead of manually running setup commands on the server, Ansible does it all automatically. It connects to your EC2 instance and installs everything needed to run the app.

From your local machine, run:

```bash
cd ansible
ansible-playbook -i YOUR-EC2-IP, playbook.yml --private-key grace-batch.pem -u ec2-user
```

Ansible will automatically:
1. Update all server packages
2. Install Docker and Docker Compose
3. Start the Docker service
4. Copy all project files to the server
5. Run docker-compose up -d to start all containers

---

### Step 7 — Clone the Repository on EC2

Pull all the project files from GitHub onto the EC2 server:

```bash
git clone https://github.com/bemsimbomrandy93-netizen/restaurant-app.git
cd restaurant-app
```

This gives you the source code, Docker configuration, Terraform files, and Ansible playbook all in one place.

---

### Step 8 — AWS S3 Setup (Static Food Images)

The food images are stored on AWS S3 instead of inside the Docker container. This is a real-world best practice — static assets should be served from object storage, not bundled with application code.

1. Go to AWS Console → S3 → Create Bucket
2. Name it: nosoma
3. Region: us-east-2
4. Uncheck Block Public Access under bucket permissions
5. Add the following bucket policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::nosoma/*"
        }
    ]
}
```

6. Upload the following images to the bucket:
   - eru.jpg
   - egusi.jpg
   - bunny chow.jpg

The images are served from these URLs:
https://nosoma.s3.us-east-2.amazonaws.com/eru.jpg
https://nosoma.s3.us-east-2.amazonaws.com/egusi.jpg
https://nosoma.s3.us-east-2.amazonaws.com/bunny+chow.jpg

---

### Step 9 — Application File Contents

Here are all the files that make up the application:

#### docker-compose.yml
The brain of the application. It defines and connects all three containers together.

services:

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      DB_HOST: db
      DB_USER: root
      DB_PASSWORD: restaurant
      DB_NAME: orders
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: restaurant
      MYSQL_DATABASE: orders
    volumes:
      - db_data:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  db_data:

#### frontend/Dockerfile
Builds the Nginx container that serves the UI.

FROM nginx:latest

COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

#### frontend/nginx.conf
Configures Nginx to serve static files and forward API calls to the Flask backend.

server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    location /order {
        proxy_pass http://backend:5000/order;
        proxy_set_header Content-Type application/json;
    }
}

#### backend/Dockerfile
Builds the Python Flask container.

FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]

#### backend/requirements.txt
Python dependencies for the Flask backend.

flask
mysql-connector-python

#### backend/app.py
The Flask API that receives orders and saves them to MySQL.

from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)


@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    food = data['food']
    db = mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO orders (food) VALUES (%s)",
        (food,)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({
        "message": f"Order received for {food}"
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

#### db/init.sql
Creates the orders table when the MySQL container starts for the first time.

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food VARCHAR(255)
);

---

### Step 10 — Run the Application

Inside the EC2 instance, navigate to the project folder and start all containers:

```bash
cd restaurant-app
docker compose up --build -d
```

- --build rebuilds the Docker images from the Dockerfiles
- -d runs the containers in the background (detached mode)

Verify all containers are running:
```bash
docker compose ps
```

You should see three containers running:
- restaurant-app-frontend-1 running on port 80
- restaurant-app-backend-1 running on port 5000
- restaurant-app-db-1 running on port 3306

---

### Step 11 — Access the Application

Open your browser and navigate to:

http://YOUR-EC2-IP

You should see the African Restaurant UI. Select a food item, place an order, and see the confirmation message.

---

### Step 12 — Verify the Database

To confirm that orders are being saved to the MySQL database, access the MySQL container and run a query:

```bash
docker exec -it restaurant-app-db-1 mysql -uroot -prestaurant
```

- docker exec runs a command inside a running container
- -it opens an interactive terminal so you can type SQL commands
- restaurant-app-db-1 is the name of the MySQL container
- -uroot logs into MySQL as the root user
- -prestaurant means the password is restaurant (no space between -p and the password)

Then inside the MySQL shell:

```sql
USE orders;
SELECT * FROM orders;
```

You will see all the orders that have been placed through the app.

---

### Step 13 — CI/CD Pipeline (GitHub Actions)

The project includes an automated CI/CD pipeline. Every time a developer pushes new code to the main branch, GitHub Actions runs automatically — no manual deployment needed.

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
| DOCKER_USERNAME | justrandy1030 |
| DOCKER_PASSWORD | Your Docker Hub access token (dckr_pat_...) |

---

## Summary

This system separates responsibilities into three layers: the frontend handles user interaction using Nginx, the backend processes requests using Flask, and the database stores persistent data using MySQL 8.0. Docker Compose connects all three containers into a single distributed application, while AWS S3 handles static assets like food images. Infrastructure is provisioned automatically using Terraform, the server is configured using Ansible, and every code change is automatically tested and deployed using GitHub Actions CI/CD. This mirrors real-world cloud-native architecture used in production systems today.

---

## Author
Bemsimbom Randy — DevOps Engineer
GitHub: https://github.com/bemsimbomrandy93-netizen
Docker Hub: https://hub.docker.com/u/justrandy1030
