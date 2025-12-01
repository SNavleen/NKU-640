"""
Task schemas for request/response validation.
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum


class PriorityEnum(str, Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(BaseModel):
    """Base task schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    completed: bool = False
    dueDate: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    categories: Optional[List[str]] = Field(None, max_items=10)

    @validator("title")
    def title_not_empty(cls, v):
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()

    @validator("description")
    def description_sanitize(cls, v):
        """Sanitize description."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v

    @validator("categories")
    def categories_validate(cls, v):
        """Validate categories."""
        if v is not None:
            if len(v) > 10:
                raise ValueError("Maximum 10 categories allowed")
            for category in v:
                if not isinstance(category, str):
                    raise ValueError("All categories must be strings")
                if len(category) > 50:
                    raise ValueError("Each category must be max 50 characters")
            return [c.strip() for c in v if c.strip()]
        return v


class TaskCreate(TaskBase):
    """Schema for creating a task."""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    completed: Optional[bool] = None
    dueDate: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    categories: Optional[List[str]] = Field(None, max_items=10)

    @validator("title")
    def title_not_empty(cls, v):
        """Validate title is not empty or whitespace."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Title cannot be empty or whitespace")
            return v.strip()
        return v

    @validator("description")
    def description_sanitize(cls, v):
        """Sanitize description."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v

    @validator("categories")
    def categories_validate(cls, v):
        """Validate categories."""
        if v is not None:
            if len(v) > 10:
                raise ValueError("Maximum 10 categories allowed")
            for category in v:
                if not isinstance(category, str):
                    raise ValueError("All categories must be strings")
                if len(category) > 50:
                    raise ValueError("Each category must be max 50 characters")
            return [c.strip() for c in v if c.strip()]
        return v


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: str
    listId: str
    title: str
    description: Optional[str] = None
    completed: bool
    dueDate: Optional[datetime] = None
    priority: Optional[str] = None
    categories: Optional[List[str]] = None
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        """Convert ORM object to schema with camelCase."""
        return cls(
            id=obj.id,
            listId=obj.list_id,
            title=obj.title,
            description=obj.description,
            completed=obj.completed,
            dueDate=obj.due_date,
            priority=obj.priority.value if obj.priority else None,
            categories=obj.categories_list,
            createdAt=obj.created_at,
            updatedAt=obj.updated_at,
        )
