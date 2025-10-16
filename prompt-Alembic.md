### ROLE
You are a Senior Python Developer specializing in database management and DevOps.

### OBJECTIVE
Generate the complete file and directory structure for integrating Alembic into an existing FastAPI project. The setup must be configured for an asynchronous application using `asyncpg` and should generate the initial migration script for the user management schema.

### CONTEXT
- The FastAPI application's source code is located in a directory named `app/`.
- The database connection URL is provided via an environment variable `DATABASE_URL`.
- The SQLAlchemy models will be defined in `app/models.py`.

### REQUIRED TABLES FOR INITIAL MIGRATION
Your initial migration script must create the following four tables:
1.  `users`: with `id`, `email`, `hashed_password`, `subscription_tier`.
2.  `user_transactions`: for manual trade entries.
3.  `user_portfolios`: for aggregated portfolio states.
4.  `ai_conversations`: for user chat history.

### DELIVERABLES
1.  **Alembic Directory Structure:** Create the full `alembic/` directory and its contents.
2.  **`alembic.ini`:** The main configuration file.
3.  **`alembic/env.py`:** The script for configuring and running migrations. It MUST be configured for an asynchronous environment.
4.  **`alembic/script.py.mako`:** The migration script template.
5.  **Initial Migration File:** The auto-generated first migration script located in `alembic/versions/` that contains the `upgrade()` and `downgrade()` functions to create and drop the four required tables.

Provide the complete file contents for each of these deliverables.