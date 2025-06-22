from pydantic import BaseModel
from datetime import datetime

class ClientBase(BaseModel):
    client_name: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    client_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True