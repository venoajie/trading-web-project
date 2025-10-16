
# <!-- FILENAME: PROJECT_BLUEPRINT.md -->
# PROJECT BLUEPRINT: Trading App Web Service

<!-- 
This document is the canonical source of truth for the Trading App project.
It is a living document and MUST be updated at the conclusion of each development phase.
Provide the latest version of this file at the start of every new AI development session.
-->

- **Version:** 1.3.0
- **Status:** Active Development
- **Change Log (v1.3.0):** Completed Phase 1. Implemented JWT-based authentication and CRUD endpoints for the backend user core.
- **Change Log (v1.2.0):** Completed Phase 0, Step 0.2. Integrated Alembic for database migrations and defined initial SQLAlchemy models.
- **Change Log (v1.1.0):** Completed Phase 0, Step 0.1. Established foundational project structure including directories, dependency management (`pyproject.toml`), and a multi-stage `Dockerfile`.
- **Change Log (v1.0.0):** Initial blueprint creation. Establishes the full project scope, architecture, and phased implementation plan based on the analysis of the existing cloud ecosystem.

---

## 1. System Overview & Core Purpose

This project is to build the **Trading App**, a secure, user-facing web service that acts as the primary interface for an existing, sophisticated backend data pipeline and RAG (Retrieval-Augmented Generation) service.

Its purpose is not to reinvent the backend, but to **integrate seamlessly** into the existing production environment on the `shared-prod-vm-database` OCI VM. It will provide users with features for portfolio management, trade journaling, and AI-powered analysis while strictly adhering to the established architectural patterns of the ecosystem.

## 2. Guiding Principles

These principles govern all development decisions and AI-generated code:

1.  **Ecosystem Integration:** Adhere to all documented patterns (PgBouncer, shared Docker network, etc.). The application is a guest in an existing system.
2.  **Backend Robustness:** Prioritize a well-designed, secure, and testable API. The frontend can be simple initially but must be built on this solid foundation.

## 3. Core Architecture

The Trading App is a containerized FastAPI application co-located with the existing database and services on a single VM.

```
+-------------------------------------------------------------------------+
| OCI VM (`shared-prod-vm-database`, ARM64)                               |
|                                                                         |
|  +---------------------------+       +--------------------------------+ |
|  | Nginx (Reverse Proxy)     |<----->| Static Frontend (React Files)  | |
|  | - SSL Termination         |       | (Hosted on OCI Object Storage) | |
|  | - Rate Limiting           |       +--------------------------------+ |
|  +------------+--------------+                                          |
|               |                                                         |
|  +------------v------------------------------------------------------+  |
|  | Docker Network (`central-data-platform`)                          |  |
|  |                                                                   |  |
|  | +-----------------+   /api/   +-----------------+                 |  |
|  | | Nginx Container |<----------| Trading App API |                 |  |
|  | +-----------------+           | (FastAPI)       |                 |  |
|  |                               +-------+---------+                 |  |
|  |                                       |                           |  |
|  |      (API Call to `librarian:port`)   |   (DB Call to `pgbouncer:6432`) |
|  |                                       |                           |  |
|  |  +-----------------+        +---------v---------+        +---------v---------+   |
|  |  | Librarian Svc.  |<-------| (This service)    |------->| PgBouncer Svc.    |   |
|  |  | (Existing)      |        +-------------------+        | (Existing)        |   |
|  |  +-----------------+                                     +-------------------+   |
|  |                                                                                |
|  +--------------------------------------------------------------------------------+
+------------------------------------------------------------------------------------+
```

-   **Compute:** A single `trading_app` Docker container running on the existing OCI VM.
-   **Database Access (MANDATORY):** All connections MUST go through the `pgbouncer:6432` service.
-   **RAG Access (MANDATORY):** All AI context queries MUST be made via an API call to the existing `librarian` service.

## 4. Technology Stack

