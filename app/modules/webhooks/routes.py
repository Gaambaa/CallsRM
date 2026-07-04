from fastapi import APIRouter, BackgroundTasks, Request
from app.database import async_session
from app.modules.webhooks.service import WebhookService

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
    try:
        value = payload["entry"][0]["changes"][0]["value"]
    except (KeyError, IndexError):
        return

    async with async_session() as session:
        if "messages" in value:
            await WebhookService.process_message(session, value)
        elif "calls" in value:
            await WebhookService.process_call(session, value)