from sqlalchemy.orm import Session
from .models import Skills
from database.db import get_db
from fastapi import Depends


def list_skills(db: Session = Depends(get_db)):
    return db.query(Skills).all()
