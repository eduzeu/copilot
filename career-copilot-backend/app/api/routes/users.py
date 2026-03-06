from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.user_management import get_user, update_profile, delete_user
from app.api.deps import get_db

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/me/{user_id}")

def get_current_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)

@router.put("/me/{user_id}")
def update_profile_endpoint(user_id: int, body: dict, db: Session = Depends(get_db)):
    updated_user = update_profile(db, user_id, body)
    return updated_user 

@router.delete("/me/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return {"message": "User deleted successfully"} 