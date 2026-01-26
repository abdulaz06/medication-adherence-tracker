from sqlalchemy import text
from app.db.session import engine
from app.models.base import Base

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

def db_check() -> bool:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True