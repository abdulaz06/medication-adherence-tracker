from fastapi import FastAPI
from app.db import db_check, create_tables

app = FastAPI(title="Medication Adherence Tracker API")

@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check_route():
    db_check()
    return {"db": "ok"}