"""
User routes for profile management.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.auth import get_current_user

router = APIRouter()


@router.get("/users/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile information.

    Requires valid JWT token in Authorization header.
    Returns user profile without password.
    """
    return UserResponse.from_orm(current_user)
