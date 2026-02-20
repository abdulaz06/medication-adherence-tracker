from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import create_tables, db_check
from app.routers import auth, dose_logs, items, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    yield
    # Shutdown (nothing needed for now)


app = FastAPI(
    title="Medication Adherence Tracker API",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------- CORS (allow Flutter dev & any frontend) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Routers ----------
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(dose_logs.router)


# ---------- Utility endpoints ----------
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/db-check", tags=["system"])
def db_check_route():
    return {"ok": db_check()}
