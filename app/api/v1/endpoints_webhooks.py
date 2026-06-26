from fastapi import APIRouter, BackgroundTasks, Request
from app.database import async_session
from app.services.contact_service import get_or_create_contact

router = APIRouter()

@router.post("/webhooks")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    # Meta requires a 200 OK response in under 20ms.
    # If we exceed this, Meta retries and may disable our endpoint.
    # So we return immediately and process the payload in the background.
    payload = await request.json()
    background_tasks.add_task(process_webhook, payload)
    return {"status": "ok"}

async def process_webhook(payload: dict):
    # Heavy logic runs here — DB writes, contact creation, etc.
    # This runs AFTER the 200 OK is already sent to Meta.
    try:
        value = payload["entry"][0]["changes"][0]["value"]
    except (KeyError, IndexError):
        # Payload malformed or not from Meta — ignore silently
        return

    async with async_session() as session:
        if "messages" in value:
            phone_number = value["contacts"][0]["wa_id"]
            name = value["contacts"][0]["profile"]["name"]
            contact = await get_or_create_contact(session, phone_number, name)
            print(f"contacto: {contact.phone_number}")
        elif "calls" in value:
            print("llamada recibida")