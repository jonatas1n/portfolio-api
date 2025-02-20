from sqlalchemy import create_engine, text
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import ssl

from .base import Base
import os

DATABASE_HOST = os.getenv("DATABASE_HOST", "")
DATABASE_USER = os.getenv("DATABASE_USER", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")
DATABASE_PORT = os.getenv("DATABASE_PORT", "16604")
CA_CERTIFICATE = os.getenv("CA_CERTIFICATE", "").replace("  ", "\n")


DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cadata=CA_CERTIFICATE)

engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": ssl_context}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))
    conn.commit()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    import experiences.models
    import projects.models
    import skills.models
    import users.models

    inspector = reflection.Inspector.from_engine(engine)

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            for table_name in Base.metadata.tables:
                columns_in_db = {col['name'] for col in inspector.get_columns(table_name)}
                columns_in_model = {col.name for col in Base.metadata.tables[table_name].columns}
                missing_columns = columns_in_model - columns_in_db

                if missing_columns:
                    print(f"Table '{table_name}' is missing columns: {missing_columns}")
                    
                    for column in missing_columns:
                        column_obj = Base.metadata.tables[table_name].columns[column]
                        column_type = column_obj.type.compile(engine.dialect)  # Compilar tipo corretamente

                        alter_stmt = text(f"ALTER TABLE {table_name} ADD COLUMN {column} {column_type}")
                        conn.execute(alter_stmt)

            trans.commit()
        except SQLAlchemyError as e:
            trans.rollback()
            print(f"Error updating database schema: {e}")

    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_db()
