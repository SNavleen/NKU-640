"""
JWT token generation and verification service.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from jose import JWTError, jwt

from app.config import get_settings

settings = get_settings()


def create_access_token(data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing token payload (e.g., {"sub": user_id})
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRY)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    # Encode token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Dict[str, any]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Invalid token: {str(e)}")


def get_token_expiry(token: str) -> datetime:
    """
    Get the expiration time of a JWT token.

    Args:
        token: JWT token string

    Returns:
        Expiration datetime

    Raises:
        JWTError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": False}  # Don't verify expiration for this check
        )
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
        raise JWTError("Token does not contain expiration time")
    except JWTError as e:
        raise JWTError(f"Invalid token: {str(e)}")
