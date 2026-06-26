# 🍽️ Restaurant App — DevOps Project

## Overview
A containerized restaurant ordering app deployed on AWS EC2 using Docker Compose.

## Architecture
- **Frontend:** Nginx (HTML, CSS)
- **Backend:** Python (Flask)
- **Database:** MySQL 5.7
- **Infrastructure:** AWS EC2 (Amazon Linux 2023)
- **Containerization:** Docker & Docker Compose

## Project Structure
restaurant-app/
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── styles.css
│   └── nginx.conf
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── db/
│   └── init.sql
└── docker-compose.yml

## How to Run
# Clone the repo
git clone https://github.com/Bemsimbom Randy/restaurant-app.git
cd restaurant-app

# Start all containers
docker compose up --build -d

## Author
Bemsimbom Randy — DevOps Engineer
