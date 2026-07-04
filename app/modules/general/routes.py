from fastapi import APIRouter
from pydantic import BaseModel
from app.services.meta_api_client import send_whatsapp_message

router = APIRouter()

class SendMessageRequest(BaseModel):
    to: str
    message: str

@router.get("/health")
def health():
    return {"status": "ok", "service": "CallsRM"}

@router.post("/messages/send")
async def send_message(payload: SendMessageRequest):
    await send_whatsapp_message(payload.to, payload.message)
    return {"status": "sent", "to": payload.to}