"""
Task routes for CRUD operations on tasks.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.database import get_db
from app.models.list import TodoList
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.utils.validators import validate_uuid

router = APIRouter()


@router.get("/lists/{list_id}/tasks", response_model=List[TaskResponse])
def get_tasks_in_list(list_id: str, db: Session = Depends(get_db)):
    """
    Retrieve all tasks in a specific list.

    - **list_id**: UUID v4 of the list

    Returns array of all tasks in the specified list.
    """
    # Validate UUID
    validate_uuid(list_id, "List ID")

    # Check if list exists
    lst = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not lst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    # Get all tasks for this list
    tasks = db.query(Task).filter(Task.list_id == list_id).all()
    return [TaskResponse.from_orm(task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single task by ID.

    - **task_id**: UUID v4 of the task

    Returns the task object if found.
    """
    # Validate UUID
    validate_uuid(task_id, "Task ID")

    # Get task from database
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    return TaskResponse.from_orm(task)


@router.post(
    "/lists/{list_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED
)
def create_task(list_id: str, task_data: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task in a specific list.

    - **list_id**: UUID v4 of the list
    - **title**: Required, 1-255 characters, cannot be only whitespace
    - **description**: Optional, max 2000 characters
    - **completed**: Optional, boolean (default: false)
    - **dueDate**: Optional, ISO 8601 datetime
    - **priority**: Optional, enum ('low', 'medium', 'high')
    - **categories**: Optional, array of strings, max 10 items, each max 50 characters

    Returns the created task object with generated ID and timestamps.
    """
    # Validate UUID
    validate_uuid(list_id, "List ID")

    # Check if list exists
    lst = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not lst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    # Create new task
    new_task = Task(
        list_id=list_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        due_date=task_data.dueDate,
        priority=task_data.priority,
        categories=json.dumps(task_data.categories) if task_data.categories else None,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return TaskResponse.from_orm(new_task)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing task.

    - **task_id**: UUID v4 of the task
    - **title**: Optional, 1-255 characters if provided
    - **description**: Optional, max 2000 characters if provided
    - **completed**: Optional, boolean
    - **dueDate**: Optional, ISO 8601 datetime or null
    - **priority**: Optional, enum ('low', 'medium', 'high') or null
    - **categories**: Optional, array of strings, max 10 items

    At least one field must be provided for update.
    Returns the updated task object.
    """
    # Validate UUID
    validate_uuid(task_id, "Task ID")

    # Check if at least one field is provided
    update_data = task_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update",
            headers={"X-Error-Code": "VALIDATION_ERROR"},
        )

    # Get task from database
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    # Update fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    if "dueDate" in update_data:
        task.due_date = task_data.dueDate
    if "priority" in update_data:
        task.priority = task_data.priority
    if "categories" in update_data:
        task.categories = json.dumps(task_data.categories) if task_data.categories else None

    db.commit()
    db.refresh(task)

    return TaskResponse.from_orm(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete a task.

    - **task_id**: UUID v4 of the task

    Returns 204 No Content on success.
    """
    # Validate UUID
    validate_uuid(task_id, "Task ID")

    # Get task from database
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    # Delete task
    db.delete(task)
    db.commit()

    return None
