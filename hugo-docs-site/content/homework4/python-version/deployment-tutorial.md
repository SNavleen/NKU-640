---
marp: true
theme: default
paginate: true
header: 'Docker Deployment Tutorial'
footer: 'NKU 640 | Homework 4 | Python FastAPI Deployment'
---

<!-- _class: lead -->

# Docker Deployment Tutorial

**Deploying Python FastAPI REST API with Docker**

A Step-by-Step Guide with Commands and Screenshots

---

## Table of Contents

1. **Prerequisites & Setup**
2. **Local Development**
3. **Docker Configuration**
4. **Production Deployment**
5. **Testing & Verification**
6. **Troubleshooting**

---

<!-- _class: lead -->

# 1. Prerequisites & Setup

What You Need to Get Started

---

## System Requirements

**Development Environment:**
- Python 3.11 or higher
- Docker Desktop (or Docker Engine)
- Docker Compose
- Git
- Terminal/Command Prompt

**Production Server (Optional):**
- Ubuntu 20.04/22.04 LTS or similar Linux
- 2GB RAM minimum
- 10GB disk space
- Root or sudo access

---

## Required Software

**Core Dependencies:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Check Docker installation
docker --version
docker-compose --version

# Check Git
git --version
```

**Package Managers:**
```bash
# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use pip
pip install uv
```

---

## Project Setup

**1. Clone Repository:**
```bash
cd ~/Documents/NKU/640
git clone <repository-url> NKU-640
cd NKU-640/homework4/python-version
```

**2. Verify Project Structure:**
```bash
ls -la
# Should see: app/ tests/ docker/ pyproject.toml docker-compose.yml
```

**3. Copy Environment File:**
```bash
cp .env.example .env
# Edit .env with your settings
```

---

<!-- _class: lead -->

# 2. Local Development

Running the API Locally

---

## Option 1: uv (Recommended)

**Install Dependencies:**
```bash
# Fast dependency management
uv sync
```

**Run Development Server:**
```bash
# Hot reload enabled
uv run uvicorn app.main:app --reload
```

**Access the API:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

---

## Option 2: Docker Development

**Build and Run:**
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f app
```

**Verify Services:**
```bash
# Check running containers
docker-compose ps

# Should show: todo_api, todo_nginx
```

---

## Local Testing

**Health Check:**
```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status": "healthy", ...}
```

**API Documentation:**
- Open http://localhost:8000/docs
- Try the interactive endpoints
- Verify Swagger UI loads

**Database:**
```bash
# Check SQLite database
ls -la data/todo.db
# Should exist and have recent modification time
```

---

<!-- _class: lead -->

# 3. Docker Configuration

Understanding the Container Setup

---

## Docker Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   NGINX         │    │   FastAPI        │
│   (Port 80)     │◄──►│   (Port 8000)    │
│                 │    │                 │
│ • Reverse Proxy │    │ • REST API      │
│ • Rate Limiting │    │ • SQLite DB     │
│ • SSL Ready     │    │ • Health Checks │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┘
              Volume Mount
              (./data/todo.db)
```

---

## Dockerfile Analysis

**Python Application Container:**
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN uv sync --no-install-project

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Docker Compose Configuration

**docker-compose.yml:**
```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: todo_api
    environment:
      DATABASE_URL: sqlite:///./data/todo.db
      JWT_SECRET: ${JWT_SECRET:-change-this-secret}
      DEBUG_MODE: ${DEBUG_MODE:-true}
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: todo_nginx
    ports:
      - "80:80"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      app:
        condition: service_healthy
```

---

## Nginx Configuration

**docker/nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_status 429;

    upstream fastapi {
        server app:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://fastapi;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Health check (no rate limiting)
        location /api/v1/health {
            proxy_pass http://fastapi;
        }

        # Static files (if any)
        location /static/ {
            alias /app/static/;
        }
    }
}
```

---

## Environment Variables

**.env file:**
```bash
# Application
APP_NAME="TODO REST API"
APP_VERSION="1.0.0"
DEBUG_MODE=true
LOG_LEVEL=debug

# Database
DATABASE_URL=sqlite:///./data/todo.db

# JWT Security
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY=3600

# Password Security
BCRYPT_ROUNDS=12

# API Settings
API_V1_PREFIX=/api/v1
```

