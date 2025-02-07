from sqlalchemy.orm import Session
from .models import Experiences
from database.db import get_db
from fastapi import Depends

def list_experiences(db: Session = Depends(get_db)):
    return db.query(Experiences).all()
