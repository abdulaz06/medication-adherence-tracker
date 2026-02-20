from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

# TODO: move to settings/env later
DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # sqlite only
)


# ---------- SQLite FK enforcement ----------
# SQLite ignores foreign keys by default; this fixes that.
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    import sqlite3

    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()