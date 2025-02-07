from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller import list_skills
from database.db import get_db

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("/")
def list(db: Session = Depends(get_db)):
    return list_skills(db)
