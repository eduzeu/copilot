from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import RegisterRequest, TokenResponse, UserPublic
from app.services.auth import register_user, login_user
from app.schemas.auth import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"]) 

@router.post("/register", response_model=UserPublic, status_code=201)
def register_user_endpoint(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    token = login_user(db, request.email, request.password)
    return TokenResponse(access_token=token, token_type="bearer")
