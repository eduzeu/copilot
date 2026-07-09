from datetime import date, datetime
from pydantic import BaseModel, HttpUrl
from datetime import date 
from app.utils.enums import ApplicationStatus


class ApplicationCreateRequest(BaseModel):
    company: str
    role_title: str
    date_applied: date
    status: ApplicationStatus
    location: str

class ApplicationUpdateRequest(BaseModel):
    company: str | None = None
    role_title: str | None = None
    date_applied: date | None = None
    status: ApplicationStatus | None = None 
  
class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company: str
    role_title: str
    date_applied: date
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True