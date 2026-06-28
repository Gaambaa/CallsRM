import httpx
from app.config import settings

async def forward_to_n8n(event_type: str, data: dict):
    # If n8n webhook URL is not configured, skip silently
    if not settings.n8n_webhook_url:
        return
    
    payload = {
        "event_type": event_type,
        "data": data
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.n8n_webhook_url, json=payload)
        if response.status_code != 200:
            print(f"n8n webhook failed: {response.status_code}")