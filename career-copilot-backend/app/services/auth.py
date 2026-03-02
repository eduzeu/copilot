from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.core.security import create_access_token, verify_password, hash_password
from fastapi import HTTPException
from app.schemas.auth import RegisterRequest, TokenResponse, UserPublic

def register_user(request: RegisterRequest, db: Session) -> User: 
  check_user = db.query(User).filter(User.email == request.email).first()
  if check_user:
    raise HTTPException(status_code=400, detail="Email already registered")
   
  print("Hashing password:", request.password)
  new_user = User(email=request.email, hashed_password=hash_password(request.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def login_user(db: Session, email: str, password: str) -> User: 
  user = db.query(User).filter(User.email == email).first() 
  check_password = verify_password(password, user.hashed_password)  
  if not user or not check_password: 
    raise HTTPException(status_code=400, detail="Invalid email or password")
  return create_access_token(subject=str(user.id))  