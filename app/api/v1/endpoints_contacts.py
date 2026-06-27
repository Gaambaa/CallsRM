from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_session
from app.models import Contact

router = APIRouter()

@router.get("/contacts")
async def get_contacts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Contact))
    contacts = result.scalars().all()
    return contacts