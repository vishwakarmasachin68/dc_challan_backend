from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectBase(BaseModel):
    project_name: str
    client_id: int
    location_id: int
    has_po: bool = False
    po_number: Optional[str] = None
    field_supervisor: str
    project_details: Optional[str] = None

class ProjectCreate(ProjectBase):
    team_members: List[str]

class Project(ProjectBase):
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True