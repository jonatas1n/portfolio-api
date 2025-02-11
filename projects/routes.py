from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller import list_projects, list_projects_technologies
from database.db import get_db

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def list(db: Session = Depends(get_db), technologies: list[str] = []):
    return list_projects(db, technologies)


@router.get("/technologies")
def technologies(db: Session = Depends(get_db)):
    technologies_list = list_projects_technologies(db)
    return {"technologies": technologies_list}
