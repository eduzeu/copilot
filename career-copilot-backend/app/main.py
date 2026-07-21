from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import auth, applications, resumes, analysis, coach, dashboard, profile, users
from app.core.config import settings
from app.db.session import engine

app = FastAPI(title="Career Copilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(resumes.router)
app.include_router(analysis.router)
app.include_router(coach.router)
app.include_router(dashboard.router)
app.include_router(users.router)
app.include_router(profile.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/live", tags=["health"])
def liveness():
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
def readiness():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(status_code=503, content={"status": "unavailable", "database": "down"})
    return {"status": "ok", "database": "up"}


@app.exception_handler(SQLAlchemyError)
async def database_error_handler(_: Request, __: SQLAlchemyError):
    return JSONResponse(
        status_code=503,
        content={"detail": "The database is temporarily unavailable. Please try again shortly."},
    )
