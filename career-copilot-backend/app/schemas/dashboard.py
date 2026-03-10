from pydantic import BaseModel, HttpUrl 



class DashboardData:
    def __init__(self, user_id: int, data: dict):
        self.user_id = user_id
        self.data = data

class DashboardResponse(BaseModel):
    user_id: int
    total_applications: int
    pending_applications: int
    interviewing: int
    offers: int
    interview_rate: float
    offer_rate: float

    class Config:
        orm_mode = True
    

class DashboardUpdateRequest(BaseModel):
    total_applications: int | None = None
    pending_applications: int | None = None
    interviewing: int | None = None
    offers: int | None = None
    interview_rate: float | None = None
    offer_rate: float | None = None