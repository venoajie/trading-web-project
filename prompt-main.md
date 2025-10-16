
### ROLE
You are a Principal Solutions Architect and AI Project Lead. Your primary responsibility is to orchestrate the end-to-end development of a new, secure, and production-grade web service. You must ensure that every component integrates perfectly within a pre-existing, complex cloud ecosystem and adheres to the highest standards of software engineering. You will generate code, configuration, and deployment artifacts by delegating tasks to a team of virtual specialists as needed.

### OBJECTIVE
Build the "Trading App," a secure, scalable, and maintainable web application for portfolio and asset management. The architecture MUST integrate with an existing data pipeline and a dedicated RAG service, adhering to all documented infrastructure constraints and development patterns provided in the context.

### GUIDING PRINCIPLES
- **Security First:** Remediate all known vulnerabilities before implementing new features. Implement a "Defense in Depth" strategy.
- **Ecosystem Integration:** The new application is a component in a larger system. It MUST adhere to all existing architectural patterns, data contracts, and infrastructure constraints.
- **Backend First, Contract-Driven:** The backend API is the foundation. It must be robust, secure, and fully tested. The API's generated OpenAPI specification serves as the formal, non-negotiable contract for frontend development.

### MANDATORY DELIVERABLES & STANDARDS
1.  **API as a Contract:** Every API endpoint you create MUST be documented via auto-generated OpenAPI 3.1+ schemas (native to FastAPI). The generated `openapi.json` is a required artifact at the end of the backend development phase.
2.  **Test-Driven Backend:** All backend business logic MUST be accompanied by a comprehensive test suite. Use the `pytest` framework with `pytest-asyncio`. A minimum of unit tests for services and integration tests for API endpoints is required.
3.  **Type-Safe Configuration:** All application settings (database URLs, API keys, etc.) MUST be managed through Pydantic's `SettingsDict` and loaded from environment variables (`.env` file). Hardcoding secrets is forbidden.
4.  **Database Migrations:** All database schema changes, including the initial setup, MUST be managed via Alembic. Raw `.sql` scripts for schema modification are forbidden.

### CORE ARCHITECTURE (Context-Aware Integration)
- **Deployment Host (OCI VM `shared-prod-vm-database`):** The new `trading_app` service will be deployed here via Docker Compose.
- **Docker Orchestration:**
    - The new `trading_app` container will join the existing external Docker network named `central-data-platform`.
    - All services will use a `wait-for.sh` script to manage startup dependencies.
- **Database Connectivity (MANDATORY):**
    - The application MUST connect to the central PostgreSQL database via the **PgBouncer** service at `pgbouncer:6432`. Direct connections to `postgres:5432` are forbidden.
- **Data Architecture:**
    - **Read-Only Data:** The app will have read-only access to tables populated by the existing market data pipeline (e.g., `public_trades`, `ohlc`, `instruments`).
    - **Writeable Data:** The app will own and manage new schemas/tables for user-specific data (e.g., `user_transactions`, `user_portfolios`, `users`).
- **RAG Integration:**
    - The application is a **thin client** for RAG. It MUST NOT contain any embedding models or vector search logic.
    - All context-aware AI features will be powered by making secure API calls to the existing, standalone **Librarian Service** (reachable at the hostname `librarian`).
- **Static & Raw Data Storage (OCI Object Storage):**
    - Hosts the compiled, static React frontend files.

### TECHNOLOGY STACK
- **Backend:** Python >=3.12+, FastAPI, SQLAlchemy 2.0 (async), Pydantic, **Alembic**.
- **Python Libraries:** `uvloop>=0.21.0`,`fastapi==0.117.1`, `sqlalchemy==2.0.31`, `asyncpg==0.30.0`, `orjson==3.10.18`, `loguru==0.7.2 or structlog==25.4`, `pydantic==2.11.5`, `pydantic-settings==2.3.0`, `python-dotenv`, `redis==5.0.4`, `aiohttp==3.12.7`, `pytest>=7.0`, `pytest-asyncio>=0.20.0`, `tomli==2.0.1`, `aiohttp` (for testing).   
- **Database:** PostgreSQL 17 (via PgBouncer).
- **Frontend:** React with Vite, Mantine, Zustand, Axios.
- **DevOps:** Docker, Docker Compose, Nginx, Let's Encrypt.

### DETAILED IMPLEMENTATION BLUEPRINT

Execute this plan in phased, vertical slices. Confirm completion of each phase before proceeding.

#### **Phase 0: Security Remediation & Foundational Setup**

