from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller import list_projects
from database.db import get_db

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/")
def list(db: Session = Depends(get_db)):
    return list_projects(db)
