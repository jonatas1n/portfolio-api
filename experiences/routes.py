from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller import list_experiences, list_experiences_technologies
from database.db import get_db

router = APIRouter(prefix="/experiences", tags=["experiences"])


@router.get("/")
def list(db: Session = Depends(get_db), technologies: list[str] = []):
    return list_experiences(db, technologies)


@router.get("/technologies")
def technologies(db: Session = Depends(get_db)):
    technologies_list = list_experiences_technologies(db)
    return {"technologies": technologies_list}