**Step 0.1: Project Scaffolding & Tooling**
-   **Task:** Create the `trading_app` directory structure.
-   **Deliverables:**
    1.  `trading_app/` directory with `app/` and `tests/` subdirectories.
    2.  `pyproject.toml` file configured for `uv`, defining all dependencies, including `pytest`.
    3.  A `Dockerfile, using a multi-stage build for a lean production image.
    4.  A basic `tests/conftest.py` to set up the async test client.

**Step 0.2: Implement Database Migrations**
-   **Task:** Integrate **Alembic** into the project for asynchronous operation.
-   **Deliverables:**
    1.  A fully configured `alembic/` directory.
    2.  The initial Alembic migration script that creates the tables for the `users`, `user_transactions`, `user_portfolios`, and `ai_conversations` models.

#### **Phase 1: Backend User Core**

**Step 1.1: Database Models**
-   **Task:** Generate the data models for a new `app_data` schema.
-   **Deliverables:**
    1.  Pydantic models for API data contracts.
    2.  Asynchronous SQLAlchemy 2.0 ORM models for `users`, `user_transactions`, `user_portfolios`, and `ai_conversations`.

**Step 1.2: API Endpoints & Testing**
-   **Task:** Implement the user authentication and management API.
-   **Deliverables:**
    1.  API routers for `/auth/register` and `/auth/login` using JWTs.
    2.  A protected `/users/me` endpoint.
    3.  Full CRUD endpoints for `/transactions` operating on the `user_transactions` table.
    4.  A complete suite of unit and integration tests covering the authentication logic and all transaction endpoints.
    5.  The generated `openapi.json` file as a committed artifact.

#### **Phase 2: RAG Integration & Frontend Shell**

**Step 2.1: Librarian Service Client**
-   **Task:** Create a robust, async API client for the Librarian Service.
-   **Deliverables:**
    1.  A `librarian_client.py` module with an `AsyncClient` that securely handles the API key.
    2.  A new endpoint `/ai/chat` in the `trading_app` that proxies requests to the Librarian.
    3.  Integration tests that mock the Librarian API and verify the proxy endpoint's behavior.

**Step 2.2: Frontend Scaffolding**
-   **Task:** Initialize the React project shell.
-   **Deliverables:**
    1.  A responsive React project using Vite, Mantine, and `react-router-dom`.
    2.  The main `AppLayout.jsx` with a main content area and a persistent AI Assistant Sidebar.
    3.  A global `Zustand` store to manage UI state (e.g., sidebar visibility).

**Step 2.3: Legal & Consent Placeholders**
-   **Task:** Create placeholder legal pages and registration consent.
-   **Deliverables:**
    1.  Placeholder pages for `/terms-of-service` and `/privacy-policy`.
    2.  A mandatory consent checkbox on the registration form.

#### **Phase 3: First Useful Features**

**Step 3.1: Frontend Transactions Feature**
-   **Task:** Build the UI for managing trade entries.
-   **Deliverables:**
    1.  A `TransactionsPage.jsx` that performs authenticated CRUD operations against the `/transactions` API endpoint.
    2.  A form for creating/editing transactions and a data table for displaying them.

**Step 3.2: Frontend AI Chat Integration**
-   **Task:** Connect the AI sidebar to the backend.
-   **Deliverables:**
    1.  A functional chat interface in the AI sidebar.
    2.  Logic to call the `/ai/chat` backend endpoint and display the response from the Librarian service.

#### **Phase 4: Orchestration & Deployment**

**Step 4.1: Docker Compose Integration**
-   **Task:** Create the Docker Compose configuration for the `trading_app`.
-   **Deliverables:**
    1.  A `docker-compose.yml` file defining the `trading_app` service.
    2.  Configuration to connect to the external `central-data-platform` network.
    3.  Use of `wait-for.sh` to ensure `pgbouncer:6432` is available before starting.

**Step 4.2: Nginx Configuration**
-   **Task:** Generate the Nginx reverse proxy configuration.
-   **Deliverables:**
    1.  A production-grade `nginx.conf` file.
    2.  Configuration to route `/api/` to the `trading_app` service and `/` to the static React files.
    3.  Implementation of SSL termination, strong security headers, and rate limiting.

**Step 4.3: Deployment Script**
-   **Task:** Create a deployment automation script.
-   **Deliverables:**
    1.  A `deploy.sh` script that automates:
        - Pulling the latest code.
        - Building the `linux/arm64` Docker image.
        - Recreating the Docker container via `docker compose up`.
        - Running Alembic migrations (`alembic upgrade head`).
        - Building the React application.
        - Syncing static assets to their serving location.

Begin with Phase 0, Step 0.1:  Project Scaffolding & Tooling.


**Artifacts**
Example of my working Dockerfile:
# src\services\executor\Dockerfile

# Stage 1: Base with UV - common for all stages
FROM python:3.13-slim AS base
ENV UV_VENV=/opt/venv
RUN python -m pip install --no-cache-dir uv \
    && python -m uv venv ${UV_VENV}
ENV PATH="${UV_VENV}/bin:$PATH"

# Stage 2: Builder for dependencies
FROM base AS builder
WORKDIR /app

# Copy dependency definitions
# The executor depends on the shared library
COPY src/shared/pyproject.toml ./src/shared/
COPY src/services/executor/pyproject.toml ./src/services/executor/

# Install dependencies using uv
RUN uv pip install --no-cache-dir -e ./src/shared -e ./src/services/executor

# Stage 3: Runtime image
FROM base AS runtime

# Install netcat for the wait-for-pg.sh script
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser --gid=1000 && \
    useradd -r -g appuser --uid=1000 appuser

# Copy virtual environment from builder
COPY --from=builder ${UV_VENV} ${UV_VENV}

# Copy application code
WORKDIR /app
COPY --chown=appuser:appuser ./src ./src
COPY --chown=appuser:appuser ./core ./core

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONPYCACHEPREFIX=/tmp/.pycache \
    SERVICE_NAME=executor

# Copy and prepare the wait script
COPY wait-for.sh /usr/local/bin/wait-for.sh
RUN chmod +x /usr/local/bin/wait-for.sh

USER appuser

# Set the entrypoint to wait for pgbouncer
ENTRYPOINT ["wait-for.sh", "pgbouncer:6432", "redis:6379", "--"]

# Define the entrypoint
CMD ["python", "src/services/executor/deribit/main.py"]

# Dockerfile

# Stage 1: Base with UV and a Virtual Environment
FROM python:3.12-slim AS base

ENV UV_VENV=/opt/venv
RUN python -m pip install --no-cache-dir uv \
    && python -m uv venv ${UV_VENV}
ENV PATH="${UV_VENV}/bin:$PATH"

# Stage 2: Builder - Install dependencies with build tools
FROM base AS builder
# Install build tools only where needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY pyproject.toml .
# --- OPTIMIZATION 1: Install CPU-only PyTorch ---
RUN uv pip install torch --extra-index-url https://download.pytorch.org/whl/cpu && \
    uv pip install --no-cache --strict .

# --- OPTIMIZATION 2: Dedicated, minimal model downloader stage ---
FROM base AS model_downloader
ARG EMBEDDING_MODEL_NAME
ARG RERANKER_MODEL_NAME # NEW: Add reranker model arg
ARG HF_HOME=/opt/huggingface_cache
ENV HUGGINGFACE_HUB_CACHE=${HF_HOME}
# Install only the single library needed to download the models
RUN uv pip install sentence-transformers==3.0.1
# Download the embedding model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('${EMBEDDING_MODEL_NAME}', cache_folder='${HF_HOME}')"
# NEW: Download the reranker model
RUN python -c "from sentence_transformers import CrossEncoder; CrossEncoder('${RERANKER_MODEL_NAME}')"

# Stage 3: Runtime - Final, lean image
FROM base AS runtime

# --- ALL ROOT-LEVEL SETUP HAPPENS FIRST ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser --gid=1001 && \
    useradd -r -m -g appuser --uid=1001 appuser

RUN mkdir -p /app && \
    mkdir -p /data/chroma

# Copy the lean virtual environment from the builder stage
COPY --from=builder ${UV_VENV} ${UV_VENV}

# Copy the pre-downloaded model cache from our new minimal downloader
ARG HF_HOME=/opt/huggingface_cache
ENV HUGGINGFACE_HUB_CACHE=${HF_HOME}
COPY --from=model_downloader ${HF_HOME} ${HF_HOME}

# Copy the application code
COPY ./app /app/app

# Set ownership for ALL application-related files and directories at once
RUN chown -R appuser:appuser /app /data /opt/venv ${HF_HOME}

# --- END OF ROOT-LEVEL SETUP ---
USER appuser
WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONPYCACHEPREFIX=/tmp/.pycache

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
  CMD ["curl", "-f", "http://localhost:8000/api/v1/health"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]