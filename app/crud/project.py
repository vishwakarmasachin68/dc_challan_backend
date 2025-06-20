from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.team_member import TeamMember
from app.schemas.project import ProjectCreate
from app.schemas.team_member import TeamMemberCreate
from fastapi import APIRouter
router = APIRouter(prefix="/clients", tags=["clients"])

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.project_id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: ProjectCreate):
    db_project = Project(
        project_name=project.project_name,
        client_id=project.client_id,
        location_id=project.location_id,
        has_po=project.has_po,
        po_number=project.po_number,
        field_supervisor=project.field_supervisor,
        project_details=project.project_details
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Add team members
    for member_name in project.team_members:
        db_member = TeamMember(
            project_id=db_project.project_id,
            member_name=member_name
        )
        db.add(db_member)
    db.commit()
    
    return db_project

def update_project(db: Session, project_id: int, project: ProjectCreate):
    db_project = get_project(db, project_id)
    if db_project:
        db_project.project_name = project.project_name
        db_project.client_id = project.client_id
        db_project.location_id = project.location_id
        db_project.has_po = project.has_po
        db_project.po_number = project.po_number
        db_project.field_supervisor = project.field_supervisor
        db_project.project_details = project.project_details
        
        # Update team members
        # First, delete existing members
        db.query(TeamMember).filter(TeamMember.project_id == project_id).delete()
        # Then add new members
        for member_name in project.team_members:
            db_member = TeamMember(
                project_id=project_id,
                member_name=member_name
            )
            db.add(db_member)
        
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

def get_project_team_members(db: Session, project_id: int):
    return db.query(TeamMember).filter(TeamMember.project_id == project_id).all()