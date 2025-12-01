"""
Tests for list endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_create_list_success(client):
    """Test creating a new list."""
    list_data = {
        "name": "Groceries",
        "description": "Weekly shopping list"
    }
    response = client.post("/api/v1/lists", json=list_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Groceries"
    assert data["description"] == "Weekly shopping list"
    assert "id" in data
    assert "createdAt" in data


def test_create_list_no_description(client):
    """Test creating a list without description."""
    list_data = {"name": "Todo List"}
    response = client.post("/api/v1/lists", json=list_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Todo List"
    assert data["description"] is None


def test_create_list_empty_name(client):
    """Test creating a list with empty name."""
    list_data = {"name": "   "}
    response = client.post("/api/v1/lists", json=list_data)

    assert response.status_code == 422


def test_create_list_missing_name(client):
    """Test creating a list without name."""
    list_data = {"description": "No name"}
    response = client.post("/api/v1/lists", json=list_data)

    assert response.status_code == 422


def test_get_all_lists(client, test_list):
    """Test retrieving all lists."""
    response = client.get("/api/v1/lists")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(lst["id"] == test_list["id"] for lst in data)


def test_get_list_by_id(client, test_list):
    """Test retrieving a specific list by ID."""
    response = client.get(f"/api/v1/lists/{test_list['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_list["id"]
    assert data["name"] == test_list["name"]


def test_get_list_invalid_uuid(client):
    """Test retrieving a list with invalid UUID."""
    response = client.get("/api/v1/lists/invalid-uuid")

    assert response.status_code == 400
    assert "invalid" in response.json()["detail"].lower()


def test_get_list_not_found(client):
    """Test retrieving a non-existent list."""
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    response = client.get(f"/api/v1/lists/{fake_uuid}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_list(client, test_list):
    """Test updating a list."""
    update_data = {
        "name": "Updated List",
        "description": "Updated description"
    }
    response = client.patch(f"/api/v1/lists/{test_list['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated List"
    assert data["description"] == "Updated description"
    assert "updatedAt" in data


def test_update_list_partial(client, test_list):
    """Test partial update of a list."""
    update_data = {"name": "Partially Updated"}
    response = client.patch(f"/api/v1/lists/{test_list['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Partially Updated"
    assert data["description"] == test_list["description"]


def test_update_list_not_found(client):
    """Test updating a non-existent list."""
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    update_data = {"name": "Updated"}
    response = client.patch(f"/api/v1/lists/{fake_uuid}", json=update_data)

    assert response.status_code == 404


def test_delete_list(client, test_list):
    """Test deleting a list."""
    response = client.delete(f"/api/v1/lists/{test_list['id']}")

    assert response.status_code == 204

    # Verify list is deleted
    response = client.get(f"/api/v1/lists/{test_list['id']}")
    assert response.status_code == 404


def test_delete_list_not_found(client):
    """Test deleting a non-existent list."""
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    response = client.delete(f"/api/v1/lists/{fake_uuid}")

    assert response.status_code == 404
