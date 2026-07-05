import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest.fixture(scope="session")
async def jwt_token(client):
    response = await client.post("/auth/login", json={
        "email": "franco@callsrm.com",
        "password": "test123"
    })
    return response.json()["access_token"]

async def test_get_contacts_without_token(client):
    response = await client.get("/contacts")
    assert response.status_code == 401

async def test_get_contacts_with_token(client, jwt_token):
    response = await client.get("/contacts", headers={
        "Authorization": f"Bearer {jwt_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)