
# trading_app/tests/test_ai_api.py
import pytest
from httpx import AsyncClient
from starlette import status
from unittest.mock import patch, AsyncMock

from app.api.deps import get_current_user
from tests.utils import get_test_user, get_user_token_headers

@pytest.mark.asyncio
@patch("app.clients.librarian.LibrarianClient.query", new_callable=AsyncMock)
async def test_chat_with_ai_success(
    mock_librarian_query: AsyncMock,
    client: AsyncClient,
    # This setup overrides the dependency for this test run
    # to return a valid user without a real DB hit
    # (assuming a test utility function `get_test_user` exists)
):
    # Arrange
    # 1. Mock the external service response
    mock_response = {"answer": "The market is volatile.", "sources": []}
    mock_librarian_query.return_value = mock_response

    # 2. Get a valid auth header for a test user
    headers = await get_user_token_headers(client) # Assumes a utility to create user and get token
    
    # Act
    response = await client.post(
        "/api/v1/ai/chat",
        headers=headers,
        json={"prompt": "What is the market outlook?"},
    )

    # Assert
    # 1. Check for success status and correct response payload
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["answer"] == "The market is volatile."
    assert "conversation_id" in data

    # 2. Verify that our mock client was called exactly once with the correct prompt
    mock_librarian_query.assert_called_once()
    call_args = mock_librarian_query.call_args[1]
    assert call_args["prompt"] == "What is the market outlook?"

@pytest.mark.asyncio
async def test_chat_with_ai_unauthenticated(client: AsyncClient):
    # Act
    response = await client.post(
        "/api/v1/ai/chat",
        json={"prompt": "This should fail."},
    )
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED