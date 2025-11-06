from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserDTO(BaseModel):
    id: Optional[int] 
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserResponseDTO(BaseModel):
    id: Optional[int] 
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    sub: int
    exp: int