"""
Authentication service for user verification and token validation.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.services.jwt import verify_token
from app.utils.security import verify_password

security = HTTPBearer()


def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Authenticate a user by username and password.

    Args:
        db: Database session
        username: User's username
        password: User's password

    Returns:
        User object if authentication successful

    Raises:
        HTTPException: If authentication fails
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.

    Args:
        credentials: HTTP authorization credentials containing JWT token
        db: Database session

    Returns:
        User object if token is valid

    Raises:
        HTTPException: If token is invalid, expired, or blacklisted
    """
    token = credentials.credentials

    # Check if token is blacklisted
    blacklisted = db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
    if blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify token
    try:
        payload = verify_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


def blacklist_token(db: Session, token: str, user_id: str, expires_at: datetime):
    """
    Add a token to the blacklist.

    Args:
        db: Database session
        token: JWT token to blacklist
        user_id: ID of the user who owns the token
        expires_at: Token expiration time
    """
    # Clean up expired tokens first
    db.query(TokenBlacklist).filter(TokenBlacklist.expires_at < datetime.utcnow()).delete()

    # Add token to blacklist
    blacklisted_token = TokenBlacklist(
        token=token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(blacklisted_token)
    db.commit()
