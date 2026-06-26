from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Contact

async def get_or_create_contact(session: AsyncSession, phone_number: str, name: str = None):
    # Try to find existing contact
    result = await session.execute(select(Contact).where(Contact.phone_number == phone_number))
    contact = result.scalars().first()
    
    if contact:
        return contact
    
    # Create new contact if not found
    contact = Contact(phone_number=phone_number, name=name)
    session.add(contact)
    await session.commit()
    await session.refresh(contact)
    return contact