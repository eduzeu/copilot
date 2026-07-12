from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
