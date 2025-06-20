from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ChallanItemBase(BaseModel):
    sno: int
    asset_name: str
    description: str
    quantity: int
    serial_no: str
    returnable: bool = False
    expected_return_date: Optional[date] = None

class ChallanItemCreate(ChallanItemBase):
    pass

class ChallanItem(ChallanItemBase):
    item_id: int
    challan_id: int
    created_at: datetime

    class Config:
        from_attributes = True