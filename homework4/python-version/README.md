# TODO REST API - Python FastAPI Implementation

A secure REST API for managing TODO lists and tasks with JWT authentication, built with FastAPI and SQLite.

## Features

- RESTful API design with JSON request/response
- JWT-based authentication with token blacklisting
- SQLite database with SQLAlchemy ORM
- Comprehensive input validation
- Password hashing with bcrypt
- Health check endpoint with system monitoring
- Docker support for easy deployment
- Comprehensive test suite with pytest
- API documentation with Swagger UI

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: SQLite (built-in)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Testing**: pytest with coverage
- **Package Management**: uv
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx

## Quick Start

### Prerequisites

- Python 3.11+
- uv (recommended) or pip
- Docker & Docker Compose (for containerized deployment)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd homework4/python-version
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run with Docker Compose:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### Local Development

1. Install dependencies:
```bash
uv sync
```

2. Run the development server:
```bash
uv run uvicorn app.main:app --reload
```

4. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/signup` | Create new user account | No |
| POST | `/api/v1/auth/login` | Authenticate and get JWT token | No |
| POST | `/api/v1/auth/logout` | Logout and blacklist token | Yes |
| GET | `/api/v1/users/profile` | Get current user profile | Yes |

### Lists

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/lists` | Get all lists | No |
| POST | `/api/v1/lists` | Create new list | No |
| GET | `/api/v1/lists/{id}` | Get list by ID | No |
| PATCH | `/api/v1/lists/{id}` | Update list | No |
| DELETE | `/api/v1/lists/{id}` | Delete list | No |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/lists/{listId}/tasks` | Get tasks in list | No |
| POST | `/api/v1/lists/{listId}/tasks` | Create task in list | No |
| GET | `/api/v1/tasks/{id}` | Get task by ID | No |
| PATCH | `/api/v1/tasks/{id}` | Update task | No |
| DELETE | `/api/v1/tasks/{id}` | Delete task | No |

### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/health` | Check API health and status | No |

## Testing

Run the test suite:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/test_auth.py

# Run with verbose output
uv run pytest -v
```

## Project Structure

```
python-version/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── list.py
│   │   ├── task.py
│   │   └── token_blacklist.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── list.py
│   │   └── task.py
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── lists.py
│   │   └── tasks.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── jwt.py
│   │   └── auth.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── security.py
│       └── validators.py
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_lists.py
│   ├── test_tasks.py
│   └── test_health.py
├── docker/
│   └── nginx.conf           # Nginx configuration
├── scripts/                 # Utility scripts
├── .env.example             # Environment variables template
├── .gitignore
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker image definition
├── pyproject.toml           # Project dependencies
├── README.md                # This file
├── API_CONTRACT.md          # Complete API specification
├── SAFETY_RULES.md          # Security guidelines
└── QUICKSTART.md            # Quick start guide
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL`: SQLite connection string
- `JWT_SECRET`: Secret key for JWT token signing (CHANGE IN PRODUCTION!)
- `JWT_EXPIRY`: Token expiration time in seconds (default: 3600)
- `DEBUG_MODE`: Enable debug mode (default: true)
- `LOG_LEVEL`: Logging level (debug, info, warning, error)

## Security Features

1. **Password Security**
   - Bcrypt hashing with cost factor 12
   - Passwords never stored or returned in plain text

2. **JWT Authentication**
   - Token-based authentication
   - Automatic token expiration (1 hour default)
   - Token blacklisting on logout

3. **Input Validation**
   - UUID v4 validation for all IDs
   - String length limits
   - Email format validation
   - SQL injection prevention via ORM

4. **Security Headers**
   - X-Frame-Options
   - X-Content-Type-Options
   - X-XSS-Protection
   - Referrer-Policy

5. **Rate Limiting**
   - Nginx-based rate limiting (10 requests/second)

## Deployment

### Docker Deployment

1. Build and start all services:
```bash
docker-compose up -d
```

2. Check service status:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f app
```

4. Stop services:
```bash
docker-compose down
```

### Production Checklist

- [ ] Change `JWT_SECRET` to a strong random value
- [ ] Set `DEBUG_MODE=false`
- [ ] Set `LOG_LEVEL=error`
- [ ] Use HTTPS (configure SSL in Nginx)
- [ ] Update CORS settings in nginx.conf
- [ ] Set proper file permissions
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Review and adjust rate limiting

## Database Management

### Migrations

This project uses SQLAlchemy with declarative models. Tables are created automatically on startup.

For production, consider using Alembic for database migrations:

```bash
# Initialize Alembic (one time)
uv run alembic init alembic

# Create migration
uv run alembic revision --autogenerate -m "description"

# Apply migration
uv run alembic upgrade head
```

### Database Access

```bash
# Access PostgreSQL CLI
docker exec -it todo_postgres psql -U todo_user -d todo_db

# View tables
\dt

# Query data
SELECT * FROM users;
SELECT * FROM lists;
SELECT * FROM tasks;
```

## Troubleshooting

### Database Connection Error

Check if the SQLite database file exists:
```bash
ls -la data/todo.db
```

Verify connection settings in `.env`:
```bash
DATABASE_URL=sqlite:///./data/todo.db
```

### Import Errors

Make sure dependencies are installed:
```bash
uv sync
```

### Port Already in Use

Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8001 to an available port
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Submit a pull request

## License

This project is part of NKU-640 coursework.

## Documentation

- [API Contract](API_CONTRACT.md) - Complete API specification
- [Safety Rules](SAFETY_RULES.md) - Security guidelines and best practices
- [Quick Start](QUICKSTART.md) - Getting started guide
- [API Docs](http://localhost:8000/docs) - Interactive API documentation (when running)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check existing issues
4. Create a new issue with details

## Changelog

### Version 1.0.0 (2025-12-01)
- Initial release
- JWT authentication with token blacklisting
- CRUD operations for lists and tasks
- SQLite database integration
- Docker support
- Comprehensive test suite
- API documentation
