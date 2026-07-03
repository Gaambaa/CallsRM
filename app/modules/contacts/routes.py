from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.modules.contacts.controller import ContactController

router = APIRouter()

@router.get("/contacts")
async def get_contacts(session: AsyncSession = Depends(get_session)):
    return await ContactController.get_all_contacts(session)

@router.get("/contacts/{contact_id}/messages")
async def get_contact_messages(contact_id: int, session: AsyncSession = Depends(get_session)):
    return await ContactController.get_contact_messages(session, contact_id)

@router.get("/contacts/{contact_id}/calls")
async def get_contact_calls(contact_id: int, session: AsyncSession = Depends(get_session)):
    return await ContactController.get_contact_calls(session, contact_id)

@router.get("/calls")
async def get_all_calls(session: AsyncSession = Depends(get_session)):
    return await ContactController.get_all_calls(session)