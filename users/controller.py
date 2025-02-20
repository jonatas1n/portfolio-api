from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from database.db import get_db
from users.models import Users


class RegisterUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user: RegisterUserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = Users(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    