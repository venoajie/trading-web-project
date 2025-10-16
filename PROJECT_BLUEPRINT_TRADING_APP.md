### `PROJECT_BLUEPRINT_TRADING_APP.md` 

```markdown
# PROJECT BLUEPRINT: Trading App Web Service

<!-- 
This document is the canonical source of truth for the Trading App project.
It is a living document and MUST be updated at the conclusion of each development phase.
Provide the latest version of this file at the start of every new AI development session.
-->

- **Version:** 1.1.0
- **Status:** Active Development
- **Change Log (v1.1.0):** Added Section 7, "System Interface Contracts." This section formally defines the APIs and data schemas for all external dependencies, making this blueprint a self-contained "mediator" document. This is a critical enhancement for multi-session AI development.
- **Change Log (v1.0.0):** Initial blueprint creation. Establishes the full project scope, architecture, and phased implementation plan.

---

## 1. System Overview & Core Purpose
(No changes from v1.0.0)

## 2. Guiding Principles
(No changes from v1.0.0)

## 3. Core Architecture
(No changes from v1.0.0)

## 4. Technology Stack
(No changes from v1.0.0)

---

## 5. Implementation Roadmap
(No changes from v1.0.0 - all statuses remain `pending`)

---

## 6. Architectural Decision Records (ADR)
(No changes from v1.0.0)

---

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
    -   `timestamp`: `timestamptz`
    -   `price`: `numeric`
    -   `amount`: `numeric`
    -   `side`: `text` ('buy' or 'sell')

### 7.3. Infrastructure & Host Interface
These are the non-negotiable connection parameters for the host environment.

-   **Database Host:** `pgbouncer`
-   **Database Port:** `6432`
-   **Shared Docker Network:** `central-data-platform`
-   **Host Architecture:** `linux/arm64`
```

This upgraded blueprint now perfectly fulfills your requirement. By formally defining the contracts in Section 7, it provides the AI with all the necessary information to build the `trading_app` and its integrations correctly, without needing to process the other, more detailed blueprints. It is a robust, self-contained specification ready for multi-session development.