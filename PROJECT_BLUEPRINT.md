
# <!-- FILENAME: PROJECT_BLUEPRINT_RUNTIME.md -->
# PROJECT BLUEPRINT (RUNTIME): Trading App Web Service
<!-- 
This document is the canonical source of truth for the Trading App's runtime architecture.
It describes the system as it currently exists in its production-ready state.
Provide this file at the start of any AI session focused on troubleshooting, modification, or analysis.
-->

- **Version:** 1.0.0
- **Status:** Production Ready

---

## 1. System Overview

This system is a secure, user-facing web service that acts as the primary interface for an existing backend data pipeline and RAG (Retrieval-Augmented Generation) service. It provides users with features for portfolio management, trade journaling, and AI-powered analysis.

The architecture is a containerized full-stack application, orchestrated by Docker Compose. It is designed for seamless integration into the existing `shared-prod-vm-database` cloud environment.

### 1.1. Ecosystem Glossary
- **The Trading App (This System):** The full-stack application described in this document. It is the **primary user interface** for portfolio data and AI-driven insights. It is a **consumer** of data from the Data Pipeline and the Librarian Service.
- **The Data Pipeline (External Provider):** An existing, high-throughput system responsible for ingesting and persisting market data. The Trading App treats this as a **read-only source of truth** for market information (e.g., `ohlc`, `instruments`).
- **The Librarian Service (External Provider):** The centralized, production-grade RAG API. The Trading App is a **thin client** to this service; all complex RAG query logic is offloaded to the Librarian.
- **PgBouncer (Infrastructure):** The mandatory connection pooler for all PostgreSQL database interactions. All services, including the Trading App, **MUST** connect through it.


---

## 2. Core Architecture & Principles

### 2.1. Guiding Principles
1.  **Ecosystem Integration:** The application is a guest in a larger ecosystem. It **MUST** adhere to all documented patterns (PgBouncer, shared Docker network).
2.  **API-Driven & Decoupled:** The frontend and backend are decoupled. The backend API is the **sole authority** on business logic and data state. The frontend is a pure-state renderer that reacts to the API.

### 2.2. Architectural Diagram
The Trading App is a containerized FastAPI application and React frontend, co-located with existing services on a single VM and connected via a shared Docker network. Nginx acts as a reverse proxy and secure entry point.

