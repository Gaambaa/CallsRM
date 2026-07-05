from pydantic import BaseModel
from datetime import datetime

class CallResponse(BaseModel):
    call_id: str
    contact_id: int | None
    from_number: str
    event: str
    direction: str
    status: str
    timestamp: int
    created_at: datetime

    model_config = {"from_attributes": True}