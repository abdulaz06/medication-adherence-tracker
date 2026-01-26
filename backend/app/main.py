from fastapi import FastAPI
from app.db import create_tables, db_check
from app.routers import users, items

app = FastAPI(title="Medication Adherence Tracker API")

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/db-check")
def db_check_route():
    return {"ok": db_check()}

app.include_router(users.router)
app.include_router(items.router)