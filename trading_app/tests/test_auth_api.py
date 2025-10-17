
# trading_app/tests/test_auth_api.py
import pytest
from httpx import AsyncClient
from starlette import status
from faker import Faker

fake = Faker()

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    email = fake.email()
    password = fake.password()
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == email
    assert "id" in data
    assert "hashed_password" not in data # Critical security check

@pytest.mark.asyncio
async def test_login_for_access_token(client: AsyncClient):
    email = fake.email()
    password = fake.password()
    # First, create the user
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )
    # Then, try to log in
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"