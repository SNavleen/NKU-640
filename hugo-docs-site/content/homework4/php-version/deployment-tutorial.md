---
marp: true
theme: default
paginate: true
header: 'NGINX Deployment Tutorial'
footer: 'NKU 640 | Homework 4 | Stage 1 - NGINX Deployment'
---

<!-- _class: lead -->

# NGINX Deployment Tutorial

**Deploying PHP REST API with NGINX**

A Step-by-Step Guide with Screenshots

---

## Table of Contents

1. **Prerequisites & Setup**
2. **Server Installation**
3. **Application Deployment**
4. **NGINX Configuration**
5. **Testing & Verification**
6. **Troubleshooting**

---

<!-- _class: lead -->

# 1. Prerequisites & Setup

What You Need to Get Started

---

## System Requirements

**Server Environment:**
- Ubuntu 20.04 / 22.04 LTS (or similar Linux distribution)
- Minimum 1GB RAM
- 10GB disk space
- Root or sudo access

**Required Software:**
- NGINX web server
- PHP 8.1 or higher
- PHP-FPM (FastCGI Process Manager)
- SQLite3
- Composer (PHP package manager)

**Network Requirements:**
- Open port 80 (HTTP)
- Optional: Port 443 (HTTPS with SSL)

---

## Deployment Overview

```
┌─────────────────────────────────────────────┐
│         Internet / Client Requests          │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  NGINX Server  │  (Port 80/443)
         │  Web Server    │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │   PHP-FPM      │  (FastCGI)
         │   PHP Runtime  │
         └────────┬───────┘
                  │
                  ▼
    ┌─────────────────────────────┐
    │   PHP TODO REST API         │
    │   /var/www/php-todo-api     │
    └─────────────┬───────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  SQLite DB     │
         │  todo.db       │
         └────────────────┘
```

---

<!-- _class: lead -->

# 2. Server Installation

Installing Required Software

---

## Step 1: Update System Packages

**Connect to your server via SSH:**

```bash
ssh user@your-server-ip
```

**Update package lists and upgrade existing packages:**

```bash
sudo apt update
sudo apt upgrade -y
```

**Expected output:**
- Package lists are updated
- System packages are upgraded
- May require reboot if kernel is updated

---

## Step 2: Install NGINX

**Install NGINX web server:**

```bash
sudo apt install nginx -y
```

**Verify NGINX installation:**

```bash
nginx -v
```

**Expected output:**
```
nginx version: nginx/1.18.0 (Ubuntu)
```

**Check NGINX status:**

```bash
sudo systemctl status nginx
```

---

## Screenshot: NGINX Status Check

**Terminal output showing NGINX is running:**

![NGINX Status](screenshots/nginx-status.png)

**Key indicators:**
- ✅ `Active: active (running)`
- ✅ Green text indicating healthy status
- ✅ Process ID (PID) displayed
- ✅ Recent log entries visible

---

## Step 3: Install PHP and Extensions

**Install PHP 8.1 and required extensions:**

```bash
sudo apt install -y php8.1 php8.1-fpm php8.1-sqlite3 \
    php8.1-mbstring php8.1-xml php8.1-curl php8.1-zip
```

**Verify PHP installation:**

```bash
php -v
```

**Expected output:**
```
PHP 8.1.33 (cli) (built: Oct 24 2024 14:23:01) (NTS)
Copyright (c) The PHP Group
Zend Engine v4.1.33
```

---

## Step 4: Install Composer

**Download and install Composer:**

```bash
curl -sS https://getcomposer.org/installer | sudo php -- \
    --install-dir=/usr/local/bin --filename=composer
```

**Verify Composer installation:**

```bash
composer --version
```

**Expected output:**
```
Composer version 2.8.3 2024-10-22 15:15:06
```

---

## Screenshot: PHP & Composer Versions

**Terminal output showing installed versions:**

![PHP and Composer Versions](screenshots/php-composer-versions.png)

**Should display:**
- ✅ PHP 8.1.x version
- ✅ Composer 2.x version
- ✅ No errors or warnings

---

<!-- _class: lead -->

