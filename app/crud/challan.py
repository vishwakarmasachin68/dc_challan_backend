from sqlalchemy.orm import Session
from app.models.challan import Challan
from app.models.challan_item import ChallanItem
from app.schemas.challan import ChallanCreate
from app.schemas.challan_item import ChallanItemCreate

def get_challan(db: Session, challan_id: int):
    return db.query(Challan).filter(Challan.challan_id == challan_id).first()

def get_challan_by_dc_number(db: Session, dc_number: str):
    return db.query(Challan).filter(Challan.dc_number == dc_number).first()

def get_challans(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Challan).offset(skip).limit(limit).all()

def create_challan(db: Session, challan: ChallanCreate):
    db_challan = Challan(
        dc_number=challan.dc_number,
        date=challan.date,
        preparer_name=challan.preparer_name,
        client_id=challan.client_id,
        location_id=challan.location_id,
        project_id=challan.project_id,
        has_po=challan.has_po,
        po_number=challan.po_number
    )
    db.add(db_challan)
    db.commit()
    db.refresh(db_challan)
    
    # Add challan items
    for item in challan.items:
        db_item = ChallanItem(
            challan_id=db_challan.challan_id,
            sno=item.sno,
            asset_name=item.asset_name,
            description=item.description,
            quantity=item.quantity,
            serial_no=item.serial_no,
            returnable=item.returnable,
            expected_return_date=item.expected_return_date
        )
        db.add(db_item)
    db.commit()
    
    return db_challan

def update_challan(db: Session, challan_id: int, challan: ChallanCreate):
    db_challan = get_challan(db, challan_id)
    if db_challan:
        db_challan.dc_number = challan.dc_number
        db_challan.date = challan.date
        db_challan.preparer_name = challan.preparer_name
        db_challan.client_id = challan.client_id
        db_challan.location_id = challan.location_id
        db_challan.project_id = challan.project_id
        db_challan.has_po = challan.has_po
        db_challan.po_number = challan.po_number
        
        # Update items
        # First, delete existing items
        db.query(ChallanItem).filter(ChallanItem.challan_id == challan_id).delete()
        # Then add new items
        for item in challan.items:
            db_item = ChallanItem(
                challan_id=challan_id,
                sno=item.sno,
                asset_name=item.asset_name,
                description=item.description,
                quantity=item.quantity,
                serial_no=item.serial_no,
                returnable=item.returnable,
                expected_return_date=item.expected_return_date
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_challan)
    return db_challan

def delete_challan(db: Session, challan_id: int):
    db_challan = get_challan(db, challan_id)
    if db_challan:
        db.delete(db_challan)
        db.commit()
    return db_challan

def get_challan_items(db: Session, challan_id: int):
    return db.query(ChallanItem).filter(ChallanItem.challan_id == challan_id).all()