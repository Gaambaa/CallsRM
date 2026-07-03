from fastapi import APIRouter
from pydantic import BaseModel
from app.services.meta_api_client import send_whatsapp_message

router = APIRouter()

class N8nCallbackRequest(BaseModel):
    phone: str
    message: str

@router.post("/n8n/callback")
async def n8n_callback(payload: N8nCallbackRequest):
    # n8n sends us a phone and message, we forward it to WhatsApp
    await send_whatsapp_message(payload.phone, payload.message)
    return {"status": "sent", "to": payload.phone}