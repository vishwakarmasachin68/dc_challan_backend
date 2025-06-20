from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate

def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.client_id == client_id).first()

def get_client_by_name(db: Session, client_name: str):
    return db.query(Client).filter(Client.client_name == client_name).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: ClientCreate):
    db_client = Client(client_name=client.client_name)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client