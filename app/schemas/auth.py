from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    email: str
    
    model_config = {"from_attributes": True}