---

<!-- _class: lead -->

# 4. Production Deployment

Deploying to Production Server

---

## Server Preparation

**1. Update System:**
```bash
sudo apt update && sudo apt upgrade -y
```

**2. Install Docker:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

**3. Install Git:**
```bash
sudo apt install git -y
```

---

## Application Deployment

**1. Clone Repository:**
```bash
cd /opt
sudo git clone <repository-url> todo-api
sudo chown -R $USER:$USER todo-api
cd todo-api/homework4/python-version
```

**2. Configure Environment:**
```bash
# Copy and edit environment file
cp .env.example .env

# Generate secure JWT secret
openssl rand -base64 32

# Edit .env with production values
nano .env
```

**3. Deploy Application:**
```bash
# Build and start services
docker-compose up -d --build

# Wait for health checks
sleep 30

# Verify deployment
docker-compose ps
```

---

## SSL Configuration (Optional)

**Using Let's Encrypt:**
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Update nginx configuration for SSL
sudo nano docker/nginx.conf
```

**nginx.conf with SSL:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... rest of configuration
}
```

---

## Domain Configuration

**DNS Setup:**
1. Point domain to server IP
2. Wait for DNS propagation (can take 24-48 hours)
3. Test domain resolution: `nslookup yourdomain.com`

**Firewall Configuration:**
```bash
# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

<!-- _class: lead -->

# 5. Testing & Verification

Ensuring Everything Works

---

## Health Check Testing

**API Health:**
```bash
# Test health endpoint
curl https://yourdomain.com/api/v1/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2025-12-01T...",
  "service": "TODO REST API",
  "version": "1.0.0",
  "checks": {
    "database": {"status": "healthy"},
    "python": {"status": "healthy"},
    "disk": {"status": "healthy"},
    "memory": {"status": "healthy"}
  }
}
```

---

## End-to-End Testing

**1. User Registration:**
```bash
curl -X POST https://yourdomain.com/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

**2. Save Token:**
```bash
# Extract token from response
TOKEN=$(curl -s -X POST https://yourdomain.com/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","email":"test2@example.com","password":"pass123"}' \
  | jq -r '.token')
```

**3. Test Protected Endpoints:**
```bash
# Get user profile
curl -H "Authorization: Bearer $TOKEN" \
     https://yourdomain.com/api/v1/users/profile

# Create a list
LIST_RESPONSE=$(curl -s -X POST https://yourdomain.com/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"title":"Test List"}')

LIST_ID=$(echo $LIST_RESPONSE | jq -r '.id')

# Create a task
curl -X POST https://yourdomain.com/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","priority":"high"}'
```

---

## Load Testing

**Basic Load Test:**
```bash
# Install hey (load testing tool)
# go install github.com/rakyll/hey@latest

# Test API endpoints
hey -n 100 -c 10 https://yourdomain.com/api/v1/health

# Test with authentication
hey -n 50 -c 5 -H "Authorization: Bearer $TOKEN" \
    https://yourdomain.com/api/v1/users/profile
```

**Rate Limiting Test:**
```bash
# Test rate limiting (should get 429 after limit)
for i in {1..15}; do
  curl -s https://yourdomain.com/api/v1/health
  echo "Request $i completed"
  sleep 0.1
done
```

---

## Monitoring Setup

**View Application Logs:**
```bash
# Application logs
docker-compose logs -f app

# Nginx access logs
docker-compose logs -f nginx

# System resource usage
docker stats
```

**Log Analysis:**
```bash
# Search for errors
docker-compose logs app | grep ERROR

# Check response times
docker-compose logs app | grep "Time:"
```

---

<!-- _class: lead -->

# 6. Troubleshooting

Common Issues and Solutions

---

## Container Issues

**Containers Not Starting:**
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose up -d --build
```

**Health Check Failures:**
```bash
# Check health endpoint manually
curl http://localhost:8000/api/v1/health

# Debug health check
docker-compose exec app curl -f http://localhost:8000/api/v1/health

