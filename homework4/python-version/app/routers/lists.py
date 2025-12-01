"""
List routes for CRUD operations on todo lists.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.list import TodoList
from app.schemas.list import ListCreate, ListUpdate, ListResponse
from app.utils.validators import validate_uuid

router = APIRouter()


@router.get("/lists", response_model=List[ListResponse])
def get_all_lists(db: Session = Depends(get_db)):
    """
    Retrieve all lists.

    Returns array of all todo lists in the system.
    """
    lists = db.query(TodoList).all()
    return [ListResponse.from_orm(lst) for lst in lists]


@router.get("/lists/{list_id}", response_model=ListResponse)
def get_list(list_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single list by ID.

    - **list_id**: UUID v4 of the list

    Returns the list object if found.
    """
    # Validate UUID
    validate_uuid(list_id, "List ID")

    # Get list from database
    lst = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not lst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    return ListResponse.from_orm(lst)


@router.post("/lists", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
def create_list(list_data: ListCreate, db: Session = Depends(get_db)):
    """
    Create a new list.

    - **name**: Required, 1-255 characters, cannot be only whitespace
    - **description**: Optional, max 1000 characters

    Returns the created list object with generated ID and timestamps.
    """
    # Create new list
    new_list = TodoList(name=list_data.title, description=list_data.description)

    db.add(new_list)
    db.commit()
    db.refresh(new_list)

    return ListResponse.from_orm(new_list)


@router.patch("/lists/{list_id}", response_model=ListResponse)
def update_list(list_id: str, list_data: ListUpdate, db: Session = Depends(get_db)):
    """
    Update an existing list.

    - **list_id**: UUID v4 of the list
    - **title**: Optional, 1-255 characters if provided
    - **description**: Optional, max 1000 characters if provided

    At least one field must be provided for update.
    Returns the updated list object.
    """
    # Validate UUID
    validate_uuid(list_id, "List ID")

    # Check if at least one field is provided
    if not any([list_data.title, list_data.description is not None]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update",
            headers={"X-Error-Code": "VALIDATION_ERROR"},
        )

    # Get list from database
    lst = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not lst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    # Update fields
    if list_data.title is not None:
        lst.name = list_data.title
    if list_data.description is not None:
        lst.description = list_data.description

    db.commit()
    db.refresh(lst)

    return ListResponse.from_orm(lst)


@router.delete("/lists/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: str, db: Session = Depends(get_db)):
    """
    Delete a list and all associated tasks.

    - **list_id**: UUID v4 of the list

    Cascade deletes all tasks associated with this list.
    Returns 204 No Content on success.
    """
    # Validate UUID
    validate_uuid(list_id, "List ID")

    # Get list from database
    lst = db.query(TodoList).filter(TodoList.id == list_id).first()
    if not lst:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found",
            headers={"X-Error-Code": "NOT_FOUND"},
        )

    # Delete list (cascade will delete tasks)
    db.delete(lst)
    db.commit()

    return None
