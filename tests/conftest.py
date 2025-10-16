
# trading_app/tests/conftest.py

import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient

from app.main import app

@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    An asynchronous test client for the application.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac