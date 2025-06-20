from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_name(db, client_name=client.client_name)
    if db_client:
        raise HTTPException(status_code=400, detail="Client already exists")
    return crud.create_client(db=db, client=client)