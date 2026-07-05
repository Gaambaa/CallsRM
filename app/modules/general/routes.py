from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.meta_api_client import send_whatsapp_message
from app.core.security import get_current_user

router = APIRouter()

class SendMessageRequest(BaseModel):
    to: str
    message: str

@router.get("/health")
def health():
    return {"status": "ok", "service": "CallsRM"}

@router.post("/messages/send")
async def send_message(
    payload: SendMessageRequest,
    current_user: str = Depends(get_current_user)
):
    await send_whatsapp_message(payload.to, payload.message)
    return {"status": "sent", "to": payload.to}