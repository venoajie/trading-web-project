

# Stage 1: Base - A common, lean foundation with Python and uv
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PYTHONPYCACHEPREFIX=/tmp/.pycache \
    UV_VENV=/opt/venv

# Install uv, our package manager
RUN python -m pip install --no-cache-dir uv==0.2.19

# Create a virtual environment
RUN python -m uv venv ${UV_VENV}
ENV PATH="${UV_VENV}/bin:$PATH"

# Stage 2: Builder - Install dependencies into the venv
FROM base AS builder
WORKDIR /app

# Copy only the dependency definition file
COPY pyproject.toml .

# Install all dependencies, including dev dependencies for potential caching
RUN uv pip install --no-cache-dir '.[dev]'

# Stage 3: Runtime - The final, lean production image
FROM base AS runtime
WORKDIR /app

# Install netcat, which is required by our wait-for.sh script
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd -r appuser --gid=1001 && \
    useradd -r -m -g appuser --uid=1001 appuser

# Copy the virtual environment with dependencies from the builder stage
COPY --from=builder ${UV_VENV} ${UV_VENV}

# Copy the application code and the wait script
# Set ownership to the non-root user
COPY --chown=appuser:appuser ./trading_app/app ./app
COPY --chown=appuser:appuser ./trading_app/alembic ./alembic
COPY --chown=appuser:appuser ./alembic.ini .
COPY --chown=appuser:appuser ./wait-for.sh /usr/local/bin/wait-for.sh
RUN chmod +x /usr/local/bin/wait-for.sh

# Switch to the non-root user
USER appuser

EXPOSE 8000

# The entrypoint ensures the database is ready before the app starts
# This is a mandatory integration requirement.
ENTRYPOINT ["wait-for.sh", "pgbouncer:6432", "--"]

# The command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
