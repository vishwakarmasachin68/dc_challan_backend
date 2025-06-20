from pydantic import BaseModel
from datetime import datetime

class TeamMemberBase(BaseModel):
    member_name: str

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMember(TeamMemberBase):
    member_id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True