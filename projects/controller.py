from sqlalchemy.orm import Session
from .models import Projects
from database.db import get_db
from fastapi import Depends

def list_projects(db: Session = Depends(get_db)):
    return db.query(Projects).all()
