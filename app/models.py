from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Contact(SQLModel, table=True):
    """
    Represents a WhatsApp contact auto-created on first interaction.

    Payload example (from contacts[0]):
    {
        "profile": {"name": "Franco Prieto"},
        "wa_id": "591XXXXXXXXX"
    }
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CallSession(SQLModel, table=True):
    """
    Represents a WhatsApp call received via Meta Calling API webhook.
    Chatwoot Community Edition receives this payload but silently ignores it.

    Payload example (from calls[0]):
    {
        "id": "wacid.xxx",
        "from": "591XXXXXXXXX",
        "to": "591XXXXXXXXX",
        "event": "connect",
        "timestamp": "1780362791",
        "direction": "USER_INITIATED",
        "status": "COMPLETED"
    }
    """
    call_id: str = Field(primary_key=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    from_number: str
    event: str
    timestamp: int
    direction: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    """
    Represents a WhatsApp text message received via Meta webhook.

    Payload example (from messages[0]):
    {
        "id": "wamid.xxx",
        "from": "591XXXXXXXXX",
        "timestamp": "1782046964",
        "text": {"body": "hola"},
        "type": "text"
    }
    """
    message_id: str = Field(primary_key=True)
    contact_id: Optional[int] = Field(default=None, foreign_key="contact.id")
    from_number: str
    body: str
    type: str
    timestamp: int
    created_at: datetime = Field(default_factory=datetime.utcnow)