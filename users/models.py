from database.base import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
