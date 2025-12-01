"""
Pytest configuration and fixtures for testing.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User, TodoList, Task, TokenBlacklist

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with database override."""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    """Create a test user and return user data with token."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = client.post("/api/v1/auth/signup", json=user_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def auth_headers(test_user):
    """Return authorization headers with JWT token."""
    return {"Authorization": f"Bearer {test_user['token']}"}


@pytest.fixture
def test_list(client, db):
    """Create a test list."""
    list_data = {
        "name": "Test List",
        "description": "A test list"
    }
    response = client.post("/api/v1/lists", json=list_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def test_task(client, test_list):
    """Create a test task."""
    task_data = {
        "title": "Test Task",
        "description": "A test task",
        "completed": False,
        "priority": "medium"
    }
    response = client.post(f"/api/v1/lists/{test_list['id']}/tasks", json=task_data)
    assert response.status_code == 201
    return response.json()
