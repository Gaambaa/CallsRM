from fastapi import APIRouter, BackgroundTasks, Request
from app.database import async_session
from app.services.contact_service import get_or_create_contact
from app.models import Contact, CallSession, Message

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
            
            msg_data = value["messages"][0]
            message = Message(
                message_id=msg_data["id"],
                contact_id=contact.id,
                from_number=msg_data["from"],
                body=msg_data["text"]["body"],
                type=msg_data["type"],
                timestamp=int(msg_data["timestamp"])
            )
            session.add(message)
            await session.commit()
            print(f"mensaje guardado: {message.message_id}")

        elif "calls" in value:
            call_data = value["calls"][0]
            phone_number = call_data["from"]
            #None for name since calls don't provide a name
            contact = await get_or_create_contact(session, phone_number, None) 
            
            call = CallSession(
                call_id=call_data["id"],
                contact_id=contact.id,
                from_number=call_data["from"],
                event=call_data["event"],
                direction=call_data["direction"],
                status=call_data.get("status", "ringing"),
                timestamp=int(call_data["timestamp"])
            )
            session.add(call)
            await session.commit()
            print(f"llamada guardada: {call.call_id}")
            