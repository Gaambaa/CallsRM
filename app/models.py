from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)