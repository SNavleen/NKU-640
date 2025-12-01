"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import logging
import time
from datetime import datetime

from app.config import get_settings
from app.database import init_db
from app.routers import auth, users, lists, tasks

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A secure REST API for managing TODO lists and tasks with JWT authentication",
    docs_url="/docs" if settings.DEBUG_MODE else None,
    redoc_url="/redoc" if settings.DEBUG_MODE else None,
)


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and their processing time."""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log request details
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )

    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation error",
            "code": "VALIDATION_ERROR",
            "details": exc.errors() if settings.DEBUG_MODE else {},
        },
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "code": "DATABASE_ERROR",
            "details": str(exc) if settings.DEBUG_MODE else {},
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "code": "INTERNAL_ERROR",
            "details": str(exc) if settings.DEBUG_MODE else {},
        },
    )


# Health check endpoint
@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """
    Check the health and status of the API and its dependencies.
    """
    from app.database import engine
    import psutil

    # Check database connection
    db_status = "healthy"
    db_message = "Database connection successful"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "unhealthy"
        db_message = f"Database connection failed: {str(e)}"

    # Get system stats
    disk_usage = psutil.disk_usage("/")
    memory = psutil.virtual_memory()

    overall_status = "healthy" if db_status == "healthy" else "unhealthy"
    status_code = (
        status.HTTP_200_OK if overall_status == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "checks": {
                "database": {"status": db_status, "message": db_message},
                "python": {
                    "status": "healthy",
                    "version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
                },
                "disk": {
                    "status": "healthy",
                    "free_space_mb": round(disk_usage.free / (1024 * 1024), 1),
                    "used_percent": disk_usage.percent,
                },
                "memory": {
                    "status": "healthy",
                    "memory_usage_mb": round((memory.total - memory.available) / (1024 * 1024)),
                    "memory_available_mb": round(memory.available / (1024 * 1024)),
                },
            },
        },
    )


# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["Authentication"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])
app.include_router(lists.router, prefix=settings.API_V1_PREFIX, tags=["Lists"])
app.include_router(tasks.router, prefix=settings.API_V1_PREFIX, tags=["Tasks"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down application...")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG_MODE else None,
        "health": "/api/v1/health",
    }
