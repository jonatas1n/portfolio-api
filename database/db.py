from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .base import Base
from experiences.models import *
from projects.models import *
from skills.models import *
import os

DATABASE_HOST = os.getenv("DATABASE_HOST", "jonatas1n-desktop")
DATABASE_USER = os.getenv("DATABASE_USER", "root")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
DATABASE_NAME = os.getenv("DATABASE_NAME", "portfolio")

DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?ssl-mode=REQUIRED"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS portfolio"))
    conn.commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_db()
