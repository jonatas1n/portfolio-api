from sqlalchemy.orm import Session
from .models import Skills
from database.db import get_db
from fastapi import Depends


def list_skills(db: Session = Depends(get_db)):
    skills = db.query(Skills).all()
    grouped_skills = {}
    for skill in skills:
        if not skill.skill_type:
            continue
        grouped_skills.setdefault(skill.skill_type, []).append(skill)
    return grouped_skills
