"""
Database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db() -> Session:
    """
    Database dependency for FastAPI endpoints.
    Yields a database session and ensures cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    Creates all tables defined by SQLAlchemy models.
    """
    from app.models import user, list, task, token_blacklist
    Base.metadata.create_all(bind=engine)