# 3. Application Deployment

Deploying the PHP REST API

---

## Step 5: Create Application Directory

**Create directory for the application:**

```bash
sudo mkdir -p /var/www/php-todo-api
cd /var/www/php-todo-api
```

**Set proper ownership:**

```bash
sudo chown -R www-data:www-data /var/www/php-todo-api
```

**Note:** `www-data` is the default NGINX/PHP-FPM user on Ubuntu/Debian

---

## Step 6: Upload Application Files

**Option A: Using Git (recommended):**

```bash
cd /var/www/php-todo-api
sudo -u www-data git clone https://github.com/yourusername/NKU-640.git .
sudo -u www-data git sparse-checkout set homework4/php-version
sudo -u www-data git checkout main
```

**Option B: Using SCP (from local machine):**

```bash
# Run this on your LOCAL machine
scp -r homework4/php-version/* user@server-ip:/tmp/
ssh user@server-ip
sudo mv /tmp/* /var/www/php-todo-api/
sudo chown -R www-data:www-data /var/www/php-todo-api
```

---

## Step 7: Install Dependencies

**Navigate to application directory:**

```bash
cd /var/www/php-todo-api
```

**Install Composer dependencies:**

```bash
sudo -u www-data composer install --no-dev --optimize-autoloader
```

**Flags explained:**
- `--no-dev`: Don't install development dependencies
- `--optimize-autoloader`: Create optimized class map for better performance
- `-u www-data`: Run as web server user

---

## Screenshot: Composer Install

**Terminal showing dependency installation:**

![Composer Install](screenshots/composer-install.png)

**Should show:**
- ✅ Packages being downloaded
- ✅ Dependencies resolved
- ✅ Autoloader generated
- ✅ No errors

---

## Step 8: Configure Environment

**Copy environment template:**

```bash
sudo -u www-data cp .env.example .env
```

**Edit environment variables:**

```bash
sudo nano .env
```

**Update for production:**

```bash
# IMPORTANT: Set to false in production
DEBUG_MODE=false

# Use error level logging in production
LOG_LEVEL=error

# Database path
DATABASE_PATH=/var/www/php-todo-api/data/todo.db

# CRITICAL: Change to a strong random secret
JWT_SECRET=change-this-to-a-strong-random-secret-key-at-least-32-chars
JWT_EXPIRY=3600
```

---

## Step 9: Set Permissions

**Create necessary directories:**

```bash
sudo -u www-data mkdir -p /var/www/php-todo-api/data
sudo -u www-data mkdir -p /var/www/php-todo-api/logs
```

**Set correct permissions:**

```bash
# Application files - read only
sudo find /var/www/php-todo-api -type f -exec chmod 644 {} \;
sudo find /var/www/php-todo-api -type d -exec chmod 755 {} \;

# Data and logs - writable by web server
sudo chmod 775 /var/www/php-todo-api/data
sudo chmod 775 /var/www/php-todo-api/logs

# Environment file - restricted
sudo chmod 600 /var/www/php-todo-api/.env
```

---

<!-- _class: lead -->

# 4. NGINX Configuration

Configuring the Web Server

---

## Step 10: Create NGINX Site Configuration

**Create new site configuration file:**

```bash
sudo nano /etc/nginx/sites-available/php-todo-api
```

**Add the following configuration:**

```nginx
server {
    listen 80;
    server_name _;  # Replace with your domain or IP

    root /var/www/php-todo-api/public;
    index index.php;

    # Logging
    access_log /var/log/nginx/todo-api-access.log;
    error_log /var/log/nginx/todo-api-error.log;

    charset utf-8;
```

---

## NGINX Configuration (continued)

```nginx
    # Route all requests to index.php
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # PHP-FPM configuration
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;

        # Buffer settings
        fastcgi_buffer_size 128k;
        fastcgi_buffers 256 16k;
        fastcgi_busy_buffers_size 256k;
        fastcgi_read_timeout 240;
    }
```

---

## NGINX Configuration (continued)

