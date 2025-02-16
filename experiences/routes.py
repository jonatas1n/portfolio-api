from typing import Annotated
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .controller import list_experiences, list_experiences_technologies
from database.db import get_db

router = APIRouter(prefix="/experiences", tags=["experiences"])

class ExperiencesParams(BaseModel):
    technologies: list[str] = []

@router.get("/")
def list(filter_query: Annotated[(ExperiencesParams, Query())], db: Session = Depends(get_db)):
    return list_experiences(db, filter_query.technologies)


@router.get("/technologies")
def technologies(db: Session = Depends(get_db)):
    technologies_list = list_experiences_technologies(db)
    return {"technologies": technologies_list}