-   **Backend:** Python 3.12+, FastAPI, SQLAlchemy 2.0 (async), Pydantic, Alembic
-   **Frontend:** React, Vite, Mantine, Zustand, Axios
-   **Databases:** PostgreSQL 17 (via PgBouncer), Redis
-   **DevOps:** Docker, Docker Compose, Nginx, Let's Encrypt

---

## 5. Implementation Roadmap

This plan is divided into sequential, verifiable phases. Update the status of each step upon completion.

### **Phase 0: Project Foundation**
-   **Step 0.1: Project Scaffolding & Tooling**
    -   **Status:** `complete`
    -   **Objective:** Create the `trading_app` directory structure, `pyproject.toml`, and `Dockerfile`.
    -   **Notes:** Established `app/` and `tests/` directories, configured dependencies in `pyproject.toml` for `uv`, and created a multi-stage, non-root `Dockerfile`.

-   **Step 0.2: Implement Database Migrations**
    -   **Status:** `complete`
    -   **Objective:** Integrate Alembic to manage all database schema changes in a controlled, versioned manner.
    -   **Notes:** Integrated Alembic for async operations, defined core SQLAlchemy models, and generated the initial versioned schema baseline.

---

### **Phase 1: Backend User Core**
- **Status:** `complete`
- **Objective:** Build the core API for user authentication and data management.

-   **Step 1.1: Database Models**
    -   **Status:** `complete`
    -   **Objective:** Define SQLAlchemy models for `users`, `user_transactions`, `user_portfolios`, and `ai_conversations`.
    -   **Notes:** Established a scalable CRUD service pattern for the existing SQLAlchemy models.

-   **Step 1.2: API Endpoints**
    -   **Status:** `complete`
    -   **Objective:** Implement JWT-based registration/login and CRUD endpoints for user transactions.
    -   **Notes:** Implemented JWT-based registration/login endpoints with bcrypt hashing and a dependency for securing routes.

---

### **Phase 2: RAG Integration & Frontend Shell**
- **Status:** `pending`
- **Objective:** Connect the backend to the Librarian service and build the basic frontend structure.

-   **Step 2.1: Librarian Service Client**
    -   **Status:** `pending`
    -   **Objective:** Create a secure API client in the `trading_app` to communicate with the `librarian` service and create a proxy endpoint at `/ai/chat`.
    -   **Notes:**

-   **Step 2.2: Frontend Scaffolding**
    -   **Status:** `pending`
    -   **Objective:** Initialize a responsive React app with a persistent AI sidebar managed by Zustand.
    -   **Notes:**

-   **Step 2.3: Legal & Consent Placeholders**
    -   **Status:** `pending`
    -   **Objective:** Create placeholder legal pages and a mandatory consent checkbox for user registration.
    -   **Notes:**

---

### **Phase 3: First Useful Features**
- **Status:** `pending`
- **Objective:** Deliver the first interactive features to the user.

-   **Step 3.1: Frontend Transactions Feature**
    -   **Status:** `pending`
    -   **Objective:** Build the UI for users to create, view, and manage their manual trade entries.
    -   **Notes:**

-   **Step 3.2: Frontend AI Chat Integration**
    -   **Status:** `pending`
    -   **Objective:** Connect the AI sidebar UI to the backend's `/ai/chat` endpoint to create a functional chat experience.
    -   **Notes:**

---

### **Phase 4: Orchestration & Deployment**
- **Status:** `pending`
- **Objective:** Containerize and configure the application for deployment on the target VM.

-   **Step 4.1: Docker Compose Integration**
    -   **Status:** `pending`
    -   **Objective:** Create a `docker-compose.yml` that correctly connects the `trading_app` to the `central-data-platform` network.
    -   **Notes:**

-   **Step 4.2: Nginx Configuration**
    -   **Status:** `pending`
    -   **Objective:** Configure Nginx as a reverse proxy with SSL for the API and static frontend.
    -   **Notes:**

