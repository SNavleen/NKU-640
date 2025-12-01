"""
List schemas for request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class ListBase(BaseModel):
    """Base list schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator("title")
    @classmethod
    def name_not_empty(cls, v):
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_sanitize(cls, v):
        """Sanitize description."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class ListCreate(ListBase):
    """Schema for creating a list."""

    pass


class ListUpdate(BaseModel):
    """Schema for updating a list (all fields optional)."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator("title")
    @classmethod
    def name_not_empty(cls, v):
        """Validate title is not empty or whitespace."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError("Title cannot be empty or whitespace")
            return v.strip()
        return v

    @field_validator("description")
    @classmethod
    def description_sanitize(cls, v):
        """Sanitize description."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class ListResponse(BaseModel):
    """Schema for list response."""

    id: str
    title: str
    description: Optional[str] = None
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
            title=obj.name,
            description=obj.description,
            createdAt=obj.created_at,
            updatedAt=obj.updated_at,
        )
