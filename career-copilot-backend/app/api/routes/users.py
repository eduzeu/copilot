from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.services.user_management import update_profile, delete_user
from app.api.deps import get_db, get_current_user
from app.schemas.user import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_endpoint(current_user=Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_profile_endpoint(body: UserUpdateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_profile(db, current_user.id, body)

@router.delete("/me", status_code=204)
def delete_user_endpoint(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    delete_user(db, current_user.id)
    return Response(status_code=204)
