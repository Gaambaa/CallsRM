from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.database import get_session
from app.modules.auth.controller import AuthController
from app.schemas.auth import TokenResponse, UserResponse

router = APIRouter()

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/register", response_model=UserResponse)
async def register(payload: AuthRequest, session: AsyncSession = Depends(get_session)):
    return await AuthController.register(session, payload.email, payload.password)

@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: AuthRequest, session: AsyncSession = Depends(get_session)):
    return await AuthController.login(session, payload.email, payload.password)