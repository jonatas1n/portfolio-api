from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .base import Base
from experiences.models import *
from projects.models import *
from skills.models import *
import os

DATABASE_HOST = os.getenv("DATABASE_HOST", "")
DATABASE_USER = os.getenv("DATABASE_USER", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")
DATABASE_PORT = os.getenv("DATABASE_PORT", "16604")
CA_CERTIFICATE = os.getenv("CA_CERTIFICATE")

DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {"ca": CA_CERTIFICATE}}
)

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))
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
