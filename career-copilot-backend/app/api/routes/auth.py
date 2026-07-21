from collections import defaultdict, deque
from time import monotonic

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import RegisterRequest, TokenResponse, UserPublic
from app.services.auth import register_user, login_user
from app.schemas.auth import LoginRequest
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"]) 
_login_attempts: dict[str, deque[float]] = defaultdict(deque)


def _enforce_login_rate_limit(key: str) -> None:
    now = monotonic()
    attempts = _login_attempts[key]
    while attempts and now - attempts[0] > 60:
        attempts.popleft()
    if len(attempts) >= 10:
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again in one minute.")

@router.post("/register", response_model=UserPublic, status_code=201)
def register_user_endpoint(request: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(request, db)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    client = request.client.host if request.client else "unknown"
    rate_key = f"{client}:{payload.email.lower()}"
    _enforce_login_rate_limit(rate_key)
    try:
        token = login_user(db, payload.email, payload.password)
    except HTTPException:
        _login_attempts[rate_key].append(monotonic())
        raise
    _login_attempts.pop(rate_key, None)
    response.set_cookie(
        key="career_copilot_session",
        value=token,
        httponly=True,
        secure=settings.env.lower() in {"production", "prod"},
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return TokenResponse(access_token=token, token_type="bearer")


@router.post("/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie("career_copilot_session")
    response.status_code = 204
