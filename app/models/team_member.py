from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class TeamMember(Base):
    __tablename__ = "team_members"

    member_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False)
    member_name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())