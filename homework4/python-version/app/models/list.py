"""
TodoList database model.
"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class TodoList(Base):
    """TodoList model for organizing tasks."""

    __tablename__ = "lists"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text(1000), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="lists")
    tasks = relationship("Task", back_populates="list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TodoList(id={self.id}, name={self.name})>"
