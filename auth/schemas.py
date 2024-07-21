from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    hashed_password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
