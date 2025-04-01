import os
import dotenv
from typing import Annotated
from fastapi import Depends
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = _sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

DbSession = Annotated[_orm.Session, Depends(get_db)]