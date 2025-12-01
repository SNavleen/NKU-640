#!/bin/bash
# Local development run script using uv

set -e  # Exit on error

echo "=========================================="
echo "  TODO REST API - Local Development (uv)"
echo "=========================================="
echo

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv is not installed"
    echo "Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✓ uv is installed"

# Check if PostgreSQL is running
if command -v pg_isready &> /dev/null; then
    if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
        echo
        echo "WARNING: PostgreSQL is not running on localhost:5432"
        echo "Please start PostgreSQL or use Docker: ./scripts/setup.sh"
        echo
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# Create .env if it doesn't exist
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

# Sync dependencies using uv
echo "Syncing dependencies with uv..."
uv sync
echo "✓ Dependencies synced"

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo
echo "=========================================="
echo "  Starting API Server with uv"
echo "=========================================="
echo
echo "API URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/api/v1/health"
echo
echo "Press Ctrl+C to stop"
echo

# Run the application with uv
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
