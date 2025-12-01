# TODO REST API - Python

A secure REST API for managing TODO lists and tasks with JWT authentication, built with FastAPI and SQLAlchemy.

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Features](#features)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

```bash
# Install Python 3.11+ and uv package manager
brew install python@3.11 uv
```

### Installation

```bash
cd ./docs/homework4/python-version
uv sync
```

### Configuration

1. Generate a JWT secret:

```bash
openssl rand -base64 32
```

2. Update `.env`:

```bash
JWT_SECRET=your-generated-secret-here
JWT_EXPIRY=3600
DEBUG_MODE=true
DATABASE_URL=sqlite:///./todo.db
```

### Running the API

```bash
# Development server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Docker
docker-compose up
```

The API will be available at `http://localhost:8000`

---

## Installation

### Local Development

1. **Clone and navigate:**
   ```bash
   cd homework4/python-version
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database:**
   ```bash
   uv run python -m app.database
   ```

### Docker Deployment

```bash
docker-compose up --build
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET` | Secret key for JWT tokens | Required |
| `JWT_EXPIRY` | Token expiry in seconds | 3600 |
| `DATABASE_URL` | Database connection string | `sqlite:///./todo.db` |
| `DEBUG_MODE` | Enable debug logging | `false` |

### Database

The API uses SQLite by default. For production, update `DATABASE_URL` to your preferred database.

---

## Testing

### Run Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=app --cov-report=html

# Specific test file
uv run pytest tests/test_auth.py
```

### API Testing

Use the provided Bruno collection (`bruno/`) for comprehensive API testing:

```bash
# Import the collection into Bruno and run tests
```

### Manual Testing

```bash
# Health check
curl http://localhost:8000/api/v1/health

# API documentation
open http://localhost:8000/docs
```

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

### Lists
- `GET /api/v1/lists` - Get all user lists
- `POST /api/v1/lists` - Create new list
- `GET /api/v1/lists/{id}` - Get specific list
- `PATCH /api/v1/lists/{id}` - Update list
- `DELETE /api/v1/lists/{id}` - Delete list

### Tasks
- `GET /api/v1/lists/{list_id}/tasks` - Get tasks in list
- `POST /api/v1/lists/{list_id}/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PATCH /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

See [API Reference](API.md) for complete documentation.

---

## Features

- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **Password Security**: Argon2 password hashing (no length limits)
- **CRUD Operations**: Full Create, Read, Update, Delete for lists and tasks
- **Data Validation**: Pydantic schemas with comprehensive validation
- **Database ORM**: SQLAlchemy with SQLite/PostgreSQL support
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Error Handling**: Comprehensive error responses with proper HTTP codes
- **Logging**: Structured logging with request/response tracking
- **Testing**: Full test suite with pytest
- **Docker Support**: Containerized deployment with docker-compose

---

## Development

### Project Structure

```
app/
├── main.py              # FastAPI application
├── database.py          # Database connection and setup
├── config.py            # Configuration management
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── list.py
│   ├── task.py
│   └── token_blacklist.py
├── schemas/             # Pydantic schemas
│   ├── user.py
│   ├── list.py
│   └── task.py
├── routers/             # API route handlers
│   ├── auth.py
│   ├── lists.py
│   └── tasks.py
└── utils/
    └── security.py      # Password hashing and JWT utilities
```

### Code Quality

```bash
# Format code
uv run black .

# Lint code
uv run flake8 .

# Type checking
uv run mypy .
```

---

## Deployment

### Docker Production

```bash
# Build and run
docker-compose -f docker-compose.yml up --build

# Background
docker-compose up -d
```

### Manual Production

```bash
# Install production dependencies
uv sync --only prod

# Run with gunicorn
uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

See [Deployment Tutorial](deployment-tutorial.md) for detailed instructions.

---

## Troubleshooting

### Common Issues

**Database Connection Failed**
```
Error: (sqlite3.OperationalError) unable to open database file
```
- Ensure the database directory exists and has write permissions
- Check `DATABASE_URL` in environment variables

**JWT Token Invalid**
```
Error: Invalid token
```
- Verify `JWT_SECRET` is set correctly
- Check token expiry time

**Import Errors**
```
ModuleNotFoundError: No module named 'app'
```
- Ensure you're running from the correct directory
- Check Python path: `uv run python -c "import sys; print(sys.path)"`

### Debug Mode

Enable debug logging:

```bash
DEBUG_MODE=true uv run uvicorn app.main:app --reload
```

### Logs

Check application logs:

```bash
# Docker logs
docker-compose logs -f app

# Direct logs
tail -f logs/app.log
```

### Health Check

```bash
curl -v http://localhost:8000/api/v1/health
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run the full test suite
5. Submit a pull request

---

## License

This project is part of NKU 640 coursework.