```nginx
    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Deny access to sensitive directories
    location ~ ^/(vendor|tests|data|logs|\.env) {
        deny all;
        return 404;
    }
}
```

**Save and exit:** `Ctrl+X`, then `Y`, then `Enter`

---

## Step 11: Enable the Site

**Create symbolic link to enable the site:**

```bash
sudo ln -s /etc/nginx/sites-available/php-todo-api \
    /etc/nginx/sites-enabled/php-todo-api
```

**Remove default site (optional):**

```bash
sudo rm /etc/nginx/sites-enabled/default
```

**Test NGINX configuration:**

```bash
sudo nginx -t
```

**Expected output:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

---

## Screenshot: NGINX Configuration Test

**Terminal showing successful configuration test:**

![NGINX Config Test](screenshots/nginx-config-test.png)

**Should show:**
- ✅ `syntax is ok`
- ✅ `test is successful`
- ✅ No error messages

---

## Step 12: Start Services

**Reload NGINX to apply changes:**

```bash
sudo systemctl reload nginx
```

**Ensure PHP-FPM is running:**

```bash
sudo systemctl start php8.1-fpm
sudo systemctl enable php8.1-fpm
```

**Verify both services are active:**

```bash
sudo systemctl status nginx
sudo systemctl status php8.1-fpm
```

---

## Screenshot: Services Running

**Both NGINX and PHP-FPM active:**

![Services Status](screenshots/services-status.png)

**Both should show:**
- ✅ `Active: active (running)` in green
- ✅ Process IDs displayed
- ✅ No error messages in logs

---

<!-- _class: lead -->

# 5. Testing & Verification

Verifying the Deployment Works

---

## Step 13: Test Health Endpoint

**Test from the server itself:**

```bash
curl http://localhost/api/v1/health
```

**Expected response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-11-07T20:00:00+00:00",
  "service": "PHP TODO REST API",
  "version": "v1",
  "checks": {
    "database": {"status": "healthy"},
    "php": {"status": "healthy", "version": "8.1.33"},
    "disk": {"status": "healthy"},
    "memory": {"status": "healthy"}
  }
}
```

---

## Screenshot: Health Check Response

**Terminal showing successful health check:**

![Health Check](screenshots/health-check.png)

**Should display:**
- ✅ Status: healthy
- ✅ Database connection working
- ✅ PHP version displayed
- ✅ All checks passing

---

## Screenshot: Browser Health Check

**Browser displaying the health endpoint:**

![Browser Health Check](screenshots/browser-health-check.png)

**Should show:**
- ✅ JSON response properly formatted
- ✅ All status indicators showing "healthy"
- ✅ No 404 or 500 errors

---

## Step 14: Test API Endpoints

**Test signup endpoint:**

```bash
curl -X POST http://YOUR_SERVER_IP/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Expected response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "...",
    "username": "testuser",
    "email": "test@example.com",
    "createdAt": "2025-11-07T20:00:00Z"
  }
}
```

---

## Screenshot: API Signup Test

**Terminal showing successful user signup:**

![API Signup Test](screenshots/api-signup-test.png)

**Should display:**
- ✅ JWT token returned
- ✅ User object with ID, username, email
- ✅ 201 Created status (if using -i flag)

---

## Step 15: Test Creating a List

**Create a TODO list:**

```bash
curl -X POST http://YOUR_SERVER_IP/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Deployment Checklist",
    "description": "Tasks for NGINX deployment"
  }'
```

**Expected response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Deployment Checklist",
  "description": "Tasks for NGINX deployment",
  "createdAt": "2025-11-07T20:00:00Z",
  "updatedAt": null
}
```

---

## Screenshot: Create List Test

**Terminal showing successful list creation:**

![Create List Test](screenshots/create-list-test.png)

**Should display:**
- ✅ UUID generated for list
- ✅ List name and description returned
- ✅ Timestamps populated

---

## Screenshot: Database Verification

**Terminal showing database contents:**

![Database Verification](screenshots/database-verification.png)

**Should show:**
- ✅ Database file exists
- ✅ Proper permissions (www-data owner)
- ✅ User count matches test data

---

<!-- _class: lead -->

