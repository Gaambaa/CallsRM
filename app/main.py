from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.models import Contact, CallSession, Message
from app.api.v1.endpoints_webhooks import router as webhooks_router
from app.api.v1.endpoints_contacts import router as contacts_router
from app.api.v1.endpoints_general import router as general_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(webhooks_router)
app.include_router(contacts_router)
app.include_router(general_router)

@app.get("/")
def root():
    return {"message": "CallsRM is running"}