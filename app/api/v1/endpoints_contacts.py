from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_session
from app.models import Contact, Message, CallSession

router = APIRouter()

@router.get("/contacts")
async def get_contacts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Contact))
    contacts = result.scalars().all()
    return contacts

@router.get("/contacts/{contact_id}/messages")
async def get_contact_messages(contact_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Message).where(Message.contact_id == contact_id)
    )
    messages = result.scalars().all()
    return messages

@router.get("/contacts/{contact_id}/calls")
async def get_contact_calls(contact_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(CallSession).where(CallSession.contact_id == contact_id)
    )
    calls = result.scalars().all()
    return calls

@router.get("/calls")
async def get_all_calls(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(CallSession))
    calls = result.scalars().all()
    return calls