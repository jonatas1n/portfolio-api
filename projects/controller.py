from sqlalchemy.orm import Session
from .models import Projects
from database.db import get_db
from fastapi import Depends

def list_projects(db: Session = Depends(get_db), technologies: list[str] = []):
    if technologies:
        return db.query(Projects).filter(
            Projects.technologies.overlap(technologies)
        ).all()
    return db.query(Projects).all()

def list_projects_technologies(db: Session = Depends(get_db)):
    result = db.query(Projects.technologies).all()

    if not result:
        return []

    parsed_technologies = []

    for item in result:
        item_list = item[0]
        parsed_technologies += item_list

    parsed_technologies = list(set(parsed_technologies))
    return parsed_technologies
