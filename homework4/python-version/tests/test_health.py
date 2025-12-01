"""
Tests for health check endpoint.
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "service" in data
    assert "version" in data
    assert "checks" in data


def test_health_check_structure(client):
    """Test health check response structure."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()

    # Check main fields
    assert data["status"] in ["healthy", "unhealthy", "warning"]
    assert data["service"] == "TODO REST API"

    # Check sub-checks
    checks = data["checks"]
    assert "database" in checks
    assert "python" in checks
    assert "disk" in checks
    assert "memory" in checks


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "health" in data
