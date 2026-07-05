from pydantic import BaseModel
from datetime import datetime

class ContactResponse(BaseModel):
    id: int
    phone_number: str
    name: str | None
    created_at: datetime

    model_config = {"from_attributes": True}