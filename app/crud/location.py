from sqlalchemy.orm import Session
from app.models.location import Location
from app.schemas.location import LocationCreate
from fastapi import APIRouter
router = APIRouter(prefix="/clients", tags=["clients"])

def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.location_id == location_id).first()

def get_location_by_name(db: Session, location_name: str):
    return db.query(Location).filter(Location.location_name == location_name).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()

def create_location(db: Session, location: LocationCreate):
    db_location = Location(location_name=location.location_name)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def update_location(db: Session, location_id: int, location_name: str):
    db_location = get_location(db, location_id)
    if db_location:
        db_location.location_name = location_name
        db.commit()
        db.refresh(db_location)
    return db_location

def delete_location(db: Session, location_id: int):
    db_location = get_location(db, location_id)
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location