# Check application logs
docker-compose logs app
```

---

## Database Issues

**Database Connection Failed:**
```bash
# Check database file
ls -la data/todo.db

# Check file permissions
ls -ld data/

# Reset database if corrupted
rm data/todo.db
docker-compose restart app
```

**Migration Issues:**
```bash
# Access container
docker-compose exec app bash

# Check database tables
sqlite3 data/todo.db ".tables"

# Check table schema
sqlite3 data/todo.db ".schema users"
```

---

## Network Issues

**Port Conflicts:**
```bash
# Check what's using ports
sudo lsof -i :80
sudo lsof -i :8000

# Change ports in docker-compose.yml
ports:
  - "8080:80"    # Change from 80 to 8080
  - "8001:8000"  # Change from 8000 to 8001
```

**Firewall Issues:**
```bash
# Check firewall status
sudo ufw status

# Allow required ports
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22  # SSH access
```

---

## SSL/HTTPS Issues

**SSL Certificate Problems:**
```bash
# Check certificate validity
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Renew certificates
sudo certbot renew

# Check nginx configuration
docker-compose exec nginx nginx -t
```

**Mixed Content Issues:**
```bash
# Force HTTPS in nginx
location / {
    if ($scheme != "https") {
        return 301 https://$host$request_uri;
    }
}
```

---

## Performance Issues

**High Memory Usage:**
```bash
# Check container resources
docker stats

# Limit container memory
docker-compose.yml:
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
```

**Slow Response Times:**
```bash
# Check database performance
docker-compose exec app sqlite3 data/todo.db ".timer on" "SELECT COUNT(*) FROM tasks;"

# Add database indexes if needed
docker-compose exec app sqlite3 data/todo.db "CREATE INDEX idx_task_list ON tasks(list_id);"
```

---

## Backup and Recovery

**Database Backup:**
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
mkdir -p $BACKUP_DIR

# Stop containers temporarily
docker-compose stop app

# Copy database file
cp data/todo.db $BACKUP_DIR/todo_$TIMESTAMP.db

# Restart containers
docker-compose start app

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "todo_*.db" -mtime +7 -delete

echo "Backup completed: todo_$TIMESTAMP.db"
EOF

chmod +x backup.sh
```

**Automated Backups:**
```bash
# Add to crontab for daily backups
crontab -e
# Add: 0 2 * * * /opt/todo-api/backup.sh
```

---

## Security Hardening

**Update Docker Images:**
```bash
# Update all images
docker-compose pull

# Rebuild with latest images
docker-compose up -d --build
```

**Secure Environment Variables:**
```bash
# Use Docker secrets or external key management
echo "your-secure-jwt-secret" | docker secret create jwt_secret -

# Or use .env file with restricted permissions
chmod 600 .env
```

**Monitor Security Logs:**
```bash
# Check for suspicious activity
docker-compose logs | grep -i "unauthorized\|forbidden\|error"

# Monitor failed login attempts
docker-compose logs | grep "POST /api/v1/auth/login" | grep "401"
```

---

## Getting Help

**Debug Commands:**
```bash
# Full system information
docker system info

# Container resource usage
docker stats --no-stream

# Network inspection
docker network ls
docker network inspect todo-api_default
```

**Log Locations:**
- Application logs: `docker-compose logs app`
- Nginx logs: `docker-compose logs nginx`
- System logs: `/var/log/syslog`
- Docker logs: `/var/lib/docker/containers/*/logs`

**Community Resources:**
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Docker Documentation: https://docs.docker.com/
- SQLite Documentation: https://www.sqlite.org/docs.html

---

## Emergency Recovery

**Complete Reset:**
```bash
# Stop everything
docker-compose down -v

# Remove all containers and volumes
docker system prune -a --volumes

# Clean up networks
docker network prune

# Restart fresh
docker-compose up -d --build
```

**Data Recovery:**
```bash
# Restore from backup
cp /opt/backups/todo_20251201_020000.db data/todo.db
docker-compose restart app
```

---

*This deployment tutorial provides a comprehensive guide for deploying the Python FastAPI TODO API in both development and production environments. The Docker-based approach ensures consistent deployment across different platforms.*