from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

class ChallanItem(Base):
    __tablename__ = "challan_items"

    item_id = Column(Integer, primary_key=True, index=True)
    challan_id = Column(Integer, ForeignKey("challans.challan_id", ondelete="CASCADE"), nullable=False)
    sno = Column(Integer, nullable=False)
    asset_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    serial_no = Column(String(100), nullable=False)
    returnable = Column(Boolean, default=False)
    expected_return_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())