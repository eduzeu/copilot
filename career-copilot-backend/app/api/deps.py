from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session  
from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import User
from app.core.security import ALGORITHM 
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
  
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try: 
        payload = jwt.decode(token, settings.openai_api_key, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
  
    user = db.query(User).filter(User.id == user_id).first()
    if not user: 
        raise HTTPException(status_code=401, detail="User not found")
    return user
