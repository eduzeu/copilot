from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, applications, resumes, analysis, coach, dashboard, profile, users
from app.core.config import settings

app = FastAPI(title="Career Copilot API")

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
