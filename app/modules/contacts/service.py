from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Contact, Message, CallSession

class ContactService:
    @staticmethod
    async def get_all_contacts(session: AsyncSession):
        result = await session.execute(select(Contact))
        return result.scalars().all()

    @staticmethod
    async def get_contact_messages(session: AsyncSession, contact_id: int):
        result = await session.execute(
            select(Message).where(Message.contact_id == contact_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_contact_calls(session: AsyncSession, contact_id: int):
        result = await session.execute(
            select(CallSession).where(CallSession.contact_id == contact_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_all_calls(session: AsyncSession):
        result = await session.execute(select(CallSession))
        return result.scalars().all()