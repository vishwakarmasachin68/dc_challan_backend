from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_name(db, location_name=location.location_name)
    if db_location:
        raise HTTPException(status_code=400, detail="Location already exists")
    return crud.create_location(db=db, location=location)

@router.get("/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations

@router.get("/{location_id}", response_model=schemas.Location)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.put("/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, location_name: str, db: Session = Depends(get_db)):
    db_location = crud.update_location(db, location_id=location_id, location_name=location_name)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.delete("/{location_id}", response_model=schemas.Location)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.delete_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location