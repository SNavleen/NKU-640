# Python TODO REST API Dockerfile with uv

FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files and README (required by hatchling)
COPY pyproject.toml uv.lock README.md ./

# Remove any existing virtual environment
RUN rm -rf .venv

# Install dependencies using uv
RUN uv sync --no-dev

# Change ownership of the virtual environment to appuser
RUN chown -R appuser:appuser .venv

# Copy application code
COPY --chown=appuser:appuser . .

# Create logs and data directories
RUN mkdir -p logs data && chown -R appuser:appuser logs data

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run application using uv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
