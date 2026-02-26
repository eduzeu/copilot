from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.applications import router as applications_router
app = FastAPI(tittle=settings.app_name, debug=settings.debug)
from app.api.routes.auth import router as auth_router


app.include_router(applications_router)
app.include_router(auth_router)

@app.get("/health")
def heath_check():
    return {"status": "ok"}


