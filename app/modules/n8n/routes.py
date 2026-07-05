from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.services.meta_api_client import send_whatsapp_message
from app.config import settings

router = APIRouter()

class N8nCallbackRequest(BaseModel):
    phone: str
    message: str

@router.post("/n8n/callback")
async def n8n_callback(
    payload: N8nCallbackRequest,
    authorization: str = Header(None)
):
    # Verify that the request comes from our n8n instance
    if not authorization or authorization != f"Bearer {settings.n8n_secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    await send_whatsapp_message(payload.phone, payload.message)
    return {"status": "sent", "to": payload.phone}