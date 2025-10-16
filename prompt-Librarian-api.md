
### ROLE
You are a Senior Python Developer specializing in building robust and maintainable API clients.

### OBJECTIVE
Generate a high-quality, asynchronous Python module that acts as a client for the "Librarian Service." The client must be implemented in a single file, `librarian_client.py`, and use modern practices like `httpx` for async requests and Pydantic for data validation.

### LIBRARIAN API CONTRACT (from Section 7.1 of the main blueprint)
-   **Endpoint:** `POST /api/v1/context`
-   **Authentication:** `X-API-KEY` header.
-   **Request Body (`application/json`):**
    ```json
    { "project_name": "string", "branch_name": "string", "query": "string", "max_results": "integer" }
    ```
-   **Success Response Body (`200 OK`):**
    ```json
    { "query_id": "uuid", "context": [ { "content": "string", "metadata": {}, "score": "float" } ] }
    ```

### REQUIREMENTS
1.  **Asynchronous:** The client must use `async/await` syntax and the `httpx.AsyncClient`.
2.  **Pydantic Models:** Define Pydantic models for both the request and response bodies to ensure type safety.
3.  **Configuration:** The Librarian service URL and API key must be configurable via environment variables.
4.  **Error Handling:** The client must handle potential HTTP errors (e.g., 4xx, 5xx) and network issues gracefully, raising custom exceptions.
5.  **Singleton Pattern:** Use a singleton pattern or a dependency injection-friendly approach to manage a single `httpx.AsyncClient` instance for the application's lifecycle, preventing port exhaustion.

### DELIVERABLE
The complete, fully-documented source code for the `librarian_client.py` file, including all necessary imports, Pydantic models, the client class, and custom exceptions.
