"""
Tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_signup_success(client):
    """Test successful user registration."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["username"] == "newuser"
    assert data["user"]["email"] == "newuser@example.com"
    assert "password" not in data["user"]


def test_signup_duplicate_username(client, test_user):
    """Test signup with duplicate username."""
    user_data = {
        "username": "testuser",
        "email": "different@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 409
    assert "username already exists" in response.json()["detail"].lower()


def test_signup_duplicate_email(client, test_user):
    """Test signup with duplicate email."""
    user_data = {
        "username": "differentuser",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 409
    assert "email already exists" in response.json()["detail"].lower()


def test_signup_invalid_email(client):
    """Test signup with invalid email."""
    user_data = {
        "username": "newuser",
        "email": "invalid-email",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 422


def test_signup_short_password(client):
    """Test signup with password too short."""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "short"
    }
    response = client.post("/api/v1/auth/signup", json=user_data)

    assert response.status_code == 422


def test_login_success(client, test_user):
    """Test successful login."""
    credentials = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/auth/login", json=credentials)

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["username"] == "testuser"


def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    credentials = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=credentials)

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    credentials = {
        "username": "nonexistent",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", json=credentials)

    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_logout_success(client, auth_headers):
    """Test successful logout."""
    response = client.post("/api/v1/auth/logout", headers=auth_headers)

    assert response.status_code == 204


def test_logout_invalid_token(client):
    """Test logout with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/api/v1/auth/logout", headers=headers)

    assert response.status_code == 401


def test_token_blacklisted_after_logout(client, test_user):
    """Test that token cannot be used after logout."""
    token = test_user["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Logout
    response = client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == 204

    # Try to use token again
    response = client.get("/api/v1/users/profile", headers=headers)
    assert response.status_code == 401
    assert "revoked" in response.json()["detail"].lower()
