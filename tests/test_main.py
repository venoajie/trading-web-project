# trading_app/tests/test_main.py

import pytest
from httpx import AsyncClient
from starlette import status

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """
    Tests the health check endpoint to ensure the service is responsive.
    """
    response = await client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}