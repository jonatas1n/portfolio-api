from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from .models import Experiences
from database.db import get_db
from fastapi import Depends
from datetime import datetime
import json

def convert_date(date: datetime):
    return date.strftime("%m/%Y")

def list_experiences(db: Session, technologies: list = None):
    experiences_list = db.query(Experiences).order_by(Experiences.start_date.desc())
    
    if technologies:
        conditions = [
            func.json_contains(Experiences.technologies, func.json_array(tech))
            for tech in technologies
        ]

        experiences_list = experiences_list.filter(or_(*conditions))
    
    experiences_list = experiences_list.all()
    
    for i, experience in enumerate(experiences_list):
        start_date = experience.start_date
        start_date = convert_date(start_date)
        
        end_date = experience.end_date
        end_date = convert_date(end_date) if end_date else "Actually"
        
        experience.start_date = start_date
        experience.end_date = end_date
        
        experiences_list[i] = experience

    return experiences_list


def list_experiences_technologies(db: Session = Depends(get_db)):
    result = db.query(Experiences.technologies).all()

    if not result:
        return []

    parsed_technologies = []

    for item in result:
        item_list = item[0]
        if isinstance(item_list, str):
            item_list = json.loads(item_list)
        parsed_technologies += item_list

    parsed_technologies = list(set(parsed_technologies))
    parsed_technologies.sort()
    return parsed_technologies
