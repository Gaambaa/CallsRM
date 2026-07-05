import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "CallsRM"}

async def test_webhook_returns_200(client):
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "123",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "contacts": [{"profile": {"name": "Test"}, "wa_id": "591123"}],
                    "messages": [{
                        "id": "wamid.test-pytest-001",
                        "from": "591123",
                        "timestamp": "1782046964",
                        "text": {"body": "test"},
                        "type": "text"
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    response = await client.post("/webhooks", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

async def test_webhook_malformed_payload(client):
    response = await client.post("/webhooks", json={"random": "data"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}