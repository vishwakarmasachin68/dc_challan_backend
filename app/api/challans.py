from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/challans", tags=["challans"])

@router.post("/", response_model=schemas.Challan)
def create_challan(challan: schemas.ChallanCreate, db: Session = Depends(get_db)):
    # Check if DC number already exists
    db_challan = crud.get_challan_by_dc_number(db, dc_number=challan.dc_number)
    if db_challan:
        raise HTTPException(status_code=400, detail="DC number already exists")
    
    # Check if client exists
    db_client = crud.get_client(db, client_id=challan.client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if location exists
    db_location = crud.get_location(db, location_id=challan.location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # Check if project exists if provided
    if challan.project_id:
        db_project = crud.get_project(db, project_id=challan.project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
    
    return crud.create_challan(db=db, challan=challan)

@router.get("/", response_model=List[schemas.Challan])
def read_challans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    challans = crud.get_challans(db, skip=skip, limit=limit)
    return challans

@router.get("/{challan_id}", response_model=schemas.ChallanWithItems)
def read_challan(challan_id: int, db: Session = Depends(get_db)):
    db_challan = crud.get_challan(db, challan_id=challan_id)
    if db_challan is None:
        raise HTTPException(status_code=404, detail="Challan not found")
    
    # Get items for this challan
    items = crud.get_challan_items(db, challan_id=challan_id)
    
    # Combine challan and items data
    challan_data = schemas.ChallanWithItems(**db_challan.__dict__)
    challan_data.items = items
    
    return challan_data

@router.put("/{challan_id}", response_model=schemas.Challan)
def update_challan(challan_id: int, challan: schemas.ChallanCreate, db: Session = Depends(get_db)):
    db_challan = crud.update_challan(db, challan_id=challan_id, challan=challan)
    if db_challan is None:
        raise HTTPException(status_code=404, detail="Challan not found")
    return db_challan

@router.delete("/{challan_id}", response_model=schemas.Challan)
def delete_challan(challan_id: int, db: Session = Depends(get_db)):
    db_challan = crud.delete_challan(db, challan_id=challan_id)
    if db_challan is None:
        raise HTTPException(status_code=404, detail="Challan not found")
    return db_challan

@router.get("/{challan_id}/items", response_model=List[schemas.ChallanItem])
def read_challan_items(challan_id: int, db: Session = Depends(get_db)):
    items = crud.get_challan_items(db, challan_id=challan_id)
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this challan")
    return items