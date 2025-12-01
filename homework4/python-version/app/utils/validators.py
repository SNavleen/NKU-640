"""
Validation utilities for input validation.
"""

import uuid
from fastapi import HTTPException, status


def validate_uuid(uuid_string: str, field_name: str = "ID") -> str:
    """
    Validate that a string is a valid UUID v4.

    Args:
        uuid_string: String to validate
        field_name: Name of the field for error messages

    Returns:
        The validated UUID string

    Raises:
        HTTPException: If UUID is invalid
    """
    try:
        # Attempt to create a UUID object to validate format
        uuid_obj = uuid.UUID(uuid_string, version=4)
        return str(uuid_obj)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name} format. Must be a valid UUID v4.",
            headers={"X-Error-Code": "INVALID_UUID"}
        )
