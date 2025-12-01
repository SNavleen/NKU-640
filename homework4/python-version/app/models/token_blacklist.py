"""
Token blacklist database model.
"""

from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
import uuid

from app.database import Base


class TokenBlacklist(Base):
    """TokenBlacklist model for invalidating JWT tokens on logout."""

    __tablename__ = "token_blacklist"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    token = Column(Text, unique=True, nullable=False, index=True)
    user_id = Column(String(36), nullable=False)
    blacklisted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<TokenBlacklist(id={self.id}, user_id={self.user_id})>"
