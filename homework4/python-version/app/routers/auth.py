"""
Authentication routes for signup, login, and logout.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.jwt import create_access_token, get_token_expiry
from app.services.auth import authenticate_user, get_current_user, blacklist_token
from app.utils.security import hash_password

router = APIRouter()
security = HTTPBearer()


@router.post("/auth/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account and return a JWT token.

    - **username**: 3-50 characters, unique, alphanumeric
    - **email**: Valid email format, unique
    - **password**: Minimum 8 characters

    Returns user object and JWT token.
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
            headers={"X-Error-Code": "CONFLICT"}
        )

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
            headers={"X-Error-Code": "CONFLICT"}
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
            headers={"X-Error-Code": "CONFLICT"}
        )

    # Create access token
    access_token = create_access_token(data={"sub": new_user.id})

    return {
        "token": access_token,
        "user": UserResponse.from_orm(new_user)
    }


@router.post("/auth/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.

    - **username**: User's username
    - **password**: User's password

    Returns user object and JWT token.
    """
    # Authenticate user
    user = authenticate_user(db, credentials.username, credentials.password)

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return {
        "token": access_token,
        "user": UserResponse.from_orm(user)
    }


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout user and blacklist the current JWT token.

    Requires valid JWT token in Authorization header.
    Token will be added to blacklist and cannot be used again.
    """
    token = credentials.credentials

    # Get token expiry
    try:
        expires_at = get_token_expiry(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Blacklist the token
    blacklist_token(db, token, current_user.id, expires_at)

    return None