```
+-------------------------------------------------------------------------+
| OCI VM (`shared-prod-vm-database`, ARM64)                               |
|                                                                         |
|  +---------------------------+       +--------------------------------+ |
|  | Nginx (Reverse Proxy)     |<----->| Static Frontend (React Files)  | |
|  | - SSL Termination         |       | (Served by Nginx)              | |
|  | - Rate Limiting           |       +--------------------------------+ |
|  +------------+--------------+                                          |
|               |                                                         |
|  +------------v------------------------------------------------------+  |
|  | Docker Network (`central-data-platform`)                          |  |
|  |                                                                   |  |
|  | +-----------------+   /api/   +-----------------+                 |  |
|  | | Nginx Container |<----------| trading_app_api |                 |  |
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

---

## 3. Service Directory

### Service: `trading_app_api`
- **Role:** The **authoritative backend service**. It is solely responsible for user authentication, business logic, data persistence for user-owned entities (transactions, portfolios), and acting as a secure proxy to other backend services (Librarian).
- **Technology:** FastAPI (Python)
- **Source Location:** `/app`
- **Interacts With:**
    - **Writes To:** PostgreSQL (`users`, `user_transactions`).
    - **Reads From:** PostgreSQL (via `pgbouncer:6432`), Librarian Service (`librarian:port`).
    - **Accessed By:** `nginx` (internally on port 8000).

### Service: `trading_app_ui`
- **Role:** A **pure client-side application**. Its sole responsibility is to render the user interface and communicate with the `trading_app_api` via its defined REST contract. It contains no business logic.
- **Technology:** React (Vite)
- **Source Location:** `/frontend`
- **Interacts With:**
    - **Reads From/Writes To:** `trading_app_api` via authenticated REST calls.
- **Note:** This is a build-time artifact. The compiled static files (`/frontend/dist`) are served directly by `nginx`.

### Service: `nginx`
- **Role:** The **secure edge and traffic router**. It is the single entry point for all user traffic, responsible for SSL/TLS, security headers, and routing requests to the appropriate backend service.
- **Technology:** Nginx
- **Configuration:** `nginx.conf`
- **Interacts With:**
    - **Routes:** Forwards requests starting with `/api/` to `trading_app_api`. Serves static files from `/frontend/dist` for all other requests.

---


## 4. API Contract (`trading_app_api`)

The `trading_app_api` provides the following versioned contract for its clients.

### 4.1. `POST /api/v1/auth/register`
-   **Purpose:** Registers a new user.
-   **Authentication:** None.
-   **Request Body:** `{ "email": "string", "password": "string" }`
-   **Success Response (201):** `{ "id": "uuid", "email": "string" }`

### 4.2. `POST /api/v1/auth/login`
-   **Purpose:** Authenticates a user and returns a JWT access token.
-   **Authentication:** None.
-   **Request Body:** `application/x-www-form-urlencoded`: `username=<email>&password=<password>`
-   **Success Response (200):** `{ "access_token": "string", "token_type": "bearer" }`

### 4.3. `GET /api/v1/transactions`
-   **Purpose:** Retrieves all transactions for the currently authenticated user.
-   **Authentication:** JWT Bearer Token required.
-   **Success Response (200):** `[ { "id": "uuid", "symbol": "string", "amount": "float", ... } ]`

### 4.4. `POST /api/v1/ai/chat`
-   **Purpose:** Acts as a secure proxy to the Librarian RAG service.
-   **Authentication:** JWT Bearer Token required.
-   **Request Body:** `{ "prompt": "string" }`
-   **Success Response (200):** `{ "response": "string", "query_id": "uuid" }`
---

## 5. User Action Lifecycle (Example: Creating a Transaction)

1.  **UI Interaction (Client):** A logged-in user fills out the "New Transaction" form in the `trading_app_ui` and clicks "Submit".
2.  **API Call (Client -> Server):** The React application makes an authenticated `POST` request to `/api/v1/transactions` with the form data as the JSON payload and the user's JWT in the `Authorization` header.
3.  **Authentication (Server):** The `trading_app_api` receives the request. A FastAPI dependency validates the JWT, identifies the user, and injects the user object into the request context. If the token is invalid, a `401 Unauthorized` is returned.
4.  **Business Logic (Server):** The API endpoint logic validates the incoming transaction data (Pydantic schema).
5.  **Database Write (Server):** The service layer constructs a SQLAlchemy model instance and commits it to the PostgreSQL database via the `pgbouncer` connection.
6.  **Response (Server -> Client):** The API returns a `201 Created` status with the newly created transaction object.
7.  **UI Update (Client):** The React application receives the successful response and updates its local state, causing the new transaction to appear in the user's data table.

---

## 6. Build System & Packaging

-   **Dependency Management:** Dependencies are managed in `pyproject.toml` and installed using `uv` for speed and reliability.
-   **Containerization (`Dockerfile`):** The service is packaged as a Docker image using a multi-stage build.
    -   **Stage 1 (Builder):** Installs dependencies to leverage Docker's layer caching.
    -   **Stage 2 (Final):** Copies dependencies and source code into a minimal `python-slim` base image. The container runs as a non-root user (`appuser`) to adhere to the principle of least privilege.

---

## 7. Operational Governance

### 7.1. Configuration
- **Runtime Configuration (`.env`):** A single `.env` file at the project root contains all runtime environment variables for the service (e.g., `DATABASE_URL`, `LIBRARIAN_API_KEY`). This file is the **sole source of configuration** for a running container and is loaded via the `env_file` directive in `docker-compose.yml`.

### 7.2. Runbooks
- **Canonical Deployment Method:** `bash deploy.sh`
- **Database Migrations:** `docker-compose run --rm trading_app_api alembic revision ...`
- **Log Inspection:** `docker-compose logs -f <service_name>`

---

## 8. Known Failure Modes & Recovery

- **Failure Mode:** Application returns a "502 Bad Gateway" from Nginx.
  - **Cause & Recovery:** The `trading_app_api` container is stopped, crashing, or unhealthy and not responding to requests from Nginx.

- **Failure Mode:** Frontend UI loads, but API calls fail with a `401 Unauthorized` error.
  - **Likely Cause:** The JWT stored in the browser's local storage is expired, invalid, or missing.
  - **Recovery:** Instruct the user to log out and log back in to acquire a fresh token. Check the `trading_app_api` logs for any authentication errors.

- **Failure Mode:** AI Chat feature returns "An error occurred".
  - **Likely Cause:**
      1. The `librarian` service is down or unreachable.
      2. The `LIBRARIAN_API_KEY` in the `.env` file is missing or invalid.
  - **Recovery:**
    1.  Check the `trading_app_api` logs (`docker-compose logs -f trading_app_api`) for errors related to `/api/v1/ai/chat`.
    2.  Verify the `LIBRARIAN_API_KEY` is set correctly in the `.env` file.
    3.  From within the API container, check connectivity: `docker-compose exec trading_app_api ping librarian`.

- **Failure Mode:** The `trading_app_api` service fails to start, logging database connection errors.
  - **Likely Cause:**
      1. The `pgbouncer` service is down or unreachable on the `central-data-platform` network.
      2. The `DATABASE_URL` in the `.env` file is incorrect.
      3. The Docker `central-data-platform` network is not attached or configured correctly.
  - **Recovery:**
    1.  Verify the `DATABASE_URL` in the `.env` file is correct.
    2.  Check the status of the `pgbouncer` container.
    3.  From within the API container, attempt to connect to the database host: `docker-compose exec trading_app_api ping pgbouncer`.

- **Failure Mode:** The AI Chat feature returns "An error occurred" messages on the frontend.
  - **Likely Cause:**
      1. The `librarian` service is down or unreachable.
      2. The `LIBRARIAN_API_KEY` in the `.env` file is missing or invalid.
  - **Recovery:**
    1.  Check the `trading_app_api` logs (`docker-compose logs -f trading_app_api`) for errors related to `/api/v1/ai/chat`.
    2.  Verify the `LIBRARIAN_API_KEY` is set correctly in the `.env` file.
    3.  From within the API container, check connectivity: `docker-compose exec trading_app_api ping librarian`.
