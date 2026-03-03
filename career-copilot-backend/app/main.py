from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.applications import router as applications_router
from app.api.routes.resumes import router as resumes_router
app = FastAPI(tittle=settings.app_name, debug=settings.debug)
from app.api.routes.auth import router as auth_router
from app.api.routes.analysis import router as analysis_router


app.include_router(analysis_router)
app.include_router(applications_router)
app.include_router(resumes_router)
app.include_router(auth_router)

@app.get("/health")
def heath_check():
    return {"status": "ok"}


