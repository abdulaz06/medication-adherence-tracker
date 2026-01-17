import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.user import User  # noqa: F401
from app.models.item import Item  # noqa: F401
from app.models.dose_log import DoseLog  # noqa: F401

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL missing. Check backend/.env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

def db_check() -> None:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()