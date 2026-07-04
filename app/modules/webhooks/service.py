from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models import Contact, CallSession, Message
from app.services.contact_service import get_or_create_contact
from app.services.n8n_client import forward_to_n8n
from sqlalchemy import select

class WebhookService:
    @staticmethod
    async def process_message(session: AsyncSession, value: dict):
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

        try:
            session.add(message)
            await session.commit()
            print(f"mensaje guardado: {message.message_id}")
            await forward_to_n8n("message", {
                "contact_id": contact.id,
                "phone_number": contact.phone_number,
                "body": message.body,
                "timestamp": message.timestamp
            })
        except IntegrityError:
            await session.rollback()
            print(f"mensaje duplicado ignorado: {message.message_id}")

    @staticmethod
    async def process_call(session: AsyncSession, value: dict):
        call_data = value["calls"][0]
        phone_number = call_data["from"]
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

        try:
            session.add(call)
            await session.commit()
            print(f"llamada guardada: {call.call_id}")
            await forward_to_n8n("call", {
                "contact_id": contact.id,
                "phone_number": call.from_number,
                "event": call.event,
                "status": call.status,
                "timestamp": call.timestamp
            })
        except IntegrityError:
            await session.rollback()
            print(f"llamada duplicada ignorada: {call.call_id}")