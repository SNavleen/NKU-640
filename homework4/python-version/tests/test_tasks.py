"""
Tests for task endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


def test_create_task_success(client, test_list):
    """Test creating a new task."""
    task_data = {
        "title": "Buy milk",
        "description": "2 liters",
        "completed": False,
        "priority": "high",
        "categories": ["groceries", "dairy"]
    }
    response = client.post(f"/api/v1/lists/{test_list['id']}/tasks", json=task_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["description"] == "2 liters"
    assert data["completed"] is False
    assert data["priority"] == "high"
    assert data["categories"] == ["groceries", "dairy"]
    assert "id" in data
    assert "createdAt" in data


def test_create_task_minimal(client, test_list):
    """Test creating a task with minimal data."""
    task_data = {"title": "Simple task"}
    response = client.post(f"/api/v1/lists/{test_list['id']}/tasks", json=task_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Simple task"
    assert data["completed"] is False
    assert data["priority"] is None


def test_create_task_with_due_date(client, test_list):
    """Test creating a task with due date."""
    due_date = (datetime.utcnow() + timedelta(days=7)).isoformat()
    task_data = {
        "title": "Task with deadline",
        "dueDate": due_date
    }
    response = client.post(f"/api/v1/lists/{test_list['id']}/tasks", json=task_data)

    assert response.status_code == 201
    data = response.json()
    assert data["dueDate"] is not None


def test_create_task_empty_title(client, test_list):
    """Test creating a task with empty title."""
    task_data = {"title": "   "}
    response = client.post(f"/api/v1/lists/{test_list['id']}/tasks", json=task_data)

    assert response.status_code == 422


def test_create_task_missing_title(client, test_list):
    """Test creating a task without title."""
    task_data = {"description": "No title"}
    response = client.post(f"/api/v1/lists/{test_list['id']}/tasks", json=task_data)

    assert response.status_code == 422


def test_create_task_invalid_priority(client, test_list):
    """Test creating a task with invalid priority."""
    task_data = {
        "title": "Task",
        "priority": "urgent"
    }
    response = client.post(f"/api/v1/lists/{test_list['id']}/tasks", json=task_data)

    assert response.status_code == 422


def test_create_task_list_not_found(client):
    """Test creating a task in non-existent list."""
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    task_data = {"title": "Task"}
    response = client.post(f"/api/v1/lists/{fake_uuid}/tasks", json=task_data)

    assert response.status_code == 404


def test_get_tasks_in_list(client, test_list, test_task):
    """Test retrieving all tasks in a list."""
    response = client.get(f"/api/v1/lists/{test_list['id']}/tasks")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(task["id"] == test_task["id"] for task in data)


def test_get_tasks_empty_list(client, test_list):
    """Test retrieving tasks from an empty list."""
    response = client.get(f"/api/v1/lists/{test_list['id']}/tasks")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_task_by_id(client, test_task):
    """Test retrieving a specific task by ID."""
    response = client.get(f"/api/v1/tasks/{test_task['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_task["id"]
    assert data["title"] == test_task["title"]


def test_get_task_invalid_uuid(client):
    """Test retrieving a task with invalid UUID."""
    response = client.get("/api/v1/tasks/invalid-uuid")

    assert response.status_code == 400


def test_get_task_not_found(client):
    """Test retrieving a non-existent task."""
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    response = client.get(f"/api/v1/tasks/{fake_uuid}")

    assert response.status_code == 404


def test_update_task(client, test_task):
    """Test updating a task."""
    update_data = {
        "title": "Updated task",
        "completed": True,
        "priority": "low"
    }
    response = client.patch(f"/api/v1/tasks/{test_task['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated task"
    assert data["completed"] is True
    assert data["priority"] == "low"


def test_update_task_partial(client, test_task):
    """Test partial update of a task."""
    update_data = {"completed": True}
    response = client.patch(f"/api/v1/tasks/{test_task['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == test_task["title"]


def test_update_task_categories(client, test_task):
    """Test updating task categories."""
    update_data = {"categories": ["work", "important"]}
    response = client.patch(f"/api/v1/tasks/{test_task['id']}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["categories"] == ["work", "important"]


def test_update_task_not_found(client):
    """Test updating a non-existent task."""
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    update_data = {"title": "Updated"}
    response = client.patch(f"/api/v1/tasks/{fake_uuid}", json=update_data)

    assert response.status_code == 404


def test_delete_task(client, test_task):
    """Test deleting a task."""
    response = client.delete(f"/api/v1/tasks/{test_task['id']}")

    assert response.status_code == 204

    # Verify task is deleted
    response = client.get(f"/api/v1/tasks/{test_task['id']}")
    assert response.status_code == 404


def test_delete_task_not_found(client):
    """Test deleting a non-existent task."""
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    response = client.delete(f"/api/v1/tasks/{fake_uuid}")

    assert response.status_code == 404


def test_cascade_delete_tasks_with_list(client, test_list, test_task):
    """Test that tasks are deleted when their list is deleted."""
    # Delete the list
    response = client.delete(f"/api/v1/lists/{test_list['id']}")
    assert response.status_code == 204

    # Verify task is also deleted
    response = client.get(f"/api/v1/tasks/{test_task['id']}")
    assert response.status_code == 404
