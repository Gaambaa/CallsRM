from fastapi import APIRouter, BackgroundTasks, Request

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
    value = payload["entry"][0]["changes"][0]["value"]
    
    if "messages" in value:
        print("mensaje recibido")
    elif "calls" in value:
        print("llamada recibida")