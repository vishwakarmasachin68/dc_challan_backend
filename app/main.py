from fastapi import FastAPI
from app.database import engine, Base

# Import models first to register them
from app.models import client, location, project, team_member, challan, challan_item

# Create tables
Base.metadata.create_all(bind=engine)

# Then import routers
from app.api.clients import router as clients_router
from app.api.locations import router as locations_router
from app.api.projects import router as projects_router
from app.api.challans import router as challans_router

app = FastAPI()

app.include_router(clients_router)
app.include_router(locations_router)
app.include_router(projects_router)
app.include_router(challans_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Challan Management System API"}