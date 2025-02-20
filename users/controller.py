from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database.db import get_db
from users.models import Users


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(name: str, email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_password = pwd_context.hash(password)

    new_user = Users(
        name=name,
        email=email,
        password_hash=hashed_password,
        is_admin=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
