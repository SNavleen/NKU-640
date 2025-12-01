"""
User database model.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    lists = relationship("TodoList", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
