from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.core.security import create_access_token, verify_password, get_password_hash, hash_password
from fastapi import HTTPException

def register_user(db: Session, email: str, password: str) -> User: 
  check_user = db.query(User).filter(User.email == email).first()
  if check_user:
    raise HTTPException(status_code=400, detail="Email already registered")
   
  new_user = User(email=email, hashed_password=hash_password(password))
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