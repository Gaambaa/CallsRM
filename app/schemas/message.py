from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    message_id: str
    contact_id: int | None
    from_number: str
    body: str
    type: str
    timestamp: int
    created_at: datetime

    model_config = {"from_attributes": True}