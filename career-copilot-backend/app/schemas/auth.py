#auth schema 
from pydantic import BaseModel, EmailStr, Field 

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
  
class LoginRequest(BaseModel): 
    email: EmailStr
    password: str 

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer" 

class UserPublic(BaseModel):
    id: int
    email: EmailStr 

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    token: TokenResponse
    user: UserPublic 

  