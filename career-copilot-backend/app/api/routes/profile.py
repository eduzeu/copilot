from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.career_profile import CareerProfileOut, CareerProfileUpdate
from app.services.career_profile_service import get_or_create_profile, profile_response, update_profile

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/", response_model=CareerProfileOut)
def get_profile(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return profile_response(get_or_create_profile(db, user.id))


@router.put("/", response_model=CareerProfileOut)
def save_profile(req: CareerProfileUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return profile_response(update_profile(db, user.id, req))
