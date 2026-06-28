import httpx
from app.config import settings

async def send_whatsapp_message(to: str, message: str):
    # If WhatsApp credentials are not configured, skip silently
    if not settings.whatsapp_token or not settings.whatsapp_phone_number_id:
        print("WhatsApp credentials not configured, skipping")
        return
    
    url = f"https://graph.facebook.com/v19.0/{settings.whatsapp_phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"WhatsApp API failed: {response.status_code} - {response.text}")
        return response