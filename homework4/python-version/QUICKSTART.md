# Quick Start Guide

Get the TODO REST API up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for easiest setup)
- Or PostgreSQL 15+ (for local development)

## Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# 1. Navigate to the project directory
cd homework4/python-version

# 2. Copy environment variables
cp .env.example .env

# 3. Start all services
docker-compose up -d

# 4. Check status
docker-compose ps

# 5. View logs
docker-compose logs -f app
```

That's it! The API is now running at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/v1/health

## Option 2: Local Development

### Step 1: Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### Step 2: Set Up Database

No database setup required! SQLite database file will be created automatically in the `data/` directory.

### Step 3: Install Dependencies

```bash
# Install all dependencies
uv sync
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (defaults should work)
```

### Step 5: Run the Application

```bash
# Start the development server
uv run uvicorn app.main:app --reload
```

The API is now running at http://localhost:8000

## First API Call

Test the health endpoint:

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-01T12:00:00Z",
  "service": "TODO REST API",
  "version": "1.0.0",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "Database connection successful"
    },
    ...
  }
}
```

## Create Your First List

```bash
# Create a new todo list
curl -X POST http://localhost:8000/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First List",
    "description": "Getting started with the TODO API"
  }'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "My First List",
  "description": "Getting started with the TODO API",
  "createdAt": "2025-12-01T12:00:00Z",
  "updatedAt": null
}
```

## Create Your First Task

```bash
# Save the list ID from previous response
LIST_ID="550e8400-e29b-41d4-a716-446655440000"

# Create a task
curl -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Task",
    "description": "Learn how to use the API",
    "priority": "high"
  }'
```

## User Authentication

### Sign Up

```bash
# Create a new user account
SIGNUP_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "securepass123"
  }')

# Extract the token
TOKEN=$(echo $SIGNUP_RESPONSE | jq -r '.token')
echo "Your token: $TOKEN"
```

### Get Your Profile

```bash
# Use the token to access protected endpoints
curl http://localhost:8000/api/v1/users/profile \
  -H "Authorization: Bearer $TOKEN"
```

### Logout

```bash
# Logout and blacklist the token
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

## Interactive API Documentation

Visit http://localhost:8000/docs for:
- Interactive API explorer
- Try out endpoints directly in browser
- View request/response schemas
- See validation rules

## Testing the API

Run the test suite:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_lists.py -v
```

## Common Commands

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app

# Restart API
docker-compose restart app

# Rebuild after code changes
docker-compose up -d --build
```

### Database Commands

```bash
# Access PostgreSQL CLI
docker exec -it todo_postgres psql -U todo_user -d todo_db

# Inside psql:
\dt                    # List tables
SELECT * FROM lists;   # Query lists
SELECT * FROM tasks;   # Query tasks
\q                     # Exit
```

### Development Commands

```bash
# Start dev server with hot reload
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest

# Format code
uv run black app/

# Lint code
uv run ruff check app/

# Check types
uv run mypy app/
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml or uvicorn command
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check logs
docker logs todo_postgres

# Restart database
docker-compose restart db
```

### Import Errors

```bash
# Reinstall dependencies
uv sync --force

# Verify Python version
python --version  # Should be 3.11+
```

## Next Steps

1. **Read the Documentation:**
   - [README.md](README.md) - Complete project documentation
   - [API_CONTRACT.md](API_CONTRACT.md) - API specification
   - [SAFETY_RULES.md](SAFETY_RULES.md) - Security guidelines

2. **Explore the API:**
   - Visit http://localhost:8000/docs
   - Try all endpoints
   - Test error cases

3. **Run Tests:**
   - Explore test files in `tests/`
   - Run tests with `uv run pytest -v`
   - Check coverage with `--cov=app`

4. **Customize:**
   - Add new endpoints
   - Modify validation rules
   - Enhance authentication

5. **Deploy:**
   - Follow deployment guide in README.md
   - Set up production environment
   - Configure monitoring

## Example Workflow

Here's a complete example of creating a todo list with tasks:

```bash
# 1. Create a user account
SIGNUP=$(curl -s -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","email":"bob@example.com","password":"password123"}')

TOKEN=$(echo $SIGNUP | jq -r '.token')

# 2. Create a list
LIST=$(curl -s -X POST http://localhost:8000/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"name":"Groceries","description":"Weekly shopping"}')

LIST_ID=$(echo $LIST | jq -r '.id')

# 3. Add tasks to the list
curl -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","priority":"high","categories":["dairy"]}'

curl -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy bread","priority":"medium","categories":["bakery"]}'

curl -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy eggs","priority":"high","categories":["dairy"]}'

# 4. Get all tasks in the list
curl http://localhost:8000/api/v1/lists/$LIST_ID/tasks

# 5. Mark a task as completed
TASK_ID="<task-id-from-response>"
curl -X PATCH http://localhost:8000/api/v1/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# 6. Get all lists
curl http://localhost:8000/api/v1/lists

# 7. Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

## Getting Help

- Check the [README.md](README.md) for detailed information
- Review [API_CONTRACT.md](API_CONTRACT.md) for API specifications
- Read [SAFETY_RULES.md](SAFETY_RULES.md) for security best practices
- Check logs: `docker-compose logs -f app`
- Visit interactive docs: http://localhost:8000/docs

## What's Next?

You're now ready to:
- Build a frontend application
- Integrate with mobile apps
- Add new features
- Deploy to production
- Explore advanced features

Happy coding!