-   **Step 4.3: Deployment Script**
    -   **Status:** `pending`
    -   **Objective:** Create a `deploy.sh` script to automate the entire build and deployment process.
    -   **Notes:**

---

## 6. Architectural Decision Records (ADR)

This section records significant architectural decisions made during development that may deviate from the initial plan.

-   **ADR-001: Mandatory Use of Alembic for Migrations**
    -   **Status:** `Accepted`
    -   **Context:** The project requires a robust method for applying schema changes to a production database without data loss. Direct `ALTER TABLE` commands are forbidden by existing patterns.
    -   **Decision:** We will use Alembic as the official tool for all database migrations. The initial schema will be created via an Alembic script, not a raw `.sql` file.
    -   **Consequences:** Increased initial setup complexity but provides long-term safety, version control for the database schema, and repeatability.

-   **ADR-002: Pydantic for Type-Safe Configuration**
    -   **Status:** `Accepted`
    -   **Context:** The application requires a secure, reliable, and type-safe method for managing configuration, especially secrets like the database URL, which must be loaded from the environment.
    -   **Decision:** We will use Pydantic's `BaseSettings` class as the sole mechanism for loading and accessing application configuration. All configuration values will be sourced from environment variables.
    -   **Consequences:** This eliminates hardcoded secrets, provides automatic type validation on application startup, and improves the developer experience via autocompletion and clear schema definition in `app.core.config`.

## 7. System Interface Contracts

This section defines the stable interfaces this `trading_app` service consumes from the surrounding ecosystem. It is the definitive guide for how our application interacts with its neighbors, eliminating the need to consult their internal blueprints.

### 7.1. Librarian Service (RAG) Interface
The `trading_app` acts as a client to the central Librarian service for all RAG queries.

-   **Hostname (within Docker network):** `librarian`
-   **Endpoint:** `POST /api/v1/context`
-   **Authentication:** `X-API-KEY` header containing the shared secret.
-   **Request Body (`application/json`):**
    ```json
    {
      "project_name": "string",
      "branch_name": "string",
      "query": "string",
      "max_results": "integer",
      "filters": { "key": "value" }
    }
    ```
-   **Success Response Body (`200 OK`):**
    ```json
    {
      "query_id": "uuid",
      "context": [
        {
          "content": "string",
          "metadata": {
            "file_path": "string",
            "start_line": "integer"
          },
          "score": "float"
        }
      ],
      "processing_time_ms": "integer"
    }
    ```

### 7.2. Data Pipeline (Read-Only) Interface
The `trading_app` has read-only access to specific tables populated by the existing V2.5 data pipeline. The following table schemas are guaranteed to be available.

-   **Table: `instruments`**
    -   `id`: `integer` (Primary Key)
    -   `symbol`: `text` (e.g., 'BTC-PERPETUAL')
    -   `exchange`: `text` (e.g., 'deribit')
    -   `asset_type`: `text` (e.g., 'future', 'spot')
    -   `is_active`: `boolean`

-   **Table: `ohlc` (1-minute bars)**
    -   `instrument_id`: `integer` (Foreign Key to `instruments.id`)
    -   `timestamp`: `timestamptz`
    -   `open`: `numeric`
    -   `high`: `numeric`
    -   `low`: `numeric`
    -   `close`: `numeric`
    -   `volume`: `numeric`

-   **Table: `public_trades`**
    -   `instrument_id`: `integer` (Foreign Key to `instruments.id`)
    -   `timestamp`: `timestamtetz`
    -   `price`: `numeric`
    -   `amount`: `numeric`
    -   `side`: `text` ('buy' or 'sell')

### 7.3. Infrastructure & Host Interface
These are the non-negotiable connection parameters for the host environment.

-   **Database Host:** `pgbouncer`
-   **Database Port:** `6432`
-   **Shared Docker Network:** `central-data-platform`
-   **Host Architecture:** `linux/arm64`