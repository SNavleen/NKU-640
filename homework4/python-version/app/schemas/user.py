"""
User schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v):
        """Validate username is alphanumeric."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores and hyphens allowed)")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""

    id: str
    username: str
    email: str
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
            username=obj.username,
            email=obj.email,
            createdAt=obj.created_at,
            updatedAt=obj.updated_at,
        )


class TokenResponse(BaseModel):
    """Schema for authentication token response."""

    token: str
    user: UserResponse
