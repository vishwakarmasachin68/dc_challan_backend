from fastapi import FastAPI
from app.database import engine
from app.models import client, location, project, team_member, challan, challan_item
from app.api.clients import router as clients_router
from app.api.locations import router as locations_router
from app.api.projects import router as projects_router
from app.api.challans import router as challans_router

# Create all database tables
client.Base.metadata.create_all(bind=engine)
location.Base.metadata.create_all(bind=engine)
project.Base.metadata.create_all(bind=engine)
team_member.Base.metadata.create_all(bind=engine)
challan.Base.metadata.create_all(bind=engine)
challan_item.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include all routers
app.include_router(clients_router)
app.include_router(locations_router)
app.include_router(projects_router)
app.include_router(challans_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Challan Management System API"}