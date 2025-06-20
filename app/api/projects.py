from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # Check if client exists
    db_client = crud.get_client(db, client_id=project.client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if location exists
    db_location = crud.get_location(db, location_id=project.location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    return crud.create_project(db=db, project=project)

@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{project_id}", response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.get("/{project_id}/team-members", response_model=List[schemas.TeamMember])
def read_project_team_members(project_id: int, db: Session = Depends(get_db)):
    members = crud.get_project_team_members(db, project_id=project_id)
    if not members:
        raise HTTPException(status_code=404, detail="No team members found for this project")
    return members