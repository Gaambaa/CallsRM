from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.modules.contacts.service import ContactService

class ContactController:
    @staticmethod
    async def get_all_contacts(session: AsyncSession):
        contacts = await ContactService.get_all_contacts(session)
        return contacts

    @staticmethod
    async def get_contact_messages(session: AsyncSession, contact_id: int):
        messages = await ContactService.get_contact_messages(session, contact_id)
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found for this contact")
        return messages

    @staticmethod
    async def get_contact_calls(session: AsyncSession, contact_id: int):
        calls = await ContactService.get_contact_calls(session, contact_id)
        if not calls:
            raise HTTPException(status_code=404, detail="No calls found for this contact")
        return calls

    @staticmethod
    async def get_all_calls(session: AsyncSession):
        calls = await ContactService.get_all_calls(session)
        return calls