from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.applications import router as applications_router
app = FastAPI(tittle=settings.app_name, debug=settings.debug)
app.include_router(applications_router)

@app.get("/health")
def heath_check():
    return {"status": "ok"}



