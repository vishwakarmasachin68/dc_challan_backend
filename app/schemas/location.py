from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LocationBase(BaseModel):
    location_name: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    location_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True