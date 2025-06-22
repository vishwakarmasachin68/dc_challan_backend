from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text  # Add this import
from fastapi import HTTPException
from app.models.client import Client
from app.schemas.client import ClientCreate

def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.client_id == client_id).first()

def get_client_by_name(db: Session, client_name: str):
    return db.query(Client).filter(Client.client_name == client_name).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: ClientCreate):
    # Check if client exists by name
    if get_client_by_name(db, client_name=client.client_name):
        raise HTTPException(status_code=400, detail="Client name already exists")
    
    db_client = Client(client_name=client.client_name)
    db.add(db_client)
    
    try:
        db.commit()
        db.refresh(db_client)
        return db_client
    except IntegrityError as e:
        db.rollback()
        if "duplicate key" in str(e):
            # Reset sequence using text() wrapper
            db.execute(text("SELECT setval('clients_client_id_seq', (SELECT MAX(client_id) FROM clients)"))
            db.commit()
            return create_client(db, client)  # Retry
        raise HTTPException(status_code=400, detail=str(e))