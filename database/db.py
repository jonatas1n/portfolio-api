from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .base import Base
from experiences.models import *
from projects.models import *
from skills.models import *

engine = create_engine(
    "mysql+mysqlconnector://root:password@jonatas1n-desktop/portfolio"
)

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