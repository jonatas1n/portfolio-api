from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db

from .controller import create_user, RegisterUserSchema

router = APIRouter(prefix="/auth", tags=["Users"])


@router.post("/register")
def register_user(user: RegisterUserSchema, db: Session = Depends(get_db)):
    create_user(user, db)
    return {"message": "Usuário registrado com sucesso!"}
