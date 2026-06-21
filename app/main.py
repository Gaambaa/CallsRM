from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.models import Contact, CallSession, Message

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "CallsRM is running"}