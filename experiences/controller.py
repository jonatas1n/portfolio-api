from sqlalchemy.orm import Session
from .models import Experiences
from database.db import get_db
from fastapi import Depends
import json

def list_experiences(db: Session = Depends(get_db), technologies: list[str] = []):
    if technologies:
        return db.query(Experiences).filter(
            Experiences.technologies.overlap(technologies)
        ).all()
    return db.query(Experiences).all()

def list_experiences_technologies(db: Session = Depends(get_db)):
    result = db.query(Experiences.technologies).all()

    if not result:
        return []
    
    parsed_technologies = []

    for item in result:
        item_list = json.loads(item[0])
        print(type(item_list))
        parsed_technologies += item_list

    parsed_technologies = list(set(parsed_technologies))
    return parsed_technologies
