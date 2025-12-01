#!/bin/bash
# One-command Docker setup script using uv

set -e  # Exit on error

echo "=========================================="
echo "  TODO REST API - Docker Setup (uv)"
echo "=========================================="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose is not installed"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker is installed"

# Generate JWT secret if .env doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env

    # Generate random JWT secret
    JWT_SECRET=$(openssl rand -base64 32)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|your-secret-key-min-32-bytes-replace-this-in-production|$JWT_SECRET|g" .env
    else
        # Linux
        sed -i "s|your-secret-key-min-32-bytes-replace-this-in-production|$JWT_SECRET|g" .env
    fi

    echo "✓ Generated JWT secret"
fi

# Create logs directory
mkdir -p logs
echo "✓ Created logs directory"

# Stop any existing containers
echo
echo "Stopping existing containers..."
docker-compose down || true

# Build and start containers
echo
echo "Building Docker images with uv..."
docker-compose build

echo
echo "Starting containers..."
docker-compose up -d

# Wait for services to be healthy
echo
echo "Waiting for services to be ready..."
sleep 5

# Check if database is ready
echo "Checking database connection..."
for i in {1..30}; do
    if docker-compose exec -T db pg_isready -U todo_user -d todo_db > /dev/null 2>&1; then
        echo "✓ Database is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: Database failed to start"
        docker-compose logs db
        exit 1
    fi
    echo "  Waiting for database... ($i/30)"
    sleep 2
done

# Check if API is ready
echo "Checking API health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        echo "✓ API is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "ERROR: API failed to start"
        docker-compose logs app
        exit 1
    fi
    echo "  Waiting for API... ($i/30)"
    sleep 2
done

# Show status
echo
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo
echo "API URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/api/v1/health"
echo
echo "Database:"
echo "  Host: localhost:5432"
echo "  Database: todo_db"
echo "  User: todo_user"
echo "  Password: todo_password"
echo
echo "Useful Commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop containers:  docker-compose down"
echo "  Restart:          docker-compose restart"
echo "  Run tests:        docker-compose exec app uv run pytest"
echo
echo "=========================================="

# Test API
echo
echo "Testing API..."
echo
HEALTH_RESPONSE=$(curl -s http://localhost:8000/api/v1/health)
echo "Health Check Response:"
echo "$HEALTH_RESPONSE" | python3 -m json.tool
echo
echo "✓ Setup successful!"
