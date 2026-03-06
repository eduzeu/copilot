from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException




def get_user(db: Session, user_id: int) -> User: 
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
      raise HTTPException(status_code=404, detail="User not found")
    return user

def update_profile(db: Session, user_id: int, body: dict) -> User: 
    user = get_user(db, user_id)
    for key, value in body.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> None: 
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return None 

