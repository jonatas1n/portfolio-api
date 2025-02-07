from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .controller import list_experiences
from database.db import get_db

router = APIRouter(prefix="/experiences", tags=["experiences"])

@router.get("/")
def list(db: Session = Depends(get_db)):
    return list_experiences(db)
