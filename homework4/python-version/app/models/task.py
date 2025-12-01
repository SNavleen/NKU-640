"""
Task database model.
"""

from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
import json

from app.database import Base


class PriorityEnum(str, enum.Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    """Task model representing individual todo items."""

    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    list_id = Column(String(36), ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text(2000), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    due_date = Column(DateTime, nullable=True)
    priority = Column(SQLEnum(PriorityEnum), nullable=True)
    categories = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    list = relationship("TodoList", back_populates="tasks")

    @property
    def categories_list(self):
        """Get categories as a list."""
        if self.categories:
            try:
                return json.loads(self.categories)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    @categories_list.setter
    def categories_list(self, value):
        """Set categories from a list."""
        if value:
            self.categories = json.dumps(value)
        else:
            self.categories = None

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title})>"
