from uuid import UUID
from pydantic import BaseModel

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayloadSchema(BaseModel):
    sub: UUID = None
    exp: int = None