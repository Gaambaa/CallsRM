import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

async def test_register_user(client):
    response = await client.post("/auth/register", json={
        "email": "pytest2@callsrm.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "pytest2@callsrm.com"

async def test_login_user(client):
    response = await client.post("/auth/login", json={
        "email": "pytest2@callsrm.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_login_wrong_password(client):
    response = await client.post("/auth/login", json={
        "email": "pytest2@callsrm.com",
        "password": "wrong"
    })
    assert response.status_code == 401