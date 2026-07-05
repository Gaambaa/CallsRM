from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.models import Contact, CallSession, Message
from app.modules.webhooks.routes import router as webhooks_router
from app.modules.general.routes import router as general_router
from app.modules.n8n.routes import router as n8n_router
from app.modules.contacts.routes import router as contacts_module_router
from app.modules.auth.routes import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(webhooks_router)
app.include_router(general_router)
app.include_router(n8n_router)
app.include_router(contacts_module_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "CallsRM is running"}