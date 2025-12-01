"""
Configuration management for the TODO REST API.
Loads settings from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "TODO REST API"
    APP_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = True
    LOG_LEVEL: str = "debug"

    # Database
    DATABASE_URL: str = "sqlite:///./data/todo.db"

    # JWT Configuration
    JWT_SECRET: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY: int = 3600  # 1 hour in seconds

    # Password Hashing
    BCRYPT_ROUNDS: int = 12

    # API Settings
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