# 6. Troubleshooting

Common Issues and Solutions

---

## Common Issue 1: 502 Bad Gateway

**Symptom:**
- NGINX returns 502 error
- "Connection refused" or "upstream server"

**Causes & Solutions:**

1. **PHP-FPM not running:**
   ```bash
   sudo systemctl status php8.1-fpm
   sudo systemctl start php8.1-fpm
   ```

2. **Wrong socket path in NGINX config:**
   - Check: `/var/run/php/php-fpm.sock` exists
   - Verify NGINX config has correct path

3. **Permission issues:**
   ```bash
   sudo chmod 666 /var/run/php/php-fpm.sock
   ```

---

## Common Issue 2: 404 Not Found

**Symptom:**
- All endpoints return 404
- NGINX serves but PHP not executed

**Causes & Solutions:**

1. **Wrong document root:**
   - Verify NGINX config: `root /var/www/php-todo-api/public;`
   - Check that `public/index.php` exists

2. **Rewrite rules not working:**
   - Ensure `try_files $uri $uri/ /index.php?$query_string;` is present

3. **Restart NGINX:**
   ```bash
   sudo systemctl restart nginx
   ```

---

## Common Issue 3: Database Errors

**Symptom:**
- "Unable to open database file"
- Database connection errors

**Causes & Solutions:**

1. **Directory permissions:**
   ```bash
   sudo chown -R www-data:www-data /var/www/php-todo-api/data
   sudo chmod 775 /var/www/php-todo-api/data
   ```

2. **Wrong database path in .env:**
   - Verify: `DATABASE_PATH=/var/www/php-todo-api/data/todo.db`

3. **Create directory if missing:**
   ```bash
   sudo -u www-data mkdir -p /var/www/php-todo-api/data
   ```

---

## Common Issue 4: Permission Denied

**Symptom:**
- "Permission denied" errors in logs
- Cannot write to logs or database

**Solution:**

```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/php-todo-api

# Fix permissions
sudo chmod 755 /var/www/php-todo-api
sudo chmod 775 /var/www/php-todo-api/data
sudo chmod 775 /var/www/php-todo-api/logs
sudo chmod 600 /var/www/php-todo-api/.env
```

---

## Final Deployment Checklist

**Before going to production:**

✅ Set `DEBUG_MODE=false` in `.env`
✅ Use strong random `JWT_SECRET` (32+ chars)
✅ Set `LOG_LEVEL=error` for production
✅ Verify all services are enabled (auto-start on boot)
✅ Configure firewall (allow only 80/443)
✅ Install SSL certificate (HTTPS)
✅ Set up regular database backups
✅ Monitor disk space and memory
✅ Configure log rotation
✅ Test all API endpoints
✅ Document server IP and credentials

---

## Screenshot: Final Working Deployment

**Complete working NGINX deployment:**

![Final Deployment](screenshots/final-deployment.png)

**This screenshot shows:**
- ✅ NGINX status: active and running
- ✅ PHP-FPM status: active and running
- ✅ Successful health check response
- ✅ API responding to requests

---

## Summary

**What we accomplished:**

1. ✅ Installed NGINX, PHP 8.1, and dependencies
2. ✅ Deployed PHP REST API to `/var/www/php-todo-api`
3. ✅ Configured NGINX with FastCGI for PHP
4. ✅ Set proper permissions and security
5. ✅ Tested all endpoints successfully
6. ✅ Verified database operations


---

## Resources

**Documentation:**
- [NGINX Documentation](https://nginx.org/en/docs/)
- [PHP-FPM Configuration](https://www.php.net/manual/en/install.fpm.php)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Let's Encrypt (SSL)](https://letsencrypt.org/)

**Monitoring Tools:**
- [htop](https://htop.dev/) - System monitoring
- [Netdata](https://www.netdata.cloud/) - Real-time monitoring
- [PM2](https://pm2.keymetrics.io/) - Process management

**Security:**
- [UFW Firewall Guide](https://help.ubuntu.com/community/UFW)
- [OWASP Security Guidelines](https://owasp.org/)

