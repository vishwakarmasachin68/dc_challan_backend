from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class ChallanBase(BaseModel):
    dc_number: str
    date: date
    preparer_name: str
    client_id: int
    location_id: int
    project_id: Optional[int] = None
    has_po: bool = False
    po_number: Optional[str] = None

class ChallanCreate(ChallanBase):
    items: List['ChallanItemCreate']

class Challan(ChallanBase):
    challan_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChallanWithItems(Challan):
    items: List['ChallanItem']

class ChallanList(BaseModel):
    challans: List[Challan]