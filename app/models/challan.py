from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Challan(Base):
    __tablename__ = "challans"

    challan_id = Column(Integer, primary_key=True, index=True)
    dc_number = Column(String(50), unique=True, nullable=False)
    date = Column(Date, nullable=False)
    preparer_name = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.location_id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    has_po = Column(Boolean, default=False)
    po_number = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())